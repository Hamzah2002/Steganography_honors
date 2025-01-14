from PIL import Image, ImageOps
import os

def to_binary(value, bits=8):
    """ Convert an integer to a binary string of a specified length with leading zeros. """
    return bin(value)[2:].zfill(bits)


def add_padding(image, target_width, target_height):
    """
    Adds padding to the image to fit the target dimensions.
    Pads equally on all sides if possible.
    """
    width, height = image.size
    padding_width = (target_width - width) // 2
    padding_height = (target_height - height) // 2

    padding = (
        padding_width,          # Left
        padding_height,         # Top
        target_width - width - padding_width,  # Right
        target_height - height - padding_height  # Bottom
    )

    padded_image = ImageOps.expand(image, padding)
    return padded_image


def hide_image():
    host_image_path = input("Enter the path to the host image (PNG/BMP): ").strip()
    secret_image_path = input("Enter the path to the secret image (PNG/BMP): ").strip()
    output_image_path = input("Enter the path to save the output stego image: ").strip()

    try:
        host_image = Image.open(host_image_path).convert("RGB")
        secret_image = Image.open(secret_image_path).convert("RGB")

        host_width, host_height = host_image.size
        secret_width, secret_height = secret_image.size

        print(f"Host image size: {host_width}x{host_height}")
        print(f"Original secret image size: {secret_width}x{secret_height}")

        # If the secret image is smaller, pad it to fit inside the host image
        if secret_width < host_width or secret_height < host_height:
            print("Padding the secret image to fit the host image dimensions...")
            secret_image = add_padding(secret_image, host_width, host_height)
            secret_width, secret_height = secret_image.size
            print(f"Padded secret image size: {secret_width}x{secret_height}")

        host_pixels = host_image.load()
        secret_pixels = secret_image.load()

        # Store the secret dimensions as 12 bits each (first pixel)
        secret_width_binary = to_binary(secret_width, 12)
        secret_height_binary = to_binary(secret_height, 12)
        dimension_binary = secret_width_binary + secret_height_binary

        host_pixels[0, 0] = (
            int(dimension_binary[:8], 2),
            int(dimension_binary[8:16], 2),
            int(dimension_binary[16:24], 2)
        )

        print(f"Embedding dimensions: {secret_width}x{secret_height}")

        idx = 0
        for y in range(secret_height):
            for x in range(secret_width):
                if (x == 0 and y == 0):
                    continue

                r_host, g_host, b_host = host_pixels[x, y]
                r_secret, g_secret, b_secret = secret_pixels[x, y]

                # Embed 4 MSBs of the secret RGB into 4 LSBs of the host RGB
                r_new = (r_host & 0xF0) | (r_secret >> 4)
                g_new = (g_host & 0xF0) | (g_secret >> 4)
                b_new = (b_host & 0xF0) | (b_secret >> 4)

                host_pixels[x, y] = (r_new, g_new, b_new)

        host_image.save(output_image_path)
        print(f"Secret image successfully hidden in {output_image_path}")

    except Exception as e:
        print(f"Error during hiding: {e}")


def extract_image():
    steg_image_path = input("Enter the path to the stego image (PNG/BMP): ").strip()
    output_secret_image_path = input("Enter the path to save the extracted secret image: ").strip()

    try:
        steg_image = Image.open(steg_image_path).convert("RGB")
        steg_pixels = steg_image.load()

        # Read the dimensions from the first pixel
        r, g, b = steg_pixels[0, 0]
        width_binary = to_binary(r, 8) + to_binary(g, 8)[:4]
        height_binary = to_binary(g, 8)[4:] + to_binary(b, 8)
        secret_width = int(width_binary, 2)
        secret_height = int(height_binary, 2)

        print(f"Extracted dimensions: {secret_width}x{secret_height}")

        secret_image = Image.new("RGB", (secret_width, secret_height))
        secret_pixels = secret_image.load()

        # Extract the secret image pixel data
        for y in range(secret_height):
            for x in range(secret_width):
                if (x == 0 and y == 0):
                    continue

                r, g, b = steg_pixels[x, y]

                # Extract 4 bits from each channel and reconstruct the secret RGB values
                r_binary = to_binary(r, 8)[4:] + '0000'
                g_binary = to_binary(g, 8)[4:] + '0000'
                b_binary = to_binary(b, 8)[4:] + '0000'

                r_secret = int(r_binary, 2)
                g_secret = int(g_binary, 2)
                b_secret = int(b_binary, 2)

                secret_pixels[x, y] = (r_secret, g_secret, b_secret)

        secret_image.save(output_secret_image_path)
        print(f"Secret image extracted successfully and saved to {output_secret_image_path}")

    except Exception as e:
        print(f"Error during extraction: {e}")


def main():
    print("Welcome to Image Steganography Tool")
    print("1. Hide an image inside another image")
    print("2. Extract a hidden image from a stego image")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        hide_image()
    elif choice == "2":
        extract_image()
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
