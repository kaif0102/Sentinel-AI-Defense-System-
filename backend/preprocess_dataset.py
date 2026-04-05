import pandas as pd
import os
import re
import string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_PATH = os.path.join(BASE_DIR, "..", "data", "raw", "train.csv")

PROCESSED_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed",
    "train_clean.csv"
)
os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"\d+", "", text)

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    text = text.strip()

    return text


print("Loading dataset...")

df = pd.read_csv(RAW_PATH)


print("Cleaning text...")

df["clean_text"] = df["text"].apply(clean_text)


print("Removing duplicates...")

df.drop_duplicates(subset=["clean_text"], inplace=True)


print("Removing missing values...")

df.dropna(inplace=True)


print("Saving cleaned dataset...")

df.to_csv(PROCESSED_PATH, index=False)


print("Preprocessing complete.")