from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout
)
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from styles import styles
import os
import traceback


class RetroStegApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 💀 Setup Main Window
        self.setWindowTitle("💀 ByteSmuggler 💀")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(f"background-color: {styles.BACKGROUND_COLOR};")

        # 📝 Load pixel-style font
        self.font = styles.FONT_RETRO

        # 🎞️ CRT Flicker Effect (Background)
        self.crt_effect = QLabel(self)
        crt_gif_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "crt_flicker.gif"))
        if os.path.exists(crt_gif_path):
            self.crt_gif = QMovie(crt_gif_path)
            self.crt_effect.setMovie(self.crt_gif)
            self.crt_effect.setScaledContents(True)
            self.crt_gif.start()
        self.crt_effect.setGeometry(0, 0, 800, 600)
        self.crt_effect.lower()  # Ensure it stays in the background

        # 🎮 Animated Skeleton Icon (GIF)
        self.skull_animation = QLabel(self)
        skull_gif_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "skeleton.gif"))
        if os.path.exists(skull_gif_path):
            self.skull_gif = QMovie(skull_gif_path)
            self.skull_animation.setMovie(self.skull_gif)
            self.skull_animation.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.skull_gif.start()
        else:
            self.skull_animation.setText("❌ Skeleton GIF Not Found!")

        # 📢 Title Label with Typing Effect
        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(self.font)
        self.label.setStyleSheet(styles.LABEL_STYLE)
        self.typing_text = "💀 ByteSmuggler 💀"
        self.text_index = 0
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.typing_effect)
        self.typing_timer.start(100)

        # 🎮 Buttons with Glitch Hover Effect
        self.btn_hide_image = self.create_glitch_button("🖼️ Hide Image")
        self.btn_extract_image = self.create_glitch_button("📷 Extract Image")
        self.btn_hide_text = self.create_glitch_button("✍ Hide Text")
        self.btn_extract_text = self.create_glitch_button("🔍 Extract Text")
        self.btn_encrypt = self.create_glitch_button("🔐 Encrypt Image")
        self.btn_decrypt = self.create_glitch_button("🔓 Decrypt Image")

        # 📌 Main Layout Configuration
        layout = QVBoxLayout()
        layout.addWidget(self.skull_animation)
        layout.addWidget(self.label)
        layout.addWidget(self.btn_hide_image)
        layout.addWidget(self.btn_extract_image)
        layout.addWidget(self.btn_hide_text)
        layout.addWidget(self.btn_extract_text)
        layout.addWidget(self.btn_encrypt)
        layout.addWidget(self.btn_decrypt)

        # 📦 Set Main Widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 🔗 Connect Buttons to Features
        self.btn_hide_image.clicked.connect(self.open_image_hiding)
        self.btn_extract_image.clicked.connect(self.open_image_extract)
        self.btn_hide_text.clicked.connect(self.open_text_hiding)
        self.btn_extract_text.clicked.connect(self.open_text_extract)
        self.btn_encrypt.clicked.connect(self.open_encrypt)
        self.btn_decrypt.clicked.connect(self.open_decrypt)

        # 🎵 Music Player Setup
        self.init_music()

        # 🎵 Music Control Buttons (Top-Right Corner)
        self.music_controls = QWidget(self)
        self.music_layout = QHBoxLayout()
        self.music_layout.setContentsMargins(0, 0, 10, 0)  # Ensure right alignment

        # ⏭️ Next Song Button
        self.btn_next_song = QPushButton("🎵 >>", self)
        self.btn_next_song.setFont(self.font)
        self.btn_next_song.setStyleSheet(styles.BUTTON_STYLE)
        self.btn_next_song.clicked.connect(self.play_next_song)
        self.music_layout.addWidget(self.btn_next_song)

        # 🔇 Mute Button
        self.btn_mute = QPushButton("🔇", self)
        self.btn_mute.setFont(self.font)
        self.btn_mute.setStyleSheet(styles.BUTTON_STYLE)
        self.btn_mute.clicked.connect(self.toggle_mute)
        self.music_layout.addWidget(self.btn_mute)

        self.music_controls.setLayout(self.music_layout)
        self.music_controls.setFixedSize(160, 40)  # Keep it compact
        self.update_music_button_position()  # Ensure proper positioning

        # 🔄 Resize Event Handling (Keeps Music Controls in Place)
        self.resized = False

    def resizeEvent(self, event):
        """ Updates the position of the music button when the window resizes (fixes fullscreen issue). """
        super().resizeEvent(event)
        self.update_music_button_position()

    def update_music_button_position(self):
        """ Keeps the music control buttons pinned to the top-right corner. """
        self.music_controls.move(self.width() - 180, 10)  # Ensure it stays in place
        self.music_controls.show()

    # 🎵 **MUSIC PLAYER METHODS**
    def init_music(self):
        """ Sets up the music player. """
        self.music_files = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", f"song{i}.mp3"))
            for i in range(1, 5)
        ]

        self.current_song_index = 0
        self.audio_output = QAudioOutput()
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)

        # 🔊 Set volume to 0 (it will fade in)
        self.audio_output.setVolume(0.0)

        self.play_song()

    def play_song(self):
        """Plays the current song in the playlist with a smooth volume transition."""
        song_path = self.music_files[self.current_song_index]

        if not os.path.exists(song_path):
            print(f"❌ ERROR: {song_path} not found.")
            return

        song_url = QUrl.fromLocalFile(song_path)  # Convert string to QUrl
        self.media_player.setSource(song_url)
        self.media_player.play()
        print(f"Now playing: {song_path}")

        # 🎵 Start a volume fade-in effect over 5 seconds
        self.fade_in_volume()

    def fade_in_volume(self):
        """Gradually increases the volume over 5 seconds."""
        self.audio_output.setVolume(0.0)  # Start at 0
        self.volume_level = 0.0
        self.volume_timer = QTimer(self)
        self.volume_timer.timeout.connect(self.increase_volume)
        self.volume_timer.start(250)  # Adjust every 250ms (1/4 second)

    def increase_volume(self):
        """Increases the volume smoothly."""
        if self.volume_level < 0.5:
            self.volume_level += 0.05  # Increase in small steps
            self.audio_output.setVolume(self.volume_level)
        else:
            self.volume_timer.stop()  # Stop increasing after reaching full volume

    def play_next_song(self):
        """Switch to the next song in the playlist with fade-in effect."""
        self.current_song_index = (self.current_song_index + 1) % len(self.music_files)
        self.play_song()

    def toggle_mute(self):
        """Toggles mute/unmute for the music."""
        if self.audio_output.volume() > 0:
            self.audio_output.setVolume(0)
            self.btn_mute.setText("🔊")  # Show unmute icon
        else:
            self.fade_in_volume()  # Use fade-in effect when unmuting
            self.btn_mute.setText("🔇")  # Show mute icon


    def typing_effect(self):
        """ Creates a retro terminal typing animation for the title. """
        if self.text_index < len(self.typing_text):
            self.label.setText(self.label.text() + self.typing_text[self.text_index])
            self.text_index += 1
        else:
            self.typing_timer.stop()

    def create_glitch_button(self, text):
        """ Creates a button with a hover-triggered glitch effect, while keeping it clickable. """
        btn = QPushButton(text, self)
        btn.setFont(self.font)
        btn.setStyleSheet(styles.BUTTON_STYLE)
        btn.setGraphicsEffect(styles.create_glow_effect())
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # 🎥 Glitch Effect Label
        glitch_label = QLabel(self)
        glitch_gif_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "glitch.gif"))

        if os.path.exists(glitch_gif_path):
            glitch_gif = QMovie(glitch_gif_path)
            glitch_label.setMovie(glitch_gif)
            glitch_label.setScaledContents(True)
            glitch_gif.start()
            glitch_label.hide()  # Start hidden

        # ✅ Fix: Ensure glitch effect does not block button clicks
        glitch_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        # ✅ Keep button clickable while glitch effect is shown
        btn.enterEvent = lambda event, b=btn, g=glitch_label: self.show_glitch(event, b, g)
        btn.leaveEvent = lambda event, g=glitch_label: self.hide_glitch(event, g, btn)

        return btn

    def show_glitch(self, event, button, glitch_label):
        """ Show glitch effect when hovering over a button, but keep the text above. """
        glitch_label.setGeometry(button.geometry())  # Align the glitch effect
        glitch_label.raise_()  # Keep glitch on top
        button.raise_()  # Ensure text remains visible above the glitch
        glitch_label.show()

    def hide_glitch(self, event, glitch_label, button):
        """ Hide glitch effect and keep button functional. """
        glitch_label.hide()  # Hide glitch when mouse leaves
        button.raise_()  # Ensure button stays above glitch effect

    # 🔗 Open UI Windows for Features
    def open_image_hiding(self):
        from gui.image_hiding_ui import ImageHidingWindow
        self.image_hiding_window = ImageHidingWindow()
        self.image_hiding_window.show()

    def open_image_extract(self):
        from gui.image_extract_ui import ImageExtractWindow
        self.image_extract_window = ImageExtractWindow()
        self.image_extract_window.show()

    def open_text_hiding(self):
        try:
            from gui.text_hiding_ui import TextHidingWindow
            self.text_hiding_window = TextHidingWindow()
            self.text_hiding_window.show()
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox

            # Get detailed error message
            error_trace = traceback.format_exc()
            print("🚨 ERROR in open_text_hiding():\n", error_trace)  # Print to terminal/log

            # Show full error message
            QMessageBox.critical(
                self,
                "Error",
                f"❌ Could not open Hide Text window:\n\n{str(e)}\n\nDetails:\n{error_trace}"
            )

    def open_text_extract(self):
        from gui.text_hiding_ui import TextExtractWindow
        self.text_extract_window = TextExtractWindow()
        self.text_extract_window.show()

    def open_encrypt(self):
        from gui.encryption_ui import EncryptWindow
        self.encrypt_window = EncryptWindow()
        self.encrypt_window.show()

    def open_decrypt(self):
        from gui.encryption_ui import DecryptWindow
        self.decrypt_window = DecryptWindow()
        self.decrypt_window.show()
