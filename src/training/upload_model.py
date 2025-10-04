from transformers import DistilBertForSequenceClassification, DistilBertTokenizer

model_name = "HomardBacon/distilbert-propagande-detector"

# Charger le modèle entraîné depuis ton dossier local
model = DistilBertForSequenceClassification.from_pretrained("./models/distilbert_propagande_detector")

# Charger le tokenizer entraîné
tokenizer = DistilBertTokenizer.from_pretrained("./models/distilbert_propagande_detector")

# Envoyer le modèle ET le tokenizer sur Hugging Face
model.push_to_hub(model_name, commit_message="Upload DistilBERT", force=True, token=True)
tokenizer.push_to_hub(model_name, commit_message="Upload du tokenizer DistilBERT", force=True, token=True)
