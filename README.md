# ⚡ Hybrid SLM-LLM Router Agent

An intelligent, multi-provider AI middleware system that dynamically routes user prompts between a **Local Small Language Model (SLM)** and **Cloud Large Language Models (LLMs)** based on prompt complexity. Built with **FastAPI**, **Ollama (`qwen2.5:7b`)**, **Groq (`gpt-oss-120b`)**, **Google Gemini**, **CodeCarbon**, and a real-time **Streamlit** visual analytics dashboard.

---

## 🌟 Key Features & Enhancements

### 1. 🔄 Multi-Tier Complexity Classification (Heuristic & Machine Learning)
- **Heuristic Classifier (`backend/classifier.py`):** Fast rule-based scoring (0.0 to 1.0) evaluating token length, mathematical symbols, task-heavy keywords (`explain`, `analyze`, `write code`, `derive`), and multi-step phrasing.
- **ML Classifier (`backend/ml_classifier.py`):** Pretrained/fine-tuned NLP classification pipeline (TF-IDF + Calibrated Logistic Regression) that outputs continuous complexity probabilities in `[0.0, 1.0]`. Learns semantic nuances and avoids keyword over-triggering (e.g., correctly recognizes `"Can you explain why water is wet?"` as simple).
- **Configurable Mode:** Toggle between classifiers dynamically via the `CLASSIFIER_MODE` configuration flag without changing any code.
- **Evaluation Benchmark:** Side-by-side comparative evaluation script (`scripts/evaluate_classifiers.py`) demonstrating 95%+ routing agreement.

### 2. 🛡️ Dual-Layer Resiliency & Failover (Local ➔ Cloud & Groq ➔ Gemini)
- **Local-to-Cloud Fallback:** If the local Ollama SLM server is down, unreachable, or encounters an error, the request is not dropped. The router automatically falls back to the Cloud LLM pipeline, sets `fallback_reason = "local_slm_unavailable"`, and processes the prompt seamlessly.
- **Cloud Provider Failover:** Groq API (`openai/gpt-oss-120b`) acts as primary cloud provider with automatic single-retry failover to Google Gemini (`gemini-2.5-flash`) if rate limits (HTTP 429) or timeouts occur.
- **Provider & Fallback Transparency:** Every request records the exact serving provider (`groq`, `gemini`, or `none`) and any `fallback_reason` to SQLite, badged in real-time on the Streamlit dashboard.

### 3. 🌱 Live Carbon & Energy Tracking (CodeCarbon)
- **Hardware-Measured Local Emissions:** Uses `codecarbon`'s `EmissionsTracker` on local CPU/GPU hardware to record actual energy consumption in **kWh** and emissions in **grams of CO₂** for Ollama requests.
- **Documented Cloud Baseline:** Computes cloud emissions using a documented statistical average of **0.35g CO₂ / 1,000 tokens** and **0.0004 kWh / 1,000 tokens** (sourced from Luccioni et al. 2023 and Patterson et al. 2021).
- **Environmental Analytics:** Streamlit dashboard features a dedicated **Environmental Impact** section contrasting actual hybrid emissions against a simulated 100% cloud baseline.

---

## 🏗️ System Architecture & Workflow

