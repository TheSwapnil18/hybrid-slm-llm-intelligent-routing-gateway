# ⚡ Hybrid SLM-LLM Router Agent: Comprehensive Project Report

## 1. Project Overview & Motivation
As the adoption of Artificial Intelligence accelerates across enterprise systems, organizations face significant trade-offs when relying exclusively on Cloud Large Language Models (LLMs) like GPT-4, Llama-3-70B, and Gemini:
1. **Compounding API Costs:** Cloud inference incurs fees per thousand or million tokens, making high-volume usage financially unsustainable.
2. **Variable Network Latency:** Transmitting payloads to remote data centers introduces network overhead and queue latency.
3. **Environmental Carbon Footprint:** Massive cloud GPU clusters consume immense electrical power, directly increasing global CO₂ emissions.

**The Solution:**
This project introduces a production-ready **Hybrid AI Router Agent**—an intelligent middleware system that dynamically intercepts each user prompt, evaluates its intrinsic computational and reasoning complexity, and directs it to the optimal execution environment:
- **Simple, everyday queries** (greetings, factual lookups, trivia, basic summaries) are handled by a private **Local Small Language Model (SLM)** (`qwen2.5:7b` via Ollama) at **₹0 API cost** and with direct hardware energy tracking.
- **Complex, multi-step queries** (algorithms, code synthesis, advanced math, architectural analysis) are routed to high-capacity **Cloud LLMs** (Groq `openai/gpt-oss-120b` with automated single-retry failover to **Google Gemini**).

---

## 2. System Architecture & End-to-End Workflow

The system is architected into modular, loosely coupled components:

```
                        User Prompt
                             │
                             ▼
              FastAPI Endpoint (/chat)
                             │
             [CLASSIFIER_MODE=heuristic|ml]
              ┌──────────────┴──────────────┐
              ▼                             ▼
     Heuristic Classifier          ML Classifier Pipeline
    (Syntax / Keyword Rules)       (Calibrated NLP Scorer)
              └──────────────┬──────────────┘
                             │
                  Complexity Score (0.0 - 1.0)
                             │
             ┌───────────────┴───────────────┐
      Score < 0.50                    Score >= 0.50
             │                               │
             ▼                               ▼
     LOCAL INFERENCE                 CLOUD INFERENCE
    Ollama (qwen2.5:7b)             Groq (gpt-oss-120b)
    Hardware Energy Tracking                 │
     (via CodeCarbon)                [Error / Rate-Limit?]
             │                       ├────── Yes ──────┐
             │                       ▼                 ▼
             │                  Groq Success    Failover to Gemini
             │                       │          (gemini-2.5-flash)
             │                       │                 │
             └───────────────┬───────┴─────────────────┘
                             │
                             ▼
                 SQLite Logging (requests_log)
       (latency, cost, CO2 grams, kWh, cloud_provider)
                             │
                             ▼
                Interactive Streamlit Dashboard
```

1. **Client Submission:** The client transmits a JSON payload `{"prompt": "..."}` to the FastAPI `/chat` endpoint.
2. **Complexity Scoring:** The router queries either the heuristic classifier or the trained ML model based on `CLASSIFIER_MODE`. A continuous complexity score between `0.0` and `1.0` is computed.
3. **Threshold Routing:**
   - If `Score < 0.50`: Routed to Local SLM (`qwen2.5:7b`).
   - If `Score >= 0.50`: Routed to Cloud LLM.
4. **Resilient Cloud Execution:**
   - The primary cloud provider (Groq) is invoked.
   - If Groq encounters rate limiting (HTTP 429), timeouts, or provider downtime, the system automatically fails over to Google Gemini (`gemini-2.5-flash`), logging which provider completed the task.
5. **Telemetry & Carbon Tracking:**
   - For local queries, `CodeCarbon` measures exact CPU/GPU power consumption (kWh) and real hardware CO₂ emissions.
   - For cloud queries, emissions are calculated using a documented standard of 0.35g CO₂ and 0.0004 kWh per 1,000 tokens.
6. **Structured Audit Persistence:** Details are written to an SQLite database with automatic schema migration.
7. **Visual Analytics:** The Streamlit dashboard updates metrics, interactive Altair charts, and audit logs.

---

## 3. Technology Stack

- **Backend Framework:** `FastAPI` (Python asynchronous REST API)
- **Local Inference Engine:** `Ollama` running `qwen2.5:7b` (7-billion parameter open-weights model)
- **Primary Cloud Provider:** `Groq API` routing to `openai/gpt-oss-120b`
- **Failover Cloud Provider:** `Google Gemini API` (`gemini-2.5-flash` / `gemini-1.5-flash`)
- **Carbon Accounting:** `CodeCarbon` library (`EmissionsTracker`)
- **Classification Engine:** `Scikit-Learn` (TF-IDF vectorizer + Logistic Regression) alongside rule-based regex heuristics
- **Persistence Layer:** `SQLite3` with schema self-healing/migration
- **Dashboard & Analytics:** `Streamlit` with `Altair` declarative visualizations

---

## 4. Complexity Classification Deep Dive

