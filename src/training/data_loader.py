import pandas as pd
from datasets import Dataset
import os

def load_dataset(csv_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    csv_path = os.path.join(current_dir, "dataset.csv") 
    df = pd.read_csv(csv_path)
    dataset = Dataset.from_pandas(df)
    return dataset

if __name__ == "__main__":
    dataset = load_dataset("dataset.csv")
    print(dataset)