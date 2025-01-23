from PIL import Image


class TextHiding:
    def _text_to_bin(self, text):
        """Convert text into binary."""
        return ''.join(f'{ord(c):08b}' for c in text)

    def _bin_to_text(self, binary):
        """Convert binary into text."""
        chars = [binary[i:i + 8] for i in range(0, len(binary), 8)]
        return ''.join(chr(int(char, 2)) for char in chars)

    def hide_text(self, image_path, text, output_path):
        """
        Hide text inside an image by modifying the least significant bit (LSB) of each pixel's RGB values.
        """
        image = Image.open(image_path).convert("RGB")
        binary_text = self._text_to_bin(text) + '1111111111111110'  # Add a delimiter

        if len(binary_text) > image.size[0] * image.size[1] * 3:
            raise ValueError("Text is too large to hide in this image.")

        pixels = list(image.getdata())
        new_pixels = []
        binary_index = 0

        for pixel in pixels:
            new_pixel = list(pixel)
            for i in range(3):  # For R, G, B channels
                if binary_index < len(binary_text):
                    new_pixel[i] = (new_pixel[i] & 0xFE) | int(binary_text[binary_index])
                    binary_index += 1
            new_pixels.append(tuple(new_pixel))

        # Create a new image with the modified pixels
        stego_image = Image.new(image.mode, image.size)
        stego_image.putdata(new_pixels)
        stego_image.save(output_path)
        return f"Text hidden successfully in {output_path}"

    def extract_text(self, image_path):
        """
        Extract hidden text from an image by reading the least significant bit (LSB) of each pixel's RGB values.
        """
        image = Image.open(image_path).convert("RGB")
        pixels = list(image.getdata())
        binary_data = ""

        for pixel in pixels:
            for i in range(3):  # For R, G, B channels
                binary_data += str(pixel[i] & 1)

        # Find the delimiter and decode the binary text
        delimiter = '1111111111111110'
        end_index = binary_data.find(delimiter)
        if end_index == -1:
            raise ValueError("No hidden text found in the image.")
        binary_text = binary_data[:end_index]

        extracted_text = self._bin_to_text(binary_text)
        return extracted_text
