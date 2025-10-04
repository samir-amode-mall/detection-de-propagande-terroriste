import numpy as np
import torch
import evaluate  # Utilisation de evaluate pour les métriques
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import load_dataset
from transformers import BertForSequenceClassification, DistilBertForSequenceClassification, DistilBertTokenizerFast, TrainingArguments, Trainer
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import torch.nn.functional as F

# Détection automatique du périphérique
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Chargement des métriques
accuracy_metric = evaluate.load("accuracy")
f1_metric = evaluate.load("f1")

LABELS = {
    0: "Propagande",
    1: "Neutre",
    2: "Opinion",
    3: "Fait",
    4: "Autre"
}

# Chargement du dataset
dataset = load_dataset("csv", data_files={"train": "src/training/dataset.csv", "test": "src/training/dataset.csv"})

# Initialisation de DistilBERT
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=256)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Chargement du modèle DistilBERT
student_model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=len(LABELS)).to(device)

# Chargement du modèle professeur (BERT déjà entraîné)
teacher_model = BertForSequenceClassification.from_pretrained("./models/bert_propagande_detector").to(device)
teacher_model.eval()  # Mode évaluation

def distillation_loss(student_logits, teacher_logits, temperature=2.0):
    """Perte de distillation basée sur KL-Divergence."""
    student_probs = F.log_softmax(student_logits / temperature, dim=-1)
    teacher_probs = F.softmax(teacher_logits / temperature, dim=-1)
    return F.kl_div(student_probs, teacher_probs, reduction="batchmean") * (temperature ** 2)

def compute_metrics(eval_pred):
    student_logits, labels = eval_pred
    with torch.no_grad():  # Obtenir les prédictions de BERT
        teacher_logits = teacher_model(torch.tensor(labels).unsqueeze(0).to(device)).logits.cpu()

    
    loss = distillation_loss(torch.tensor(student_logits), teacher_logits)
    predictions = np.argmax(student_logits, axis=-1)
    accuracy = accuracy_metric.compute(predictions=predictions, references=labels)
    f1 = f1_metric.compute(predictions=predictions, references=labels, average="weighted")
    return {"accuracy": accuracy["accuracy"], "f1": f1["f1"], "distillation_loss": loss.item()}

# Paramètres d'entraînement
training_args = TrainingArguments(
    output_dir="./models",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir="./logs",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    learning_rate=3e-5,
    load_best_model_at_end=True,
    metric_for_best_model="f1",
)

trainer = Trainer(
    model=student_model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()

# Évaluation finale
print("\n Évaluation finale du modèle sur le dataset de test :")
results = trainer.evaluate()

def plot_confusion_matrix(labels, predictions):
    cm = confusion_matrix(labels, predictions)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=LABELS.values(), yticklabels=LABELS.values())
    plt.xlabel("Prédictions")
    plt.ylabel("Véritables classes")
    plt.title("Matrice de Confusion")
    plt.show()

predictions_output = trainer.predict(tokenized_datasets["test"])
final_predictions = np.argmax(predictions_output.predictions, axis=-1)
true_labels = tokenized_datasets["test"]["label"]

plot_confusion_matrix(true_labels, final_predictions)

# Sauvegarde du modèle
student_model.save_pretrained("./models/distilbert_propagande_detector")
tokenizer.save_pretrained("./models/distilbert_propagande_detector")

print("\n Modèle DistilBERT sauvegardé avec succès dans ./models/distilbert_propagande_detector !")