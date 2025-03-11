# styles.py - Centralized styling for the Retro Steganography GUI

# 🎨 Colors
BACKGROUND_COLOR = "#000000"  # Pure Black (Retro CRT background)
TEXT_COLOR = "#00FF00"  # Neon Green (Terminal-style text)
BUTTON_BG_COLOR = "#101010"  # Dark Gray (for better visibility)
BUTTON_HOVER_COLOR = "#005500"  # Deep Green Glow on Hover
BORDER_COLOR = "#00FF00"  # Neon Green Border
ERROR_COLOR = "#FF0000"  # Red (for error messages)

# 📌 Stylesheets for UI Elements
LABEL_STYLE = f"""
    color: {TEXT_COLOR};
    font-size: 16px;
    padding: 5px;
"""

BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {BUTTON_BG_COLOR};
        color: {TEXT_COLOR};
        border: 2px solid {BORDER_COLOR};
        padding: 10px;
    }}
    QPushButton:hover {{
        background-color: {BUTTON_HOVER_COLOR};
    }}
"""

TEXT_INPUT_STYLE = f"""
    color: {TEXT_COLOR};
    background-color: {BACKGROUND_COLOR};
    border: 2px solid {BORDER_COLOR};
    font-size: 14px;
    padding: 5px;
"""

TEXT_OUTPUT_STYLE = f"""
    color: {TEXT_COLOR};
    background-color: {BACKGROUND_COLOR};
    border: 2px solid {BORDER_COLOR};
    font-size: 14px;
    padding: 5px;
    read-only: true;
"""

ERROR_LABEL_STYLE = f"""
    color: {ERROR_COLOR};
    font-size: 14px;
    padding: 5px;
"""
