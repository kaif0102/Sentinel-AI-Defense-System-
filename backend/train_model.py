import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

# Paths
TRAIN_PATH = "data/raw/train_merged.csv"
TEST_PATH = "data/raw/test.csv"
MODEL_DIR = "models"

print("Loading data...")
train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

# Keep only text and label
train_df = train_df[["text", "label"]].dropna()
test_df = test_df[["text", "label"]].dropna()

# Convert labels to binary (0=safe, 1=attack)
train_df["label"] = train_df["label"].astype(int)
test_df["label"] = test_df["label"].astype(int)

print(f"Training samples: {len(train_df)}")
print(f"Test samples: {len(test_df)}")
print(f"Attack ratio in train: {train_df['label'].mean():.2%}")

# Vectorize text
print("\nVectorizing text...")
vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_train = vectorizer.fit_transform(train_df["text"])
X_test = vectorizer.transform(test_df["text"])

y_train = train_df["label"]
y_test = test_df["label"]

# Train model
print("\nTraining model...")
model = LogisticRegression(
    max_iter=1000,
    C=1.0,
    class_weight="balanced"
)
model.fit(X_train, y_train)

# Evaluate
print("\nEvaluating...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2%}")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred, 
      target_names=["Safe", "Attack"]))

# Save model
print("\nSaving model...")
os.makedirs(MODEL_DIR, exist_ok=True)
with open(f"{MODEL_DIR}/classifier.pkl", "wb") as f:
    pickle.dump(model, f)
with open(f"{MODEL_DIR}/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model saved to models/classifier.pkl")
print("✅ Vectorizer saved to models/vectorizer.pkl")