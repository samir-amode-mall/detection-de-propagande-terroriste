from src.ui.analysis_window import AnalysisWindow
from src.analysis.text_analysis import SentimentAnalyzer

class TextWindow(AnalysisWindow):
    def __init__(self):
        super().__init__("texte", SentimentAnalyzer())
