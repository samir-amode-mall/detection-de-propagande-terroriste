from PyQt5.QtWidgets import QPushButton, QMessageBox, QVBoxLayout
from src.ui.analysis_window import AnalysisWindow
from src.analysis.pictures_analysis import ImageAnalyzer
from src.analysis.text_analysis import analyze_and_get_results

class PictureWindow(AnalysisWindow):
    def __init__(self):
        super().__init__("image", ImageAnalyzer())

        self.analyze_button.setText("Analyser l'image")

        self.semantic_button = QPushButton("Analyser le texte extrait", self)
        self.semantic_button.clicked.connect(self.analyze_extracted_text)

        layout = self.centralWidget().layout()
        layout.addWidget(self.semantic_button)

    def run_analysis(self, image_path):
        try:
            # OCR : extraction du texte depuis l’image
            texte_extrait = self.analyzer.analyze_image(image_path)

            # Afficher dans la zone de texte
            self.text_input.setPlainText(texte_extrait)

            # Stocker le résultat brut comme une analyse partielle
            self.analysis_results.append({"text": texte_extrait})
            self.result_display.setText("✅ Texte extrait avec succès. Cliquez sur 'Analyser le texte extrait'.")
        except Exception as e:
            self.result_display.setText(f"⚠️ Erreur lors de l’analyse de l’image : {e}")

    def analyze_extracted_text(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Erreur", "Aucun texte extrait détecté.")
            return

        result = analyze_and_get_results(text)
        self.analysis_results.append(result)
        self.display_result(result)
