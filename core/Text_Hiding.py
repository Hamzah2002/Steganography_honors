from PIL import Image


class SteganographyText:

    def _text_to_bin(self, text):
        """Convert text to a binary string."""
        return ''.join(f'{ord(c):08b}' for c in text)

    def _bin_to_text(self, binary):
        """Convert binary string to text."""
        chars = [binary[i:i + 8] for i in range(0, len(binary), 8)]
        return ''.join(chr(int(char, 2)) for char in chars)

    def _add_delimiter(self, binary_text):
        """Add a delimiter to indicate the end of the message."""
        delimiter = '1111111111111110'  # A unique 16-bit sequence to mark the end
        return binary_text + delimiter

    def _extract_until_delimiter(self, binary_data):
        """Extract binary data until the delimiter is reached."""
        delimiter = '1111111111111110'
        end_index = binary_data.find(delimiter)
        if end_index != -1:
            return binary_data[:end_index]
        return binary_data

    def _encode_metadata(self, image, position, size):
        """Encode the metadata (position and size) into the first few pixels of the image."""
        pixels = list(image.getdata())
        new_pixels = pixels[:]

        # Metadata format: (x, y, width, height)
        x, y = position
        width, height = size

        # Encode metadata in the first three pixels (6 values for x, y, width, height)
        new_pixels[0] = ((x >> 8) & 0xFF, x & 0xFF, (y >> 8) & 0xFF)
        new_pixels[1] = (y & 0xFF, (width >> 8) & 0xFF, width & 0xFF)
        new_pixels[2] = ((height >> 8) & 0xFF, height & 0xFF, 0)

        # Replace original image's pixels
        new_image = Image.new(image.mode, image.size)
        new_image.putdata(new_pixels)
        return new_image

    def _decode_metadata(self, image):
        """Decode the metadata (position and size) from the first few pixels of the image."""
        pixels = list(image.getdata())

        # Metadata is stored in the first three pixels
        x = (pixels[0][0] << 8) | pixels[0][1]
        y = (pixels[0][2] << 8) | pixels[1][0]
        width = (pixels[1][1] << 8) | pixels[1][2]
        height = (pixels[2][0] << 8) | pixels[2][1]

        return (x, y), (width, height)

    def hide_text(self, image_path, text, output_path, position=(0, 0), size=(100, 100)):
        """Hide a text string inside an image."""
        image = Image.open(image_path)
        binary_text = self._text_to_bin(text)
        binary_text = self._add_delimiter(binary_text)

        if len(binary_text) > image.size[0] * image.size[1] * 3 - 3 * 8:
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

        # Create the stego image with the embedded text
        new_image = Image.new(image.mode, image.size)
        new_image.putdata(new_pixels)

        # Encode metadata (location and size)
        stego_image = self._encode_metadata(new_image, position, size)
        stego_image.save(output_path)
        print(f"Text and metadata hidden successfully in {output_path}")

    def extract_text(self, image_path):
        """Extract hidden text and metadata from an image."""
        image = Image.open(image_path)
        position, size = self._decode_metadata(image)

        print(f"Decoded metadata: Position={position}, Size={size}")

        pixels = list(image.getdata())
        binary_data = ""
        for pixel in pixels[3:]:  # Skip the first three pixels with metadata
            for i in range(3):  # For R, G, B channels
                binary_data += str(pixel[i] & 1)

        # Extract text until the delimiter
        binary_text = self._extract_until_delimiter(binary_data)
        extracted_text = self._bin_to_text(binary_text)
        return extracted_text, position, size


def main():
    print("Steganography Text Tool with Metadata")
    print("1. Hide a text inside an image")
    print("2. Extract a hidden text from an image")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        image_path = input("Enter the path to the image (PNG/BMP): ")
        text = input("Enter the text to hide: ")
        output_path = input("Enter the path to save the output stego image: ")
        x = int(input("Enter the x-coordinate of the hidden region: "))
        y = int(input("Enter the y-coordinate of the hidden region: "))
        width = int(input("Enter the width of the hidden region: "))
        height = int(input("Enter the height of the hidden region: "))

        try:
            steg_text = SteganographyText()
            steg_text.hide_text(image_path, text, output_path, position=(x, y), size=(width, height))
        except Exception as e:
            print(f"Error: {e}")

    elif choice == '2':
        image_path = input("Enter the path to the stego image (PNG/BMP): ")

        try:
            steg_text = SteganographyText()
            hidden_text, position, size = steg_text.extract_text(image_path)
            print(f"Extracted text: {hidden_text}")
            print(f"Hidden text was located at Position={position}, Size={size}")
        except Exception as e:
            print(f"Error: {e}")

    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == '__main__':
    main()
