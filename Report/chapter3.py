# chapter3.py - Chapter 3: System Development (Exhaustive Technical Specification & Modeling)
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter3(doc, add_p, add_h1, add_h2, add_h3, add_h4, add_image_centered, format_simple_table):
    add_h1("CHAPTER 3: SYSTEM DEVELOPMENT")

    intro_sys = (
        "This chapter presents the comprehensive architectural specification, engineering implementation, and software "
        "modeling for the Hybrid SLM-LLM Router Gateway. It details the hardware and software specifications, functional and "
        "non-functional requirements, formal system modeling via Data Flow Diagrams (DFDs) and Unified Modeling Language (UML) "
        "diagrams, deep-dive formulations of the three complexity classifiers, inference execution pipelines with automated failover, "
        "real-time hardware energy telemetry, user interface screenshots, and relational database schema auto-migrations."
    )
    add_p(intro_sys)

    # ---------------------------------------------------------
    # 3.1 REQUIREMENT SPECIFICATION
    # ---------------------------------------------------------
    add_h2("3.1 Requirement Specification")

    # 3.1.1 Hardware Requirements
    add_h3("3.1.1 Hardware Requirements")
    p_hw = (
        "The project is engineered to demonstrate that high-performance local AI inference and real-time complexity routing "
        "do not require multi-GPU server infrastructure, but can execute effectively on standard modern consumer workstation "
        "hardware. Table 3.1 defines the development testbed specifications used for local SLM execution, transformer fine-tuning, "
        "and runtime gateway hosting."
    )
    add_p(p_hw)

    hw_specs = [
        ("Host Processor (CPU)", "Intel Core i5 / i7 (11th Gen or higher) / AMD Ryzen 5 / 7 (6+ physical cores, 2.4 GHz base clock)", "Executes FastAPI async event loops, PyTorch DistilBERT tensor inference, and OS background threads"),
        ("System Memory (RAM)", "16.0 GB DDR4 / DDR5 (minimum 8 GB required for 4-bit 7B quantized execution)", "Houses Qwen2.5-7B GGUF weights in memory (~4.7 GB allocation) alongside OS and Python runtimes"),
        ("Storage Subsystem", "512 GB PCIe NVMe Solid State Drive (SSD)", "High-speed loading of model binaries, transformer tokenizers, and persistent SQLite database I/O"),
        ("Graphics (GPU)", "Integrated Intel Iris Xe / NVIDIA GeForce RTX Dedicated (Optional)", "Accelerates local Ollama GGUF matrix-vector multiplications when GPU offloading is available"),
        ("Hardware Power Sensors", "Intel Running Average Power Limit (RAPL) / On-board ACPI Battery Interface", "Enables CodeCarbon in-memory profiler to sample live processor electrical draw (Watts)"),
        ("Network Connectivity", "Broadband Internet (10+ Mbps low-latency connection)", "Facilitates high-speed RESTful JSON transmissions to cloud Groq LPU and Google Gemini APIs")
    ]
    add_p("Table 3.1: Hardware Development & Deployment Testbed Specifications", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=10, space_after=4)
    tbl_hw = doc.add_table(rows=len(hw_specs) + 1, cols=3)
    tbl_hw.rows[0].cells[0].paragraphs[0].text = "Hardware Component"
    tbl_hw.rows[0].cells[1].paragraphs[0].text = "Specification / Testbed Configuration"
    tbl_hw.rows[0].cells[2].paragraphs[0].text = "Operational Role in Project"
    for r_i, (comp, spec, role) in enumerate(hw_specs, start=1):
        tbl_hw.rows[r_i].cells[0].paragraphs[0].text = comp
        tbl_hw.rows[r_i].cells[0].paragraphs[0].runs[0].bold = True
        tbl_hw.rows[r_i].cells[1].paragraphs[0].text = spec
        tbl_hw.rows[r_i].cells[2].paragraphs[0].text = role
    format_simple_table(tbl_hw, col_widths=[1.5, 2.5, 2.2])

    # 3.1.2 Software Requirements
    add_h3("3.1.2 Software Requirements & Technology Stack")
    p_sw = (
        "The software architecture relies on modern, production-tested open-source libraries, frameworks, and APIs. "
        "Table 3.2 details the technology stack, software versions, and responsibilities."
    )
    add_p(p_sw)

    sw_specs = [
        ("Operating System", "Microsoft Windows 11 Home / Pro (64-bit)", "Host environment running FastAPI, Ollama daemon, and Chrome headless CDP"),
        ("Python Environment", "Python 3.10+ in isolated virtual environment (venv)", "Universal runtime across backend, ML pipelines, and Streamlit visualization"),
        ("API Gateway Framework", "FastAPI (v0.115+) & Uvicorn ASGI Server", "High-throughput asynchronous REST gateway, JSON schema validation, latency timers"),
        ("Data Validation", "Pydantic (v2.10+)", "Strict data contract enforcement via ChatRequest and ChatResponse schemas"),
        ("Local Inference Daemon", "Ollama (v0.34.2+) serving qwen2.5:7b", "Executes 4-bit quantized 7-billion parameter language model via local REST API"),
        ("Primary Cloud Provider", "Groq Cloud API (openai/gpt-oss-120b)", "High-throughput LPU cloud inference at $0.03 input / $0.17 output per 1M tokens"),
        ("Failover Cloud Provider", "Google Gemini API (gemini-2.5-flash)", "Automated secondary cloud failover executing via official google-genai SDK"),
        ("Transformer Classifier", "Hugging Face Transformers & PyTorch (DistilBERT)", "Fine-tuned 6-layer sequence classifier (66M params) predicting complexity in <25ms"),
        ("Classical ML Classifier", "Scikit-Learn (TF-IDF Vectorizer + Logistic Regression)", "Alternative ML pipeline extracting sublinear n-grams serialized via joblib"),
        ("Carbon Telemetry", "CodeCarbon (v3.0+) EmissionsTracker", "In-memory hardware power (kWh) and regional CO2 emissions tracking"),
        ("Relational Persistence", "SQLite3 (Python Standard Library)", "16-column structured audit log (requests_log) with schema self-healing/migrations"),
        ("Observability Portal", "Streamlit (v1.42+) & Altair Statistical Charting", "Interactive testing console, KPI cards, financial bars, and live audit data grids")
    ]
    add_p("Table 3.2: Software Technology Stack, Frameworks & Dependency Specifications", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=10, space_after=4)
    tbl_sw = doc.add_table(rows=len(sw_specs) + 1, cols=3)
    tbl_sw.rows[0].cells[0].paragraphs[0].text = "Software / Library"
    tbl_sw.rows[0].cells[1].paragraphs[0].text = "Version / Framework"
    tbl_sw.rows[0].cells[2].paragraphs[0].text = "Functional Responsibility"
    for r_i, (lib, ver, resp) in enumerate(sw_specs, start=1):
        tbl_sw.rows[r_i].cells[0].paragraphs[0].text = lib
        tbl_sw.rows[r_i].cells[0].paragraphs[0].runs[0].bold = True
        tbl_sw.rows[r_i].cells[1].paragraphs[0].text = ver
        tbl_sw.rows[r_i].cells[2].paragraphs[0].text = resp
    format_simple_table(tbl_sw, col_widths=[1.5, 2.0, 2.7])

    # 3.1.3 Functional Requirements
    add_h3("3.1.3 Functional Requirements Specification")
    p_fr = (
        "The system's functional capabilities are organized into ten formal requirements (FR1 to FR10) summarized in Table 3.3."
    )
    add_p(p_fr)

    fr_data = [
        ("FR1", "Prompt Ingestion & Schema Validation", "The gateway shall expose an asynchronous HTTP POST endpoint /chat accepting JSON payloads with non-empty 'prompt' strings, validated via Pydantic."),
        ("FR2", "Classifier Mode Dispatching", "The system shall read the CLASSIFIER_MODE configuration variable ('heuristic', 'ml', or 'distilbert') and dynamically invoke the corresponding model without restart."),
        ("FR3", "Continuous Complexity Scoring", "The active classifier shall evaluate the semantic and structural difficulty of the prompt and return a continuous probability score p in the range [0.0, 1.0]."),
        ("FR4", "Confidence Interval Calculation", "The classification module shall calculate model decision confidence as max(p, 1-p), reflecting certainty in the selected binary category."),
        ("FR5", "Threshold Gating Decision", "The router shall compare score p against COMPLEXITY_THRESHOLD = 0.50, routing to 'local' if p < 0.50 and 'cloud' if p >= 0.50."),
        ("FR6", "Local SLM Inference Execution", "For 'local' routes, the gateway shall call the Ollama REST API with qwen2.5:7b, receiving generated text at zero token API cost."),
        ("FR7", "Multi-Provider Cloud Dispatch", "For 'cloud' routes, the gateway shall dispatch prompts to primary provider Groq (gpt-oss-120b) and capture token usage and completions."),
        ("FR8", "Automated Two-Tier Failover", "The system shall intercept Ollama timeouts and redirect to cloud (fallback_reason='local_slm_unavailable'), and intercept Groq rate limits to redirect to Gemini."),
        ("FR9", "Hardware & Carbon Telemetry", "The system shall measure local CPU energy draw (kWh) and grams of CO2 via CodeCarbon, and compute cloud emissions using 0.35g CO2 / 1k tokens."),
        ("FR10", "Relational Audit Persistence", "Every request transaction shall be atomically written to SQLite table requests_log capturing 16 schema attributes with auto-migration.")
    ]
    add_p("Table 3.3: System Functional Requirements Specification (FR1 to FR10)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=10, space_after=4)
    tbl_fr = doc.add_table(rows=len(fr_data) + 1, cols=3)
    tbl_fr.rows[0].cells[0].paragraphs[0].text = "Req ID"
    tbl_fr.rows[0].cells[1].paragraphs[0].text = "Functional Requirement Name"
    tbl_fr.rows[0].cells[2].paragraphs[0].text = "Detailed Requirement Specification"
    for r_i, (fid, fname, fdesc) in enumerate(fr_data, start=1):
        tbl_fr.rows[r_i].cells[0].paragraphs[0].text = fid
        tbl_fr.rows[r_i].cells[0].paragraphs[0].runs[0].bold = True
        tbl_fr.rows[r_i].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tbl_fr.rows[r_i].cells[1].paragraphs[0].text = fname
        tbl_fr.rows[r_i].cells[1].paragraphs[0].runs[0].bold = True
        tbl_fr.rows[r_i].cells[2].paragraphs[0].text = fdesc
    format_simple_table(tbl_fr, col_widths=[0.8, 2.0, 3.4])

    # 3.1.4 Non-Functional Requirements
    add_h3("3.1.4 Non-Functional Requirements Specification")
    p_nfr = (
        "Non-functional constraints define the operational performance, availability, maintainability, and security bounds of the system (Table 3.4)."
    )
    add_p(p_nfr)

    nfr_data = [
        ("NFR1", "Classification Latency Overhead", "The transformer classification forward pass shall execute in less than 30.0 milliseconds on standard CPU hardware to preserve overall pipeline throughput."),
        ("NFR2", "High-Availability & Uptime", "The gateway shall guarantee 99.9% request fulfillment uptime via automated bidirectional fallbacks preventing uncaught runtime crashes."),
        ("NFR3", "Zero Data Loss Schema Evolution", "The SQLite database layer shall inspect PRAGMA table_info on startup and execute non-destructive ALTER TABLE migrations when schema columns are added."),
        ("NFR4", "Data Privacy & Local Perimeter", "Simple, sensitive, or routine user queries shall remain strictly confined to the local workstation RAM, never transmitting payloads across WAN networks."),
        ("NFR5", "Modular Decoupling", "The classification, routing, inference, and persistence subsystems shall be completely isolated into distinct Python modules for independent refactoring."),
        ("NFR6", "Telemetry Transparency", "All estimated metrics (such as cloud emissions derived from 0.35g CO2 / 1k tokens) shall be explicitly labeled as 'Estimated' across all dashboard views."),
        ("NFR7", "Stateless Middleware Scalability", "The FastAPI routing core shall maintain stateless execution, enabling multi-worker horizontal scaling behind reverse proxies without session lockouts."),
        ("NFR8", "Security & Secret Isolation", "All commercial API keys (GROQ_API_KEY, GEMINI_API_KEY) shall be strictly isolated within local .env files and omitted from version control.")
    ]
    add_p("Table 3.4: System Non-Functional Requirements Specification (NFR1 to NFR8)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=10, space_after=4)
    tbl_nfr = doc.add_table(rows=len(nfr_data) + 1, cols=3)
    tbl_nfr.rows[0].cells[0].paragraphs[0].text = "NFR ID"
    tbl_nfr.rows[0].cells[1].paragraphs[0].text = "Quality Attribute"
    tbl_nfr.rows[0].cells[2].paragraphs[0].text = "Non-Functional Target Metric & Constraint"
    for r_i, (nid, nname, ndesc) in enumerate(nfr_data, start=1):
        tbl_nfr.rows[r_i].cells[0].paragraphs[0].text = nid
        tbl_nfr.rows[r_i].cells[0].paragraphs[0].runs[0].bold = True
        tbl_nfr.rows[r_i].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tbl_nfr.rows[r_i].cells[1].paragraphs[0].text = nname
        tbl_nfr.rows[r_i].cells[1].paragraphs[0].runs[0].bold = True
        tbl_nfr.rows[r_i].cells[2].paragraphs[0].text = ndesc
    format_simple_table(tbl_nfr, col_widths=[0.8, 2.0, 3.4])

    # ---------------------------------------------------------
    # 3.1.5 DATA FLOW DIAGRAMS
    # ---------------------------------------------------------
    add_h3("3.1.5 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)")

    p_model = (
        "Software modeling ensures rigorous architectural discipline before code deployment. The following subsections present "
        "the complete Data Flow Diagrams (DFDs) across Levels 0, 1, and 2, followed by comprehensive Unified Modeling Language (UML) "
        "diagrams modeling static object structures, use cases, sequential message passing, state transitions, and component packages."
    )
    add_p(p_model)
    add_p("A. Data Flow Diagram Level 0: Context Level Diagram", bold=True)
    add_p(
        "Figure 3.1 illustrates the Level 0 Context Diagram representing the high-level boundary of the Hybrid SLM-LLM Router Gateway. "
        "The system interacts with four primary external entities: the End User / Client, the Local Ollama SLM, External Cloud LLM APIs "
        "(Groq and Gemini), the Host Hardware Sensors (monitored by CodeCarbon), and the System Administrator."
    )
    add_image_centered(r"Report\figures\fig_3_1_dfd_level_0.png", "Figure 3.1: Data Flow Diagram (DFD) - Level 0: Context Level Diagram", width_in=5.8)

    add_p("B. Data Flow Diagram Level 1: Subsystem Functional Decomposition", bold=True)
    add_p(
        "Figure 3.2 decomposes Process 0.0 into seven core functional processes: 1.0 Prompt Ingestion & Validation, 2.0 Complexity Classification "
        "(querying Datastore D1: Pretrained Model Weights), 3.0 Model Routing & Dispatch Policy, 4.0 Local SLM Inference, 5.0 Cloud LLM Inference, "
        "6.0 Telemetry, Energy & Cost Accounting (writing to Datastore D2: SQLite requests_log), and 7.0 Dashboard Visual Analytics Rendering."
    )
    add_image_centered(r"Report\figures\fig_3_2_dfd_level_1.png", "Figure 3.2: Data Flow Diagram (DFD) - Level 1: Subsystem Functional Decomposition", width_in=6.0)

    add_p("C. Data Flow Diagram Level 2: Micro Process Decomposition", bold=True)
    add_p(
        "Figure 3.3 provides granular micro-process decomposition of the internal classification and multi-tier dispatch pipelines. Process 2.0 "
        "is expanded into WordPiece Tokenization (2.1), Transformer Forward Pass (2.2), and Softmax Scoring (2.3). The dispatch subsystem "
        "details the CodeCarbon tracking initialization (4.1), Ollama invocation (4.2), primary Groq LPU dispatch (5.1), and Gemini failover (5.2)."
    )
    add_image_centered(r"Report\figures\fig_3_3_dfd_level_2.png", "Figure 3.3: Data Flow Diagram (DFD) - Level 2: Micro Process Decomposition", width_in=6.0)

    # 3.1.6 Specification Document & UML Diagrams
    add_h3("3.1.6 Specification Document & UML Diagrams of all Modules")

    add_p("A. UML Use Case Diagram", bold=True)
    add_p(
        "Figure 3.4 captures system behavior from the perspective of user and system actors. Primary actors include the End User and "
        "System Administrator. Secondary system actors include the Local Ollama Daemon, Cloud API Services, and CodeCarbon Hardware Profiler. "
        "Core use cases include prompt submission, complexity evaluation (with <<include>> relationship), local routing, cloud execution, "
        "failover handling, live telemetry tracking, and visual analytics monitoring."
    )
    add_image_centered(r"Report\figures\fig_3_4_uml_use_case.png", "Figure 3.4: UML Use Case Diagram: Actor Roles and System Functional Boundaries", width_in=5.8)

    add_p("B. UML Class Diagram", bold=True)
    add_p(
        "Figure 3.5 models the static object-oriented structure, class attributes, method signatures, visibility modifiers, and associations. "
        "Key encapsulated classes include FastAPIRouter (controller), ChatSchemas (Pydantic validation models), DistilBERTClassifier (Hugging Face "
        "PyTorch wrapper with model caching), AlternativeClassifiers (heuristic regex and classical TF-IDF), LocalInferenceEngine (Ollama client with "
        "CodeCarbon telemetry), CloudInferenceEngine (multi-provider dispatcher), and DatabaseManager (SQLite connection pool and auto-migration engine)."
    )
    add_image_centered(r"Report\figures\fig_3_5_uml_class.png", "Figure 3.5: UML Class Diagram: Object-Oriented Software Architecture and Interfaces", width_in=6.0)

    add_p("C. UML Sequence Diagram", bold=True)
    add_p(
        "Figure 3.6 presents the chronological message-passing sequence across six lifelines: Client, FastAPI Gateway, DistilBERT Classifier, "
        "Local SLM, Cloud LLM, and SQLite DB. The diagram models the parallel execution alternatives for the normal local route (score < 0.50) "
        "and the cloud failover route (score >= 0.50), illustrating Groq rate-limit exception interception and immediate Gemini failover."
    )
    add_image_centered(r"Report\figures\fig_3_6_uml_sequence.png", "Figure 3.6: UML Sequence Diagram: Dual-Path Execution with Automated Failover", width_in=6.0)

    add_p("D. UML Activity Diagram", bold=True)
    add_p(
        "Figure 3.7 models procedural control flow, decision diamonds, concurrent fork/join pathways, and exception handling. It traces the prompt "
        "lifecycle from entry validation, through DistilBERT inference, threshold gating (p >= 0.50), Ollama execution with exception catch to "
        "cloud fallback, Groq execution with failover to Gemini, metric collating, and HTTP response serialization."
    )
    add_image_centered(r"Report\figures\fig_3_7_uml_activity.png", "Figure 3.7: UML Activity Diagram: Dynamic Decision Flow and Fallback Lifecycle", width_in=5.6)

    add_p("E. UML Component Diagram", bold=True)
    add_p(
        "Figure 3.8 depicts the structural organization of software components across the Presentation Tier (Streamlit, Swagger UI), "
        "Gateway & Logic Tier (FastAPI Gateway, ComplexityClassifier, RoutingPolicy, TelemetryEngine), and Execution & Persistence Tier "
        "(Ollama Service, Cloud Dispatch Service, SQLite Persistence, and Serialized Model Artifacts)."
    )
    add_image_centered(r"Report\figures\fig_3_8_uml_component.png", "Figure 3.8: UML Component Diagram: Multi-Tier Architectural Packages and Dependencies", width_in=6.0)

    add_p("F. UML State Machine Diagram", bold=True)
    add_p(
        "Figure 3.9 illustrates the state transitions of a request object across its lifecycle: [Start] -> Ingested (Schema Validated) -> "
        "Classifying (DistilBERT Forward Pass) -> RouteSelected -> LocalRunning / CloudRunning -> FailoverTriggered (if exception caught) -> "
        "LoggingMetrics -> Responded -> [End]."
    )
    add_image_centered(r"Report\figures\fig_3_9_uml_state_machine.png", "Figure 3.9: UML State Machine Diagram: Request Lifecycle States and Transitions", width_in=5.8)

    # ---------------------------------------------------------
    # G. MODULE SPECIFICATION: COMPLEXITY CLASSIFIER
    # ---------------------------------------------------------
    add_h4("G. Module Specification: Complexity Classification Engine")

    p_class_intro = (
        "To systematically evaluate prompt complexity, the project designed, implemented, and evaluated three distinct classification "
        "architectures: a deterministic rule-based heuristic, a classical TF-IDF with calibrated Logistic Regression pipeline, and a fine-tuned "
        "DistilBERT deep transformer sequence classifier."
    )
    add_p(p_class_intro)

    # 1. Heuristic
    add_p("1. Rule-Based Deterministic Heuristic Scorer", bold=True)
    p_heur = (
        "The baseline heuristic classifier (implemented in backend/classifier.py) operates as a deterministic accumulator that increments "
        "a score from 0.0 based on lexical length, mathematical symbols, conjunctions, and high-reasoning keywords:\n\n"
        "1. Length Rules: If token count > 40 words, add +0.4; if token count > 15 words, add +0.2.\n"
        "2. Mathematical Symbols: If prompt contains operators (+, -, *, /, =, %) or digits, add +0.2.\n"
        "3. Reasoning Keywords: If prompt matches any high-reasoning keyword ('explain', 'analyze', 'write code', 'calculate', 'compare', "
        "'reason', 'synthesize', 'evaluate', 'summarize', 'derive'), add +0.5 (applied once).\n"
        "4. Multi-Step Phrasing: If prompt contains sequential indicators ('then' or both 'first' and 'second'), add +0.2.\n"
        "5. Normalization: The final score is clamped: score = min(accumulated_score, 1.0).\n\n"
        "Heuristic Limitation & False Positives: While computationally instantaneous (0.05 ms), the heuristic exhibits severe keyword "
        "over-triggering. For example, the query 'Explain pizza' matches the keyword 'explain', instantly forcing score = 0.50 and routing "
        "a trivial culinary question to an expensive cloud model."
    )
    add_p(p_heur)

    # 2. Classical ML
    add_p("2. Classical Machine Learning: TF-IDF Vectorizer + Logistic Regression", bold=True)
    p_ml = (
        "To mitigate heuristic fragility, a machine learning pipeline was implemented in backend/ml_classifier.py and trained via "
        "scripts/train_ml_classifier.py. The pipeline combines Term Frequency-Inverse Document Frequency (TF-IDF) n-gram vectorization "
        "with calibrated Logistic Regression:\n\n"
        "1. TF-IDF Formulation: For term t in prompt d across corpus D:\n"
        "   TF-IDF(t, d, D) = [1 + log(TF(t, d))] * [log((1 + |D|) / (1 + |{d in D : t in d}|)) + 1]\n"
        "   Configured with sublinear_tf=True, ngram_range=(1, 2) extracting unigrams and bigrams, and max_features=2500.\n\n"
        "2. Logistic Regression: Maps the high-dimensional sparse vector x to a probability:\n"
        "   z = w^T * x + b\n"
        "   P(complex) = 1 / (1 + exp(-z))\n"
        "   Configured with inverse regularization strength C=1.5, class_weight='balanced', and solver='liblinear'.\n\n"
        "Advantage: Learns co-occurrence patterns, avoiding keyword over-triggering on phrases like 'Can you explain why water is wet?'."
    )
    add_p(p_ml)

    # 3. DistilBERT
    add_p("3. Deep Learning: Fine-Tuned DistilBERT Transformer Classifier", bold=True)
    p_distil = (
        "The production routing model (backend/ml_classifier_distilbert.py) utilizes a fine-tuned distilbert-base-uncased transformer "
        "sequence classifier (66 million parameters across 6 transformer layers, 768 hidden dimension, 12 self-attention heads). "
        "Fine-tuned in notebooks/finetune_classifier.ipynb on Google Colab (Tesla T4 GPU), the model processes prompts as follows:\n\n"
        "1. WordPiece Tokenization: Maps text to vocabulary indices (30,522 tokens) with special tokens [CLS] and [SEP], truncated or "
        "padded to max_length=128.\n"
        "2. Multi-Head Self-Attention: For query, key, value matrices Q, K, V:\n"
        "   Attention(Q, K, V) = softmax((Q * K^T) / sqrt(d_k)) * V\n"
        "3. Classification Head: The pooled hidden state of the [CLS] token h_[CLS] in R^768 is projected via a linear layer:\n"
        "   logits = W * h_[CLS] + b_cls, where W in R^(2 x 768)\n"
        "4. Softmax Normalization: The probability of class 1 (complex) is computed:\n"
        "   p = exp(logit_1) / [exp(logit_0) + exp(logit_1)]\n"
        "5. Decision & Confidence: Route = 'local' if p < 0.50 else 'cloud'; Confidence = max(p, 1 - p).\n\n"
        "Performance: Executes forward pass in 15 to 25 ms on CPU, delivering 99.17% validation accuracy."
    )
    add_p(p_distil)

    # 4. Dataset Evolution
    add_p("4. Dataset Engineering & Evolutionary Lifecycle", bold=True)
    p_data = (
        "The machine learning models were developed through four evolutionary dataset iterations (Table 3.5), transitioning from an initial "
        "120-prompt seed to a balanced, multi-domain curated corpus of 1,200 prompts (training_final.csv)."
    )
    add_p(p_data)

    ds_history = [
        ("v1: training_prompts.csv", "120 Prompts", "81 Simple, 39 Complex (67.5% / 32.5% Imbalanced)", "Hand-crafted prototype seed dataset used for initial TF-IDF feasibility testing; superceded due to small size and class imbalance."),
        ("v2: training_prompts_v2.csv", "450 Prompts", "225 Simple, 225 Complex (50.0% / 50.0% Balanced)", "Expanded synthetic dataset introducing contrast pairs (long simple queries vs. short math queries); still modest for 66M transformer."),
        ("v3: training_prompts_v3.csv", "1,730 Prompts", "853 Simple, 877 Complex (GSM8K, SQuAD, Dolly-15k)", "Attempted merge of public benchmarks. Dropped due to SQuAD context-dependency flaw (questions missing passages) and Dolly noise."),
        ("Final: training_final.csv", "1,200 Prompts", "600 Simple, 600 Complex (Exactly 50% / 50% Balanced)", "Production curated corpus: 8 distinct domains (150 prompts each), deduplicated, shuffled with seed 42. Zero missing values.")
    ]
    add_p("Table 3.5: Training Dataset Evolution and Version Comparison (v1 to Final)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=10, space_after=4)
    tbl_ds = doc.add_table(rows=len(ds_history) + 1, cols=4)
    tbl_ds.rows[0].cells[0].paragraphs[0].text = "Dataset Version"
    tbl_ds.rows[0].cells[1].paragraphs[0].text = "Sample Count"
    tbl_ds.rows[0].cells[2].paragraphs[0].text = "Class Distribution"
    tbl_ds.rows[0].cells[3].paragraphs[0].text = "Architectural Evaluation & Fate"
    for r_i, (dver, dcnt, ddist, dfate) in enumerate(ds_history, start=1):
        tbl_ds.rows[r_i].cells[0].paragraphs[0].text = dver
        tbl_ds.rows[r_i].cells[0].paragraphs[0].runs[0].bold = True
        tbl_ds.rows[r_i].cells[1].paragraphs[0].text = dcnt
        tbl_ds.rows[r_i].cells[2].paragraphs[0].text = ddist
        tbl_ds.rows[r_i].cells[3].paragraphs[0].text = dfate
    format_simple_table(tbl_ds, col_widths=[1.5, 0.9, 1.8, 2.0])

    p_cats = (
        "Table 3.6 presents the domain category breakdown of the deployed 1,200-sample dataset (training_final.csv), demonstrating "
        "strict class balance across four simple and four complex operational categories."
    )
    add_p(p_cats)

    cat_data = [
        ("1", "simple_general_facts", "150", "Simple (0)", "Elementary world knowledge, geography, scientific constants, trivia"),
        ("2", "simple_india_facts", "150", "Simple (0)", "Indian history, geography, governance, sports, and cultural trivia"),
        ("3", "casual_conversational", "150", "Simple (0)", "Greetings, small talk, pleasantries, daily life conversational queries"),
        ("4", "deceptively_simple", "150", "Simple (0)", "Wordy, long conversational queries that ask basic questions (mitigates brevity bias)"),
        ("5", "multistep_math_reasoning", "150", "Complex (1)", "Word problems, calculus, proofs by contradiction, stochastic modeling"),
        ("6", "complex_code", "150", "Complex (1)", "Async queues, data structures, algorithms, concurrency, transformer code"),
        ("7", "deep_technical_analysis", "150", "Complex (1)", "Distributed systems architecture, network protocols, comparative tradeoffs"),
        ("8", "advanced_reasoning_creative", "150", "Complex (1)", "Macroeconomic policy, philosophical analysis, complex essay generation")
    ]
    add_p("Table 3.6: Curated 8-Category Prompt Distribution (training_final.csv)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=10, space_after=4)
    tbl_cat = doc.add_table(rows=len(cat_data) + 1, cols=5)
    tbl_cat.rows[0].cells[0].paragraphs[0].text = "ID"
    tbl_cat.rows[0].cells[1].paragraphs[0].text = "Category Domain"
    tbl_cat.rows[0].cells[2].paragraphs[0].text = "Count"
    tbl_cat.rows[0].cells[3].paragraphs[0].text = "Target Class"
    tbl_cat.rows[0].cells[4].paragraphs[0].text = "Semantic Description & Sample Scope"
    for r_i, (cid, cname, ccnt, ccls, cdesc) in enumerate(cat_data, start=1):
        tbl_cat.rows[r_i].cells[0].paragraphs[0].text = cid
        tbl_cat.rows[r_i].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tbl_cat.rows[r_i].cells[1].paragraphs[0].text = cname
        tbl_cat.rows[r_i].cells[1].paragraphs[0].runs[0].bold = True
        tbl_cat.rows[r_i].cells[2].paragraphs[0].text = ccnt
        tbl_cat.rows[r_i].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tbl_cat.rows[r_i].cells[3].paragraphs[0].text = ccls
        tbl_cat.rows[r_i].cells[4].paragraphs[0].text = cdesc
    format_simple_table(tbl_cat, col_widths=[0.5, 2.0, 0.7, 1.0, 2.0])

    # ---------------------------------------------------------
    # H. MODULE SPECIFICATION: INFERENCE ENGINES & FAILOVER
    # ---------------------------------------------------------
    add_h4("H. Module Specification: Inference Execution Engines & Multi-Tier Failover")
    p_inf = (
        "The inference execution layer is structured into three specialized pipelines:\n\n"
        "1. Local SLM Pipeline (backend/local_inference.py): Connects to the local Ollama daemon running qwen2.5:7b. Requests are "
        "transmitted via HTTP POST to http://127.0.0.1:11434/api/generate with JSON payload {'model': 'qwen2.5:7b', 'prompt': prompt, 'stream': False}. "
        "Incurred API cost is strictly $0.00.\n\n"
        "2. Cloud LLM Dispatcher (backend/cloud_inference.py): Manages cloud inference across two commercial providers. The primary "
        "provider is Groq LPU executing openai/gpt-oss-120b, delivering 300+ tokens/second. If Groq encounters rate limiting (HTTP 429), "
        "timeouts, or network connection failures, the exception handler catches the error and immediately dispatches the prompt to "
        "Google Gemini (gemini-2.5-flash) using the official google-genai SDK.\n\n"
        "3. Dual-Layer Bidirectional Fallback: The gateway provides end-to-end fault tolerance against both edge and cloud outages:\n"
        "   - Tier-1 Local-to-Cloud Fallback: If Ollama crashes or is offline, the router intercepts requests.RequestException, logs "
        "     fallback_reason = 'local_slm_unavailable', and forwards the query to the cloud pipeline, ensuring continuous service.\n"
        "   - Tier-2 Reverse Cloud Fallback: If both cloud providers fail or internet access drops, complex queries reverse-fallback "
        "     to the local SLM with fallback_reason = 'cloud_llm_unavailable'."
    )
    add_p(p_inf)

    # ---------------------------------------------------------
    # I. MODULE SPECIFICATION: TELEMETRY & COST ACCOUNTING
    # ---------------------------------------------------------
    add_h4("I. Module Specification: Telemetry, Environmental & Cost Tracking Engines")
    p_tel = (
        "The gateway implements continuous telemetry tracking across financial, electrical, and carbon dimensions:\n\n"
        "1. Financial Cost Modeling: Local queries incur $0.00. For cloud requests, cost is computed based on actual prompt and completion tokens:\n"
        "   Cost_Groq = (N_prompt * $0.03 / 1,000,000) + (N_completion * $0.17 / 1,000,000)\n"
        "   Cost_Gemini = (N_prompt * $0.075 / 1,000,000) + (N_completion * $0.30 / 1,000,000)\n"
        "   Cost_INR = Cost_USD * 83.0 (Fixed exchange multiplier).\n\n"
        "2. Counterfactual Cost Savings: The system quantifies avoided expenditure by comparing actual hybrid cost against what the "
        "workload would have cost if 100% of prompts had been sent to the cloud:\n"
        "   Cost_baseline = Cost_actual + SUM_{j in Local} [(len(P_j)/4 * $0.03/1M) + (len(R_j)/4 * $0.17/1M)]\n"
        "   Cost_Saved = Cost_baseline - Cost_actual\n\n"
        "3. Environmental Carbon Telemetry: Local SLM inference is actively monitored via CodeCarbon (EmissionsTracker), sampling CPU/GPU "
        "energy in kilowatt-hours (kWh) and regional carbon emissions in grams of CO2. Cloud emissions are estimated using documented "
        "empirical constants (0.35g CO2 and 0.0004 kWh per 1,000 tokens; Luccioni et al. 2023, Patterson et al. 2021)."
    )
    add_p(p_tel)

    # ---------------------------------------------------------
    # 3.2 USER INTERFACE DESIGN (SCREENSHOTS)
    # ---------------------------------------------------------
    add_h2("3.2 User Interface Design")
    p_ui = (
        "The system provides an intuitive, high-visibility user interface developed in Streamlit (dashboard/app.py) and interactive "
        "OpenAPI Swagger documentation via FastAPI. The following seven screenshots depict the running system in operation."
    )
    add_p(p_ui)

    add_image_centered(r"Report\screenshots\screen_1_playground_journey.png", "Screenshot 3.1: Interactive Prompt Routing Playground & Real-Time Request Journey Trace", width_in=6.1)
    add_p(
        "Screenshot 3.1 displays the interactive testing console. Users can enter arbitrary prompts or select from curated demo queries. "
        "Below the input box, the 6-stage Execution Journey visually illuminates the active route in green (Local SLM qwen2.5:7b, latency 22,782 ms), "
        "displaying complexity score 0.01 and 98.5% confidence alongside the decision tree and classify vs. inference latency breakdown."
    )

    add_image_centered(r"Report\screenshots\screen_2_metrics_and_charts.png", "Screenshot 3.2: System-Wide Operational KPIs & Workload Distribution Analytics", width_in=6.1)
    add_p(
        "Screenshot 3.2 presents executive KPI summary cards: Total Requests (35), Routed Local (20 at ₹0.00 Zero Cost), Routed Cloud (15 with "
        "3 failovers badged), Total Cost Saved (₹0.5568), and Cloud API Calls Avoided (57.1%, exceeding the 40% benchmark). Below the cards, the "
        "continuous complexity scatter chart plots all 35 requests relative to the red 0.50 threshold line."
    )

    add_image_centered(r"Report\screenshots\screen_3_environmental_timeline.png", "Screenshot 3.3: Financial Impact & Cumulative Savings Trends", width_in=6.1)
    add_p(
        "Screenshot 3.3 depicts the visual analytics section: cumulative cost and CO2 savings trend graphs over time, the traffic route share "
        "donut chart, the financial impact bar chart contrasting actual incurred cost against the 100% cloud baseline, and the average speed chart."
    )

    add_image_centered(r"Report\screenshots\screen_4_database_log.png", "Screenshot 3.4: Environmental Carbon Accounting & Live Historical Request Audit Log", width_in=6.1)
    add_p(
        "Screenshot 3.4 shows the environmental carbon telemetry cards (14.230 g CO2 saved, 0.018820 kWh consumed) and the emissions comparison "
        "bar chart. Below, Step 5 displays the historical SQLite audit table with color-coded badges (Local, Cloud, Local Fallback with warning icon)."
    )

    add_image_centered(r"Report\screenshots\screen_fastapi_docs.png", "Screenshot 3.5: FastAPI Interactive OpenAPI / Swagger Documentation Portal (/docs)", width_in=5.8)
    add_p(
        "Screenshot 3.5 illustrates the auto-generated Swagger documentation interface at http://127.0.0.1:8000/docs, documenting the GET /, "
        "GET /health, and POST /chat endpoints alongside data schemas."
    )

    add_image_centered(r"Report\screenshots\screen_fastapi_chat_expanded.png", "Screenshot 3.6: Swagger Interactive /chat Endpoint Request and Response Schema Specification", width_in=5.8)
    add_p(
        "Screenshot 3.6 depicts the expanded POST /chat endpoint in Swagger UI, showing request parameter requirements and the strongly-typed "
        "Pydantic ChatResponse JSON schema."
    )

    add_image_centered(r"Report\screenshots\screen_fastapi_health.png", "Screenshot 3.7: Subsystem Connectivity Diagnostics & Health API Response (/health)", width_in=5.5)
    add_p(
        "Screenshot 3.7 displays the live JSON payload returned by GET /health, confirming online status, Ollama availability (true), Groq and "
        "Gemini key configuration (true), active classifier mode (distilbert), model load status (true), and threshold (0.5)."
    )

    # ---------------------------------------------------------
    # 3.3 DATABASE DESIGN / ER DIAGRAMS
    # ---------------------------------------------------------
    add_h2("3.3 Database Design / ER Diagrams")
    p_db = (
        "The persistence layer is implemented via a lightweight, high-reliability SQLite relational database (router_logs.db) defined in "
        "backend/database.py. Figure 3.10 illustrates the Entity-Relationship (ER) model for the primary requests_log entity."
    )
    add_p(p_db)

    add_image_centered(r"Report\figures\fig_3_10_database_er.png", "Figure 3.10: Relational Database Entity-Relationship (ER) Diagram (requests_log Table)", width_in=5.8)

    p_ddl = (
        "The DDL specification and complete data dictionary for table requests_log is defined in Table 3.7."
    )
    add_p(p_ddl)

    schema_data = [
        ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Surrogate unique identifier for each processed request transaction"),
        ("timestamp", "TEXT", "NOT NULL (ISO 8601)", "UTC timestamp recorded at HTTP entry (YYYY-MM-DDTHH:MM:SS.mmmmmm)"),
        ("prompt", "TEXT", "NOT NULL", "Full raw text of the incoming prompt submitted by the client"),
        ("route_taken", "TEXT", "NOT NULL ('local'|'cloud')", "Final routing destination resolved by the classifier and gateway policy"),
        ("complexity_score", "REAL", "RANGE [0.0, 1.0]", "Predicted probability score p computed by the active classification engine"),
        ("latency_ms", "REAL", "POSITIVE FLOAT", "Total end-to-end round-trip latency measured in milliseconds"),
        ("estimated_cost_usd", "REAL", "POSITIVE FLOAT", "Calculated API expenditure in USD ($0.00 for local SLM execution)"),
        ("response_preview", "TEXT", "NULLABLE", "Full generated completion text returned by the serving language model"),
        ("cloud_provider", "TEXT", "DEFAULT 'none'", "Serving provider: 'none' (Local Ollama), 'groq', or 'gemini' (Failover)"),
        ("co2_grams", "REAL", "DEFAULT 0.0", "Carbon emissions footprint in grams (measured via CodeCarbon or estimated)"),
        ("energy_kwh", "REAL", "DEFAULT 0.0", "Electrical energy consumed during request execution in kilowatt-hours"),
        ("fallback_reason", "TEXT", "DEFAULT NULL", "Exception flag: 'local_slm_unavailable', 'cloud_llm_unavailable', or NULL"),
        ("classifier_confidence","REAL", "DEFAULT NULL", "Certainty score computed as max(p, 1-p) in range [0.50, 1.00]"),
        ("classify_ms", "REAL", "DEFAULT NULL", "Time spent exclusively executing the complexity classification step (ms)"),
        ("inference_ms", "REAL", "DEFAULT NULL", "Time spent exclusively generating completion tokens in the model (ms)"),
        ("model_name", "TEXT", "DEFAULT NULL", "Exact serving model identifier (e.g., 'qwen2.5:7b', 'openai/gpt-oss-120b')")
    ]
    add_p("Table 3.7: Relational Database Schema Data Dictionary (requests_log Table)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=10, space_after=4)
    tbl_sch = doc.add_table(rows=len(schema_data) + 1, cols=4)
    tbl_sch.rows[0].cells[0].paragraphs[0].text = "Column Name"
    tbl_sch.rows[0].cells[1].paragraphs[0].text = "SQLite Type"
    tbl_sch.rows[0].cells[2].paragraphs[0].text = "Constraints"
    tbl_sch.rows[0].cells[3].paragraphs[0].text = "Data Dictionary Description"
    for r_i, (cname, ctype, ccon, cdesc) in enumerate(schema_data, start=1):
        tbl_sch.rows[r_i].cells[0].paragraphs[0].text = cname
        tbl_sch.rows[r_i].cells[0].paragraphs[0].runs[0].bold = True
        tbl_sch.rows[r_i].cells[1].paragraphs[0].text = ctype
        tbl_sch.rows[r_i].cells[2].paragraphs[0].text = ccon
        tbl_sch.rows[r_i].cells[3].paragraphs[0].text = cdesc
    format_simple_table(tbl_sch, col_widths=[1.4, 0.9, 1.5, 2.4])

    p_mig = (
        "Non-Destructive Schema Auto-Migration: To guarantee high maintainability (NFR3), backend/database.py executes an automatic "
        "schema audit during init_db() on application startup. It queries PRAGMA table_info(requests_log) to inspect all existing column "
        "names. If newer telemetry columns (such as cloud_provider, co2_grams, fallback_reason, or model_name) are missing from an older database "
        "file, the module executes non-destructive ALTER TABLE requests_log ADD COLUMN ... DDL statements. This self-healing design prevents "
        "system crashes when switching branches or deploying database upgrades."
    )
    add_p(p_mig)

    doc.add_page_break()
    print("Chapter 3 generated successfully.")
