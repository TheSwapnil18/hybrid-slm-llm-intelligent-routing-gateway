# chapter5.py - Chapter 5: Conclusion & Future Scope, References, and Acknowledgements
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_text_data import REFERENCES_LIST

def build_chapter5_content(doc, add_p, add_h1, add_h2, add_h3):
    # =========================================================
    # CHAPTER 5: CONCLUSION & FUTURE SCOPE
    # =========================================================
    add_h1("CHAPTER 5: CONCLUSION & FUTURE SCOPE")

    # ---------------------------------------------------------
    # 5.1 CONCLUSION
    # ---------------------------------------------------------
    add_h2("5.1 Conclusion")

    p_c1 = (
        "The explosive proliferation of generative artificial intelligence and frontier Large Language Models (LLMs) has "
        "created an unsustainable operational paradox for modern software engineering: while foundation models offer remarkable "
        "reasoning capabilities, their blanket deployment for all user queries introduces excessive financial expenditures, severe "
        "API quota bottlenecks, catastrophic privacy risks, and unacceptable greenhouse gas emissions. This mini-project has successfully "
        "designed, engineered, empirically validated, and deployed the Hybrid SLM-LLM Router Gateway—an intelligent, adaptive middleware "
        "solution that dynamically arbitrates user prompts between compact on-premise Small Language Models (SLMs) and hyperscale cloud LLMs."
    )
    add_p(p_c1)

    p_c2 = (
        "Key engineering achievements and experimental conclusions established by this work include:\n"
        "1. Multi-Tier Intelligent Classification: The project developed, trained, and benchmarked three distinct complexity classifiers. "
        "The TF-IDF with Logistic Regression model emerged as the optimal production engine, achieving a remarkable 95.8% 5-fold cross-validation "
        "accuracy and 93.3% unseen test benchmark accuracy with a sub-millisecond inference latency of just 0.22 ms and a compact 1.4 MB footprint.\n"
        "2. Massive Workload Offloading: Live empirical testing across 35 diverse queries demonstrated that 60.0% of user requests (21/35) "
        "were successfully resolved locally by the Qwen 2.5 7B SLM, reserving premium cloud models strictly for cognitively demanding tasks.\n"
        "3. Decisive Financial Cost Savings: By offloading simpler queries to local on-premise compute, the hybrid architecture reduced total API "
        "expenditures from ₹1.04 (under a 100% cloud baseline) to ₹0.41, delivering a verified 60.6% cost reduction.\n"
        "4. Measurable Carbon Emission Mitigation: Integrated hardware power telemetry via CodeCarbon verified that actual greenhouse gas emissions "
        "totaled 14.8g CO2 equivalent compared to 29.0g under the counterfactual cloud baseline, achieving an outstanding 49.0% environmental carbon reduction.\n"
        "5. Zero-Downtime Resilient Failover: The 3-tier cascade architecture (Groq LPU -> Google Gemini 2.5 Flash -> Local Ollama) demonstrated "
        "100% request completion resilience across simulated HTTP 429 rate limits, server connection errors, and total internet disconnections.\n"
        "6. Enterprise-Ready Observability: An interactive Streamlit analytical dashboard and OpenAPI/Swagger gateway provide real-time request journey "
        "tracing, financial savings tracking, automated SQLite schema persistence, and carbon monitoring."
    )
    add_p(p_c2)

    # Limitations subsection under 5.1
    add_p("Technical Limitations & Operational Constraints", bold=True)

    p_lim1 = (
        "Despite its demonstrated efficacy, several technical limitations were identified during empirical evaluation:\n"
        "• CPU Generation Throughput Constraints: On consumer-grade CPU testbeds lacking dedicated tensor acceleration hardware, local SLM "
        "generation throughput averaged 12.8 tokens per second. While entirely acceptable for concise responses (2-3 seconds), longer generation "
        "prompts require up to 19.5 seconds, which may impact user satisfaction in latency-sensitive workflows.\n"
        "• Single-Turn Complexity Focus: The current classifier evaluates prompt complexity based strictly on the current query text. In multi-turn "
        "conversations spanning lengthy chat histories, accumulated context length can introduce subtle reasoning complexities not captured in a single turn.\n"
        "• Cold-Start Model Latency: In edge environments where system memory is constrained, local SLM models unloaded from RAM incur an initial "
        "cold-start delay of 3 to 5 seconds upon first invocation while GGUF weights are paged into memory."
    )
    add_p(p_lim1)

    # ---------------------------------------------------------
    # 5.2 FUTURE SCOPE
    # ---------------------------------------------------------
    add_h2("5.2 Future Scope")

    p_fut1 = (
        "The architectural foundations established in this project provide numerous promising directions for future research and engineering:\n"
        "1. Hardware Acceleration via Edge NPUs: Porting the local inference engine to leverage dedicated Neural Processing Units (NPUs), "
        "Apple Silicon Metal, or NVIDIA TensorRT-LLM runtimes to boost local generation throughput from 12.8 tokens/sec to over 60 tokens/sec.\n"
        "2. Reinforcement Learning & Contextual Bandits: Upgrading the static threshold classifier to a dynamic Contextual Bandit or Reinforcement "
        "Learning with Human Feedback (RLHF) agent that dynamically learns and adjusts routing thresholds based on live implicit user feedback "
        "(e.g., response regeneration requests, prompt reformulations, and thumbs-up/down ratings).\n"
        "3. Speculative Decoding Integration: Implementing speculative decoding wherein the local SLM generates candidate token drafts that are "
        "verified and accepted in parallel batches by the cloud LLM, slashing cloud generation latency while cutting token billing.\n"
        "4. Multimodal Routing Capabilities: Extending the router to classify and arbitrate multimodal inputs (images, audio, code documents) "
        "between lightweight vision models (e.g., Moondream, Qwen-VL) and multimodal frontier APIs.\n"
        "5. Federated Enterprise Fleet Management: Developing an enterprise telemetry aggregator allowing hundreds of edge router gateways to "
        "synchronize audit metrics, share routing policy weights, and adhere to centralized data governance policies."
    )
    add_p(p_fut1)
    doc.add_page_break()

