from PyQt6.QtGui import QFont, QColor, QMovie
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QLabel
import os


glitch_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "glitch.gif"))
print(f"Glitch GIF Path: {glitch_path}")
print(f"File Exists: {os.path.exists(glitch_path)}")

# 🎨 **Color Palette**
BACKGROUND_COLOR = "#000000"  # Pure Black (Retro CRT background)
TEXT_COLOR = "#00FF00"  # Neon Green (Terminal-style text)
ACCENT_COLOR = "#FF0000"  # Neon Red (For warnings/errors)
BORDER_COLOR = "#00FFFF"  # Cyan Neon Border
HIGHLIGHT_COLOR = "#FF00FF"  # Magenta glow (for buttons & effects)
BUTTON_BG_COLOR = "#101010"  # Dark Gray (better visibility)

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
    background-color: #111111;  /* Dark gray for retro look */
    border: 2px solid {BORDER_COLOR};  /* Cyan neon border */
    color: {TEXT_COLOR};  /* Green neon text */
    padding: 10px;
    font-family: 'Courier New';
    font-size: 14px;
    letter-spacing: 1px;
"""



# 🎮 **Button Styling (Now Uses a GIF Overlay)**
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
        border-color: {HIGHLIGHT_COLOR}; /* Magenta Border on Hover */
        text-shadow: 0px 0px 10px {HIGHLIGHT_COLOR}; /* Glow Effect */
    }}
    QPushButton:pressed {{
        background-color: #222222; /* Slightly Lighter When Clicked */
    }}
"""

# 🌀 **Dynamic GIF Overlay (Glitch Effect)**
def create_glitch_label(parent):
    """Creates a QLabel with a QMovie glitch animation overlay."""
    glitch_label = QLabel(parent)
    glitch_label.setGeometry(parent.geometry())  # Make it same size as button
    glitch_movie = QMovie(GLITCH_GIF_PATH)
    glitch_label.setMovie(glitch_movie)
    glitch_movie.start()
    glitch_label.hide()  # Hide by default
    return glitch_label

# 💀 **Skeleton Theme - Neon Glow Effect**
def create_glow_effect():
    glow = QGraphicsDropShadowEffect()
    glow.setColor(QColor(BORDER_COLOR))  # Cyan glow
    glow.setBlurRadius(20)
    glow.setOffset(0, 0)
    return glow
