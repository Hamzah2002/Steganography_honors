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

        # Create AES cipher with CTR mode using the same counter settings as in decryption
        ctr = Counter.new(
            128,                   # 128-bit block size
            initial_value=0,       # Start counter at 0 (this must match decryption)
            little_endian=False,   # Big-endian mode (this must match decryption)
            prefix=b'',            # No prefix
            suffix=b''             # No suffix
        )
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        encrypted_data = np.frombuffer(cipher.encrypt(flat_data.tobytes()), dtype=np.uint8)
        return encrypted_data.reshape(shape)  # Reshape to original format

def main():
    if len(sys.argv) != 4:
        print("Usage: python encrypt.py <input_image_path> <password> <output_encrypted_path>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    password = sys.argv[2]
    output_encrypted_path = sys.argv[3]

    # Validate input image
    if not os.path.exists(input_image_path):
        print("❌ Error: Input image does not exist.")
        sys.exit(1)

    # Load image
    image = Image.open(input_image_path).convert("RGB")
    image_array = np.array(image, dtype=np.uint8)

    # Encrypt image
    encryptor = ImageEncryptor(password)
    encrypted_array = encryptor.encrypt_image(image_array)

    # Create folder if needed
    os.makedirs(os.path.dirname(os.path.abspath(output_encrypted_path)), exist_ok=True)

    # Save encrypted image
    encrypted_image = Image.fromarray(encrypted_array)
    try:
        encrypted_image.save(output_encrypted_path, format="PNG", optimize=True)
        print(f"✅ Image encrypted successfully: {output_encrypted_path}")
    except Exception as e:
        print(f"❌ Error saving encrypted image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
