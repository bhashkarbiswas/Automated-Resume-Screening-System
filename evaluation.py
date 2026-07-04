import os
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(BASE_DIR, "evaluation", "results.csv")

if not os.path.exists(RESULTS_FILE):
    print("Error: results.csv not found.")
    exit()

df = pd.read_csv(RESULTS_FILE)

df = df[df["Actual_Label"].notna()]
df = df[df["Actual_Label"].astype(str).str.strip() != ""]

if len(df) == 0:
    print("No Actual_Label values found.")
    print("Please fill the Actual_Label column in results.csv.")
    exit()

actual = df["Actual_Label"]
predicted = df["Predicted_Label"]

accuracy = accuracy_score(actual, predicted)

precision = precision_score(
    actual,
    predicted,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    actual,
    predicted,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    actual,
    predicted,
    average="weighted",
    zero_division=0
)

avg_processing_time = df["Processing_Time"].mean()

print("\n========== Evaluation Results ==========\n")

print(f"Accuracy               : {accuracy * 100:.2f}%")
print(f"Precision              : {precision * 100:.2f}%")
print(f"Recall                 : {recall * 100:.2f}%")
print(f"F1-score               : {f1 * 100:.2f}%")
print(f"Average Processing Time: {avg_processing_time:.3f} sec")