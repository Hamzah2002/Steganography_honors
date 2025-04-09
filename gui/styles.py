# styles.py
from PyQt6.QtGui import QFont, QColor, QMovie
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QLabel
import os

# 🎨 **Color Palette**
BACKGROUND_COLOR = "#000000"  # Pure Black (Retro CRT background)
TEXT_COLOR = "#00FF00"        # Neon Green (Terminal-style text)
ACCENT_COLOR = "#FF0000"      # Neon Red (For warnings/errors)
BORDER_COLOR = "#00FFFF"      # Cyan Neon Border
HIGHLIGHT_COLOR = "#FF00FF"   # Magenta glow (for buttons & effects)
BUTTON_BG_COLOR = "#101010"   # Dark Gray (better visibility)

# 📂 **Glitch GIF Path**
GLITCH_GIF_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "glitch.gif"))

# 🖥️ **Fonts**
FONT_RETRO = QFont("Courier New", 14, QFont.Weight.Bold)

# 📢 **Label Styling**
LABEL_STYLE = f"""
    color: {TEXT_COLOR};
    font-size: 16px;
    letter-spacing: 2px;
    text-transform: uppercase;
    text-shadow: 0px 0px 10px {ACCENT_COLOR};
"""

# 🖊️ **Text Input Styling (For QTextEdit)**
TEXT_INPUT_STYLE = f"""
    background-color: #111111;
    border: 2px solid {BORDER_COLOR};
    color: {TEXT_COLOR};
    padding: 10px;
    font-family: 'Courier New';
    font-size: 14px;
    letter-spacing: 1px;
"""

# 🎮 **Button Styling**
BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {BUTTON_BG_COLOR};
        border: 2px solid {BORDER_COLOR};
        padding: 10px;
        color: {TEXT_COLOR};
        font-weight: bold;
        font-family: 'Courier New';
        transition: all 0.2s ease-in-out;
    }}
    QPushButton:hover {{
        border-color: {HIGHLIGHT_COLOR};
        text-shadow: 0px 0px 10px {HIGHLIGHT_COLOR};
    }}
    QPushButton:pressed {{
        background-color: #222222;
    }}
"""

# 🚨 **MessageBox Styling**
# This style ensures that any QMessageBox that uses it will display with a black background,
# neon green text, and buttons that match your retro theme.
MESSAGE_BOX_STYLE = f"""
    QMessageBox {{
        background-color: {BACKGROUND_COLOR} !important;
    }}
    QMessageBox QLabel {{
        background-color: {BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR} !important;
        font-size: 14px !important;
    }}
    QMessageBox QPushButton {{
        background-color: {BUTTON_BG_COLOR} !important;
        border: 2px solid {BORDER_COLOR} !important;
        color: {TEXT_COLOR} !important;
        font-family: 'Courier New';
    }}
    QMessageBox QPushButton:hover {{
        border-color: {HIGHLIGHT_COLOR} !important;
        text-shadow: 0px 0px 10px {HIGHLIGHT_COLOR} !important;
    }}
    QMessageBox QPushButton:pressed {{
        background-color: #222222 !important;
    }}
"""

# 🌀 **Dynamic GIF Overlay (Glitch Effect)**
def create_glitch_label(parent):
    glitch_label = QLabel(parent)
    glitch_label.setGeometry(parent.geometry())
    glitch_movie = QMovie(GLITCH_GIF_PATH)
    glitch_label.setMovie(glitch_movie)
    glitch_movie.start()
    glitch_label.hide()
    return glitch_label

# 💀 **Neon Glow Effect (for buttons, labels, etc.)**
def create_glow_effect():
    glow = QGraphicsDropShadowEffect()
    glow.setColor(QColor(BORDER_COLOR))
    glow.setBlurRadius(20)
    glow.setOffset(0, 0)
    return glow
