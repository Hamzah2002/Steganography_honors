from PIL import Image
import random


class Hider:
    def __init__(self):
        self.text_steganography = SteganographyText()

    def _int_to_bin(self, rgb):
        """Convert an integer tuple to a binary (string) tuple."""
        r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        """Convert a binary (string) tuple to an integer tuple."""
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb1, rgb2):
        """
        Embed the secret RGB tuple into the host RGB tuple.
        Takes 4 bits from the secret image and retains 4 bits from the host image.
        """
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        merged_rgb = (
            r1[:4] + r2[:4],  # 4 bits from host + 4 bits from secret
            g1[:4] + g2[:4],
            b1[:4] + b2[:4]
        )
        return self._bin_to_int(merged_rgb)

    def resize_secret(self, secret_image, host_image_size):
        """
        Resize the secret image to 50% of the host image size while preserving its aspect ratio.
        Rotate the secret image by 180 degrees to obfuscate it.
        """
        secret_image = secret_image.convert("RGB").rotate(180)  # Rotate for obfuscation
        host_width, host_height = host_image_size

        # Calculate the new size while maintaining aspect ratio
        secret_width, secret_height = secret_image.size
        scale_factor = 0.5  # 50% of host size
        max_width = int(host_width * scale_factor)
        max_height = int(host_height * scale_factor)

        aspect_ratio = secret_width / secret_height
        if aspect_ratio > 1:
            # Landscape orientation
            new_width = min(max_width, secret_width)
            new_height = int(new_width / aspect_ratio)
        else:
            # Portrait or square orientation
            new_height = min(max_height, secret_height)
            new_width = int(new_height * aspect_ratio)

        return secret_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def merge(self, host_image, secret_image):
        """
        Embed the secret image into the host image at a random position.
        """
        # Resize the secret image while maintaining aspect ratio
        secret_image_resized = self.resize_secret(secret_image, host_image.size)

        # Randomly select a position within the host image bounds
        host_width, host_height = host_image.size
        secret_width, secret_height = secret_image_resized.size
        max_x = host_width - secret_width
        max_y = host_height - secret_height
        pos_x = random.randint(0, max_x)
        pos_y = random.randint(0, max_y)

        # Encode metadata into the host image (position and size)
        metadata = f"{pos_x},{pos_y},{secret_width},{secret_height}"
        host_image = self.text_steganography.hide_text_in_metadata(host_image, metadata)

        # Debugging: Verify the metadata being encoded
        print(f"Metadata to encode: {metadata}")

        # Load pixel maps for embedding
        host_pixels = host_image.load()
        secret_pixels = secret_image_resized.load()

        # Embed the secret image into the host image at the chosen position
        for x in range(secret_width):
            for y in range(secret_height):
                host_x = pos_x + x
                host_y = pos_y + y
                host_rgb = host_pixels[host_x, host_y]
                secret_rgb = secret_pixels[x, y]
                host_pixels[host_x, host_y] = self._merge_rgb(host_rgb, secret_rgb)

        return host_image


class SteganographyText:
    def hide_text_in_metadata(self, image, text):
        """
        Encode metadata into the first few pixels of the image.
        """
        binary_text = ''.join(f'{ord(c):08b}' for c in text) + '1111111111111110'  # Add delimiter
        pixels = list(image.getdata())
        new_pixels = []

        binary_index = 0
        for pixel in pixels:
            new_pixel = list(pixel)
            for i in range(3):  # R, G, B channels
                if binary_index < len(binary_text):
                    new_pixel[i] = (new_pixel[i] & 0xFE) | int(binary_text[binary_index])
                    binary_index += 1
            new_pixels.append(tuple(new_pixel))

        # Debugging: Verify binary metadata being encoded
        print(f"Encoded metadata (binary with delimiter): {binary_text}")

        new_image = Image.new(image.mode, image.size)
        new_image.putdata(new_pixels)
        return new_image




def main():
    print("Steganography - Hide an Image")
    host_image_path = input("Enter the path to the host image (PNG/BMP): ")
    secret_image_path = input("Enter the path to the secret image (PNG/BMP): ")
    output_image_path = input("Enter the path to save the output stego image: ")

    try:
        # Open the host and secret images
        host_image = Image.open(host_image_path)
        secret_image = Image.open(secret_image_path)

        # Embed the secret image into the host image
        hider = Hider()
        stego_image = hider.merge(host_image, secret_image)

        # Save the resulting stego image
        stego_image.save(output_image_path)
        print(f"Stego image saved successfully to: {output_image_path}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
