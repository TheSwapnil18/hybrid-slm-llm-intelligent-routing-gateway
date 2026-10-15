import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from .classifier import calculate_complexity as calculate_complexity_heuristic
from .ml_classifier import calculate_complexity_ml
from .local_inference import generate_local
from .cloud_inference import generate_cloud
from .database import init_db, log_request

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

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    prompt = request.prompt
    if not prompt or not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    # Determine classifier based on CLASSIFIER_MODE config flag
    classifier_mode = os.environ.get("CLASSIFIER_MODE", "heuristic").lower()
    if classifier_mode == "ml":
        score = calculate_complexity_ml(prompt)
    else:
        score = calculate_complexity_heuristic(prompt)

    # Routing Decision
    route = "local" if score < COMPLEXITY_THRESHOLD else "cloud"

    try:
        if route == "local":
            result = generate_local(prompt)
            provider = "none"
        else:
            result = generate_cloud(prompt)
            provider = result.get("provider", "groq")

        co2_grams = result.get("co2_grams", 0.0)
        energy_kwh = result.get("energy_kwh", 0.0)

        # Log complete record into SQLite
        log_request(
            prompt=prompt,
            route_taken=route,
            complexity_score=score,
            latency_ms=result["latency_ms"],
            estimated_cost_usd=result["cost_usd"],
            response_preview=result["response"],
            cloud_provider=provider,
            co2_grams=co2_grams,
            energy_kwh=energy_kwh
        )

        return ChatResponse(
            response=result["response"],
            route=route,
            complexity_score=score,
            latency_ms=result["latency_ms"],
            cloud_provider=provider,
            co2_grams=co2_grams,
            energy_kwh=energy_kwh,
            classifier_mode=classifier_mode
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
