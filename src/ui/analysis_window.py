from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QLabel, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from src.ui.results_window import ResultsWindow
from src.report.pdf_generator import PDFGenerator
from src.analysis.text_analysis import analyze_and_get_results

class AnalysisThread(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        result = analyze_and_get_results(self.text)
        self.finished.emit(result)

class AnalysisWindow(QMainWindow):
    def __init__(self, analysis_type, analyzer):
        super().__init__()
        self.setWindowTitle(f"Analyse {analysis_type.capitalize()}")
        self.setGeometry(100, 100, 800, 600)

        self.analysis_type = analysis_type
        self.analyzer = analyzer
        self.selected_file = None
        self.analysis_results = []

        layout = QVBoxLayout()
        self.result_label = QLabel(f"Analyse {analysis_type.capitalize()}", self)
        layout.addWidget(self.result_label)

        self.text_input = QTextEdit(self)
        layout.addWidget(QLabel("Texte extrait / Saisi :"))
        layout.addWidget(self.text_input)

        self.file_button = QPushButton("Importer un fichier", self)
        self.file_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.file_button)

        self.analyze_button = QPushButton("Analyser", self)
        self.analyze_button.clicked.connect(self.perform_analysis)
        layout.addWidget(self.analyze_button)

        self.result_display = QLabel("Résultat :", self)
        layout.addWidget(self.result_display)

        self.results_button = QPushButton("Voir Résultats Avancés", self)
        self.results_button.clicked.connect(self.show_results)
        layout.addWidget(self.results_button)

        self.pdf_button = QPushButton("Générer le rapport PDF", self)
        self.pdf_button.setEnabled(False)
        self.pdf_button.clicked.connect(self.generate_pdf)
        layout.addWidget(self.pdf_button)

        self.back_button = QPushButton("Retour au Menu", self)
        self.back_button.clicked.connect(self.back_to_menu)
        layout.addWidget(self.back_button)

        self.progress_label = QLabel("")
        layout.addWidget(self.progress_label)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def perform_analysis(self):
        text = self.text_input.toPlainText().strip()
        if text:
            self.progress_label.setText("Analyse en cours...")
            self.thread = AnalysisThread(text)
            self.thread.finished.connect(self.handle_analysis_result)
            self.thread.start()
        elif self.selected_file:
            self.run_analysis(self.selected_file)
            if self.analysis_type in ["audio", "image"] and self.analysis_results:
                extracted_text = self.analysis_results[-1].get("text", "")
                self.text_input.setPlainText(extracted_text)
        else:
            self.result_label.setText("Veuillez entrer du texte ou importer un fichier.")

    def handle_analysis_result(self, result):
        self.analysis_results.append(result)
        self.display_result(result)
        self.progress_label.setText("")

    def run_analysis(self, data):
        result = analyze_and_get_results(data)
        self.analysis_results.append(result)
        self.display_result(result)

    def display_result(self, result):
        if "error" in result:
            self.result_display.setText(f" {result['error']}")
            self.pdf_button.setEnabled(False)
        else:
            self.result_display.setText(f"Résultat : {result['sentiment']} (Confiance : {result['confidence']}%)")
            self.pdf_button.setEnabled(True)

    def generate_pdf(self):
        if not self.analysis_results:
            QMessageBox.warning(self, "Erreur", "Aucune analyse disponible pour générer un PDF.")
            return

        latest_result = self.analysis_results[-1]
        text = latest_result.get("text", "")

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le rapport PDF", "rapport_analyse.pdf", "PDF Files (*.pdf)"
        )

        if file_path:
            pdf_gen = PDFGenerator()
            pdf_gen.generate_pdf(text, latest_result, save_path=file_path)
            QMessageBox.information(self, "Succès", f"Rapport enregistré :\n{file_path}")

    def show_results(self):
        if self.analysis_results:
            self.results_window = ResultsWindow(self.analysis_results)
            self.results_window.show()
        else:
            QMessageBox.warning(self, "Résultats avancés", "Aucune analyse disponible pour afficher des statistiques.")

    def back_to_menu(self):
        from src.ui.main_window import MainWindow
        self.menu_window = MainWindow()
        self.menu_window.show()
        self.close()

    def open_file_dialog(self):
        if self.analysis_type == "audio":
            file_filter = "Fichiers audio (*.mp3 *.wav *.m4a *.flac);;Tous les fichiers (*)"
        elif self.analysis_type == "image":
            file_filter = "Images (*.png *.jpg *.jpeg *.bmp *.tiff);;Tous les fichiers (*)"
        else:
            file_filter = "Fichiers texte (*.txt);;Tous les fichiers (*)"

        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", file_filter)

        if file_path:
            self.selected_file = file_path
            self.result_label.setText(f"Fichier sélectionné : {file_path}")

            if self.analysis_type == "texte":
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        file_content = file.read()
                    self.text_input.setPlainText(file_content)
                except Exception as e:
                    print(f"Erreur de lecture du fichier : {e}")
                    self.result_label.setText("Impossible de lire le fichier.")
