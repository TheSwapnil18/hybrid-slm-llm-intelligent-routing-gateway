import requests
import time
import logging

logger = logging.getLogger("local_inference")

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"

def generate_local(prompt: str):
    """
    Executes prompt locally via Ollama with live CodeCarbon emissions tracking.
    Measures actual local CPU/GPU hardware energy consumption (kWh) and CO2 emissions (g).
    """
    tracker = None
    try:
        from codecarbon import EmissionsTracker
        # Run CodeCarbon in memory without polluting disk with CSV files
        tracker = EmissionsTracker(save_to_file=False, log_level="error")
        tracker.start()
    except Exception as e:
        logger.debug(f"CodeCarbon initialization notice: {e}")
        tracker = None

    start_time = time.time()
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        latency_ms = (time.time() - start_time) * 1000

        # Calculate actual emissions and energy consumption from CodeCarbon
        co2_grams = 0.0
        energy_kwh = 0.0
        if tracker is not None:
            try:
                emissions_kg = tracker.stop()
                if emissions_kg is not None and emissions_kg > 0:
                    co2_grams = float(emissions_kg) * 1000.0  # kg -> grams
                
                final_data = getattr(tracker, "final_emissions_data", None)
                if final_data and getattr(final_data, "energy_consumed", None) is not None:
                    energy_kwh = float(final_data.energy_consumed)
            except Exception as e:
                logger.debug(f"CodeCarbon tracking stop notice: {e}")

        return {
            "response": result.get("response", ""),
            "latency_ms": latency_ms,
            "cost_usd": 0.0,  # Local SLM inference has zero API cost
            "co2_grams": co2_grams,
            "energy_kwh": energy_kwh,
            "model_name": MODEL_NAME
        }
    except requests.exceptions.RequestException as e:
        if tracker is not None:
            try:
                tracker.stop()
            except Exception:
                pass
        raise Exception(f"Local SLM error (is Ollama running with {MODEL_NAME}?): {str(e)}")
