import pandas as pd
import os

# build safe absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "raw", "train.csv")

# load dataset
train_df = pd.read_csv(DATA_PATH)

print("\nFirst 5 rows:\n")
print(train_df.head())

print("\nColumn names:\n")
print(train_df.columns)

print("\nDataset shape:\n")
print(train_df.shape)

print("\nLabel distribution:\n")
print(train_df["label"].value_counts())

print("\nAttack categories:\n")
print(train_df["category"].value_counts())