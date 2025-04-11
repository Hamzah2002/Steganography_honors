import sys
import os
import numpy as np
from PIL import Image


class LSBHider:
    def __init__(self, host_image_path, secret_image_path, output_path):
        self.host_image_path = host_image_path
        self.secret_image_path = secret_image_path
        self.output_path = output_path

    def process_secret_image(self, host_size):
        """ Resize and preprocess the secret image before embedding. """
        secret_image = Image.open(self.secret_image_path).convert("RGB")

        # Flip the secret image vertically before processing
        secret_image = secret_image.transpose(Image.FLIP_TOP_BOTTOM)

        # Step 1: If the secret is larger than the host, resize it to fit while maintaining aspect ratio
        if secret_image.width > host_size[0] or secret_image.height > host_size[1]:
            secret_image.thumbnail((host_size[0], host_size[1]), Image.Resampling.LANCZOS)

        # Step 2: Mandatory 50% downsize
        new_width = max(1, secret_image.width // 2)
        new_height = max(1, secret_image.height // 2)
        secret_image = secret_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return secret_image

    def find_darkest_region(self, host_array, secret_size):
        """ Find the darkest region in the host image for best concealment. """
        grayscale = np.mean(host_array, axis=2)  # Convert RGB to grayscale
        darkest_y, darkest_x = np.unravel_index(np.argmin(grayscale), grayscale.shape)  # Find darkest pixel

        # Ensure the secret image fits inside the found position
        darkest_x = min(darkest_x, host_array.shape[1] - secret_size[0])
        darkest_y = min(darkest_y, host_array.shape[0] - secret_size[1])

        return darkest_x, darkest_y

    def embed_secret(self):
        """ Embed the secret image into the host image using 4-bit LSB encoding. """
        print(f"\n🔹 Hiding '{self.secret_image_path}' inside '{self.host_image_path}'")

        # Load images
        host_image = Image.open(self.host_image_path).convert("RGB")
        secret_image = self.process_secret_image(host_image.size)

        # Convert to NumPy arrays
        host_array = np.array(host_image, dtype=np.uint8)
        secret_array = np.array(secret_image, dtype=np.uint8)

        # Find the darkest region for embedding
        x_offset, y_offset = self.find_darkest_region(host_array, secret_image.size)

        # Create a blank image the same size as the host and paste the secret into the darkest location
        temp_secret = Image.new("RGB", host_image.size, (0, 0, 0))
        temp_secret.paste(secret_image, (x_offset, y_offset))

        # Convert back to NumPy
        secret_array = np.array(temp_secret, dtype=np.uint8)

        # Extract the most significant 4 bits of the secret image
        secret_array = (secret_array >> 4) & 0x0F  # Keep upper 4 bits

        # Clear the least significant 4 bits of the host image
        host_array = host_array & 0xF0  # Clear lower 4 bits

        # Embed the secret image
        embedded_array = host_array | secret_array  # Merge upper 4 bits into host

        # Save optimized PNG
        output_image = Image.fromarray(embedded_array)
        output_path = self.ensure_png_extension()
        output_image.save(output_path, format="PNG", optimize=True, compress_level=6)  # Reduced compression level

        print(f"✅ Stego image saved successfully to: {output_path}")

    def ensure_png_extension(self):
        """ Ensure the output file has a .png extension. """
        return os.path.splitext(self.output_path)[0] + ".png"

def embed_secret_wrapper(host_image_path, secret_image_path, output_image_path):
    hider = LSBHider(host_image_path, secret_image_path, output_image_path)
    hider.embed_secret()



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python hider.py <host_image_path> <secret_image_path> <output_image_path>")
        sys.exit(1)

    hider = LSBHider(sys.argv[1], sys.argv[2], sys.argv[3])
    hider.embed_secret()
