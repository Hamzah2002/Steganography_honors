import sys
import os
import numpy as np
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util import Counter
import hashlib


class ImageDecryptor:
    def __init__(self, password):
        """Generate a key from the password using SHA-256."""
        self.key = hashlib.sha256(password.encode()).digest()

    def decrypt_image(self, encrypted_array):
        """
        Decrypt the image using AES-CTR mode.
        The counter is constructed explicitly to match the encryption settings.
        """
        # Preserve the original shape
        shape = encrypted_array.shape
        # Flatten the image data for decryption
        flat_data = encrypted_array.flatten()

        # Create a counter with explicit parameters:
        ctr = Counter.new(
            128,  # 128-bit block size
            initial_value=0,  # Start the counter at 0 (must match encryption)
            little_endian=False,  # Big-endian mode (must match encryption)
            prefix=b'',  # No prefix bytes
            suffix=b''  # No suffix bytes
        )
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        # Decrypt the byte stream
        decrypted_bytes = cipher.decrypt(flat_data.tobytes())
        # Convert bytes back to a numpy array and reshape to original dimensions
        decrypted_data = np.frombuffer(decrypted_bytes, dtype=np.uint8)
        return decrypted_data.reshape(shape)


def main():
    if len(sys.argv) != 4:
        print("Usage: python decrypt.py <input_encrypted_image_path> <password> <output_decrypted_path>")
        sys.exit(1)

    input_encrypted_path = sys.argv[1]
    password = sys.argv[2]
    output_decrypted_path = sys.argv[3]

    # Check that the input encrypted image exists
    if not os.path.exists(input_encrypted_path):
        print("❌ Error: Encrypted image does not exist.")
        sys.exit(1)

    try:
        # Open the encrypted image and convert it to RGB format
        encrypted_image = Image.open(input_encrypted_path).convert("RGB")
        encrypted_array = np.array(encrypted_image, dtype=np.uint8)
    except Exception as e:
        print(f"❌ Error loading encrypted image: {e}")
        sys.exit(1)

    try:
        decryptor = ImageDecryptor(password)
        decrypted_array = decryptor.decrypt_image(encrypted_array)
    except Exception as e:
        print(f"❌ Error during decryption: {e}")
        sys.exit(1)

    decrypted_image = Image.fromarray(decrypted_array)

    # Ensure the output directory exists
    output_dir = os.path.dirname(os.path.abspath(output_decrypted_path))
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Save the decrypted image as PNG
        decrypted_image.save(output_decrypted_path, format="PNG", optimize=True)
        print(f"✅ Image decrypted successfully: {output_decrypted_path}")
    except Exception as e:
        print(f"❌ Error saving decrypted image: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
