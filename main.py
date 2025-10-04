from PyQt5.QtWidgets import QApplication
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.ui.login_window import LoginWindow  

if __name__ == "__main__":
    app = QApplication(sys.argv)

    qss_path = "src/ui/style.qss"
    if os.path.exists(qss_path):
        with open(qss_path, "r") as file:
            app.setStyleSheet(file.read())

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
