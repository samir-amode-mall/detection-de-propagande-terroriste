from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget
import pyqtgraph as pg

class StatsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statistiques d'Analyse")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Graphique PyQtGraph
        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)


        x = [1, 2, 3, 4, 5]  
        y = [5, 9, 2, 7, 3]  

        self.graphWidget.plot(x, y, pen="b", symbol="o")


        self.back_button = QPushButton("Retour au Menu")
        self.back_button.clicked.connect(self.back_to_menu)
        layout.addWidget(self.back_button)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def back_to_menu(self):
        """Retour au menu principal"""
        from src.ui.main_window import MainWindow
        self.menu_window = MainWindow()
        self.menu_window.show()
        self.close()
