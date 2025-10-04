from PyQt5.QtWidgets import QPushButton, QMessageBox, QVBoxLayout, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
from src.ui.analysis_window import AnalysisWindow
from src.analysis.speech_to_text import SpeechAnalyzer
from src.analysis.text_analysis import analyze_and_get_results

class TranscriptionThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, analyzer, file_path):
        super().__init__()
        self.analyzer = analyzer
        self.file_path = file_path

    def run(self):
        try:
            result = self.analyzer.analyze(self.file_path)
            if "error" in result:
                self.error.emit(result["error"])
            else:
                self.finished.emit(result["text"])
        except Exception as e:
            self.error.emit(str(e))

class AudioWindow(AnalysisWindow):
    def __init__(self):
        super().__init__("audio", SpeechAnalyzer())

        self.analyze_button.setText("Analyser l'audio")

        self.semantic_button = QPushButton("Analyser le texte extrait", self)
        self.semantic_button.clicked.connect(self.analyze_extracted_text)
        self.semantic_button.setEnabled(False)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0) 
        self.progress_bar.setVisible(False)

        layout = self.centralWidget().layout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.semantic_button)

    def perform_analysis(self):
        if not self.selected_file:
            self.result_label.setText("Veuillez importer un fichier audio.")
            return

        self.progress_bar.setVisible(True)
        self.result_display.setText("Transcription en cours...")
        self.semantic_button.setEnabled(False)

        self.thread = TranscriptionThread(self.analyzer, self.selected_file)
        self.thread.finished.connect(self.handle_transcription_success)
        self.thread.error.connect(self.handle_transcription_error)
        self.thread.start()

    def handle_transcription_success(self, text):
        self.progress_bar.setVisible(False)
        self.text_input.setPlainText(text)
        self.result_display.setText("Transcription terminée.")
        self.semantic_button.setEnabled(True)

    def handle_transcription_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.result_display.setText(f"{error_msg}")
        self.semantic_button.setEnabled(False)

    def analyze_extracted_text(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Erreur", "Aucun texte extrait trouvé pour analyse.")
            return

        result = analyze_and_get_results(text)
        self.analysis_results.append(result)
        self.display_result(result)
