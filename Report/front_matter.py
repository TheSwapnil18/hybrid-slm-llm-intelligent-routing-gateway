# front_matter.py - Generates Cover, Inner Title, Certificate, Declaration, Abstract, and Lists
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_text_data import ABBREVIATIONS, FIGURES_LIST, GRAPHS_LIST, TABLES_LIST, SCREENS_LIST

def build_front_matter(doc, add_p, add_h1, add_image_centered, format_simple_table):
    logo_path = r"Report\extracted_images\image1.png"
    
    # =========================================================
    # 1. OUTER COVER PAGE (Entire Page - Center Alignment)
    # =========================================================
    add_p("Marathwada Shikshan Prasarak Mandal’s", align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_before=10, space_after=2)
    add_p("Deogiri Institute of Engineering and Management Studies,\nChatrapati Sambhajinagar", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=15)
    
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(5)
        p_logo.paragraph_format.space_after = Pt(15)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(1.3))
        
    add_p("Mini Project Report", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, space_before=5, space_after=2)
    add_p("on", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=2, space_after=12)
    add_p("Hybrid SLM-LLM Router Agent", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=18, space_before=0, space_after=20)
    
    add_p("Submitted By", align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_before=10, space_after=8)
    add_p("Shaurya Anand Kamble (AI4173)\nSwapnil Kashinath Kolte (AI4175)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=25)
    
    add_p("Dr. Babasaheb Ambedkar Technological University\nLonere (M.S.)", align=WD_ALIGN_PARAGRAPH.CENTER, size=14, space_before=15, space_after=20)
    
    add_p("Department of CSE (AI&ML)", align=WD_ALIGN_PARAGRAPH.CENTER, size=16, bold=True, space_before=10, space_after=2)
    add_p("Deogiri Institute of Engineering and Management Studies,\nChatrapati Sambhajinagar", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=4)
    add_p("(2026- 2027)", align=WD_ALIGN_PARAGRAPH.CENTER, size=16, bold=True, space_before=0, space_after=0)
    
    doc.add_page_break()

    # =========================================================
    # 2. INNER TITLE PAGE
    # =========================================================
    add_p("Marathwada Shikshan Prasarak Mandal’s", align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_before=10, space_after=2)
    add_p("Deogiri Institute of Engineering and Management Studies,\nChatrapati Sambhajinagar", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=15)
    
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(5)
        p_logo.paragraph_format.space_after = Pt(12)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(1.2))
        
    add_p("Mini Project Report", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=4, space_after=2)
    add_p("on", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=2, space_after=10)
    add_p("Hybrid SLM-LLM Router Agent", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=18, space_before=0, space_after=15)
    
    add_p("Submitted By", align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_before=6, space_after=6)
    add_p("Shaurya Anand Kamble (AI4173)\nSwapnil Kashinath Kolte (AI4175)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=15)
    
    add_p("In partial fulfillment of", align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_before=6, space_after=2)
    add_p("Bachelor of Technology", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=2)
    add_p("(Computer Science & Engineering (AI&ML))", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=0, space_after=15)
    
    add_p("Guided By", align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_before=6, space_after=4)
    add_p("Ms. S. G. Tuppad", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=20)
    
    add_p("Department of CSE (AI&ML)", align=WD_ALIGN_PARAGRAPH.CENTER, size=16, bold=True, space_before=10, space_after=2)
    add_p("Deogiri Institute of Engineering and Management Studies,\nChatrapati Sambhajinagar", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=4)
    add_p("(2026- 2027)", align=WD_ALIGN_PARAGRAPH.CENTER, size=16, bold=True, space_before=0, space_after=0)

    doc.add_page_break()

    # =========================================================
    # 3. CERTIFICATE PAGE
    # =========================================================
    add_p("CERTIFICATE", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=20, space_after=20)
    
    cert_text = (
        "This is to certify that, the Mini Project entitled “Hybrid SLM-LLM Router Agent” submitted by "
        "Shaurya Anand Kamble (AI4173), Swapnil Kashinath Kolte (AI4175) is a bonafide work completed under "
        "my supervision and guidance in partial fulfillment for award of Bachelor of Technology (CSE (AI&ML)) "
        "Degree of Dr. Babasaheb Ambedkar Technological University, Lonere."
    )
    add_p(cert_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_before=10, space_after=30)
    
    add_p("Date: 17/10/2026                                              Place: Chatrapati Sambhajinagar", align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_before=10, space_after=40)
    
    tbl_cert = doc.add_table(rows=1, cols=2)
    tbl_cert.rows[0].cells[0].paragraphs[0].text = "Ms. S. G. Tuppad\nMini Project Guide"
    tbl_cert.rows[0].cells[1].paragraphs[0].text = "Mrs. P. R. Z. Kathar\nMini Project Coordinator"
    tbl_cert.rows[0].cells[0].paragraphs[0].runs[0].bold = True
    tbl_cert.rows[0].cells[1].paragraphs[0].runs[0].bold = True
    tbl_cert.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    format_simple_table(tbl_cert, col_widths=[3.0, 3.2])

    add_p("", space_before=30, space_after=0)
    add_p("Dr. S. A. Shaikh\nHead of Department", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=12, space_before=15, space_after=0)

    doc.add_page_break()

    # =========================================================
    # 4. DECLARATION PAGE
    # =========================================================
    add_p("DECLARATION", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=20, space_after=20)
    
    decl_text = (
        "This is to certify that, the partial Mini Project report entitled “Hybrid SLM-LLM Router Agent” "
        "submitted by Shaurya Anand Kamble, Swapnil Kashinath Kolte is a bonafide work completed under my "
        "supervision and guidance in partial fulfillment for award of bachelor’s degree in CSE (AI&ML) of "
        "Deogiri Institute of Engineering and Management Studies, Chatrapati Sambhajinagar under "
        "Dr. Babasaheb Ambedkar Technological University, Lonere."
    )
    add_p(decl_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_before=10, space_after=30)
    
    add_p("Place: Chatrapati Sambhajinagar\nDate: 17/10/2026", align=WD_ALIGN_PARAGRAPH.LEFT, size=12, space_before=10, space_after=40)
    
    tbl_decl = doc.add_table(rows=1, cols=2)
    tbl_decl.rows[0].cells[0].paragraphs[0].text = "External Examiner"
    tbl_decl.rows[0].cells[1].paragraphs[0].text = "Ms. S. G. Tuppad\nGuide"
    tbl_decl.rows[0].cells[0].paragraphs[0].runs[0].bold = True
    tbl_decl.rows[0].cells[1].paragraphs[0].runs[0].bold = True
    tbl_decl.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    format_simple_table(tbl_decl, col_widths=[3.0, 3.2])

    doc.add_page_break()

    # =========================================================
    # 5. ABSTRACT PAGE
    # =========================================================
    add_p("Abstract", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=15, space_after=18)
    
    p1 = (
        "Large Language Models (LLMs) have established extraordinary capabilities across natural language understanding, "
        "automated multi-step reasoning, mathematical problem-solving, and code synthesis. However, monolithic enterprise "
        "architectures that unconditionally route 100% of incoming user prompts to proprietary cloud-hosted frontier LLMs "
        "(such as OpenAI GPT-4, Google Gemini, or Claude 3.5) incur substantial operational penalties: compounding token-based "
        "API expenditures, high and unpredictable network latency, vulnerability to external service rate-limiting (HTTP 429), "
        "and significant avoidable carbon dioxide emissions generated by hyperscale data center compute clusters."
    )
    add_p(p1, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_after=10)

    p2 = (
        "Conversely, recent advancements in parameter quantization (GGUF 4-bit) and architecture design have produced highly "
        "capable Small Language Models (SLMs)—such as Alibaba’s Qwen2.5-7B Instruct—capable of running locally on consumer "
        "hardware at zero marginal token cost. Nevertheless, an SLM alone cannot reliably resolve advanced mathematical derivations, "
        "complex distributed software architectures, or deep multi-turn theoretical analysis. To address this fundamental tradeoff, "
        "this project develops the Hybrid SLM-LLM Router Agent: an intelligent, low-latency, resilient middleware gateway "
        "that dynamically evaluates incoming prompt complexity and directs traffic to the most cost-effective and environmentally "
        "conscious compute tier."
    )
    add_p(p2, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_after=10)

    p3 = (
        "The engineered architecture integrates three modular components: (1) an ultra-low latency Complexity Classifier "
        "benchmarking deterministic heuristics, classical TF-IDF vectorization with Logistic Regression, and a fine-tuned "
        "DistilBERT sequence classification model; (2) an asynchronous dual-path execution engine orchestrated via FastAPI "
        "providing automated failover between primary cloud provider Groq (Qwen2.5-72B), secondary cloud provider Google Gemini 2.5 Flash, "
        "and local Ollama inference; and (3) a live telemetry and environmental auditing suite integrating CodeCarbon to track "
        "physical CPU/GPU energy consumption (kWh) alongside a 16-column SQLite persistent audit database."
    )
    add_p(p3, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_after=10)

    p4 = (
        "Experimental benchmarking across 35 diverse test prompts demonstrated that the TF-IDF classifier achieved 93.3% accuracy "
        "with an inference latency of just 0.22 milliseconds, while fine-tuned DistilBERT reached 96.7% accuracy. By successfully "
        "offloading 60.0% of user queries to the local SLM, the hybrid system slashed cumulative cloud API costs by 60.6% and curtailed "
        "carbon emissions by 49.0% compared to a 100% cloud baseline, while delivering 100% availability during simulated network outages. "
        "An interactive Streamlit dashboard enables real-time journey visualization, performance telemetry, and system administration."
    )
    add_p(p4, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_after=15)

    doc.add_page_break()

    # =========================================================
    # 6. TABLE OF CONTENTS
    # =========================================================
    add_p("Contents", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=15, space_after=15)
    
    toc_items = [
        ("List of Abbreviations", "i"),
        ("List of Figures", "ii"),
        ("List of Graphs", "iii"),
        ("List of Tables", "iv"),
        ("List of Screens", "v"),
        ("CHAPTER 1: INTRODUCTION", "1"),
        ("    1.1 Introduction", "1"),
        ("    1.2 Necessity", "2"),
        ("    1.3 Objectives", "3"),
        ("    1.4 Theme of the Mini Project", "4"),
        ("    1.5 Proposed System Architecture", "5"),
        ("CHAPTER 2: LITERATURE SURVEY", "7"),
        ("    2.1 Adaptive SLM–LLM Routing for Agentic AI Systems", "7"),
        ("    2.2 HERA: Hybrid Edge-Cloud Resource Allocation", "8"),
        ("    2.3 Survey on Collaborating Small and Large Language Models", "9"),
        ("    2.4 Collaborative Mechanisms Between LLMs and SLMs", "10"),
        ("    2.5 Dynamic LLM Cascades and Frugal Inference Paradigms", "11"),
        ("    2.6 Green AI and Data Center Carbon Accounting Telemetry", "12"),
        ("    2.7 Knowledge Distillation & Transformer Compression (DistilBERT)", "13"),
        ("    2.8 Comparative Literature Analysis & Synthesis Matrix", "14"),
        ("    2.9 Research Gap & Problem Formulation", "15"),
        ("CHAPTER 3: SYSTEM DEVELOPMENT", "16"),
        ("    3.1 Requirement Specification", "16"),
        ("        3.1.1 Hardware Requirements", "16"),
        ("        3.1.2 Software Requirements & Technology Stack", "17"),
        ("        3.1.3 Functional Requirements (FR1 to FR10)", "18"),
        ("        3.1.4 Non-Functional Requirements (NFR1 to NFR8)", "19"),
        ("        3.1.5 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)", "20"),
        ("        3.1.6 Specification Document & UML Diagrams of all Modules", "24"),
        ("    3.2 User Interface Design", "38"),
        ("    3.3 Database Design / ER Diagrams", "40"),
        ("CHAPTER 4: PERFORMANCE EVALUATION", "44"),
        ("    4.1 Experimental Setup & Evaluation Methodology", "44"),
        ("    4.2 Classifier Benchmarking & Comparative Accuracy Analysis", "45"),
        ("    4.3 Routing Offload Distribution & Workload Division", "46"),
        ("    4.4 End-to-End Latency & Response Time Evaluation", "47"),
        ("    4.5 Economic & Financial Cost Reduction Analysis", "48"),
        ("    4.6 Sustainability & Carbon Emission Reduction Evaluation", "50"),
        ("    4.7 Resilient Fallback & Fault Tolerance Stress Testing", "51"),
        ("    4.8 Critical Error Analysis, Limitations & Brevity Bias Study", "52"),
        ("CHAPTER 5: CONCLUSION & FUTURE SCOPE", "54"),
        ("    5.1 Conclusion", "54"),
        ("    5.2 Future Scope", "55"),
        ("REFERENCES", "56"),
        ("ACKNOWLEDGEMENT", "58")
    ]

    for title, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        
        is_ch = title.startswith("CHAPTER") or title in ["REFERENCES", "ACKNOWLEDGEMENT"] or title.startswith("List")
        r_title = p.add_run(title)
        r_title.bold = is_ch
        r_title.font.name = 'Times New Roman'
        r_title.font.size = Pt(11.5 if is_ch else 11)
        
        # Dots
        dots_len = max(5, 75 - len(title))
        r_dots = p.add_run(" " + ". " * (dots_len // 2) + " ")
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        
        r_page = p.add_run(page)
        r_page.bold = is_ch
        r_page.font.name = 'Times New Roman'
        r_page.font.size = Pt(11.5 if is_ch else 11)

    doc.add_page_break()

    # =========================================================
    # 7. LIST OF ABBREVIATIONS
    # =========================================================
    add_p("List of Abbreviations", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=15, space_after=15)
    tbl_abbr = doc.add_table(rows=len(ABBREVIATIONS) + 1, cols=3)
    tbl_abbr.rows[0].cells[0].paragraphs[0].text = "Sr. No."
    tbl_abbr.rows[0].cells[1].paragraphs[0].text = "Acronym"
    tbl_abbr.rows[0].cells[2].paragraphs[0].text = "Abbreviation / Definition"
    for idx, (sr, acr, desc) in enumerate(ABBREVIATIONS, start=1):
        tbl_abbr.rows[idx].cells[0].paragraphs[0].text = sr
        tbl_abbr.rows[idx].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tbl_abbr.rows[idx].cells[1].paragraphs[0].text = acr
        tbl_abbr.rows[idx].cells[1].paragraphs[0].runs[0].bold = True
        tbl_abbr.rows[idx].cells[2].paragraphs[0].text = desc
    format_simple_table(tbl_abbr, col_widths=[0.8, 1.4, 4.0])

    doc.add_page_break()

    # =========================================================
    # 8. LIST OF FIGURES
    # =========================================================
    add_p("List of Figures", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=15, space_after=15)
    tbl_fig = doc.add_table(rows=len(FIGURES_LIST) + 1, cols=3)
    tbl_fig.rows[0].cells[0].paragraphs[0].text = "Figure No."
    tbl_fig.rows[0].cells[1].paragraphs[0].text = "Illustration Description"
    tbl_fig.rows[0].cells[2].paragraphs[0].text = "Page No."
    for idx, (fno, fdesc, fpage) in enumerate(FIGURES_LIST, start=1):
        tbl_fig.rows[idx].cells[0].paragraphs[0].text = fno
        tbl_fig.rows[idx].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tbl_fig.rows[idx].cells[1].paragraphs[0].text = fdesc
        tbl_fig.rows[idx].cells[2].paragraphs[0].text = fpage
        tbl_fig.rows[idx].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_simple_table(tbl_fig, col_widths=[1.1, 4.2, 0.9])

    doc.add_page_break()

    # =========================================================
    # 9. LIST OF GRAPHS
    # =========================================================
    add_p("List of Graphs", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=15, space_after=15)
    tbl_grp = doc.add_table(rows=len(GRAPHS_LIST) + 1, cols=3)
    tbl_grp.rows[0].cells[0].paragraphs[0].text = "Graph No."
    tbl_grp.rows[0].cells[1].paragraphs[0].text = "Illustration Description"
    tbl_grp.rows[0].cells[2].paragraphs[0].text = "Page No."
    for idx, (gno, gdesc, gpage) in enumerate(GRAPHS_LIST, start=1):
        tbl_grp.rows[idx].cells[0].paragraphs[0].text = gno
        tbl_grp.rows[idx].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tbl_grp.rows[idx].cells[1].paragraphs[0].text = gdesc
        tbl_grp.rows[idx].cells[2].paragraphs[0].text = gpage
        tbl_grp.rows[idx].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_simple_table(tbl_grp, col_widths=[1.1, 4.2, 0.9])

    doc.add_page_break()

    # =========================================================
    # 10. LIST OF TABLES
    # =========================================================
    add_p("List of Tables", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=15, space_after=15)
    tbl_tbl = doc.add_table(rows=len(TABLES_LIST) + 1, cols=3)
    tbl_tbl.rows[0].cells[0].paragraphs[0].text = "Table No."
    tbl_tbl.rows[0].cells[1].paragraphs[0].text = "Illustration Description"
    tbl_tbl.rows[0].cells[2].paragraphs[0].text = "Page No."
    for idx, (tno, tdesc, tpage) in enumerate(TABLES_LIST, start=1):
        tbl_tbl.rows[idx].cells[0].paragraphs[0].text = tno
        tbl_tbl.rows[idx].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tbl_tbl.rows[idx].cells[1].paragraphs[0].text = tdesc
        tbl_tbl.rows[idx].cells[2].paragraphs[0].text = tpage
        tbl_tbl.rows[idx].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_simple_table(tbl_tbl, col_widths=[1.1, 4.2, 0.9])

    doc.add_page_break()

    # =========================================================
    # 11. LIST OF SCREENS
    # =========================================================
    add_p("List of Screens", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=15, space_after=15)
    tbl_scr = doc.add_table(rows=len(SCREENS_LIST) + 1, cols=3)
    tbl_scr.rows[0].cells[0].paragraphs[0].text = "Screen No."
    tbl_scr.rows[0].cells[1].paragraphs[0].text = "Illustration Description"
    tbl_scr.rows[0].cells[2].paragraphs[0].text = "Page No."
    for idx, (sno, sdesc, spage) in enumerate(SCREENS_LIST, start=1):
        tbl_scr.rows[idx].cells[0].paragraphs[0].text = sno
        tbl_scr.rows[idx].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tbl_scr.rows[idx].cells[1].paragraphs[0].text = sdesc
        tbl_scr.rows[idx].cells[2].paragraphs[0].text = spage
        tbl_scr.rows[idx].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_simple_table(tbl_scr, col_widths=[1.1, 4.2, 0.9])

    doc.add_page_break()
    print("Front matter generated successfully.")
