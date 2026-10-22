# chapter1.py - Chapter 1: Introduction (Exhaustive Academic Text)
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter1(doc, add_p, add_h1, add_h2, add_h3, add_image_centered):
    add_h1("CHAPTER 1: INTRODUCTION")
    
    # ---------------------------------------------------------
    # 1.1 INTRODUCTION
    # ---------------------------------------------------------
    add_h2("1.1 Introduction")
    
    p1 = (
        "In contemporary computer science and artificial intelligence engineering, the deployment of Large Language Models "
        "(LLMs) has fundamentally transformed the paradigm of human-computer interaction, cognitive automation, automated "
        "code synthesis, and decision-support systems. Frontier models such as OpenAI's GPT-4, Anthropic's Claude 3.5 Sonnet, "
        "and Google's Gemini family demonstrate unprecedented proficiency across natural language understanding, complex "
        "multi-step mathematical proofs, contextual code generation, and multi-turn technical dialogue. Driven by massive "
        "transformer architectures comprising tens to hundreds of billions of parameters, these foundation models have become "
        "the default computational backbone for modern enterprise AI solutions, customer service bots, interactive copilot "
        "interfaces, and autonomous agent frameworks."
    )
    add_p(p1)

    p2 = (
        "However, the operational reality of deploying commercial Generative AI architectures reveals critical structural "
        "inefficiencies. Currently, standard enterprise software patterns treat cloud LLM APIs as monolithic black boxes: "
        "every incoming query—regardless of whether it is an elementary conversational greeting ('Good morning'), a routine factual "
        "lookup ('What is the boiling point of water?'), a basic syntax question, or an advanced theoretical derivation—is "
        "dispatched indiscriminately to remote hyperscale cloud inference clusters. This monolithic routing approach introduces "
        "four severe compounding liabilities:"
    )
    add_p(p2)

    bullets_intro = [
        ("Compounding Financial Expenditures: ", "Commercial LLMs bill on a per-token basis (both input and completion tokens). Multiplying thousands of daily requests across an organization leads to unsustainable API bills, where a significant majority of queries consume expensive 120B+ parameter compute budgets on tasks that could be handled by much smaller models."),
        ("Variable Latency & Inherent Network Overhead: ", "Transmitting prompt payloads across regional wide-area networks (WANs) to remote cloud data centers introduces network queuing delays, socket handshakes, and serialization overhead. In time-sensitive agentic workflows, waiting 3 to 10 seconds for a trivial confirmation prompt slows downstream tasks."),
        ("Fragility and Service Rate-Limiting: ", "Heavy dependence on single third-party proprietary APIs leaves client systems completely vulnerable to external vendor outages, HTTP 429 (Too Many Requests) throttling, quota exhaustion, and localized internet routing failures, degrading system availability."),
        ("Environmental Energy and Carbon Footprint: ", "Frontier model inference runs on massive, power-intensive GPU data center clusters (e.g., 8x H100 nodes pulling hundreds of kilowatts). Running trivial string transformations or basic queries on 70B+ parameter models causes significant avoidable electrical energy consumption and carbon emissions.")
    ]
    for b_title, b_desc in bullets_intro:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_bullet = p.add_run("• ")
        r_bullet.bold = True
        r_title = p.add_run(b_title)
        r_title.bold = True
        r_desc = p.add_run(b_desc)

    p3 = (
        "In sharp contrast to this monolithic cloud dependency, recent breakthroughs in deep learning model compression, "
        "quantization (e.g., GGUF 4-bit integer quantization), and architecture optimization have catalyzed the rise of "
        "Small Language Models (SLMs). Models such as Alibaba’s Qwen2.5-7B Instruct, Microsoft’s Phi-3.5/Phi-4-mini, and "
        "Mistral-7B possess billions of parameters but can execute locally on consumer workstations and laptops with 8 to 16 GB "
        "of RAM at zero marginal API cost. Local SLMs deliver rapid execution for everyday conversation, syntactic restructuring, "
        "and factual queries, while preserving complete data privacy. However, SLMs suffer from degraded performance when confronted "
        "with deep architectural analysis, advanced multi-variable mathematics, or complex algorithmic design."
    )
    add_p(p3)

    p4 = (
        "Therefore, neither an all-cloud architecture nor an all-local architecture provides an optimal Pareto tradeoff between "
        "cost, latency, response quality, and environmental sustainability. What is required is an intelligent middleware layer: "
        "a Hybrid SLM-LLM Router Gateway that dynamically inspects each incoming user query in real time, evaluates its intrinsic "
        "computational and semantic complexity, and routes it to the optimal compute layer. Simple queries are fulfilled locally "
        "by the SLM at ₹0.00 cost, while complex, reasoning-intensive tasks are escalated to high-capacity cloud LLMs."
    )
    add_p(p4)

    # ---------------------------------------------------------
    # 1.2 NECESSITY
    # ---------------------------------------------------------
    add_h2("1.2 Necessity")

    p5 = (
        "The necessity of developing an intelligent hybrid router middleware arises directly from the economic, operational, "
        "and architectural realities of modern production artificial intelligence systems:"
    )
    add_p(p5)

    nec_points = [
        ("1. Economic Unsustainability of Frontier LLMs: ", "As GenAI integration expands from exploratory prototypes to production enterprise workflows, monthly API bills escalate geometrically. For applications processing hundreds of thousands of prompts per month, paying commercial rates for trivial queries is economically wasteful. A router provides immediate cost control by offloading 50% to 70% of routine traffic to local execution."),
        ("2. Real-Time Latency Optimization for Agentic Chains: ", "Autonomous multi-agent frameworks (such as LangChain, AutoGen, and CrewAI) generate extensive internal sub-prompts for planning, formatting, and validation. Forcing every intermediate reflection step through remote cloud APIs introduces cumulative delays. A hybrid router enables instantaneous local execution for intermediate syntactic checks, reserving cloud latency only for critical synthesis."),
        ("3. High-Availability & Fault Tolerance: ", "Production applications require 99.9% uptime. Relying solely on a single cloud vendor creates a critical single point of failure. If the cloud vendor suffers downtime or imposes aggressive rate-limits, the entire application halts. The necessity of a resilient routing middleware lies in its ability to implement bidirectional fallbacks—failing over to alternative cloud providers or falling back to local models when services fail."),
        ("4. Data Privacy and Local Sovereignty: ", "Certain user queries contain internal operational context, employee queries, or preliminary drafts that do not require cloud exposure. Enabling local model execution ensures that routine corporate data remains within the local network perimeter, mitigating compliance exposure under global data sovereignty frameworks."),
        ("5. Green Computing & Corporate Sustainability: ", "The computing community faces intensifying pressure to reduce the carbon footprint of AI workloads. Every forward pass through an unquantized 120-billion parameter cloud cluster draws significant power. Dynamically offloading appropriate tasks to efficient 7B quantized local engines directly reduces electrical energy waste and carbon emissions.")
    ]
    for n_title, n_desc in nec_points:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_title = p.add_run(n_title)
        r_title.bold = True
        r_desc = p.add_run(n_desc)

    # ---------------------------------------------------------
    # 1.3 OBJECTIVES
    # ---------------------------------------------------------
    add_h2("1.3 Objectives")

    p6 = (
        "The primary engineering and research objectives of the Hybrid SLM-LLM Router Agent project are formalized as follows:"
    )
    add_p(p6)

    objs = [
        ("Objective 1: Multi-Tier Complexity Classification Engine", "Design, implement, and benchmark three distinct prompt complexity classification paradigms: a rule-based regex heuristic, a classical TF-IDF with calibrated Logistic Regression pipeline, and an optimized, fine-tuned DistilBERT transformer sequence classifier (66M parameters). Target a classification latency under 30 milliseconds on consumer CPU hardware and exceed 88% cross-validation accuracy."),
        ("Objective 2: Intelligent Dynamic Threshold Routing", "Implement a configurable probability threshold gate (calibrated at p = 0.50) within an asynchronous FastAPI middleware to direct prompts scored below 0.50 to a local SLM and prompts at or above 0.50 to cloud LLMs, ensuring seamless routing without modifying client application code."),
        ("Objective 3: Target Workload Offload and Cost Reduction", "Achieve a minimum 40% empirical reduction in external cloud API calls across benchmark query distributions, translating to a measurable financial expenditure reduction of greater than 50% compared to a counterfactual 100% all-cloud baseline."),
        ("Objective 4: Dual-Layer Resilient Failover & Fault Tolerance", "Engineer a two-tier fault-tolerant exception handling architecture: (a) Tier-1 Local-to-Cloud fallback that intercepts local Ollama downtime or socket timeouts and redirects traffic to the cloud with audit transparency, and (b) Tier-2 Cloud-to-Cloud failover that catches Groq LPU rate limits (HTTP 429) or timeouts and dispatches queries to Google Gemini 2.5 Flash within the same execution cycle."),
        ("Objective 5: Live Hardware Carbon and Energy Accounting", "Integrate the CodeCarbon telemetry engine into the local execution path to sample real-time CPU/GPU power draw (kWh) and regional carbon emissions (g CO2) via hardware counters and TDP profiles, paired with literature-grounded empirical cloud estimation (0.35g CO2 / 1k tokens)."),
        ("Objective 6: Comprehensive Observability & Visual Analytics", "Develop an interactive Streamlit analytics dashboard providing live prompt routing tests, step-by-step visual execution journey traces, Altair financial and latency comparative charts, and an auto-migrating SQLite audit log recording 16 granular metrics per interaction.")
    ]
    for o_title, o_desc in objs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_title = p.add_run(o_title + ": ")
        r_title.bold = True
        r_desc = p.add_run(o_desc)

    # ---------------------------------------------------------
    # 1.4 THEME OF THE MINI PROJECT
    # ---------------------------------------------------------
    add_h2("1.4 Theme of the Mini Project")

    p7 = (
        "The overarching theme of this mini project is 'Intelligent Computational Resource Optimization and Sustainable Edge-Cloud "
        "Synergy for Generative AI'. It bridges the gap between state-of-the-art Natural Language Processing (NLP), Transformer "
        "sequence classification, systems programming, and Green Computing."
    )
    add_p(p7)

    p8 = (
        "Rather than treating foundation models as homogenous or competing entities, the project champions an architectural "
        "symbiosis: compact, highly specialized machine learning classifiers act as intelligent triage controllers, matching the "
        "difficulty of human inquiries with the minimum necessary computing tier. The theme centers on operational pragmatism—delivering "
        "measurable financial cost savings, latency predictability, resilient system uptime, and environmental accountability "
        "without sacrificing user response quality."
    )
    add_p(p8)

    # ---------------------------------------------------------
    # 1.5 PROPOSED SYSTEM ARCHITECTURE
    # ---------------------------------------------------------
    add_h2("1.5 Proposed System Architecture")

    p9 = (
        "The proposed system architecture is designed as a modular, loosely-coupled, multi-tiered middleware gateway. The system "
        "is organized into five primary functional layers: the Client Presentation Layer, the FastAPI Routing & Gateway Layer, "
        "the Complexity Classification Engine, the Multi-Provider Inference Execution Layer, and the Telemetry & Persistence Layer."
    )
    add_p(p9)

    add_image_centered(r"Report\figures\fig_1_1_system_architecture.png", "Figure 1.1: Hybrid SLM-LLM Router Gateway Architecture Overview", width_in=6.1)

    p10 = (
        "The operational lifecycle of a user request proceeds through these architectural stages:"
    )
    add_p(p10)

    stages = [
        ("Stage 1: Ingestion & Validation: ", "The client application (e.g., Streamlit web portal or third-party client) transmits an HTTP POST request containing a JSON payload {'prompt': '...'} to the FastAPI endpoint /chat. Pydantic models strictly validate the request structure, verify string integrity, and initialize high-resolution monotonic latency timers."),
        ("Stage 2: Complexity Evaluation: ", "The prompt string is passed to the active classification subsystem configured by the CLASSIFIER_MODE environment variable. In DistilBERT mode, the text is tokenized into WordPiece subword tokens (capped at 128 tokens), processed through 6 transformer encoder layers, and normalized via softmax to output a continuous complexity probability p in the range [0.0, 1.0]. Classification confidence is computed as max(p, 1-p)."),
        ("Stage 3: Decision Gating & Dynamic Dispatch: ", "The complexity score p is evaluated against COMPLEXITY_THRESHOLD = 0.50. If p < 0.50, the prompt is designated as simple and dispatched to the Local SLM path. If p >= 0.50, the prompt is designated as complex and dispatched to the Cloud LLM pipeline."),
        ("Stage 4: Local SLM Execution with Live Telemetry: ", "For local requests, the router dispatches an HTTP POST request to the local Ollama daemon (127.0.0.1:11434) running the 4-bit quantized Qwen2.5-7B Instruct model. Simultaneously, CodeCarbon starts an in-memory EmissionsTracker, sampling host CPU/GPU energy consumption (kWh) and regional carbon emissions (g CO2). If Ollama is unreachable, Tier-1 fallback redirects the query to the cloud pipeline with fallback_reason = 'local_slm_unavailable'."),
        ("Stage 5: Cloud LLM Dispatch with Automated Failover: ", "For cloud requests, the gateway dispatches the prompt to primary cloud provider Groq LPU serving openai/gpt-oss-120b. If Groq encounters rate limiting (HTTP 429) or timeouts, exception handlers intercept the error and execute an immediate single-retry failover to Google Gemini 2.5 Flash. If both cloud providers fail, Tier-2 reverse fallback redirects to the local Ollama SLM."),
        ("Stage 6: Structured Relational Audit Logging & Client Response: ", "Upon completion, the gateway collates all execution telemetry—including total latency, classification time, inference time, calculated cost in USD and INR, energy consumed, carbon emitted, serving provider, and model name—and writes a 16-column record into the SQLite requests_log table with schema auto-migration. Finally, an HTTP 200 ChatResponse JSON payload is returned to the client.")
    ]
    for s_title, s_desc in stages:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_title = p.add_run(s_title)
        r_title.bold = True
        r_desc = p.add_run(s_desc)

    doc.add_page_break()
    print("Chapter 1 generated successfully.")
