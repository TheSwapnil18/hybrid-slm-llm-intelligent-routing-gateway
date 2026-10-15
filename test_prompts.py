import requests

API_URL = "http://127.0.0.1:8000/chat"

prompts = [
    "Hello! How are you?",
    "What is 2 + 2?",
    "Write a quick summary of what an API is.",
    "Explain why the sky is blue using principles of Rayleigh scattering and compare it to Mie scattering in the atmosphere.",
    "What's the capital of France?",
    "Write code in Python to implement a binary search tree with insert, delete, and find methods. Then analyze its time complexity.",
    "Give me a recipe for chocolate cake.",
    "Calculate the derivative of f(x) = 3x^2 + 2x - 5 and explain the steps.",
    "Who won the world cup in 2022?",
    "First, summarize the plot of Inception. Then, compare its narrative structure to The Matrix.",
    "Is a tomato a fruit or a vegetable?",
    "Write code for a neural network from scratch using numpy.",
    "Tell me a short joke.",
    "Analyze the geopolitical implications of renewable energy adoption in developing nations over the next decade.",
    "What is the date today?"
]

print("=" * 60)
print("  Starting tests for Hybrid SLM-LLM Router Agent")
print("=" * 60)

for idx, prompt in enumerate(prompts, 1):
    print(f"[{idx:02d}/{len(prompts):02d}] Prompt: {prompt[:50]}...")
    
    try:
        response = requests.post(API_URL, json={"prompt": prompt})
        response.raise_for_status()
        data = response.json()
        
        route = data.get("route", "").upper()
        provider = data.get("cloud_provider", "none")
        provider_label = "Local (Ollama)" if route == "LOCAL" else f"Cloud ({provider.title()})"
        co2 = data.get("co2_grams", 0.0)
        mode = data.get("classifier_mode", "heuristic")

        print(f"  Route:            {route} [{provider_label}]")
        print(f"  Complexity Score: {data['complexity_score']:.2f} (Mode: {mode})")
        print(f"  Latency:          {data['latency_ms']:.0f} ms ({data['latency_ms']/1000.0:.2f} s)")
        print(f"  Est. CO2:         {co2:.4f} grams")
        print("-" * 60)
        
    except requests.exceptions.RequestException as e:
        print(f"  Error: {e}")
        try:
            print(f"  Details: {response.json()}")
        except Exception:
            pass
        print("-" * 60)
