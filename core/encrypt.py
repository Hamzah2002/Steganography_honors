import sys
import os
import numpy as np
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util import Counter
import hashlib


class ImageEncryptor:
    def __init__(self, password):
        """Generate a key from the password using SHA-256."""
        self.key = hashlib.sha256(password.encode()).digest()

    def encrypt_image(self, image_array):
        """Encrypts the image using AES-CTR mode with explicit counter parameters."""
        shape = image_array.shape  # Preserve shape for reconstruction
        flat_data = image_array.flatten()

        # Create AES cipher with CTR mode using explicit counter parameters.
        ctr = Counter.new(
            128,  # 128-bit block size
            initial_value=0,  # Start counter at 0 (this must match decryption)
            little_endian=False,  # Big-endian mode (this must match decryption)
            prefix=b'',  # No prefix
            suffix=b''  # No suffix
        )
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        encrypted_data = np.frombuffer(cipher.encrypt(flat_data.tobytes()), dtype=np.uint8)
        return encrypted_data.reshape(shape)


def encrypt_image_wrapper(input_image_path, password, output_encrypted_path):
    """
    Helper function to encrypt an image.

    Args:
        input_image_path (str): Path to the input image.
        password (str): Password used for encryption.
        output_encrypted_path (str): Where to save the encrypted image.

    Returns:
        str: Success message.

    Raises:
        Exception: If any error occurs during encryption or saving.
    """
    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Input image not found: {input_image_path}")

    # Load image and convert to numpy array
    image = Image.open(input_image_path).convert("RGB")
    image_array = np.array(image, dtype=np.uint8)

    # Encrypt the image array
    encryptor = ImageEncryptor(password)
    encrypted_array = encryptor.encrypt_image(image_array)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_encrypted_path)), exist_ok=True)

    # Save the encrypted image
    encrypted_image = Image.fromarray(encrypted_array)
    try:
        encrypted_image.save(output_encrypted_path, format="PNG", optimize=True)
        return f"✅ Image encrypted successfully: {output_encrypted_path}"
    except Exception as e:
        raise Exception(f"Error saving encrypted image: {e}")


def main():
    if len(sys.argv) != 4:
        print("Usage: python encrypt.py <input_image_path> <password> <output_encrypted_path>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    password = sys.argv[2]
    output_encrypted_path = sys.argv[3]

    try:
        message = encrypt_image_wrapper(input_image_path, password, output_encrypted_path)
        print(message)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
