from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from PyQt6.QtGui import QFont
import os
from styles import styles

# Import the helper function from uncover.py
from core.uncover import extract_secret_wrapper


class ImageExtractWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Extract Hidden Image")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")  # Use global background color

        # Load font
        self.font = QFont("Courier New", 12, QFont.Weight.Bold)

        # Labels
        self.label = QLabel("Step 1: Select a stego image", self)
        self.label.setFont(self.font)
        self.label.setStyleSheet(styles.LABEL_STYLE)

        # Buttons (Initially, only the first button is visible)
        self.btn_select_stego = QPushButton("Select Stego Image")
        self.btn_save_output = QPushButton("Save Extracted Image")
        self.btn_extract = QPushButton("Extract Image")

        # Apply centralized styling
        for btn in [self.btn_select_stego, self.btn_save_output, self.btn_extract]:
            btn.setFont(self.font)
            btn.setStyleSheet(styles.BUTTON_STYLE)

        # Hide the next steps initially
        self.btn_save_output.hide()
        self.btn_extract.hide()

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.btn_select_stego)
        self.layout.addWidget(self.btn_save_output)
        self.layout.addWidget(self.btn_extract)

        self.setLayout(self.layout)

        # Button actions
        self.btn_select_stego.clicked.connect(self.select_stego_image)
        self.btn_save_output.clicked.connect(self.select_output_path)
        self.btn_extract.clicked.connect(self.extract_image)

        # Paths
        self.stego_image_path = ""
        self.output_image_path = ""

    def select_stego_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Stego Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.stego_image_path = path
            self.label.setText("Step 2: Choose where to save the extracted image")
            self.btn_save_output.show()

    def select_output_path(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Extracted Image", "", "Images (*.png)")
        if path:
            self.output_image_path = path
            self.label.setText("Step 3: Click 'Extract Image' to complete the process")
            self.btn_extract.show()

    def extract_image(self):
        if not self.stego_image_path or not self.output_image_path:
            self.label.setText("❌ Error: Select all files first.")
            return

        try:
            # Directly extract the secret using the helper function
            extract_secret_wrapper(self.stego_image_path, self.output_image_path)
            self.label.setText(f"✅ Image extracted successfully! Saved to:\n{self.output_image_path}")
            self.btn_extract.hide()  # Hide the button after completion

        except Exception as e:
            self.label.setText(f"❌ Extraction failed: {e}")
