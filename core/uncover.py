import sys
import os
import numpy as np
from PIL import Image


class LSBUnhider:
    def __init__(self, stego_image_path, output_path):
        self.stego_image_path = stego_image_path
        self.output_path = output_path

    def extract_secret(self):
        """ Extract the hidden secret image from the host image. """
        if not os.path.exists(self.stego_image_path):
            print(f"❌ Error: Stego image '{self.stego_image_path}' not found.")
            return

        print(f"\n🔹 Extracting secret from '{self.stego_image_path}'")

        try:
            # Load the stego image
            stego_image = Image.open(self.stego_image_path).convert("RGB")
            stego_array = np.array(stego_image, dtype=np.uint8)

            # Extract the least significant 4 bits (secret image data)
            secret_array = (stego_array & 0x0F) << 4  # Shift back to restore color range

            # Convert to image
            extracted_image = Image.fromarray(secret_array)

            # Step 1: Crop out the embedded region (Assuming it was intelligently placed)
            extracted_np = np.array(extracted_image)
            nonzero_pixels = np.where(extracted_np > 0)  # Find pixels with data
            if len(nonzero_pixels[0]) == 0:  # If nothing found, exit
                print("❌ No hidden image detected!")
                return

            # Get bounding box of nonzero pixels
            y_min, y_max = np.min(nonzero_pixels[0]), np.max(nonzero_pixels[0])
            x_min, x_max = np.min(nonzero_pixels[1]), np.max(nonzero_pixels[1])

            # Crop to region of interest
            extracted_image = extracted_image.crop((x_min, y_min, x_max, y_max))

            # Step 2: Restore original size by doubling dimensions (since it was downsized by 50%)
            original_width = extracted_image.width * 2
            original_height = extracted_image.height * 2
            extracted_image = extracted_image.resize((original_width, original_height), Image.Resampling.LANCZOS)

            # Step 3: Flip the image back to its original orientation
            extracted_image = extracted_image.transpose(Image.FLIP_TOP_BOTTOM)

            # Save extracted secret image
            output_path = self.ensure_png_extension()
            extracted_image.save(output_path, format="PNG", optimize=True)

            print(f"✅ Secret image extracted and saved to: {output_path}")

        except Exception as e:
            print(f"❌ Error during extraction: {e}")

    def ensure_png_extension(self):
        """ Ensure the output file has a .png extension. """
        return os.path.splitext(self.output_path)[0] + ".png"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python uncover.py <stego_image_path> <output_image_path>")
        sys.exit(1)

    # Convert paths to absolute paths
    stego_image_path = os.path.abspath(sys.argv[1])
    output_image_path = os.path.abspath(sys.argv[2])

    unhider = LSBUnhider(stego_image_path, output_image_path)
    unhider.extract_secret()
