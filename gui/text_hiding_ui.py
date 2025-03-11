from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QTextEdit, QMessageBox
from PyQt6.QtGui import QFont
import sys
import subprocess
import styles  # Import centralized styling
import traceback
from PyQt6.QtWidgets import QMessageBox

class TextHidingWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hide Text in Image")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")

        # Load font
        self.font = QFont("Courier New", 12, QFont.Weight.Bold)

        # Labels
        self.label = QLabel("Select an image and enter text:", self)
        self.label.setFont(self.font)
        self.label.setStyleSheet(styles.LABEL_STYLE)

        # Input Fields
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

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.btn_select_image)
        layout.addWidget(self.btn_save_output)
        layout.addWidget(self.btn_hide_text)

        self.setLayout(layout)

        # Button actions
        self.btn_select_image.clicked.connect(self.select_image)
        self.btn_save_output.clicked.connect(self.select_output_path)
        self.btn_hide_text.clicked.connect(self.hide_text)

        # Paths
        self.image_path = ""
        self.output_image_path = ""

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.bmp)")
        if path:
            self.image_path = path

    def select_output_path(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Stego Image", "", "Images (*.bmp)")  # Save as BMP for stability
        if path:
            self.output_image_path = path



    def hide_text(self):
        if not self.image_path:
            QMessageBox.critical(self, "Error", "❌ Please select an image first.")
            return

        if not self.output_image_path:
            QMessageBox.critical(self, "Error", "❌ Please select an output path.")
            return

        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.critical(self, "Error", "❌ Please enter text to hide.")
            return

        try:
            # Attempt to run the subprocess and capture errors
            result = subprocess.run(
                [sys.executable, "core/Text_Hiding.py", "hide", self.image_path, text, self.output_image_path],
                capture_output=True, text=True
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip() or "Unknown error occurred."
                QMessageBox.critical(self, "Error", f"❌ Failed to hide text:\n{error_msg}")
                return

            QMessageBox.information(self, "Success", f"✅ Text hidden successfully in:\n{self.output_image_path}")

        except FileNotFoundError as e:
            QMessageBox.critical(self, "Error", "❌ core/Text_Hiding.py not found.")
            print("FileNotFoundError:", e)

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"❌ Subprocess error:\n{e.stderr}")
            print("CalledProcessError:", e)

        except Exception as e:
            # Capture full error trace
            error_trace = traceback.format_exc()
            QMessageBox.critical(self, "Critical Error", f"❌ Unexpected error:\n{str(e)}")
            print("Unexpected Error:\n", error_trace)


# -------------------------- TEXT EXTRACTION UI -------------------------- #
class TextExtractWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Extract Hidden Text")
        self.setGeometry(300, 300, 500, 300)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")

        # Load font
        self.font = QFont("Courier New", 12, QFont.Weight.Bold)

        # Labels
        self.label = QLabel("Select an image with hidden text:", self)
        self.label.setFont(self.font)
        self.label.setStyleSheet(styles.LABEL_STYLE)

        # Buttons
        self.btn_select_image = QPushButton("📁 Select Image")
        self.btn_extract_text = QPushButton("🔍 Extract Text")

        # Text Output
        self.extracted_text = QTextEdit(self)
        self.extracted_text.setFont(self.font)
        self.extracted_text.setReadOnly(True)
        self.extracted_text.setStyleSheet(styles.TEXT_INPUT_STYLE)

        # Apply styling
        for btn in [self.btn_select_image, self.btn_extract_text]:
            btn.setFont(self.font)
            btn.setStyleSheet(styles.BUTTON_STYLE)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select_image)
        layout.addWidget(self.btn_extract_text)
        layout.addWidget(self.extracted_text)

        self.setLayout(layout)

        # Button actions
        self.btn_select_image.clicked.connect(self.select_image)
        self.btn_extract_text.clicked.connect(self.extract_text)

        # Paths
        self.image_path = ""

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.bmp)")
        if path:
            self.image_path = path

    def extract_text(self):
        if not self.image_path:
            QMessageBox.critical(self, "Error", "❌ Please select an image first.")
            return

        try:
            # Run subprocess with error handling
            result = subprocess.run(
                [sys.executable, "core/Text_Hiding.py", "extract", self.image_path],
                capture_output=True, text=True, check=True
            )

            extracted_text = result.stdout.strip()

            if extracted_text:
                self.extracted_text.setText(extracted_text)
                QMessageBox.information(self, "Success", f"✅ Extracted text:\n{extracted_text}")
            else:
                self.extracted_text.setText("⚠ No hidden text found.")
                QMessageBox.warning(self, "Warning", "⚠ No hidden text found.")

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "❌ core/Text_Hiding.py not found.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"❌ Error extracting text:\n{e.stderr}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ Unexpected error:\n{str(e)}")
