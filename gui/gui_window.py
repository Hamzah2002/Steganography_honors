from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import styles  # Import centralized styles

class RetroStegApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 🖥️ Set up the main window
        self.setWindowTitle("Retro Steganography Tool")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")  # Use global background color

        # 📝 Load pixel-style font
        self.font = QFont("Courier New", 14, QFont.Weight.Bold)

        # 📢 Title Label
        self.label = QLabel("RETRO STEGANOGRAPHY TOOL", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(self.font)
        self.label.setStyleSheet(styles.LABEL_STYLE)  # Use global label styling

        # 🎮 Buttons for different actions
        self.btn_hide_image = QPushButton("🖼️ Hide Image")
        self.btn_extract_image = QPushButton("📷 Extract Image")
        self.btn_hide_text = QPushButton("✍ Hide Text")
        self.btn_extract_text = QPushButton("🔍 Extract Text")
        self.btn_encrypt = QPushButton("🔐 Encrypt Image")
        self.btn_decrypt = QPushButton("🔓 Decrypt Image")

        # 🎨 Apply centralized button styling
        for btn in [self.btn_hide_image, self.btn_extract_image, self.btn_hide_text, self.btn_extract_text, self.btn_encrypt, self.btn_decrypt]:
            btn.setFont(self.font)
            btn.setStyleSheet(styles.BUTTON_STYLE)

        # 📌 Layout Configuration
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_hide_image)
        layout.addWidget(self.btn_extract_image)
        layout.addWidget(self.btn_hide_text)
        layout.addWidget(self.btn_extract_text)
        layout.addWidget(self.btn_encrypt)
        layout.addWidget(self.btn_decrypt)

        # 📦 Set Main Widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 🔗 Button Actions (Connecting them to feature UIs)
        self.btn_hide_image.clicked.connect(self.open_image_hiding)
        self.btn_extract_image.clicked.connect(self.open_image_extract)
        self.btn_hide_text.clicked.connect(self.open_text_hiding)
        self.btn_extract_text.clicked.connect(self.open_text_extract)
        self.btn_encrypt.clicked.connect(self.open_encrypt)
        self.btn_decrypt.clicked.connect(self.open_decrypt)

    def open_image_hiding(self):
        from gui.image_hiding_ui import ImageHidingWindow
        self.image_hiding_window = ImageHidingWindow()
        self.image_hiding_window.show()

    def open_image_extract(self):
        from gui.image_extract_ui import ImageExtractWindow  # ✅ Correct file for extraction
        self.image_extract_window = ImageExtractWindow()
        self.image_extract_window.show()

    def open_text_hiding(self):
        from gui.text_hiding_ui import TextHidingWindow
        self.text_hiding_window = TextHidingWindow()
        self.text_hiding_window.show()

    def open_text_extract(self):
        from gui.text_hiding_ui import TextExtractWindow
        self.text_extract_window = TextExtractWindow()
        self.text_extract_window.show()

    def open_encrypt(self):
        from gui.encryption_ui import EncryptWindow
        self.encrypt_window = EncryptWindow()
        self.encrypt_window.show()

    def open_decrypt(self):
        from gui.encryption_ui import DecryptWindow
        self.decrypt_window = DecryptWindow()
        self.decrypt_window.show()
