# train_proficiency_model.py
import pandas as pd
import joblib
import os
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# Config
# -----------------------------
DATASET_PATH = "evaluation_dataset.csv"
MODEL_PATH = "proficiency_model.pkl"
OUTPUT_DIR = "."

# -----------------------------
# Load dataset
# -----------------------------
print("Loading dataset...")
df = pd.read_csv(DATASET_PATH)
texts = df["snippet"].tolist()
labels = df["true_level"].tolist()

# -----------------------------
# Embeddings
# -----------------------------
print("Generating embeddings...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
X = embedding_model.encode(texts)

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.2, random_state=42, stratify=labels
)

# -----------------------------
# Train classifier
# -----------------------------
print("Training classifier...")
clf = LogisticRegression(max_iter=1000, class_weight="balanced")
clf.fit(X_train, y_train)

# -----------------------------
# Evaluate
# -----------------------------
print("Evaluating model...")
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc:.2f}")
print(classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=clf.classes_)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=clf.classes_, yticklabels=clf.classes_)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "training_confusion_matrix.png"))
plt.close()

# Save classification report as heatmap
report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
df_report = pd.DataFrame(report).transpose()
plt.figure(figsize=(8, 4))
sns.heatmap(df_report.iloc[:-1, :-1], annot=True, fmt=".2f", cmap="Blues")
plt.title("Classification Report")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "training_classification_report.png"))
plt.close()

# -----------------------------
# Save model
# -----------------------------
joblib.dump(clf, MODEL_PATH)
print(f"✅ Model saved as {MODEL_PATH}")
