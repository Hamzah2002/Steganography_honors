from gui.gui_window import RetroStegApp  # Import the main window class
from PyQt6.QtWidgets import QApplication
import sys


def main():
    """Entry point for the Retro Steganography GUI application."""
    app = QApplication(sys.argv)  # Create the application instance
    window = RetroStegApp()  # Instantiate the main window
    window.show()  # Show the window
    sys.exit(app.exec())  # Start the event loop

if __name__ == "__main__":
    main()
