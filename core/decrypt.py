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
        """Decrypts the image using AES-CTR mode."""
        shape = encrypted_array.shape  # Preserve shape
        flat_data = encrypted_array.flatten()

        # Create AES cipher
        ctr = Counter.new(128)
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)

        decrypted_data = np.frombuffer(cipher.decrypt(flat_data.tobytes()), dtype=np.uint8)
        return decrypted_data.reshape(shape)  # Reshape to original format


def main():
    if len(sys.argv) != 4:
        print("Usage: python decrypt.py <input_encrypted_image_path> <password> <output_decrypted_path>")
        sys.exit(1)

    input_encrypted_path = sys.argv[1]
    password = sys.argv[2]
    output_decrypted_path = sys.argv[3]

    if not os.path.exists(input_encrypted_path):
        print("❌ Error: Encrypted image does not exist.")
        sys.exit(1)

    # Load encrypted image
    encrypted_image = Image.open(input_encrypted_path).convert("RGB")
    encrypted_array = np.array(encrypted_image, dtype=np.uint8)

    # Decrypt image
    decryptor = ImageDecryptor(password)
    decrypted_array = decryptor.decrypt_image(encrypted_array)

    # Save decrypted image
    decrypted_image = Image.fromarray(decrypted_array)
    decrypted_image.save(output_decrypted_path, format="PNG", optimize=True)

    print(f"✅ Image decrypted successfully: {output_decrypted_path}")


if __name__ == "__main__":
    main()
