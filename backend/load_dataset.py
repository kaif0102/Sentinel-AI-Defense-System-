from datasets import load_dataset
import pandas as pd
import os

print("Downloading dataset...")

dataset = load_dataset(
    "neuralchemy/Prompt-injection-dataset",
    "core"
)

# Fix path issue by building absolute project-safe path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "raw")

os.makedirs(RAW_DATA_PATH, exist_ok=True)

print("Saving train split...")
train_df = pd.DataFrame(dataset["train"])
train_df.to_csv(os.path.join(RAW_DATA_PATH, "train.csv"), index=False)

print("Saving validation split...")
val_df = pd.DataFrame(dataset["validation"])
val_df.to_csv(os.path.join(RAW_DATA_PATH, "val.csv"), index=False)

print("Saving test split...")
test_df = pd.DataFrame(dataset["test"])
test_df.to_csv(os.path.join(RAW_DATA_PATH, "test.csv"), index=False)

print("Dataset downloaded successfully")