from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QMenuBar, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.ui.text_window import TextWindow
from src.ui.picture_window import PictureWindow
from src.ui.audio_window import AudioWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Terrorism Propaganda Finder - Menu")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.show_main_interface()

    def show_main_interface(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Fichier")
        import_action = QAction("Importer un fichier", self)
        import_action.triggered.connect(self.import_file)
        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(import_action)
        file_menu.addAction(quit_action)

        layout = QVBoxLayout()

        logo_label = QLabel()
        pixmap = QPixmap("src/ui/assets/file.png")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        self.text_button = QPushButton("Analyse de Texte")
        self.image_button = QPushButton("Analyse d'Image")
        self.audio_button = QPushButton("Analyse Audio")
        self.quit_button = QPushButton("Quitter")

        self.text_button.clicked.connect(lambda: self.open_analysis("texte"))
        self.image_button.clicked.connect(lambda: self.open_analysis("image"))
        self.audio_button.clicked.connect(lambda: self.open_analysis("audio"))
        self.quit_button.clicked.connect(self.close)

        for button in [self.text_button, self.image_button, self.audio_button, self.quit_button]:
            layout.addWidget(button)

        self.central_widget.setLayout(layout)

    def open_analysis(self, analysis_type):
        if analysis_type == "texte":
            self.analysis_window = TextWindow()
        elif analysis_type == "image":
            self.analysis_window = PictureWindow()
        elif analysis_type == "audio":
            self.analysis_window = AudioWindow()
        
        self.analysis_window.show()
        self.close() 

    def import_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner un fichier", "",
            "Tous les fichiers (*);;Textes (*.txt);;Images (*.png *.jpg);;Audios (*.mp3 *.wav);;Vidéos (*.mp4 *.avi)",
            options=options
        )
        if file_path:
            QMessageBox.information(self, "Fichier sélectionné", f"Vous avez sélectionné :\n{file_path}")

