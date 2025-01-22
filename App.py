import subprocess
import sys
import os


def main():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    core_dir = os.path.join(base_dir, "core")  # Adjust for 'core' subdirectory

    print("Steganography Tool")
    print("1. Hide an image inside another image")
    print("2. Extract a hidden image from a stego image")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        # Run the hiding script in the 'core' directory
        hider_script = os.path.join(core_dir, "hider.py")
        subprocess.run([sys.executable, hider_script])
    elif choice == '2':
        # Run the uncovering script in the 'core' directory
        uncover_script = os.path.join(core_dir, "uncover.py")
        subprocess.run([sys.executable, uncover_script])
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
