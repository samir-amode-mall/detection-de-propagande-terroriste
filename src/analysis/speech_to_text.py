import whisper

class SpeechAnalyzer:
    def __init__(self, model_size="base"):
        """Initialise le modèle Whisper."""
        self.model = whisper.load_model(model_size) 

    def analyze_audio(self, audio_path):
        """Convertit un fichier audio en texte."""
        try:
            result = self.model.transcribe(audio_path)
            return {"text": result["text"]}
        except Exception as e:
            return {"error": f"Erreur lors de la transcription : {str(e)}"}

    def analyze(self, audio_path):
        """Alias de analyze_audio() pour être compatible avec AnalysisWindow."""
        return self.analyze_audio(audio_path)
