# report_text_data.py - Exhaustive Academic Text Content for Hybrid SLM-LLM Router Agent Report

ABBREVIATIONS = [
    ("1", "SLM", "Small Language Model (1B - 7B parameter open-weights models)"),
    ("2", "LLM", "Large Language Model (70B+ parameter frontier models)"),
    ("3", "API", "Application Programming Interface"),
    ("4", "REST", "Representational State Transfer (HTTP stateless architectural style)"),
    ("5", "JSON", "JavaScript Object Notation"),
    ("6", "HTTP", "Hypertext Transfer Protocol"),
    ("7", "DFD", "Data Flow Diagram (Gane-Sarson / Yourdon structured notation)"),
    ("8", "UML", "Unified Modeling Language (OMG Standard for software modeling)"),
    ("9", "ER", "Entity-Relationship (Relational database conceptual model)"),
    ("10", "TF-IDF", "Term Frequency - Inverse Document Frequency"),
    ("11", "NLP", "Natural Language Processing"),
    ("12", "BERT", "Bidirectional Encoder Representations from Transformers"),
    ("13", "DistilBERT", "Distilled Bidirectional Encoder Representations from Transformers"),
    ("14", "LPU", "Language Processing Unit (Groq custom tensor accelerator)"),
    ("15", "RAPL", "Running Average Power Limit (Hardware power telemetry interface)"),
    ("16", "TDP", "Thermal Design Power (Hardware maximum baseline power profile)"),
    ("17", "GPU", "Graphics Processing Unit"),
    ("18", "CPU", "Central Processing Unit"),
    ("19", "RAM", "Random Access Memory"),
    ("20", "SQLite", "Structured Query Language Lite (Self-contained serverless RDBMS)"),
    ("21", "KPI", "Key Performance Indicator"),
    ("22", "CO2", "Carbon Dioxide (Greenhouse gas equivalent emissions)"),
    ("23", "kWh", "Kilowatt-Hour (Metric unit of electrical energy)"),
    ("24", "GGUF", "GPT-Generated Unified Format (Quantized model binary container)"),
    ("25", "LRU", "Least Recently Used (Cache eviction policy)"),
    ("26", "ASGI", "Asynchronous Server Gateway Interface (Python standard for async servers)"),
    ("27", "WSGI", "Web Server Gateway Interface (Python legacy synchronous web standard)"),
    ("28", "DDL", "Data Definition Language (SQL schema creation statements)"),
    ("29", "CV", "Cross-Validation (Statistical resampling model evaluation)"),
    ("30", "OOD", "Out-of-Distribution (Data differing from training distribution)")
]

FIGURES_LIST = [
    ("1.1", "Hybrid SLM-LLM Router Gateway Architecture Overview", "10"),
    ("3.1", "Data Flow Diagram (DFD) - Level 0: Context Level Diagram", "18"),
    ("3.2", "Data Flow Diagram (DFD) - Level 1: Subsystem Functional Decomposition", "20"),
    ("3.3", "Data Flow Diagram (DFD) - Level 2: Micro Process Decomposition (Classification & Dispatch)", "22"),
    ("3.4", "UML Use Case Diagram: Actor Roles and System Functional Boundaries", "24"),
    ("3.5", "UML Class Diagram: Object-Oriented Software Architecture and Interfaces", "26"),
    ("3.6", "UML Sequence Diagram: Dual-Path Execution with Automated Failover", "28"),
    ("3.7", "UML Activity Diagram: Dynamic Decision Flow and Fallback Lifecycle", "30"),
    ("3.8", "UML Component Diagram: Multi-Tier Architectural Packages and Dependencies", "32"),
    ("3.9", "UML State Machine Diagram: Request Lifecycle States and Transitions", "34"),
    ("3.10", "Relational Database Entity-Relationship (ER) Diagram (requests_log Table)", "40")
]

GRAPHS_LIST = [
    ("4.1", "Complexity Classifier Accuracy Benchmark (Heuristic vs. TF-IDF vs. DistilBERT)", "44"),
    ("4.2", "Workload Offload Distribution (60.0% Local SLM vs. 40.0% Cloud LLM)", "46"),
    ("4.3", "Average Response Latency Comparison (Local CPU vs. Cloud LPU / Gemini)", "47"),
    ("4.4", "Financial Expenditure Comparison (Actual Hybrid Architecture vs. 100% Cloud Baseline)", "49"),
    ("4.5", "Environmental Carbon Emissions Footprint (Actual vs. 100% Cloud Counterfactual)", "50")
]

