import sys
import subprocess
import traceback
import os

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QTextEdit, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import styles  # Import your centralized styling


class TextHidingWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hide Text in Image")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")

        # Load font
        self.font = QFont("Courier New", 12, QFont.Weight.Bold)

        # Label
        self.label = QLabel("STEP 1: Select an image", self)
        self.label.setFont(self.font)
        self.label.setStyleSheet(styles.LABEL_STYLE)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Text Input Field
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Enter text to hide here...")
        self.text_input.setFont(self.font)
        self.text_input.setStyleSheet(styles.TEXT_INPUT_STYLE)

        # Buttons
        self.btn_select_image = QPushButton("📁 Select Image")
        self.btn_save_output = QPushButton("💾 Save Output Image")
        self.btn_hide_text = QPushButton("🔥 Hide Text")

        # Apply styling
        for btn in [self.btn_select_image, self.btn_save_output, self.btn_hide_text]:
            btn.setFont(self.font)
            btn.setStyleSheet(styles.BUTTON_STYLE)

        # Initially hide the Save Output and Hide Text steps
        self.btn_save_output.hide()
        self.btn_hide_text.hide()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.btn_select_image)
        layout.addWidget(self.btn_save_output)
        layout.addWidget(self.btn_hide_text)
        self.setLayout(layout)

        # Button connections
        self.btn_select_image.clicked.connect(self.select_image)
        self.btn_save_output.clicked.connect(self.select_output_path)
        self.btn_hide_text.clicked.connect(self.hide_text)

        # Store paths
        self.image_path = ""
        self.output_image_path = ""

    def select_image(self):
        """Step 1: Select the image for hiding text."""
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.bmp)")
        if path:
            self.image_path = path
            # Update label and show Save Output button
            self.label.setText("STEP 2: Choose where to save the stego image")
            self.btn_save_output.show()

    def select_output_path(self):
        """
        Step 2: Select the output file path, allowing either .png or .bmp.
        If no extension is typed, default to .png.
        """
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Stego Image",
            "",
            "Images (*.png *.bmp)"
        )
        if path:
            # Ensure the user has an actual extension:
            _, ext = os.path.splitext(path)
            if not ext:  # If user typed something without .png or .bmp
                path += ".png"  # Default to .png

            # Now set the final output path
            self.output_image_path = path

            self.label.setText("STEP 3: Enter your text above, then click 'Hide Text'")
            self.btn_hide_text.show()

    def hide_text(self):
        """Step 3: Embed the provided text into the selected image."""
        # Basic validations with forced style for error messages:
        if not self.image_path:
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
            msg_box.setText("❌ Please select an image first.")
            msg_box.exec()
            return

        if not self.output_image_path:
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
            msg_box.setText("❌ Please select an output path.")
            msg_box.exec()
            return

        text = self.text_input.toPlainText().strip()
        if not text:
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
            msg_box.setText("❌ Please enter text to hide.")
            msg_box.exec()
            return

        try:
            # Construct the script path. Ensure your file in the core folder is named exactly "text_hiding.py"
            script_path = os.path.join(os.path.dirname(__file__), "..", "core", "text_hiding.py")

            # Print debugging info:
            print("Running hide subprocess:")
            print("  Script Path: ", script_path)
            print("  Image Path:  ", self.image_path)
            print("  Output Path: ", self.output_image_path)

            result = subprocess.run(
                [
                    sys.executable,
                    script_path,
                    "hide",
                    self.image_path,
                    text,
                    self.output_image_path
                ],
                capture_output=True,
                text=True
            )

            # Print subprocess outputs for debugging:
            print("Subprocess STDOUT:", result.stdout)
            print("Subprocess STDERR:", result.stderr)

            if result.returncode != 0:
                error_msg = result.stderr.strip() or "Unknown error occurred."
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
                msg_box.setText(f"❌ Failed to hide text:\n{error_msg}")
                msg_box.exec()
                return

            # If successful, inform the user:
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
            msg_box.setText(f"✅ Text hidden successfully in:\n{self.output_image_path}")
            msg_box.exec()

        except FileNotFoundError as e:
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
            msg_box.setText("❌ Could not find 'text_hiding.py' in the 'core' folder.")
            msg_box.exec()
            print("FileNotFoundError:", e)

        except subprocess.CalledProcessError as e:
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
            msg_box.setText(f"❌ Subprocess error:\n{e.stderr}")
            msg_box.exec()
            print("CalledProcessError:", e)

        except Exception as e:
            error_trace = traceback.format_exc()
            msg_box = QMessageBox(self)
            msg_box.setStyleSheet("""
                QMessageBox { background-color: #000000 !important; }
                QMessageBox QLabel { background-color: #000000 !important; color: #00FF00 !important; font-size: 14px !important; }
                QMessageBox QPushButton { background-color: #101010 !important; border: 2px solid #00FFFF !important; color: #00FF00 !important; }
                QMessageBox QPushButton:hover { border-color: #FF00FF !important; }
                QMessageBox QPushButton:pressed { background-color: #222222 !important; }
            """)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("Critical Error")
            msg_box.setText(f"❌ Unexpected error:\n{str(e)}")
            msg_box.exec()
            print("Unexpected Error:\n", error_trace)

