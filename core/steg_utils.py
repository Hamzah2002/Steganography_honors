from PIL import Image
import os

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

        # Resize secret image if it's larger than the host image
        if secret_width > host_width or secret_height > host_height:
            print("Resizing the secret image to fit inside the host image...")
            secret_image = secret_image.resize((host_width, host_height))
            secret_width, secret_height = secret_image.size
            print(f"Resized secret image size: {secret_width}x{secret_height}")

        host_pixels = host_image.load()
        secret_pixels = secret_image.load()

        # Store dimensions in the first 4 pixels of the first row
        metadata_pixels = [(0, 0), (0, 1), (1, 0), (1, 1)]
        host_pixels[0, 0] = (secret_width & 0xFF, (secret_width >> 8) & 0xFF, 0)
        host_pixels[0, 1] = (secret_height & 0xFF, (secret_height >> 8) & 0xFF, 0)
        print(f"Embedding width: {secret_width}, height: {secret_height}")
        print(f"Metadata pixels: (0, 0): {host_pixels[0, 0]}, (0, 1): {host_pixels[0, 1]}")

        # Embed secret image data, avoiding metadata region (first two rows)
        for y in range(2, secret_height):  # Start from row 2 to avoid overwriting metadata
            for x in range(secret_width):
                r_host, g_host, b_host = host_pixels[x, y]
                r_secret, g_secret, b_secret = secret_pixels[x, y]

                r_new = (r_host & 0xF0) | (r_secret >> 4)
                g_new = (g_host & 0xF0) | (g_secret >> 4)
                b_new = (b_host & 0xF0) | (b_secret >> 4)

                host_pixels[x, y] = (r_new, g_new, b_new)

        host_image.save(output_image_path)
        print(f"Secret image hidden successfully in {output_image_path}")

    except Exception as e:
        print(f"Error during hiding: {e}")


def extract_image():
    steg_image_path = input("Enter the path to the stego image (PNG/BMP): ").strip()
    output_secret_image_path = input("Enter the path to save the extracted secret image: ").strip()

    try:
        if not os.path.exists(steg_image_path):
            print(f"Error: File {steg_image_path} not found.")
            return

        steg_image = Image.open(steg_image_path).convert("RGB")
        steg_pixels = steg_image.load()

        # Read dimensions from metadata pixels
        secret_width = steg_pixels[0, 0][0] | (steg_pixels[0, 0][1] << 8)
        secret_height = steg_pixels[0, 1][0] | (steg_pixels[0, 1][1] << 8)

        print(f"Stego image size: {steg_image.size[0]}x{steg_image.size[1]}")
        print(f"Extracted secret size: {secret_width}x{secret_height}")
        print(f"Metadata pixels: (0, 0): {steg_pixels[0, 0]}, (0, 1): {steg_pixels[0, 1]}")

        # Validate dimensions
        if secret_width > steg_image.size[0] or secret_height > steg_image.size[1]:
            raise ValueError(f"Invalid secret image dimensions detected: {secret_width}x{secret_height}")

        secret_image = Image.new("RGB", (secret_width, secret_height))
        secret_pixels = secret_image.load()

        # Extract secret image data, avoiding metadata region (first two rows)
        for y in range(2, secret_height):
            for x in range(secret_width):
                r, g, b = steg_pixels[x, y]

                r_secret = (r & 0x0F) << 4
                g_secret = (g & 0x0F) << 4
                b_secret = (b & 0x0F) << 4

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
