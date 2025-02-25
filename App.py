import subprocess
import sys
import os
from core.Text_Hiding import TextHiding  # Import the TextHiding class


def main():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    core_dir = os.path.join(base_dir, "core")  # Adjust for 'core' subdirectory

    print("\n🔹 Steganography & Encryption Tool")
    print("1. Hide an image inside another image")
    print("2. Extract a hidden image from a stego image")
    print("3. Hide text inside an image")
    print("4. Extract hidden text from an image")
    print("5. Encrypt an image before hiding")
    print("6. Decrypt an extracted image")

    choice = input("Enter your choice (1, 2, 3, 4, 5, or 6): ").strip()

    if choice == '1':
        # Hide an image inside another image
        host_image_path = input("Enter the path to the host image (PNG/JPEG): ").strip()
        secret_image_path = input("Enter the path to the secret image (PNG/JPEG): ").strip()
        output_image_path = input("Enter the path to save the output stego image: ").strip()

        if not os.path.exists(host_image_path) or not os.path.exists(secret_image_path):
            print("❌ Error: One or more input file paths are invalid.")
            return

        hider_script = os.path.join(core_dir, "hider.py")
        subprocess.run([sys.executable, hider_script, host_image_path, secret_image_path, output_image_path],
                       check=True)
        print(f"✅ Image successfully hidden in: {output_image_path}")

    elif choice == '2':
        # Extract hidden image
        stego_image_path = input("Enter the path to the stego image (PNG/JPEG): ").strip()
        extracted_image_path = input("Enter the path to save the extracted image: ").strip()

        if not os.path.exists(stego_image_path):
            print("❌ Error: Invalid stego image path.")
            return

        uncover_script = os.path.join(core_dir, "uncover.py")
        subprocess.run([sys.executable, uncover_script, stego_image_path, extracted_image_path], check=True)
        print(f"✅ Extracted image saved successfully: {extracted_image_path}")

    elif choice == '3':
        # Hide text inside an image
        image_path = input("Enter the path to the input image (PNG/BMP): ").strip()
        text = input("Enter the text to hide: ").strip()
        output_path = input("Enter the path to save the output image: ").strip()

        if not os.path.exists(image_path):
            print("❌ Error: Invalid input image path.")
            return

        try:
            text_hiding = TextHiding()
            result = text_hiding.hide_text(image_path, text, output_path)
            print(f"✅ Success: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")

    elif choice == '4':
        # Extract hidden text from an image
        image_path = input("Enter the path to the image with hidden text (PNG/BMP): ").strip()

        if not os.path.exists(image_path):
            print("❌ Error: Invalid input image path.")
            return

        try:
            text_hiding = TextHiding()
            extracted_text = text_hiding.extract_text(image_path)
            if extracted_text.strip():
                print(f"✅ Extracted text: {extracted_text}")
            else:
                print("⚠ No hidden text found.")
        except Exception as e:
            print(f"❌ Error: {e}")

    elif choice == '5':
        # Encrypt an image before hiding
        input_image_path = input("Enter the path to the image you want to encrypt: ").strip()
        password = input("Enter a password (8+ characters): ").strip()
        output_encrypted_path = input("Enter the path to save the encrypted image: ").strip()

        if not os.path.exists(input_image_path):
            print("❌ Error: Image does not exist.")
            return

        encrypt_script = os.path.join(core_dir, "encrypt.py")
        subprocess.run([sys.executable, encrypt_script, input_image_path, password, output_encrypted_path], check=True)
        print(f"✅ Image encrypted successfully: {output_encrypted_path}")

    elif choice == '6':
        # Decrypt an extracted image
        input_encrypted_path = input("Enter the path to the encrypted image: ").strip()
        password = input("Enter the password used for encryption: ").strip()
        output_decrypted_path = input("Enter the path to save the decrypted image: ").strip()

        if not os.path.exists(input_encrypted_path):
            print("❌ Error: Encrypted image does not exist.")
            return

        decrypt_script = os.path.join(core_dir, "decrypt.py")
        subprocess.run([sys.executable, decrypt_script, input_encrypted_path, password, output_decrypted_path], check=True)
        print(f"✅ Image decrypted successfully: {output_decrypted_path}")

    else:
        print("❌ Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
