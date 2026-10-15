import os
import logging
import joblib

# Fallback heuristic classifier
from .classifier import calculate_complexity as calculate_complexity_heuristic

logger = logging.getLogger("ml_classifier")

MODEL_PATH = os.path.join(os.path.dirname(__file__), "saved_models", "classifier_model.joblib")

# Cache model in memory
_CACHED_MODEL = None

def get_ml_model():
    """Loads and caches the trained ML classifier pipeline."""
    global _CACHED_MODEL
    if _CACHED_MODEL is not None:
        return _CACHED_MODEL

    if os.path.exists(MODEL_PATH):
        try:
            _CACHED_MODEL = joblib.load(MODEL_PATH)
            logger.info(f"Loaded ML complexity classifier from {MODEL_PATH}")
            return _CACHED_MODEL
        except Exception as e:
            logger.warning(f"Failed to load ML model artifact from {MODEL_PATH}: {e}")
            return None
    return None

def calculate_complexity_ml(prompt: str) -> float:
    """
    Predicts complexity score in [0.0, 1.0] using the trained ML model.
    Falls back to heuristic classifier if the ML artifact is not found.
    """
    if not prompt or not prompt.strip():
        return 0.0

    model = get_ml_model()
    if model is None:
        logger.warning("ML model artifact not found. Falling back to heuristic classifier.")
        return calculate_complexity_heuristic(prompt)

    try:
        # Predict probability of class 1 ('complex')
        probabilities = model.predict_proba([prompt])[0]
        # Class 1 is complex
        score = float(probabilities[1])
        return round(score, 4)
    except Exception as e:
        logger.warning(f"ML inference error: {e}. Falling back to heuristic.")
        return calculate_complexity_heuristic(prompt)
