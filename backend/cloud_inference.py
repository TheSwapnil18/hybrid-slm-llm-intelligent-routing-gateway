import os
import time
import logging
from openai import OpenAI

# Set up logging for provider tracking and failover notices
logger = logging.getLogger("cloud_inference")

# ============================================================================
# CLOUD CARBON FOOTPRINT ESTIMATION CONSTANTS
# ============================================================================
# Note: For cloud providers (Groq, Gemini), live server hardware telemetry is
# inaccessible. Therefore, we use documented industry-average estimates:
# - CO2: ~0.35 grams per 1,000 tokens (Source: Luccioni et al. 2023, Patterson et al. 2021)
# - Energy: ~0.0004 kWh per 1,000 tokens
# This is clearly documented and labeled as an "estimate" across the system.
# ============================================================================
CLOUD_CO2_GRAMS_PER_1K_TOKENS = 0.35
CLOUD_KWH_PER_1K_TOKENS = 0.0004

def _estimate_cloud_emissions(total_tokens: int):
    """Calculates estimated CO2 grams and kWh for cloud API calls based on token count."""
    tokens = max(1, total_tokens)
    co2_grams = (tokens / 1000.0) * CLOUD_CO2_GRAMS_PER_1K_TOKENS
    energy_kwh = (tokens / 1000.0) * CLOUD_KWH_PER_1K_TOKENS
    return co2_grams, energy_kwh

def _call_groq(prompt: str):
    """Executes prompt via Groq API (openai/gpt-oss-120b)."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    model_name = "openai/gpt-oss-120b"

    start_time = time.time()
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    latency_ms = (time.time() - start_time) * 1000
    response_text = completion.choices[0].message.content

    # Token counting & cost calculation
    # OpenRouter/Groq market baseline: $0.03 / 1M input + $0.17 / 1M output tokens
    prompt_tokens = completion.usage.prompt_tokens if completion.usage else max(1, len(prompt) // 4)
    completion_tokens = completion.usage.completion_tokens if completion.usage else max(1, len(response_text) // 4)
    estimated_cost = (prompt_tokens * 0.03 / 1_000_000) + (completion_tokens * 0.17 / 1_000_000)

    total_tokens = prompt_tokens + completion_tokens
    co2_grams, energy_kwh = _estimate_cloud_emissions(total_tokens)

    return {
        "response": response_text,
        "latency_ms": latency_ms,
        "cost_usd": estimated_cost,
        "provider": "groq",
        "co2_grams": co2_grams,
        "energy_kwh": energy_kwh
    }

def _call_gemini(prompt: str):
    """Executes prompt via Google Gemini API as an automatic failover provider."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    start_time = time.time()

    # Attempt to use the modern google.genai SDK first, fall back to google.generativeai if needed
    response_text = ""
    prompt_tokens = 0
    completion_tokens = 0

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        # Using gemini-2.5-flash as the primary fast cloud model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        response_text = response.text or ""
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", 0) or 0
            completion_tokens = getattr(response.usage_metadata, "candidates_token_count", 0) or 0
    except ImportError:
        import google.generativeai as genai_legacy
        genai_legacy.configure(api_key=api_key)
        model = genai_legacy.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        response_text = response.text or ""
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", 0) or 0
            completion_tokens = getattr(response.usage_metadata, "candidates_token_count", 0) or 0

    latency_ms = (time.time() - start_time) * 1000

    # Fallback token estimation if usage metadata was not returned (~4 chars/token)
    if prompt_tokens == 0:
        prompt_tokens = max(1, len(prompt) // 4)
    if completion_tokens == 0:
        completion_tokens = max(1, len(response_text) // 4)

    # Gemini 2.5/1.5 Flash pricing: $0.075 / 1M input + $0.30 / 1M output tokens
    estimated_cost = (prompt_tokens * 0.075 / 1_000_000) + (completion_tokens * 0.30 / 1_000_000)

    total_tokens = prompt_tokens + completion_tokens
    co2_grams, energy_kwh = _estimate_cloud_emissions(total_tokens)

    return {
        "response": response_text,
        "latency_ms": latency_ms,
        "cost_usd": estimated_cost,
        "provider": "gemini",
        "co2_grams": co2_grams,
        "energy_kwh": energy_kwh
    }

def generate_cloud(prompt: str):
    """
    Main cloud inference dispatcher with automatic single-retry failover:
    1. Try Groq (Primary Cloud Provider)
    2. If Groq fails (rate-limit, timeout, network error), automatically failover to Gemini
    3. If both fail, raise a descriptive exception
    """
    groq_error = None
    try:
        return _call_groq(prompt)
    except Exception as e:
        groq_error = e
        logger.warning(f"Groq API call failed: {e}. Initiating automatic failover to Gemini...")

    # Automatic Failover to Gemini (one retry attempt)
    try:
        return _call_gemini(prompt)
    except Exception as gemini_error:
        raise RuntimeError(
            f"All cloud providers failed. "
            f"Groq error: {groq_error} | Gemini failover error: {gemini_error}"
        )
