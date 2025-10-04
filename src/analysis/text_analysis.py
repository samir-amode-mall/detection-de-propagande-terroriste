from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from transformers_interpret import SequenceClassificationExplainer
from collections import Counter

LABELS = {
    "LABEL_0": "Propagande",
    "LABEL_1": "Neutre",
    "LABEL_2": "Opinion",
    "LABEL_3": "Fait",
    "LABEL_4": "Autre"
}

class SentimentAnalyzer:
    def __init__(self):
        self.model_name = "HomardBacon/distilbert-propagande-detector"
        self.analyzer = pipeline("text-classification", model=self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.explainer = SequenceClassificationExplainer(self.model, self.tokenizer)

    def analyze(self, text):
        if not text.strip():
            return {
                "sentiment": "Aucun texte fourni",
                "confidence": 0.0,
                "keywords": {}
            }

        result = self.analyzer(text)[0]
        label = LABELS.get(result["label"], "Inconnu")
        word_attributions = self.explainer(text)
        keywords = [word for word, score in word_attributions if score > 0.1]
        keywords_freq = dict(Counter(keywords))

        return {
            "sentiment": label,
            "confidence": round(result["score"] * 100, 2),
            "keywords": keywords_freq
        }

def analyze_and_get_results(text):
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze(text)
    return {
        "text": text,
        "sentiment": result["sentiment"],
        "confidence": result["confidence"],
        "keywords": result["keywords"]
    }
