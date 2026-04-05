import pandas as pd
import os
from datasets import load_dataset

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "train.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "raw", "train_merged.csv")

# ─────────────────────────────────────────
# LOAD ORIGINAL DATASET
# ─────────────────────────────────────────
print("Loading original dataset...")
df_original = pd.read_csv(RAW_PATH)
df_original = df_original[["text", "label"]].dropna()
df_original["label"] = df_original["label"].astype(int)
print(f"Original dataset: {len(df_original)} samples")

# ─────────────────────────────────────────
# LOAD DEEPSET DATASET
# ─────────────────────────────────────────
print("\nLoading deepset/prompt-injections...")
try:
    ds_deepset = load_dataset("deepset/prompt-injections")
    df_deepset = pd.DataFrame({
        "text": ds_deepset["train"]["text"],
        "label": ds_deepset["train"]["label"]
    })
    df_deepset["label"] = df_deepset["label"].astype(int)
    print(f"Deepset dataset: {len(df_deepset)} samples")
except Exception as e:
    print(f"Error loading deepset: {e}")
    df_deepset = pd.DataFrame(columns=["text", "label"])

# ─────────────────────────────────────────
# LOAD JACKHHAO DATASET
# ─────────────────────────────────────────
print("\nLoading jackhhao/jailbreak-classification...")
try:
    ds_jackhhao = load_dataset("jackhhao/jailbreak-classification")
    df_jackhhao = pd.DataFrame({
        "text": ds_jackhhao["train"]["prompt"],
        "label": [1 if t == "jailbreak" else 0 
                  for t in ds_jackhhao["train"]["type"]]
    })
    print(f"Jackhhao dataset: {len(df_jackhhao)} samples")
except Exception as e:
    print(f"Error loading jackhhao: {e}")
    df_jackhhao = pd.DataFrame(columns=["text", "label"])

# ─────────────────────────────────────────
# LOAD VERAZUO JAILBREAKS
# ─────────────────────────────────────────
print("\nLoading verazuo jailbreaks...")
try:
    ds_verazuo = load_dataset(
        "TrustAIRLab/in-the-wild-jailbreak-prompts",
        "jailbreak_2023_12_25",
        split="train"
    )
    df_verazuo = pd.DataFrame({
        "text": ds_verazuo["prompt"],
        "label": [1] * len(ds_verazuo)
    })
    print(f"Verazuo dataset: {len(df_verazuo)} samples")
except Exception as e:
    print(f"Error loading verazuo: {e}")
    df_verazuo = pd.DataFrame(columns=["text", "label"])

# ─────────────────────────────────────────
# MERGE ALL DATASETS
# ─────────────────────────────────────────
print("\nMerging all datasets...")
df_merged = pd.concat([
    df_original,
    df_deepset,
    df_jackhhao,
    df_verazuo
], ignore_index=True)

# Clean up
df_merged = df_merged[["text", "label"]].dropna()
df_merged["label"] = df_merged["label"].astype(int)
df_merged["text"] = df_merged["text"].astype(str)
df_merged.drop_duplicates(subset=["text"], inplace=True)

print(f"\n✅ Merged dataset: {len(df_merged)} samples")
print(f"Attack ratio: {df_merged['label'].mean():.2%}")
print(f"Safe samples: {(df_merged['label'] == 0).sum()}")
print(f"Attack samples: {(df_merged['label'] == 1).sum()}")

# Save
df_merged.to_csv(OUTPUT_PATH, index=False)
print(f"\n✅ Saved to {OUTPUT_PATH}")