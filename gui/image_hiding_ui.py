from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from PyQt6.QtGui import QFont
import sys
import subprocess
import os
import styles  # Import centralized styling

class ImageHidingWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hide an Image")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")  # Use global background color

        # Load font
        self.font = QFont("Courier New", 12, QFont.Weight.Bold)

        # Labels
        self.label = QLabel("Step 1: Select a host image", self)
        self.label.setFont(self.font)
        self.label.setStyleSheet(styles.LABEL_STYLE)  # Use label styling

        # Buttons (Initially, only the first button is visible)
        self.btn_select_host = QPushButton("📁 Select Host Image")
        self.btn_select_secret = QPushButton("📁 Select Secret Image")
        self.btn_save_output = QPushButton("💾 Save Output Image")
        self.btn_hide = QPushButton("🔥 Hide Image")

        # Apply centralized styling
        for btn in [self.btn_select_host, self.btn_select_secret, self.btn_save_output, self.btn_hide]:
            btn.setFont(self.font)
            btn.setStyleSheet(styles.BUTTON_STYLE)

        # Hide all buttons except the first one
        self.btn_select_secret.hide()
        self.btn_save_output.hide()
        self.btn_hide.hide()

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.btn_select_host)
        self.layout.addWidget(self.btn_select_secret)
        self.layout.addWidget(self.btn_save_output)
        self.layout.addWidget(self.btn_hide)

        self.setLayout(self.layout)

        # Button actions
        self.btn_select_host.clicked.connect(self.select_host_image)
        self.btn_select_secret.clicked.connect(self.select_secret_image)
        self.btn_save_output.clicked.connect(self.select_output_path)
        self.btn_hide.clicked.connect(self.hide_image)

        # Paths
        self.host_image_path = ""
        self.secret_image_path = ""
        self.output_image_path = ""

    def select_host_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Host Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.host_image_path = path
            self.label.setText("Step 2: Select a secret image")
            self.btn_select_secret.show()  # Show the next button

    def select_secret_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Secret Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.secret_image_path = path
            self.label.setText("Step 3: Choose where to save the output")
            self.btn_save_output.show()  # Show the next button

    def select_output_path(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Stego Image", "", "Images (*.png)")
        if path:
            self.output_image_path = path
            self.label.setText("Step 4: Click 'Hide Image' to complete the process")
            self.btn_hide.show()  # Show the final button

    def hide_image(self):
        if not self.host_image_path or not self.secret_image_path or not self.output_image_path:
            self.label.setText("❌ Error: Missing required files. Please complete all steps.")
            return

        # Ensure correct path to hider.py
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        hider_path = os.path.join(base_dir, "core", "hider.py")

        # Run hider.py as subprocess with error handling
        try:
            result = subprocess.run(
                [sys.executable, hider_path, self.host_image_path, self.secret_image_path, self.output_image_path],
                check=True, capture_output=True, text=True
            )
            self.label.setText(f"✅ Image hidden successfully! Saved to:\n{self.output_image_path}")
            self.btn_hide.hide()  # Hide the button after completion
        except subprocess.CalledProcessError as e:
            self.label.setText(f"❌ Error: {e.stderr.strip()}")
