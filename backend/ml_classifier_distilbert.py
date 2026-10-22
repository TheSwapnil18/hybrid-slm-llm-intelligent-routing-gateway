import os
import logging

# Fallback to existing TF-IDF ML classifier
from .ml_classifier import calculate_complexity_ml

logger = logging.getLogger("distilbert_classifier")

# Check primary location backend/saved_models/distilbert_classifier
# and secondary root location saved_models/distilbert_classifier
PRIMARY_MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models", "distilbert_classifier")
SECONDARY_MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "saved_models", "distilbert_classifier"))

_CACHED_TOKENIZER = None
_CACHED_MODEL = None
_LOAD_ATTEMPTED = False

def _find_model_directory() -> str | None:
    """Finds valid directory containing the fine-tuned DistilBERT artifacts."""
    for path in [PRIMARY_MODEL_DIR, SECONDARY_MODEL_DIR]:
        if os.path.isdir(path):
            config_file = os.path.join(path, "config.json")
            if os.path.exists(config_file):
                return path
    return None

def get_distilbert_model_and_tokenizer():
    """Loads and caches the fine-tuned DistilBERT model and tokenizer."""
    global _CACHED_TOKENIZER, _CACHED_MODEL, _LOAD_ATTEMPTED
    if _CACHED_MODEL is not None and _CACHED_TOKENIZER is not None:
        return _CACHED_MODEL, _CACHED_TOKENIZER

    if _LOAD_ATTEMPTED and (_CACHED_MODEL is None or _CACHED_TOKENIZER is None):
        return None, None

    _LOAD_ATTEMPTED = True
    model_dir = _find_model_directory()
    if not model_dir:
        logger.info(
            f"DistilBERT model files not found at '{PRIMARY_MODEL_DIR}'. "
            f"Will fall back to existing TF-IDF classifier."
        )
        return None, None

    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification

        logger.info(f"Loading fine-tuned DistilBERT model from {model_dir}...")
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        model.eval()

        _CACHED_TOKENIZER = tokenizer
        _CACHED_MODEL = model
        logger.info("Successfully loaded fine-tuned DistilBERT classifier.")
        return _CACHED_MODEL, _CACHED_TOKENIZER
    except Exception as e:
        logger.warning(f"Error loading DistilBERT model from {model_dir}: {e}. Falling back to TF-IDF.")
        return None, None

def calculate_complexity_distilbert(prompt: str) -> float:
    """
    Predicts complexity score in [0.0, 1.0] using the fine-tuned DistilBERT model.
    Label mapping: 0 = simple, 1 = complex.
    Returns the predicted probability of the 'complex' class.
    Falls back gracefully to the existing TF-IDF classifier if model files are not found.
    """
    if not prompt or not prompt.strip():
        return 0.0

    model, tokenizer = get_distilbert_model_and_tokenizer()
    if model is None or tokenizer is None:
        # Graceful fallback to existing TF-IDF classifier
        return calculate_complexity_ml(prompt)

    try:
        import torch

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=-1)
            # Class 1 is 'complex'
            complex_prob = float(probabilities[0][1].item())
            return round(complex_prob, 4)
    except Exception as e:
        logger.warning(f"DistilBERT inference error: {e}. Falling back to TF-IDF classifier.")
        return calculate_complexity_ml(prompt)

def is_distilbert_loaded() -> bool:
    """Returns True if the fine-tuned DistilBERT model is loaded or loadable."""
    global _CACHED_MODEL, _CACHED_TOKENIZER
    if _CACHED_MODEL is not None and _CACHED_TOKENIZER is not None:
        return True
    return _find_model_directory() is not None