##############################################
# Text Extraction Window for Extracting Text #
##############################################

class TextExtractWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Extract Hidden Text")
        self.setGeometry(300, 300, 500, 300)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")

        self.font = QFont("Courier New", 12, QFont.Weight.Bold)

        # Label for instructions
        self.label = QLabel("Select an image with hidden text:", self)
        self.label.setFont(self.font)
        self.label.setStyleSheet(styles.LABEL_STYLE)

        # Buttons for selecting image and extracting text
        self.btn_select_image = QPushButton("📁 Select Image")
        self.btn_extract_text = QPushButton("🔍 Extract Text")
        for btn in [self.btn_select_image, self.btn_extract_text]:
            btn.setFont(self.font)
            btn.setStyleSheet(styles.BUTTON_STYLE)

        # Text area to display the extracted text
        self.extracted_text = QTextEdit(self)
        self.extracted_text.setFont(self.font)
        self.extracted_text.setReadOnly(True)
        self.extracted_text.setStyleSheet(styles.TEXT_INPUT_STYLE)

        # Layout configuration
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select_image)
        layout.addWidget(self.btn_extract_text)
        layout.addWidget(self.extracted_text)
        self.setLayout(layout)

        # Connect button signals
        self.btn_select_image.clicked.connect(self.select_image)
        self.btn_extract_text.clicked.connect(self.extract_text)

        self.image_path = ""

    def select_image(self):
        """Select the image that contains the hidden text."""
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.bmp)")
        if path:
            self.image_path = path
            self.label.setText("Click 'Extract Text' to retrieve hidden text.")

    def extract_text(self):
        """Run the extraction subprocess to retrieve hidden text."""
        if not self.image_path:
            self.show_error("❌ Please select an image first.")
            return

        try:
            script_path = os.path.join(os.path.dirname(__file__), "..", "core", "text_hiding.py")
            print("Extract text subprocess call:")
            print("  Script Path:", script_path)
            print("  Image Path:", self.image_path)

            result = subprocess.run(
                [sys.executable, script_path, "extract", self.image_path],
                capture_output=True, text=True
            )

            print("Subprocess STDOUT:", result.stdout)
            print("Subprocess STDERR:", result.stderr)
            print("Returncode:", result.returncode)

            if result.returncode != 0:
                error_msg = result.stderr.strip() or "Unknown error occurred during extraction."
                self.show_error(f"❌ Error extracting text:\n{error_msg}")
                return

            extracted_text = result.stdout.strip()
            if extracted_text:
                self.extracted_text.setText(extracted_text)
                self.show_info(f"✅ Extracted text:\n{extracted_text}")
            else:
                self.extracted_text.setText("⚠ No hidden text found.")
                self.show_warning("⚠ No hidden text found.")

        except FileNotFoundError as e:
            self.show_error("❌ Could not find 'text_hiding.py' in the 'core' folder.")
            print("FileNotFoundError:", e)
        except Exception as e:
            error_trace = traceback.format_exc()
            self.show_error(f"❌ Unexpected error:\n{str(e)}")
            print("Unexpected Error:\n", error_trace)

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

    def show_warning(self, message):
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox { background-color: #000000 !important; }
            QMessageBox QLabel { background-color: #000000 !important; color: #00FF00 !important; font-size: 14px !important; }
            QMessageBox QPushButton { background-color: #101010 !important; border: 2px solid #00FFFF !important; color: #00FF00 !important; }
            QMessageBox QPushButton:hover { border-color: #FF00FF !important; }
            QMessageBox QPushButton:pressed { background-color: #222222 !important; }
        """)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(message)
        msg_box.exec()