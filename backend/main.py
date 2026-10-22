import os
import time
import socket
import logging
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from .classifier import calculate_complexity as calculate_complexity_heuristic
from .ml_classifier import calculate_complexity_ml
from .ml_classifier_distilbert import calculate_complexity_distilbert, is_distilbert_loaded
from .local_inference import generate_local
from .cloud_inference import generate_cloud
from .database import init_db, log_request

logger = logging.getLogger("router_main")

load_dotenv()  # Load variables from .env if present
init_db()      # Initialize and automatically migrate database schema

app = FastAPI(title="Hybrid SLM-LLM Router Agent")

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str
    route: str
    complexity_score: float
    latency_ms: float
    cloud_provider: str = "none"
    co2_grams: float = 0.0
    energy_kwh: float = 0.0
    classifier_mode: str = "heuristic"
    fallback_reason: str | None = None
    classifier_confidence: float
    classify_ms: float
    inference_ms: float
    model_name: str
    threshold: float = 0.5

COMPLEXITY_THRESHOLD = 0.5

@app.get("/")
def health_check():
    classifier_mode = os.environ.get("CLASSIFIER_MODE", "heuristic").lower()
    return {
        "status": "online",
        "service": "Hybrid SLM-LLM Router Agent",
        "classifier_mode": classifier_mode,
        "complexity_threshold": COMPLEXITY_THRESHOLD
    }

@app.get("/health")
def detailed_health():
    classifier_mode = os.environ.get("CLASSIFIER_MODE", "heuristic").lower()

    # Check Ollama status with rapid 0.25s socket ping to avoid timeouts when Ollama is stopped
    ollama_up = False
    try:
        with socket.create_connection(("127.0.0.1", 11434), timeout=0.25):
            ollama_up = True
    except Exception:
        ollama_up = False

    groq_key_configured = bool(os.environ.get("GROQ_API_KEY", "").strip())
    gemini_key_configured = bool(os.environ.get("GEMINI_API_KEY", "").strip())

    try:
        distilbert_loaded = is_distilbert_loaded()
    except Exception:
        distilbert_loaded = False

    return {
        "status": "online",
        "ollama_up": ollama_up,
        "groq_key_configured": groq_key_configured,
        "gemini_key_configured": gemini_key_configured,
        "classifier_mode": classifier_mode,
        "distilbert_loaded": distilbert_loaded,
        "threshold": COMPLEXITY_THRESHOLD
    }

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    prompt = request.prompt
    if not prompt or not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    t_total_start = time.time()

    # 1. Measure classification time
    t_class_start = time.time()
    classifier_mode = os.environ.get("CLASSIFIER_MODE", "heuristic").lower()
    if classifier_mode == "distilbert":
        score = calculate_complexity_distilbert(prompt)
    elif classifier_mode == "ml":
        score = calculate_complexity_ml(prompt)
    else:
        score = calculate_complexity_heuristic(prompt)
    classify_ms = round((time.time() - t_class_start) * 1000.0, 2)

    # 2. Compute classifier confidence
    if classifier_mode in ["distilbert", "ml"]:
        # p is the probability of complex class
        confidence = max(score, 1.0 - score)
    else:
        # Documented proxy for heuristic mode: abs(score - 0.5) * 2
        confidence = abs(score - 0.5) * 2
    classifier_confidence = round(float(confidence), 4)

    # 3. Routing Decision
    route = "local" if score < COMPLEXITY_THRESHOLD else "cloud"
    fallback_reason = None

    try:
        t_inf_start = time.time()
        if route == "local":
            try:
                result = generate_local(prompt)
                provider = "none"
                model_name = result.get("model_name", "qwen2.5:7b")
            except Exception as local_err:
                logger.warning(
                    f"Local SLM unavailable or failed ({local_err}). "
                    f"Executing resilient fallback to Cloud LLM pipeline..."
                )
                fallback_reason = "local_slm_unavailable"
                route = "cloud"
                result = generate_cloud(prompt)
                provider = result.get("provider", "groq")
                model_name = result.get("model_name", "openai/gpt-oss-120b" if provider == "groq" else "gemini-3.8-flash")
        else:
            try:
                result = generate_cloud(prompt)
                provider = result.get("provider", "groq")
                model_name = result.get("model_name", "openai/gpt-oss-120b" if provider == "groq" else "gemini-3.8-flash")
            except Exception as cloud_err:
                logger.warning(
                    f"All cloud providers failed ({cloud_err}). "
                    f"Executing resilient fallback to Local SLM (Ollama)..."
                )
                fallback_reason = "cloud_llm_unavailable"
                route = "local"
                result = generate_local(prompt)
                provider = "none"
                model_name = result.get("model_name", "qwen2.5:7b")

        inference_ms = round((time.time() - t_inf_start) * 1000.0, 2)
        total_latency_ms = round((time.time() - t_total_start) * 1000.0, 2)

        co2_grams = result.get("co2_grams", 0.0)
        energy_kwh = result.get("energy_kwh", 0.0)

        # Log complete record into SQLite
        log_request(
            prompt=prompt,
            route_taken=route,
            complexity_score=score,
            latency_ms=total_latency_ms,
            estimated_cost_usd=result["cost_usd"],
            response_preview=result["response"],
            cloud_provider=provider,
            co2_grams=co2_grams,
            energy_kwh=energy_kwh,
            fallback_reason=fallback_reason,
            classifier_confidence=classifier_confidence,
            classify_ms=classify_ms,
            inference_ms=inference_ms,
            model_name=model_name
        )

        return ChatResponse(
            response=result["response"],
            route=route,
            complexity_score=score,
            latency_ms=total_latency_ms,
            cloud_provider=provider,
            co2_grams=co2_grams,
            energy_kwh=energy_kwh,
            classifier_mode=classifier_mode,
            fallback_reason=fallback_reason,
            classifier_confidence=classifier_confidence,
            classify_ms=classify_ms,
            inference_ms=inference_ms,
            model_name=model_name,
            threshold=COMPLEXITY_THRESHOLD
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