### A. Heuristic Classifier (`backend/classifier.py`)
Applies deterministic syntax and lexical pattern matching:
1. **Length-Based Scoring:**
   - Word count > 40: `+0.4`
   - Word count > 15: `+0.2`
2. **Mathematical & Numerical Constraints:**
   - Mathematical operators (`+`, `-`, `*`, `/`, `=`, `%`) or numeric digits: `+0.2`
3. **High-Reasoning Keywords:**
   - Words such as `"explain"`, `"analyze"`, `"write code"`, `"calculate"`, `"compare"`, `"reason"`, `"synthesize"`, `"evaluate"`, `"summarize"`, `"derive"`: `+0.5` (guarantees a cloud route)
4. **Multi-Step Phrasing:**
   - Conjunctions like `"then"` or `"first" ... "second"`: `+0.2`

### B. Machine Learning Classifier (`backend/ml_classifier.py`)
- Trained on a balanced synthetic dataset of 120 curated prompts (`data/training_prompts.csv`) across categories (chat, trivia, basic Q&A, coding, advanced calculus, distributed systems).
- Uses TF-IDF sublinear n-gram feature extraction paired with calibrated Logistic Regression.
- Outputs continuous probabilities `P(complex|prompt) in [0.0, 1.0]`.
- Corrects common keyword false positives (e.g., questions containing the word `"explain"` about trivial everyday topics are correctly routed locally).
- **Agreement Benchmark:** Evaluated against 20 benchmark prompts, achieving a **95.0% routing agreement** with the baseline heuristic while improving contextual edge-case decisions.

---

## 5. Automatic Failover Mechanism (Groq ➔ Gemini)

High-availability design requires fault tolerance against third-party API disruptions:
- **Invocation Sequence:**
  1. Primary attempt: `_call_groq(prompt)` with 120B parameter model.
  2. Exception interception: Catches network errors, API timeouts, and 429 rate limits.
  3. Failover attempt: Automatically calls `_call_gemini(prompt)` with `gemini-2.5-flash`.
  4. Complete failure handling: If both providers fail, returns a structured HTTP 500/503 response without crashing the application.
- **Provider Auditing:** The database stores `cloud_provider = 'groq'` or `'gemini'`, allowing the dashboard to display an active failover badge whenever secondary routing occurs.

---

## 6. Environmental & Sustainability Metrics (CodeCarbon)

Traditional AI systems ignore environmental impact. This project implements dual-mode carbon accounting:
1. **Local Tracking:**
   `CodeCarbon` initializes in-memory process tracking during Ollama execution:
   $$\text{CO}_2\text{ (grams)} = \text{Emissions (kg)} \times 1000$$
   $$\text{Energy (kWh)} = \text{Hardware Energy Consumed}$$
2. **Cloud Estimation:**
   Since cloud data centers do not expose live board-level telemetry, emissions are estimated based on peer-reviewed literature (Luccioni et al. 2023, Patterson et al. 2021):
   $$\text{CO}_2\text{ (grams)} = \left(\frac{\text{Total Tokens}}{1000}\right) \times 0.35\text{ g}$$
   $$\text{Energy (kWh)} = \left(\frac{\text{Total Tokens}}{1000}\right) \times 0.0004\text{ kWh}$$
3. **Cumulative Savings:**
   The dashboard compares total emissions against a counterfactual baseline where 100% of queries were sent to cloud data centers:
   $$\text{CO}_2\text{ Saved} = \text{Emissions}_{\text{Simulated 100\% Cloud}} - \text{Emissions}_{\text{Actual Hybrid}}$$

---

## 7. Presentation Layer & Visual Analytics

The Streamlit dashboard (`dashboard/app.py`) provides:
1. **Executive Metric Cards:** Styled with custom CSS shadows, showing Total Queries, Local Requests (Zero Cost), Cloud Requests with Failover Breakdown, and Cumulative Financial Savings in Rupees (₹).
2. **Donut Routing Chart:** Altair chart depicting the traffic division between Local SLM and Cloud LLM.
3. **Financial Impact Chart:** Side-by-side comparison of Actual Cost vs. 100% Cloud baseline in Rupees (₹).
4. **Latency Comparison Chart:** Speed comparison in seconds between local and cloud inference.
5. **Environmental Impact Section:** Displays total CO₂ saved, total energy consumed (kWh), and emission comparison bar charts.
6. **Live Traffic Timeline:** Chronological bar monitor displaying latency and routing color-coding per request ID with hover tooltips.
7. **Live Request Table:** Formatted data grid with bold color-coded badges, un-truncated prompts, provider tags, and complete model responses.

---

## 8. Verification & Demonstration Results

- **Database Migration:** Verified smooth schema migration adding `cloud_provider`, `co2_grams`, and `energy_kwh` with zero data loss.
- **ML Classifier Training:** Achieved **89.17% 5-fold cross-validation accuracy** and **100% training accuracy** on the 120-prompt dataset.
- **Comparative Agreement:** Verified **95.0% routing alignment** between heuristic and ML classifiers across benchmark prompts.
- **Failover Reliability:** Tested provider dispatching and error handling pipelines.