```
                        User Prompt
                             │
                             ▼
              FastAPI Endpoint (/chat)
                             │
             [CLASSIFIER_MODE=heuristic|ml]
              ┌──────────────┴──────────────┐
              ▼                             ▼
     Heuristic Classifier          ML Model Pipeline
    (Syntax / Keyword Rules)       (Calibrated NLP Scorer)
              └──────────────┬──────────────┘
                             │
                  Complexity Score (0.0 - 1.0)
                             │
             ┌───────────────┴───────────────┐
      Score < 0.50                    Score >= 0.50
             │                               │
             ▼                               │
     LOCAL INFERENCE                         │
    Ollama (qwen2.5:7b)                      │
     [Ollama Down / Error?]                  │
      ├────── Yes ───────────────────────────┤
      │      (fallback_reason =              │
      │       "local_slm_unavailable")       │
      ▼                                      ▼
     CodeCarbon Live Hardware         CLOUD INFERENCE
       Energy Tracking              Groq (gpt-oss-120b)
             │                               │
             │                      [Error / Rate-Limit?]
             │                       ├────── Yes ──────┐
             │                       ▼                 ▼
             │                  Groq Success    Failover to Gemini
             │                       │          (gemini-2.5-flash)
             │                       │                 │
             └───────────────┬───────┴─────────────────┘
                             │
                             ▼
                 SQLite Logging (requests_log)
    (latency, cost, CO2, kWh, provider, fallback_reason)
                             │
                             ▼
                Interactive Streamlit Dashboard
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **API Server** | FastAPI, Uvicorn, Pydantic |
| **Local Inference** | Ollama (`qwen2.5:7b`), Requests |
| **Cloud Inference** | Groq API (`openai/gpt-oss-120b`), Google Gemini API (`gemini-2.5-flash`) |
| **Classification** | Scikit-Learn (TF-IDF, Logistic Regression), Regex Heuristics |
| **Sustainability** | CodeCarbon (`EmissionsTracker`) |
| **Database** | SQLite3 (with automatic schema migration) |
| **Frontend** | Streamlit, Altair Visualizations |

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites
- Python 3.9+ installed
- [Ollama](https://ollama.com/) installed and running locally
- [Groq API Key](https://console.groq.com/)
- [Google AI Studio API Key](https://aistudio.google.com/apikey) (for Gemini failover)

### 2. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd router-agent

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure `.env` File
Create a `.env` file in the root project folder:
```env
# Cloud LLM API Keys
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Classifier Configuration: "heuristic" or "ml"
CLASSIFIER_MODE=heuristic
```

### 4. Pull the Local Model in Ollama
In a separate terminal:
```bash
ollama serve
ollama pull qwen2.5:7b
```

### 5. Generate Training Data & Train the ML Classifier (Optional / Demo)
```bash
# Generate 120-prompt synthetic dataset
python scripts/generate_training_data.py

# Train the ML classifier pipeline
python scripts/train_ml_classifier.py

# Run side-by-side comparative evaluation
python scripts/evaluate_classifiers.py
```

### 6. Start the FastAPI Backend
```bash
uvicorn backend.main:app --reload
```
- Interactive Swagger docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/`

### 7. Launch the Streamlit Dashboard
In another terminal:
```bash
streamlit run dashboard/app.py
```
Access the dashboard at `http://localhost:8501`.

### 8. Run Benchmark Prompts
To simulate realistic traffic and populate the database:
```bash
python test_prompts.py
```

---

## 📊 Dashboard Visualizations

1. **Top Metric Cards:**
   - **Total Requests** handled.
   - **Routed Local (SLM)** with green "Zero Cost" indicator.
   - **Routed Cloud (LLM)** with active provider badge (`Groq: X | Gemini: Y (Failover)`).
   - **Total Cost Saved (₹)** calculated dynamically against simulated 100% cloud baseline.
2. **Traffic Routing Donut Chart:** Visual breakdown of local vs. cloud distribution.
3. **Financial Impact Chart:** Side-by-side bar chart of actual incurred cost vs. 100% cloud baseline in Rupees (₹).
4. **Average Speed Chart:** Latency comparison in Seconds (s) between Local SLM and Cloud LLM.
5. **🌱 Environmental Impact Section:**
   - Cumulative CO₂ saved (in grams).
   - Total energy consumed (in kWh).
   - Bar chart contrasting actual emissions against estimated 100% cloud emissions.
6. **Live Traffic Monitor:** Chronological request timeline with hover tooltips detailing prompts, latencies, routes, and serving providers.
7. **Live Request Log:** Searchable table with color-coded routing badges, un-truncated prompts, and complete model responses.

---

## ⚠️ Known Limitations & Assumptions

1. **Cloud Carbon Estimation:**
   - Real hardware energy telemetry is not exposed by commercial cloud API providers (Groq/Gemini).
   - Cloud CO₂ and kWh figures are based on peer-reviewed industry estimates (~0.35g CO₂ and 0.0004 kWh per 1,000 tokens; Luccioni et al. 2023). In the UI and logs, these figures are clearly labeled as **"Estimated"**.
2. **ML Classifier Dataset:**
   - The initial training dataset (`data/training_prompts.csv`) contains 120 balanced synthetic prompts. For production enterprise deployments, the model should be continuously retrained with verified human-in-the-loop production logs.
3. **Threshold Calibration:**
   - The routing threshold is currently set to `0.50`. Domain-specific deployments can calibrate this threshold based on cost tolerance vs. output fidelity requirements.
