from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt
from styles import styles
import os
import sys
import traceback

# Import the helper function from hider.py
from core.hider import embed_secret_wrapper


class ImageHidingWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hide an Image")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")

        # Load font
        self.font = styles.FONT_RETRO

        # 🖼️ Title Label
        self.label = QLabel("STEP 1: Select a host image", self)
        self.label.setFont(self.font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(styles.LABEL_STYLE)

        # 🎮 Load Glitch GIF for Hover Effect
        self.glitch_gif_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "glitch.gif"))

        # 🎛️ Buttons
        self.btn_select_host = QPushButton("Select Host Image", self)
        self.btn_select_secret = QPushButton("Select Secret Image", self)
        self.btn_save_output = QPushButton("Save Output Image", self)
        self.btn_hide = QPushButton("Hide Image", self)

        # Apply styles and glow effect
        for btn in [self.btn_select_host, self.btn_select_secret, self.btn_save_output, self.btn_hide]:
            btn.setFont(self.font)
            btn.setStyleSheet(styles.BUTTON_STYLE)
            btn.setGraphicsEffect(styles.create_glow_effect())
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Hide buttons initially (Step-by-step flow)
        self.btn_select_secret.hide()
        self.btn_save_output.hide()
        self.btn_hide.hide()

        # 🎥 Glitch Overlay for Buttons
        self.glitch_labels = {}  # Store glitch labels for each button
        for btn in [self.btn_select_host, self.btn_select_secret, self.btn_save_output, self.btn_hide]:
            glitch_label = QLabel(self)
            if os.path.exists(self.glitch_gif_path):
                glitch_gif = QMovie(self.glitch_gif_path)
                glitch_label.setMovie(glitch_gif)
                glitch_label.setScaledContents(True)  # Ensure it fits the button
                glitch_gif.start()
                glitch_label.hide()  # Hidden until hover
                self.glitch_labels[btn] = glitch_label

        # 📌 Layout Configuration
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select_host)
        layout.addWidget(self.btn_select_secret)
        layout.addWidget(self.btn_save_output)
        layout.addWidget(self.btn_hide)

        self.setLayout(layout)

        # Button actions
        self.btn_select_host.clicked.connect(self.select_host_image)
        self.btn_select_secret.clicked.connect(self.select_secret_image)
        self.btn_save_output.clicked.connect(self.select_output_path)
        self.btn_hide.clicked.connect(self.hide_image)

        # Hover Actions (Show and Hide Glitch)
        for btn in [self.btn_select_host, self.btn_select_secret, self.btn_save_output, self.btn_hide]:
            btn.enterEvent = lambda event, b=btn: self.show_glitch(event, b)
            btn.leaveEvent = lambda event, b=btn: self.hide_glitch(event, b)

        # File Paths
        self.host_image_path = ""
        self.secret_image_path = ""
        self.output_image_path = ""

    def select_host_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Host Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.host_image_path = path
            self.label.setText("STEP 2: Select a secret image")
            self.btn_select_secret.show()

    def select_secret_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Secret Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.secret_image_path = path
            self.label.setText("STEP 3: Choose output file location")
            self.btn_save_output.show()

    def select_output_path(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Stego Image", "", "Images (*.png)")
        if path:
            self.output_image_path = self.ensure_png_extension(path)
            self.label.setText("STEP 4: Click 'Hide Image' to complete")
            self.btn_hide.show()

    def ensure_png_extension(self, path):
        """ Ensure the output file has a .png extension. """
        return path if path.lower().endswith(".png") else f"{path}.png"

    def hide_image(self):
        if not self.host_image_path or not self.secret_image_path or not self.output_image_path:
            self.label.setText("❌ Error: Select all files first.")
            return

        try:
            # Directly embed the secret image using the helper function
            embed_secret_wrapper(self.host_image_path, self.secret_image_path, self.output_image_path)
            self.label.setText(f"✅ Image hidden successfully!\nSaved to:\n{self.output_image_path}")
            self.btn_hide.hide()
        except Exception as e:
            error_trace = traceback.format_exc()
            print("🚨 Exception in hide_image():\n", error_trace)
            self.label.setText(f"❌ Unexpected Error:\n{str(e)}\n\nCheck the terminal.")

    def show_glitch(self, event, button):
        """ Show glitch effect when hovering over a button. """
        if button in self.glitch_labels:
            glitch_label = self.glitch_labels[button]
            glitch_label.setGeometry(button.geometry())  # Position glitch exactly over button
            glitch_label.raise_()  # Make sure glitch is above the background
            button.raise_()  # Ensure button text stays visible above glitch
            glitch_label.show()

    def hide_glitch(self, event, button):
        """ Hide glitch effect when leaving a button. """
        if button in self.glitch_labels:
            self.glitch_labels[button].hide()
