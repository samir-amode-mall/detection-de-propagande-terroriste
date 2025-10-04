from transformers import BertTokenizer
from data_loader import load_dataset

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def tokenize_function(examples):
    """Tokenise le texte avec le tokenizer de BERT"""
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

 

if __name__ == "__main__":
    dataset = load_dataset("src/training/dataset.csv")  
    tokenized_datasets = dataset.map(tokenize_function, batched=True)  
    print("\nDataset tokenisé avec succès. Exemple :")
    print(tokenized_datasets[0]) 