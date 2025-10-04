from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.auth.auth_manager import login
from src.ui.main_window import MainWindow  

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connexion - TerrorISM Propagande Finder")
        self.setGeometry(400, 200, 500, 400) 


        self.setStyleSheet("""
            background-color: #3c3c3c; 
            color: white;  /* Texte blanc */
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20) 
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("TPF")
        title_label.setFont(QFont("Arial", 90, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ECF0F1; padding-bottom: 15px;")  
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setFont(QFont("Arial", 14))
        self.username_input.setStyleSheet("""
            padding: 10px;
            border: 2px solid #787878;
            border-radius: 5px;
            background-color: #787878;
            color: black;
        """)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Arial", 14))
        self.password_input.setStyleSheet("""
            padding: 10px;
            border: 2px solid #787878;
            border-radius: 5px;
            background-color: #787878;
            color: black;
        """)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Se connecter")
        self.login_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.login_button.setStyleSheet("""
            background-color: #27AE60;  /* Vert */
            color: white;
            padding: 10px;
            border-radius: 5px;
        """)
        self.login_button.clicked.connect(self.authenticate_user)

        layout.addWidget(self.login_button)

        self.quit_button = QPushButton("Quitter")
        self.quit_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.quit_button.setStyleSheet("""
            background-color: #E74C3C;  /* Rouge */
            color: white;
            padding: 10px;
            border-radius: 5px;
        """)
        self.quit_button.clicked.connect(self.close_application)

        layout.addWidget(self.quit_button)

        self.setLayout(layout)

    def authenticate_user(self):
        """Vérifie l'authentification avant d'ouvrir MainWindow"""
        username = self.username_input.text()
        password = self.password_input.text()

        response, status = login(username, password)

        if status == 200:
            QMessageBox.information(self, "Succès", "Connexion réussie !")
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Erreur", response["message"])

    def open_main_window(self):
        """Ouvre MainWindow et ferme LoginWindow"""
        self.main_window = MainWindow()
        self.main_window.show()
        self.close() 

    def close_application(self):
        """Ferme l'application"""
        self.close() 
        sys.exit() 
