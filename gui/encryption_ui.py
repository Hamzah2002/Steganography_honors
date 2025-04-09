import sys
import os
import subprocess
import traceback

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QLineEdit, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import styles  # Import your centralized styling file


#######################################
# Encryption Window (Step-by-Step)    #
#######################################

class EncryptWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encrypt an Image")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")

        # Font
        self.font = QFont("Courier New", 12, QFont.Weight.Bold)

        # Label for instructions
        self.label = QLabel("STEP 1: Select an image", self)
        self.label.setFont(self.font)
        self.label.setStyleSheet(styles.LABEL_STYLE)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Password Input (initially hidden)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password (8+ chars)...")
        self.password_input.setFont(self.font)
        self.password_input.setStyleSheet(styles.TEXT_INPUT_STYLE)
        self.password_input.hide()
        # Trigger the "next step" when user finishes typing password
        self.password_input.editingFinished.connect(self.on_password_entered)

        # Buttons (some hidden initially)
        self.btn_select_image = QPushButton("📁 Select Image")
        self.btn_save_output = QPushButton("💾 Save Encrypted Image")
        self.btn_encrypt = QPushButton("🔐 Encrypt Image")

        for btn in [self.btn_select_image, self.btn_save_output, self.btn_encrypt]:
            btn.setFont(self.font)
            btn.setStyleSheet(styles.BUTTON_STYLE)

        # Hide the Save Output and Encrypt buttons at first
        self.btn_save_output.hide()
        self.btn_encrypt.hide()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.btn_select_image)
        layout.addWidget(self.btn_save_output)
        layout.addWidget(self.btn_encrypt)
        self.setLayout(layout)

        # Connect button signals
        self.btn_select_image.clicked.connect(self.select_image)
        self.btn_save_output.clicked.connect(self.select_output_path)
        self.btn_encrypt.clicked.connect(self.encrypt_image)

        # Store paths
        self.image_path = ""
        self.output_image_path = ""

    def select_image(self):
        """STEP 1: Select the image to encrypt."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg)"
        )
        if path:
            self.image_path = path
            # Proceed to password input
            self.label.setText("STEP 2: Enter a password (8+ chars)")
            self.password_input.show()

    def on_password_entered(self):
        """
        Automatically triggered when the user finishes typing
        (editingFinished signal). If valid password, show next step.
        """
        password = self.password_input.text().strip()
        # We won't show an error message here because maybe user is still typing.
        # But let's ensure it's at least 8 chars before letting them proceed:
        if len(password) < 8:
            # Clear or re-focus if password is invalid
            self.show_error("❌ Password must be 8+ characters.")
            self.password_input.setFocus()
            return

        # If valid, show next step:
        self.label.setText("STEP 3: Choose where to save the encrypted image")
        self.btn_save_output.show()

    def select_output_path(self):
        """STEP 3: Choose where to save the encrypted image."""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Encrypted Image",
            "",
            "Images (*.png)"  # Adjust if you want multiple formats
        )
        if path:
            self.output_image_path = path
            self.label.setText("STEP 4: Click 'Encrypt Image' to finalize")
            self.btn_encrypt.show()

    def encrypt_image(self):
        """STEP 4: Run the encryption subprocess."""
        password = self.password_input.text().strip()
        if not self.image_path:
            self.show_error("❌ Error: No image selected.")
            return
        if not password or len(password) < 8:
            self.show_error("❌ Error: Please enter a valid password (8+ chars).")
            return
        if not self.output_image_path:
            self.show_error("❌ Error: No output path selected.")
            return

        try:
            # Build path to encrypt.py
            script_path = os.path.join(
                os.path.dirname(__file__), "..", "core", "encrypt.py"
            )

            print("Encrypt Subprocess Call:")
            print("  Script Path:", script_path)
            print("  Image Path:", self.image_path)
            print("  Password: (hidden)")
            print("  Output Path:", self.output_image_path)

            result = subprocess.run(
                [
                    sys.executable,
                    script_path,
                    self.image_path,
                    password,
                    self.output_image_path
                ],
                capture_output=True,
                text=True
            )

            print("Subprocess STDOUT:", result.stdout)
            print("Subprocess STDERR:", result.stderr)

            if result.returncode != 0:
                error_msg = result.stderr.strip() or "Unknown error during encryption."
                self.show_error(f"❌ Encryption failed:\n{error_msg}")
                return

            self.show_info(f"✅ Image encrypted successfully in {self.output_image_path}")

        except FileNotFoundError as e:
            self.show_error("❌ Could not find 'encrypt.py' in the 'core' folder.")
            print("FileNotFoundError:", e)
        except Exception as e:
            trace = traceback.format_exc()
            self.show_error(f"❌ Unexpected error:\n{str(e)}")
            print("Unexpected Error:\n", trace)

    # --------------------------
    # Helper Methods: show_error, show_info
    # --------------------------
    def show_error(self, message):
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox { background-color: #000000 !important; }
            QMessageBox QLabel { background-color: #000000 !important; color: #00FF00 !important; font-size: 14px !important; }
            QMessageBox QPushButton { background-color: #101010 !important; border: 2px solid #00FFFF !important; color: #00FF00 !important; }
            QMessageBox QPushButton:hover { border-color: #FF00FF !important; }
            QMessageBox QPushButton:pressed { background-color: #222222 !important; }
        """)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec()

    def show_info(self, message):
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox { background-color: #000000 !important; }
            QMessageBox QLabel { background-color: #000000 !important; color: #00FF00 !important; font-size: 14px !important; }
            QMessageBox QPushButton { background-color: #101010 !important; border: 2px solid #00FFFF !important; color: #00FF00 !important; }
            QMessageBox QPushButton:hover { border-color: #FF00FF !important; }
            QMessageBox QPushButton:pressed { background-color: #222222 !important; }
        """)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText(message)
        msg_box.exec()


#######################################
# Decryption Window (Step-by-Step)    #
#######################################

import sys
import os
import subprocess
import traceback
import logging
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QLineEdit, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import styles  # your centralized styling

# Set up basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DecryptWindow(QWidget):
    def __init__(self):
        try:
            super().__init__()
            logging.debug("DecryptWindow: __init__ start")
            self.setWindowTitle("Decrypt an Image")
            self.setGeometry(300, 300, 500, 400)
            self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")
            self.font = QFont("Courier New", 12, QFont.Weight.Bold)

            # STEP 1: Instruction label
            self.label = QLabel("STEP 1: Select an encrypted image", self)
            self.label.setFont(self.font)
            self.label.setStyleSheet(styles.LABEL_STYLE)
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logging.debug("DecryptWindow: Label created")

            # STEP 2: Password input (hidden until image is selected)
            self.password_input = QLineEdit(self)
            self.password_input.setPlaceholderText("Enter password used for encryption...")
            self.password_input.setFont(self.font)
            self.password_input.setStyleSheet(styles.TEXT_INPUT_STYLE)
            self.password_input.hide()

            # "Next" button for password step (hidden initially)
            self.btn_password_next = QPushButton("Next", self)
            self.btn_password_next.setFont(self.font)
            self.btn_password_next.setStyleSheet(styles.BUTTON_STYLE)
            self.btn_password_next.hide()
            self.btn_password_next.clicked.connect(self.on_password_entered)
            logging.debug("DecryptWindow: Password input and 'Next' button created")

            # Button: Select Encrypted Image (always shown)
            self.btn_select_image = QPushButton("📁 Select Encrypted Image", self)
            self.btn_select_image.setFont(self.font)
            self.btn_select_image.setStyleSheet(styles.BUTTON_STYLE)
            self.btn_select_image.clicked.connect(self.select_image)

            # Button: Save output (hidden until password is accepted)
            self.btn_save_output = QPushButton("💾 Save Decrypted Image", self)
            self.btn_save_output.setFont(self.font)
            self.btn_save_output.setStyleSheet(styles.BUTTON_STYLE)
            self.btn_save_output.hide()
            self.btn_save_output.clicked.connect(self.select_output_path)

            # Button: Decrypt Image (hidden until output path chosen)
            self.btn_decrypt = QPushButton("🔓 Decrypt Image", self)
            self.btn_decrypt.setFont(self.font)
            self.btn_decrypt.setStyleSheet(styles.BUTTON_STYLE)
            self.btn_decrypt.hide()
            self.btn_decrypt.clicked.connect(self.decrypt_image)

            # Layout
            layout = QVBoxLayout()
            layout.addWidget(self.label)
            layout.addWidget(self.password_input)
            layout.addWidget(self.btn_password_next)
            layout.addWidget(self.btn_select_image)
            layout.addWidget(self.btn_save_output)
            layout.addWidget(self.btn_decrypt)
            self.setLayout(layout)

            # Internal variables for file paths
            self.image_path = ""
            self.output_image_path = ""
            logging.debug("DecryptWindow: Initialization complete")
        except Exception as init_e:
            logging.error("Error during DecryptWindow initialization: " + str(init_e))
            traceback.print_exc()
            raise init_e

    def select_image(self):
        logging.debug("select_image: Opening file dialog for encrypted image")
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Encrypted Image", "", "Images (*.png *.jpg *.jpeg)"
        )
        if path:
            self.image_path = path
            self.label.setText("STEP 2: Enter the password used for encryption")
            self.password_input.show()
            self.btn_password_next.show()
            logging.debug(f"select_image: Selected image: {path}")

    def on_password_entered(self):
        password = self.password_input.text().strip()
        logging.debug(f"on_password_entered: Password entered (length {len(password)})")
        if len(password) < 8:
            self.show_error("❌ Password must be at least 8 characters.")
            self.password_input.setFocus()
            return
        self.label.setText("STEP 3: Choose where to save the decrypted image")
        self.btn_password_next.hide()  # Hide the Next button after password is accepted
        self.btn_save_output.show()
        logging.debug("on_password_entered: Password accepted, proceeding to output path selection")

    def select_output_path(self):
        logging.debug("select_output_path: Opening file dialog for output")
        path, _ = QFileDialog.getSaveFileName(self, "Save Decrypted Image", "", "Images (*.png)")
        if path:
            self.output_image_path = path
            self.label.setText("STEP 4: Click 'Decrypt Image' to finalize")
            self.btn_decrypt.show()
            logging.debug(f"select_output_path: Output path selected: {path}")

    def decrypt_image(self):
        try:
            password = self.password_input.text().strip()
            logging.debug("decrypt_image: Triggered")
            if not self.image_path:
                self.show_error("❌ Error: No encrypted image selected.")
                return
            if not password or len(password) < 8:
                self.show_error("❌ Error: Enter a valid password (8+ characters).")
                return
            if not self.output_image_path:
                self.show_error("❌ Error: No output path selected.")
                return

            # Build the script path for decrypt.py in the core folder.
            script_path = os.path.join(os.path.dirname(__file__), "..", "core", "decrypt.py")
            logging.debug(f"decrypt_image: Script path: {script_path}")
            logging.debug(f"decrypt_image: Encrypted image: {self.image_path}")
            logging.debug(f"decrypt_image: Output image: {self.output_image_path}")

            result = subprocess.run(
                [sys.executable, script_path, self.image_path, password, self.output_image_path],
                capture_output=True, text=True
            )
            logging.debug(f"decrypt_image: Subprocess return code: {result.returncode}")
            logging.debug("decrypt_image: STDOUT: " + result.stdout)
            logging.debug("decrypt_image: STDERR: " + result.stderr)

            if result.returncode != 0:
                error_msg = result.stderr.strip() or "Unknown error during decryption."
                self.show_error(f"❌ Decryption failed:\n{error_msg}")
                return

            self.show_info(f"✅ Image decrypted successfully in {self.output_image_path}")
        except Exception as e:
            self.show_error(f"❌ Unexpected error: {str(e)}")
            logging.error("decrypt_image: Exception occurred\n" + traceback.format_exc())

    def show_error(self, message):
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox { background-color: #000000 !important; }
            QMessageBox QLabel {
                background-color: #000000 !important;
                color: #00FF00 !important;  /* Neon Green Text */
                font-size: 14px !important;
            }
            QMessageBox QPushButton {
                background-color: #101010 !important;
                border: 2px solid #00FFFF !important;  /* Cyan Border */
                color: #00FF00 !important;
            }
            QMessageBox QPushButton:hover {
                border-color: #FF00FF !important;  /* Magenta on hover */
            }
            QMessageBox QPushButton:pressed {
                background-color: #222222 !important;
            }
        """)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec()

    def show_info(self, message):
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox { background-color: #000000 !important; }
            QMessageBox QLabel {
                background-color: #000000 !important;
                color: #00FF00 !important;  /* Neon Green Text */
                font-size: 14px !important;
            }
            QMessageBox QPushButton {
                background-color: #101010 !important;
                border: 2px solid #00FFFF !important;  /* Cyan Border */
                color: #00FF00 !important;
            }
            QMessageBox QPushButton:hover {
                border-color: #FF00FF !important;  /* Magenta on hover */
            }
            QMessageBox QPushButton:pressed {
                background-color: #222222 !important;
            }
        """)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText(message)
        msg_box.exec()


