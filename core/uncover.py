from PIL import Image


class Uncover:
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

    def _unmerge_rgb(self, rgb):
        """
        Extract the last 4 bits from each RGB channel to reconstruct the secret image pixel.
        """
        r, g, b = self._int_to_bin(rgb)

        # Extract the last 4 bits and pad with leading zeros to make an 8-bit value
        extracted_r = r[4:] + '0000'
        extracted_g = g[4:] + '0000'
        extracted_b = b[4:] + '0000'

        return self._bin_to_int((extracted_r, extracted_g, extracted_b))

    def extract_metadata(self, image):
        """
        Extract metadata (position and size) from the first few pixels of the image.
        """
        return self.text_steganography.extract_text_from_metadata(image)

    def unmerge(self, stego_image):
        """
        Extract the hidden image using the metadata.
        """
        # Extract metadata from the stego image
        metadata = self.extract_metadata(stego_image)

        # Validate the metadata format
        if ',' not in metadata or len(metadata.split(',')) != 4:
            raise ValueError(f"Invalid metadata format: {metadata}")

        # Parse metadata values
        try:
            pos_x, pos_y, width, height = map(int, metadata.split(','))
        except ValueError as e:
            raise ValueError(f"Failed to parse metadata values: {metadata}") from e

        # Debugging: Print extracted metadata
        print(f"Extracted Metadata - Position: ({pos_x}, {pos_y}), Size: ({width}, {height})")

        # Create a new image for the extracted secret image
        extracted_image = Image.new("RGB", (width, height))
        extracted_pixels = extracted_image.load()

        # Extract the secret image pixel by pixel
        stego_pixels = stego_image.load()
        for x in range(width):
            for y in range(height):
                extracted_pixels[x, y] = self._unmerge_rgb(stego_pixels[pos_x + x, pos_y + y])

        # Rotate the extracted image back to its original orientation
        return extracted_image.rotate(180)


class SteganographyText:
    def extract_text_from_metadata(self, image):
        """
        Extract metadata from the first few pixels of the image.
        """
        pixels = list(image.getdata())
        binary_text = ""

        # Extract metadata from the first 50 pixels
        for pixel in pixels[:50]:  # Extended range to capture full metadata
            for i in range(3):  # R, G, B channels
                binary_text += str(pixel[i] & 1)

        # Debugging: Verify binary metadata extracted
        print(f"Extracted binary metadata (full): {binary_text}")

        # Find the delimiter and extract binary metadata
        delimiter = '1111111111111110'  # Unique 16-bit delimiter
        end_index = binary_text.find(delimiter)
        if end_index == -1:
            raise ValueError("Metadata delimiter not found. Metadata extraction failed.")

        binary_text = binary_text[:end_index]

        # Convert binary data back to text
        try:
            metadata = ''.join(
                chr(int(binary_text[i:i + 8], 2)) for i in range(0, len(binary_text), 8)
            )
        except ValueError as e:
            raise ValueError(f"Failed to decode binary metadata: {binary_text}") from e

        # Debugging: Verify decoded metadata
        print(f"Decoded metadata: {metadata}")

        return metadata


def main():
    print("Steganography - Extract Hidden Image")
    stego_image_path = input("Enter the path to the stego image (PNG/BMP): ")
    output_image_path = input("Enter the path to save the extracted image: ")

    try:
        # Open the stego image
        stego_image = Image.open(stego_image_path)

        # Extract the hidden image
        uncover = Uncover()
        extracted_image = uncover.unmerge(stego_image)

        # Save the extracted image
        extracted_image.save(output_image_path)
        print(f"Extracted image saved successfully to: {output_image_path}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
