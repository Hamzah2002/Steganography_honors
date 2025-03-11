from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QLineEdit
from PyQt6.QtGui import QFont
import sys
import subprocess
import styles  # Import centralized styling

class EncryptWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encrypt an Image")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")  # Use global background color

        # Load font
        self.font = QFont("Courier New", 12, QFont.Weight.Bold)

        # Labels
        self.label = QLabel("Select an image to encrypt:", self)
        self.label.setFont(self.font)
        self.label.setStyleSheet(styles.LABEL_STYLE)

        # Password Input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password (8+ chars)...")
        self.password_input.setFont(self.font)
        self.password_input.setStyleSheet(styles.TEXT_INPUT_STYLE)

        # Buttons
        self.btn_select_image = QPushButton("📁 Select Image")
        self.btn_save_output = QPushButton("💾 Save Encrypted Image")
        self.btn_encrypt = QPushButton("🔐 Encrypt Image")

        # Apply centralized styling
        for btn in [self.btn_select_image, self.btn_save_output, self.btn_encrypt]:
            btn.setFont(self.font)
            btn.setStyleSheet(styles.BUTTON_STYLE)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.btn_select_image)
        layout.addWidget(self.btn_save_output)
        layout.addWidget(self.btn_encrypt)

        self.setLayout(layout)

        # Button actions
        self.btn_select_image.clicked.connect(self.select_image)
        self.btn_save_output.clicked.connect(self.select_output_path)
        self.btn_encrypt.clicked.connect(self.encrypt_image)

        # Paths
        self.image_path = ""
        self.output_image_path = ""

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.image_path = path

    def select_output_path(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Encrypted Image", "", "Images (*.png)")
        if path:
            self.output_image_path = path

    def encrypt_image(self):
        if not self.image_path or not self.output_image_path or not self.password_input.text():
            self.label.setText("❌ Error: Select an image and enter a password.")
            return

        password = self.password_input.text()

        # Run encrypt.py as subprocess
        subprocess.run([sys.executable, "core/encrypt.py", self.image_path, password, self.output_image_path])
        self.label.setText(f"✅ Image encrypted successfully in {self.output_image_path}")

# -------------------------- IMAGE DECRYPTION UI -------------------------- #
class DecryptWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Decrypt an Image")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")

        # Load font
        self.font = QFont("Courier New", 12, QFont.Weight.Bold)

        # Labels
        self.label = QLabel("Select an encrypted image:", self)
        self.label.setFont(self.font)
        self.label.setStyleSheet(styles.LABEL_STYLE)

        # Password Input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password used for encryption...")
        self.password_input.setFont(self.font)
        self.password_input.setStyleSheet(styles.TEXT_INPUT_STYLE)

        # Buttons
        self.btn_select_image = QPushButton("📁 Select Encrypted Image")
        self.btn_save_output = QPushButton("💾 Save Decrypted Image")
        self.btn_decrypt = QPushButton("🔓 Decrypt Image")

        # Apply centralized styling
        for btn in [self.btn_select_image, self.btn_save_output, self.btn_decrypt]:
            btn.setFont(self.font)
            btn.setStyleSheet(styles.BUTTON_STYLE)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.btn_select_image)
        layout.addWidget(self.btn_save_output)
        layout.addWidget(self.btn_decrypt)

        self.setLayout(layout)

        # Button actions
        self.btn_select_image.clicked.connect(self.select_image)
        self.btn_save_output.clicked.connect(self.select_output_path)
        self.btn_decrypt.clicked.connect(self.decrypt_image)

        # Paths
        self.image_path = ""
        self.output_image_path = ""

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Encrypted Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.image_path = path

    def select_output_path(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Decrypted Image", "", "Images (*.png)")
        if path:
            self.output_image_path = path

    def decrypt_image(self):
        if not self.image_path or not self.output_image_path or not self.password_input.text():
            self.label.setText("❌ Error: Select an image and enter a password.")
            return

        password = self.password_input.text()

        # Run decrypt.py as subprocess
        subprocess.run([sys.executable, "core/decrypt.py", self.image_path, password, self.output_image_path])
        self.label.setText(f"✅ Image decrypted successfully in {self.output_image_path}")
