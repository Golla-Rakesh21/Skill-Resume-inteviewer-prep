# utils/proficiency.py
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sentence_transformers import SentenceTransformer
import datetime

# -----------------------------
# Load model + embeddings
# -----------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
MODEL_PATH = "proficiency_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"{MODEL_PATH} not found. Run train_proficiency_model.py first to create it."
    )

clf = joblib.load(MODEL_PATH)

# -----------------------------
# Core Functions
# -----------------------------
def proficiency_score(text: str, skill: str = None):
    """
    Return probabilities for beginner/intermediate/advanced using ML model.
    Keys are lowercase for consistency.
    """
    vec = embedding_model.encode([text])
    probs = clf.predict_proba(vec)[0]
    labels = [label.lower() for label in clf.classes_]  # lowercase keys
    return dict(zip(labels, probs))


def level_from_scores(scores: dict):
    """Return best label from scores dict."""
    return max(scores.items(), key=lambda kv: kv[1])[0]


# -----------------------------
# Evaluation Helper
# -----------------------------
def evaluate_model(texts, true_labels, output_dir="reports", prefix="evaluation"):
    """
    Evaluate the ML proficiency model and save results as images in a timestamped folder.
    
    Args:
        texts (list[str]): Resume snippets or sentences.
        true_labels (list[str]): Ground-truth labels ("Beginner", "Intermediate", "Advanced").
        output_dir (str): Base directory to save report folders.
        prefix (str): Prefix for saved files.
    
    Returns:
        Tuple: (predictions list, classification report DataFrame, metrics DataFrame, report folder path)
    """
    # Create a unique timestamped folder for this evaluation
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_folder = os.path.join(output_dir, f"{prefix}_{timestamp}")
    os.makedirs(report_folder, exist_ok=True)

    # Generate predictions
    X = embedding_model.encode(texts)
    preds = clf.predict(X)

    # Accuracy
    acc = accuracy_score(true_labels, preds)
    print(f"Overall Accuracy: {acc:.2f}")

    # Classification report
    report = classification_report(true_labels, preds, output_dict=True, zero_division=0)
    df_report = pd.DataFrame(report).transpose()

    # Save classification report as image
    plt.figure(figsize=(8, 4))
    sns.heatmap(df_report.iloc[:-1, :-1], annot=True, fmt=".2f", cmap="Blues")
    plt.title("Classification Report")
    plt.tight_layout()
    report_img_path = os.path.join(report_folder, f"{prefix}_classification_report.png")
    plt.savefig(report_img_path)
    plt.close()

    # Confusion matrix
    cm = confusion_matrix(true_labels, preds, labels=clf.classes_)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=clf.classes_, yticklabels=clf.classes_)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    cm_img_path = os.path.join(report_folder, f"{prefix}_confusion_matrix.png")
    plt.savefig(cm_img_path)
    plt.close()

    # Metrics summary
    metrics_summary = {
        "accuracy": acc,
        "precision_macro": report["macro avg"]["precision"],
        "recall_macro": report["macro avg"]["recall"],
        "f1_macro": report["macro avg"]["f1-score"],
    }
    df_metrics = pd.DataFrame([metrics_summary])

    plt.figure(figsize=(6, 1.5))
    sns.heatmap(df_metrics, annot=True, fmt=".2f", cmap="Greens")
    plt.title("Metrics Summary")
    plt.tight_layout()
    metrics_img_path = os.path.join(report_folder, f"{prefix}_metrics_summary.png")
    plt.savefig(metrics_img_path)
    plt.close()

    print(f"✅ Saved report images in folder: {report_folder}")
    return preds, df_report, df_metrics, report_folder
