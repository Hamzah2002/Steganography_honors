import subprocess
import sys
import os
from core.Text_Hiding import TextHiding  # Import the TextHiding class


def main():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    core_dir = os.path.join(base_dir, "core")  # Adjust for 'core' subdirectory

    print("Steganography Tool")
    print("1. Hide an image inside another image")
    print("2. Extract a hidden image from a stego image")
    print("3. Hide text inside an image")
    print("4. Extract hidden text from an image")
    choice = input("Enter your choice (1, 2, 3, or 4): ")

    if choice == '1':
        # Run the hiding script in the 'core' directory
        hider_script = os.path.join(core_dir, "hider.py")
        subprocess.run([sys.executable, hider_script])
    elif choice == '2':
        # Run the uncovering script in the 'core' directory
        uncover_script = os.path.join(core_dir, "uncover.py")
        subprocess.run([sys.executable, uncover_script])
    elif choice == '3':
        # Use TextHiding to hide text
        image_path = input("Enter the path to the input image (PNG/BMP): ")
        text = input("Enter the text to hide: ")
        output_path = input("Enter the path to save the output image: ")

        try:
            text_hiding = TextHiding()
            result = text_hiding.hide_text(image_path, text, output_path)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
    elif choice == '4':
        # Use TextHiding to extract text
        image_path = input("Enter the path to the image with hidden text (PNG/BMP): ")

        try:
            text_hiding = TextHiding()
            extracted_text = text_hiding.extract_text(image_path)
            print(f"Extracted text: {extracted_text}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
