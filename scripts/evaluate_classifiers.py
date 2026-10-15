import os
import sys

# Ensure backend package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.classifier import calculate_complexity as heuristic_scorer
from backend.ml_classifier import calculate_complexity_ml as ml_scorer

TEST_PROMPTS = [
    # Prompts from test_prompts.py
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
    "What is the date today?",

    # Additional edge cases & domain challenges
    "Explain pizza.",  # Tricky: 'explain' keyword in heuristic, but simple concept
    "Implement an asynchronous priority queue with lock-free synchronization in Rust.",
    "Who was Albert Einstein?",
    "Can you explain why water is wet?",
    "Derive the black-scholes option pricing formula using Ito's lemma and geometric Brownian motion."
]

COMPLEXITY_THRESHOLD = 0.5

def evaluate():
    print("=" * 105)
    print("           COMPLEXITY CLASSIFIER EVALUATION: HEURISTIC vs. MACHINE LEARNING")
    print("=" * 105)
    header = f"{'#':<3} | {'Prompt Preview':<40} | {'Heuristic':<14} | {'ML Model':<14} | {'Match?':<10}"
    print(header)
    print("-" * 105)

    matches = 0
    total = len(TEST_PROMPTS)

    for idx, prompt in enumerate(TEST_PROMPTS, 1):
        # 1. Heuristic evaluation
        h_score = heuristic_scorer(prompt)
        h_route = "LOCAL" if h_score < COMPLEXITY_THRESHOLD else "CLOUD"

        # 2. ML evaluation
        m_score = ml_scorer(prompt)
        m_route = "LOCAL" if m_score < COMPLEXITY_THRESHOLD else "CLOUD"

        is_match = (h_route == m_route)
        if is_match:
            matches += 1
            match_str = " AGREE"
        else:
            match_str = "*DISAGREE"

        prompt_preview = (prompt[:37] + "...") if len(prompt) > 40 else prompt
        h_display = f"{h_score:.2f} ({h_route})"
        m_display = f"{m_score:.2f} ({m_route})"

        print(f"{idx:<3} | {prompt_preview:<40} | {h_display:<14} | {m_display:<14} | {match_str:<10}")

    agreement_pct = (matches / total) * 100.0

    print("=" * 105)
    print(f"Total Test Prompts Evaluated: {total}")
    print(f"Agreements (Same Routing Decision): {matches}")
    print(f"Disagreements: {total - matches}")
    print(f"Routing Agreement Rate: {agreement_pct:.1f}%")
    print("=" * 105)
    print("Observations:")
    print(" - 'AGREE' means both classifiers chose the same routing tier (Local vs Cloud).")
    print(" - '*DISAGREE' points to prompts where the ML model learned contextual semantics")
    print("   that refine or correct keyword-triggered heuristic over-sensitivities.")
    print("=" * 105)

if __name__ == "__main__":
    evaluate()