TABLES_LIST = [
    ("2.1", "Comparative Literature Survey & Synthesis Matrix", "15"),
    ("3.1", "Hardware Development & Deployment Testbed Specifications", "16"),
    ("3.2", "Software Technology Stack, Frameworks & Dependency Specifications", "17"),
    ("3.3", "System Functional Requirements Specification (FR1 to FR10)", "18"),
    ("3.4", "System Non-Functional Requirements Specification (NFR1 to NFR8)", "19"),
    ("3.5", "Training Dataset Evolution and Version Comparison (v1 to Final)", "36"),
    ("3.6", "Curated 8-Category Prompt Distribution (training_final.csv)", "37"),
    ("3.7", "Relational Database Schema Data Dictionary (requests_log Table)", "41"),
    ("4.1", "Classifier Accuracy, Cross-Validation, and Unseen Benchmark Evaluation", "45"),
    ("4.2", "Experimental Execution Audit Log Across 15 Diverse Benchmark Queries", "48"),
    ("4.3", "Fault Tolerance and Resilient Failover Stress Testing Results", "51")
]

SCREENS_LIST = [
    ("3.1", "Interactive Prompt Routing Playground & Real-Time Request Journey Trace", "37"),
    ("3.2", "System-Wide Operational KPIs & Workload Distribution Analytics", "38"),
    ("3.3", "Financial Impact & Cumulative Savings Trends", "38"),
    ("3.4", "Environmental Carbon Accounting & Live Historical Request Audit Log", "39"),
    ("3.5", "FastAPI Interactive OpenAPI / Swagger Documentation Portal (/docs)", "39"),
    ("3.6", "Swagger Interactive /chat Endpoint Request and Response Schema Specification", "40"),
    ("3.7", "Subsystem Connectivity Diagnostics & Health API Response (/health)", "40")
]

REFERENCES_LIST = [
    "[1] V. Sanh, L. Debut, J. Chaumond, and T. Wolf, \"DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter,\" arXiv preprint arXiv:1910.01108, 2019.",
    "[2] A. S. Luccioni, S. Viguier, and A. Roy, \"Estimating the carbon footprint of BLOOM, a 176B parameter language model,\" Journal of Machine Learning Research, vol. 24, no. 253, pp. 1-25, 2023.",
    "[3] D. Patterson, J. Gonzalez, Q. Le, C. Liang, L.-M. Munguia, D. Rothchild, D. So, M. Texier, and J. Dean, \"Carbon emissions and large neural network training,\" arXiv preprint arXiv:2104.10350, 2021.",
    "[4] Qwen Team, \"Qwen2.5: A Party of Foundation and Instruction-Tuned Models,\" Alibaba Group Technical Report, 2024.",
    "[5] L. Chen, M. Zaharia, and J. Zou, \"FrugalGPT: How to use large language models while reducing cost and improving performance,\" arXiv preprint arXiv:2305.05176, 2023.",
    "[6] I. Ong, A. S. Chen, R. L. Zhang, C. Chen, B. Chen, and M. Zaharia, \"RouteLLM: Learning to Route to Large Language Models,\" arXiv preprint arXiv:2406.18665, 2024.",
    "[7] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, \"Attention is all you need,\" Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 5998-6008, 2017.",
    "[8] V. Schmidt, K. Goyal, A. Joshi, B. Feld, L. Conell, N. Bogunovic, and S. Luccioni, \"CodeCarbon: More robust and actionable carbon emission tracking for machine learning,\" Workshop on Tackling Climate Change with AI, NeurIPS, 2021.",
    "[9] S. Ramirez, \"FastAPI: Modern, fast, web framework for building APIs with Python,\" GitHub repository, 2018.",
    "[10] E. B. Wilson, \"Probable inference, the law of compound probability, and approximate distributions,\" Journal of the American Statistical Association, vol. 22, no. 158, pp. 209-212, 1927."
]
