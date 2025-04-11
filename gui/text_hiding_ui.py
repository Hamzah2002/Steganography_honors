import sys
import traceback
import os

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QTextEdit, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from styles import styles

# Import helper functions from your core/text_hiding.py module
from core.Text_Hiding import hide_text_wrapper, extract_text_wrapper


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
            # Ensure the user has an actual extension; default to .png if not provided
            _, ext = os.path.splitext(path)
            if not ext:
                path += ".png"
            self.output_image_path = path

            self.label.setText("STEP 3: Enter your text above, then click 'Hide Text'")
            self.btn_hide_text.show()

    def hide_text(self):
        """Step 3: Embed the provided text into the selected image."""
        if not self.image_path:
            self.show_error("❌ Please select an image first.")
            return

        if not self.output_image_path:
            self.show_error("❌ Please select an output path.")
            return

        text = self.text_input.toPlainText().strip()
        if not text:
            self.show_error("❌ Please enter text to hide.")
            return

        try:
            # Directly embed the text using the helper function
            hide_text_wrapper(self.image_path, text, self.output_image_path)
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
        except Exception as e:
            error_trace = traceback.format_exc()
            self.show_error(f"❌ Failed to hide text:\n{str(e)}")
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


#################################################################
# Text Extraction Window for Extracting Hidden Text from Image  #
#################################################################

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
        """Extract hidden text using the helper function."""
        if not self.image_path:
            self.show_error("❌ Please select an image first.")
            return

        try:
            extracted_text = extract_text_wrapper(self.image_path)

            if extracted_text:
                self.extracted_text.setText(extracted_text)
                self.show_info(f"✅ Extracted text:\n{extracted_text}")
            else:
                self.extracted_text.setText("⚠ No hidden text found.")
                self.show_warning("⚠ No hidden text found.")
        except Exception as e:
            self.show_error(f"❌ Extraction failed:\n{str(e)}")
            print("Extraction error:", e)

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
