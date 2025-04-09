# core/text_hiding.py

import sys
import os
from PIL import Image

class TextHiding:
    def _text_to_bin(self, text):
        """Convert text into a string of '0'/'1' bits."""
        return ''.join(f'{ord(c):08b}' for c in text)

    def _bin_to_text(self, binary):
        """Convert a string of '0'/'1' bits back into text."""
        chars = [binary[i:i + 8] for i in range(0, len(binary), 8)]
        return ''.join(chr(int(char, 2)) for char in chars)

    def hide_text(self, image_path, text, output_path):
        """
        Hide text inside an image by modifying the least significant bit (LSB)
        of each pixel's RGB values, then save to output_path.
        """
        print(f"[text_hiding.py] hide_text called with:\n  image_path:  {image_path}\n  output_path: {output_path}")

        # 1. Open image
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Host image not found: {image_path}")

        image = Image.open(image_path).convert("RGB")

        # 2. Convert text to binary with a delimiter at the end
        delimiter = "1111111111111110"  # 2 bytes of 1's as a stop marker
        binary_text = self._text_to_bin(text) + delimiter

        # 3. Check capacity
        capacity = image.size[0] * image.size[1] * 3
        if len(binary_text) > capacity:
            raise ValueError("Text is too large to hide in this image.")

        # 4. Embed bits
        pixels = list(image.getdata())
        new_pixels = []
        binary_index = 0

        for pixel in pixels:
            new_pixel = list(pixel)
            for i in range(3):  # For R, G, B channels
                if binary_index < len(binary_text):
                    bit = int(binary_text[binary_index])
                    new_pixel[i] = (new_pixel[i] & 0xFE) | bit
                    binary_index += 1
            new_pixels.append(tuple(new_pixel))

        # 5. Create a new image with modified pixels
        stego_image = Image.new(image.mode, image.size)
        stego_image.putdata(new_pixels)

        # 6. Make sure the output folder exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # 7. Save the stego image
        try:
            stego_image.save(output_path)
            print(f"Successfully saved stego image at: {output_path}")
        except Exception as e:
            print(f"ERROR saving stego image: {e}")
            raise e

        return f"Text hidden successfully in {output_path}"

    def extract_text(self, image_path):
        """
        Extract hidden text from an image by reading the least significant bit (LSB)
        of each pixel's RGB values until the delimiter is found.
        """
        #print(f"[text_hiding.py] extract_text called with:\n  image_path: {image_path}")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Stego image not found: {image_path}")

        image = Image.open(image_path).convert("RGB")
        pixels = list(image.getdata())
        binary_data = ""

        for pixel in pixels:
            for i in range(3):  # For R, G, B channels
                binary_data += str(pixel[i] & 1)

        # 2. Locate delimiter
        delimiter = "1111111111111110"
        end_index = binary_data.find(delimiter)
        if end_index == -1:
            raise ValueError("No hidden text found in this image (delimiter missing).")

        # 3. Extract the text bits before the delimiter
        binary_text = binary_data[:end_index]
        extracted_text = self._bin_to_text(binary_text)
        #print(f"[text_hiding.py] Extracted text: {extracted_text}")

        return extracted_text


def main():
    """
    Allows command line usage:
      python text_hiding.py hide   <image_path> <text> <output_path>
      python text_hiding.py extract <image_path>
    """
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python text_hiding.py hide <image_path> <text> <output_path>")
        print("  python text_hiding.py extract <image_path>")
        sys.exit(1)

    action = sys.argv[1].lower()
    hiding = TextHiding()

    if action == "hide":
        if len(sys.argv) < 5:
            print("Usage: python text_hiding.py hide <image_path> <text> <output_path>")
            sys.exit(1)
        image_path = sys.argv[2]
        text = sys.argv[3]
        output_path = sys.argv[4]

        try:
            message = hiding.hide_text(image_path, text, output_path)
            print("[text_hiding.py] " + message)
        except Exception as e:
            print("Error in hide_text():", e)
            sys.exit(1)

    elif action == "extract":
        if len(sys.argv) < 3:
            print("Usage: python text_hiding.py extract <image_path>")
            sys.exit(1)
        image_path = sys.argv[2]
        try:
            extracted = hiding.extract_text(image_path)
            print("Extracted text:", extracted)
        except Exception as e:
            print("[text_hiding.py] Error in extract_text():", e)
            sys.exit(1)

    else:
        print(f"Unknown action '{action}'. Use 'hide' or 'extract'.")


if __name__ == "__main__":
    main()
