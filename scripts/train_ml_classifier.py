import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, accuracy_score

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "training_prompts.csv")
if not os.path.exists(DATA_PATH):
    DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "archive", "legacy_datasets", "training_prompts.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "backend", "saved_models")
MODEL_FILE = os.path.join(MODEL_DIR, "classifier_model.joblib")

def train_classifier():
    if not os.path.exists(DATA_PATH):
        print(f"Error: Dataset not found at {DATA_PATH}.")
        sys.exit(1)

    print("=" * 60)
    print("  TRAINING ML COMPLEXITY CLASSIFIER")
    print("=" * 60)
    print(f"Loading training data from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} prompts.")

    # Target: 0 for simple, 1 for complex (use native Python list/numpy array for pandas 3/arrow compatibility)
    X = [str(p) for p in df["prompt"].tolist()]
    y = np.array([1 if str(x).strip().lower() == "complex" else 0 for x in df["label"].tolist()], dtype=int)

    print(f"Class distribution: {sum(y == 0)} Simple (0), {sum(y == 1)} Complex (1)")

    # Construct an NLP Pipeline:
    # 1. TF-IDF with word n-grams (1-2) capturing syntax, technical terms, and intent
    # 2. Logistic Regression with calibrated probability output in [0.0, 1.0]
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1,
            max_features=2500
        )),
        ("clf", LogisticRegression(
            C=1.5,
            class_weight="balanced",
            max_iter=1000,
            solver="liblinear"
        ))
    ])

    # 5-fold cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring="accuracy")
    print(f"\n5-Fold Cross Validation Accuracy: {scores.mean() * 100:.2f}% (std: {scores.std() * 100:.2f}%)")

    # Fit model on the full dataset
    pipeline.fit(X, y)
    y_pred = pipeline.predict(X)
    train_acc = accuracy_score(y, y_pred)
    print(f"Full Dataset Training Accuracy: {train_acc * 100:.2f}%\n")
    print("Detailed Classification Report:")
    print(classification_report(y, y_pred, target_names=["Simple", "Complex"]))

    # Save trained artifact
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(pipeline, MODEL_FILE)
    print(f"Successfully saved ML classifier artifact to:\n  -> {MODEL_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    train_classifier()
