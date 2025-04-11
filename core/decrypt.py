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
        shape = encrypted_array.shape  # Preserve original shape
        flat_data = encrypted_array.flatten()

        ctr = Counter.new(
            128,  # 128-bit block size
            initial_value=0,  # Must match encryption
            little_endian=False,  # Must match encryption
            prefix=b'',  # No prefix
            suffix=b''  # No suffix
        )
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        decrypted_bytes = cipher.decrypt(flat_data.tobytes())
        decrypted_data = np.frombuffer(decrypted_bytes, dtype=np.uint8)
        return decrypted_data.reshape(shape)


def decrypt_image_wrapper(input_encrypted_path, password, output_decrypted_path):
    """
    Helper function to decrypt an encrypted image.

    Args:
        input_encrypted_path (str): Path to the encrypted image.
        password (str): Password used for decryption.
        output_decrypted_path (str): Where to save the decrypted image.

    Returns:
        str: Success message.

    Raises:
        Exception: If any error occurs during decryption or saving.
    """
    if not os.path.exists(input_encrypted_path):
        raise FileNotFoundError(f"Encrypted image not found: {input_encrypted_path}")

    try:
        encrypted_image = Image.open(input_encrypted_path).convert("RGB")
        encrypted_array = np.array(encrypted_image, dtype=np.uint8)
    except Exception as e:
        raise Exception(f"Error loading encrypted image: {e}")

    decryptor = ImageDecryptor(password)
    try:
        decrypted_array = decryptor.decrypt_image(encrypted_array)
    except Exception as e:
        raise Exception(f"Error during decryption: {e}")

    decrypted_image = Image.fromarray(decrypted_array)
    output_dir = os.path.dirname(os.path.abspath(output_decrypted_path))
    os.makedirs(output_dir, exist_ok=True)

    try:
        decrypted_image.save(output_decrypted_path, format="PNG", optimize=True)
        return f"✅ Image decrypted successfully: {output_decrypted_path}"
    except Exception as e:
        raise Exception(f"Error saving decrypted image: {e}")


def main():
    if len(sys.argv) != 4:
        print("Usage: python decrypt.py <input_encrypted_image_path> <password> <output_decrypted_path>")
        sys.exit(1)

    input_encrypted_path = sys.argv[1]
    password = sys.argv[2]
    output_decrypted_path = sys.argv[3]

    try:
        message = decrypt_image_wrapper(input_encrypted_path, password, output_decrypted_path)
        print(message)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