def build_references_content(doc, add_p, add_h1):
    # =========================================================
    # REFERENCES (IEEE Format - TNR 16 Bold Title)
    # =========================================================
    add_h1("REFERENCES")

    p_ref_intro = (
        "The following peer-reviewed scientific publications, technical whitepapers, and authoritative documentation form the "
        "scholarly foundation of this project:"
    )
    add_p(p_ref_intro, space_after=12)

    for ref in REFERENCES_LIST:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.line_spacing = 1.15
        r = p_ref.add_run(ref)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_page_break()

def build_acknowledgement_content(doc, add_p, add_h1):
    # =========================================================
    # ACKNOWLEDGEMENT
    # =========================================================
    add_h1("ACKNOWLEDGEMENT")

    p_ack1 = (
        "We would like to place on record our deep sense of gratitude to Dr. S. A. Shaikh, Head of the Department of Computer "
        "Science & Engineering (AI&ML), Deogiri Institute of Engineering and Management Studies, Chatrapati Sambhajinagar, for his "
        "generous guidance, administrative encouragement, and invaluable suggestions throughout the development of this project."
    )
    add_p(p_ack1, space_before=10, space_after=10)

    p_ack2 = (
        "We express our profound and sincere gratitude to our esteemed guide, Ms. S. G. Tuppad, Assistant Professor, Department of "
        "CSE (AI&ML), Deogiri Institute of Engineering and Management Studies, Chatrapati Sambhajinagar, for her stimulating guidance, "
        "continuous technical mentorship, constructive criticism, and patient supervision throughout the ideation, implementation, and "
        "evaluation of this work."
    )
    add_p(p_ack2, space_before=6, space_after=10)

    p_ack3 = (
        "We are also immensely thankful to Mrs. P. R. Z. Kathar, Mini Project Coordinator, Department of CSE (AI&ML), for her seamless "
        "coordination, scheduled reviews, and continuous guidance during all phases of the project."
    )
    add_p(p_ack3, space_before=6, space_after=10)

    p_ack4 = (
        "We are extremely thankful to Dr. S. V. Lahane, Director, Deogiri Institute of Engineering and Management Studies, Chatrapati "
        "Sambhajinagar, for providing the state-of-the-art infrastructural facilities, computational laboratories, and academic ecosystem "
        "without which this work would not have been possible."
    )
    add_p(p_ack4, space_before=6, space_after=10)

    p_ack5 = (
        "Finally, we extend our heartfelt appreciation to all faculty members, technical laboratory assistants, our dear parents, and "
        "fellow student colleagues for their unwavering moral support, helpful discussions, and encouragement throughout this endeavor."
    )
    add_p(p_ack5, space_before=6, space_after=30)

    # Signatures
    add_p("Shaurya Anand Kamble (AI4173)", bold=True, size=12, space_before=20, space_after=2)
    add_p("Swapnil Kashinath Kolte (AI4175)", bold=True, size=12, space_before=0, space_after=10)
    add_p("B.Tech CSE (Artificial Intelligence & Machine Learning)\nDeogiri Institute of Engineering and Management Studies, Chatrapati Sambhajinagar", 
          italic=True, size=11, space_before=0, space_after=0)

def build_chapter5(doc, add_p, add_h1, add_h2, add_h3, format_styled_table=None):
    build_chapter5_content(doc, add_p, add_h1, add_h2, add_h3)
    build_references_content(doc, add_p, add_h1)
    build_acknowledgement_content(doc, add_p, add_h1)
    print("Chapter 5, References, and Acknowledgements built successfully.")
