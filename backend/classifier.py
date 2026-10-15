import re

def calculate_complexity(prompt: str) -> float:
    score = 0.0
    
    # 1. Length-based scoring
    words = prompt.split()
    if len(words) > 40:
        score += 0.4
    elif len(words) > 15:
        score += 0.2
        
    # 2. Presence of math/numbers (often needs reasoning)
    if re.search(r'[\+\-\*\/\=\%]', prompt) or any(char.isdigit() for char in prompt):
        score += 0.2
        
    # 3. Keywords indicating complex reasoning or specific tasks
    complex_keywords = [
        "explain", "analyze", "write code", "calculate", "compare", 
        "reason", "synthesize", "evaluate", "summarize", "derive"
    ]
    
    prompt_lower = prompt.lower()
    for kw in complex_keywords:
        if kw in prompt_lower:
            score += 0.5
            break # Apply once
            
    # 4. Multi-step phrasing
    if "then" in prompt_lower or ("first" in prompt_lower and "second" in prompt_lower):
        score += 0.2
        
    # Cap score at 1.0
    return min(score, 1.0)
