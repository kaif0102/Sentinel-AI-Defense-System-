import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

train = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "train_merged.csv"))
test = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "test.csv"))
val = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "val.csv"))

print("=" * 50)
print("SENTINEL AI - DATASET STATISTICS")
print("=" * 50)

print(f"\nTRAINING SET:")
print(f"  Total samples:  {len(train)}")
print(f"  Columns: {train.columns.tolist()}")
print(f"  Safe samples:   {(train['label'] == 0).sum()}")
print(f"  Attack samples: {(train['label'] == 1).sum()}")
print(f"  Attack ratio:   {train['label'].mean():.2%}")

print(f"\nTEST SET:")
print(f"  Total samples:  {len(test)}")
print(f"  Columns: {test.columns.tolist()}")

print(f"\nVALIDATION SET:")
print(f"  Total samples:  {len(val)}")
print(f"  Columns: {val.columns.tolist()}")

total = len(train) + len(test) + len(val)
print(f"\nOVERALL TOTAL:  {total} samples")
print("=" * 50)