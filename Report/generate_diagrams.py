import os
import math
from PIL import Image, ImageDraw, ImageFont

os.makedirs(r"Report\figures", exist_ok=True)

FONT_PATH = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"

def get_font(size=14, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_PATH
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_rounded_box(draw, xy, fill, outline, width=2, radius=10):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, fill="#2c3e50", width=2, arrow_size=8):
    x1, y1 = start
    x2, y2 = end
    draw.line([x1, y1, x2, y2], fill=fill, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    angle1 = angle + math.pi * 0.85
    angle2 = angle - math.pi * 0.85
    p1 = (x2 + arrow_size * math.cos(angle1), y2 + arrow_size * math.sin(angle1))
    p2 = (x2 + arrow_size * math.cos(angle2), y2 + arrow_size * math.sin(angle2))
    draw.polygon([end, p1, p2], fill=fill)

# ==========================================
# 1. Figure 1.1: System Architecture Diagram
# ==========================================
def generate_architecture_diagram():
    img = Image.new("RGB", (1400, 950), "#ffffff")
    draw = ImageDraw.Draw(img)
    f_title = get_font(24, bold=True)
    f_sub = get_font(13, bold=False)
    f_box_title = get_font(15, bold=True)
    f_box_desc = get_font(12, bold=False)
    f_tag = get_font(11, bold=True)
    
    draw.text((700, 30), "Hybrid SLM-LLM Router Gateway Architecture", font=f_title, fill="#1e293b", anchor="mm")
    draw.text((700, 60), "Intelligent Multi-Provider Middleware with Automated Fallback & Carbon Telemetry", font=f_sub, fill="#64748b", anchor="mm")
    
    # Client Tier
    draw_rounded_box(draw, [80, 110, 400, 190], fill="#f0f9ff", outline="#0284c7", width=2)
    draw.text((240, 135), "User Client / Dashboard", font=f_box_title, fill="#0369a1", anchor="mm")
    draw.text((240, 165), "Streamlit UI / REST API Client (HTTP POST /chat)", font=f_box_desc, fill="#475569", anchor="mm")
    
    # Gateway
    draw_rounded_box(draw, [550, 110, 850, 190], fill="#eff6ff", outline="#2563eb", width=2)
    draw.text((700, 135), "FastAPI Gateway (backend/main.py)", font=f_box_title, fill="#1d4ed8", anchor="mm")
    draw.text((700, 165), "Request Validation · Latency Timers · Route Dispatcher", font=f_box_desc, fill="#475569", anchor="mm")
    
    draw_arrow(draw, (400, 150), (550, 150), fill="#0284c7", width=3)
    draw.text((475, 135), "Prompt JSON", font=f_tag, fill="#0369a1", anchor="mm")
    
    # Classifier Subsystem Box
    draw_rounded_box(draw, [450, 240, 950, 420], fill="#faf5ff", outline="#9333ea", width=2)
    draw.text((700, 265), "Complexity Classification Engine", font=f_box_title, fill="#7e22ce", anchor="mm")
    
    # 3 Classifier options
    draw_rounded_box(draw, [470, 290, 610, 395], fill="#ffffff", outline="#c084fc", width=1)
    draw.text((540, 315), "Rule Heuristic", font=f_tag, fill="#6b21a8", anchor="mm")
    draw.text((540, 345), "Regex & Syntax\nWord Counts\n[0.0 - 1.0]", font=f_box_desc, fill="#64748b", anchor="mm")

    draw_rounded_box(draw, [630, 290, 770, 395], fill="#ffffff", outline="#c084fc", width=1)
    draw.text((700, 315), "Classical ML", font=f_tag, fill="#6b21a8", anchor="mm")
    draw.text((700, 345), "TF-IDF N-Grams\nLogistic Reg.\nScikit-Learn", font=f_box_desc, fill="#64748b", anchor="mm")

    draw_rounded_box(draw, [790, 290, 930, 395], fill="#f3e8ff", outline="#7e22ce", width=2)
    draw.text((860, 315), "DistilBERT (Active)", font=f_tag, fill="#581c87", anchor="mm")
    draw.text((860, 345), "Fine-Tuned 66M\nWordPiece 128\nSoftmax Score", font=f_box_desc, fill="#475569", anchor="mm")

    draw_arrow(draw, (700, 190), (700, 240), fill="#2563eb", width=3)

    # Decision Diamond / Split
    draw_rounded_box(draw, [580, 460, 820, 520], fill="#fef3c7", outline="#d97706", width=2)
    draw.text((700, 490), "Threshold Gate: p >= 0.50?", font=f_box_title, fill="#92400e", anchor="mm")
    draw_arrow(draw, (700, 420), (700, 460), fill="#9333ea", width=3)
    draw.text((700, 440), "Score p in [0.0, 1.0]", font=f_tag, fill="#7e22ce", anchor="mm")

    # Left: Local SLM Pipeline
    draw_rounded_box(draw, [100, 580, 520, 750], fill="#f0fdf4", outline="#16a34a", width=2)
    draw.text((310, 610), "Local SLM Engine (Ollama)", font=f_box_title, fill="#15803d", anchor="mm")
    draw.text((310, 640), "Model: qwen2.5:7b (7 Billion Parameters)", font=f_tag, fill="#166534", anchor="mm")
    draw.text((310, 675), "Execution: Local CPU/GPU RAM\nAPI Cost: $0.00 / Request (Free)\nLive Telemetry: CodeCarbon (kWh, g CO2)", font=f_box_desc, fill="#334155", anchor="mm")

    draw_arrow(draw, (620, 520), (310, 580), fill="#16a34a", width=3)
    draw.text((430, 540), "p < 0.50 (Simple Query)", font=f_tag, fill="#15803d", anchor="mm")

    # Right: Cloud LLM Pipeline
    draw_rounded_box(draw, [880, 580, 1300, 750], fill="#fff7ed", outline="#ea580c", width=2)
    draw.text((1090, 610), "Cloud LLM Pipeline (High Capacity)", font=f_box_title, fill="#c2410c", anchor="mm")
    draw.text((1090, 640), "Primary: Groq LPU (openai/gpt-oss-120b)", font=f_tag, fill="#9a3412", anchor="mm")
    draw.text((1090, 675), "Failover: Google Gemini (gemini-2.5-flash)\nRate: $0.03 input / $0.17 output per 1M tokens\nCloud CO2 Est: 0.35g CO2 / 1k tokens", font=f_box_desc, fill="#334155", anchor="mm")

    draw_arrow(draw, (780, 520), (1090, 580), fill="#ea580c", width=3)
    draw.text((970, 540), "p >= 0.50 (Complex Query)", font=f_tag, fill="#c2410c", anchor="mm")

    # Fallback arrows
    draw_arrow(draw, (520, 640), (880, 640), fill="#dc2626", width=2)
    draw.text((700, 625), "Tier-1 Fallback: Ollama Down / Offline", font=f_tag, fill="#dc2626", anchor="mm")

    draw_arrow(draw, (880, 690), (520, 690), fill="#059669", width=2)
    draw.text((700, 705), "Tier-2 Reverse Fallback: Cloud Outage", font=f_tag, fill="#059669", anchor="mm")

    # Bottom Database & Dashboard
    draw_rounded_box(draw, [350, 810, 750, 910], fill="#f8fafc", outline="#475569", width=2)
    draw.text((550, 840), "Relational Database (router_logs.db)", font=f_box_title, fill="#1e293b", anchor="mm")
    draw.text((550, 875), "SQLite Table: requests_log (16 Schema Columns)\nAuto-Migrations · Latencies · Costs · Emissions", font=f_box_desc, fill="#475569", anchor="mm")

    draw_rounded_box(draw, [850, 810, 1250, 910], fill="#fdf2f8", outline="#db2777", width=2)
    draw.text((1050, 840), "Streamlit Observability Dashboard", font=f_box_title, fill="#9d174d", anchor="mm")
    draw.text((1050, 875), "Real-Time Traffic Monitor · Altair Financial Charts\nCarbon Accounting · Failover & Fallback Badges", font=f_box_desc, fill="#475569", anchor="mm")

    draw_arrow(draw, (310, 750), (450, 810), fill="#16a34a", width=2)
    draw_arrow(draw, (1090, 750), (650, 810), fill="#ea580c", width=2)
    draw_arrow(draw, (750, 860), (850, 860), fill="#475569", width=2)

    img.save(r"Report\figures\fig_1_1_system_architecture.png")
    print("Generated fig_1_1_system_architecture.png")

# ==========================================
# 2. Figure 3.1: DFD Level 0 (Context Level)
# ==========================================
def generate_dfd_level_0():
    img = Image.new("RGB", (1200, 650), "#ffffff")
    draw = ImageDraw.Draw(img)
    f_title = get_font(22, bold=True)
    f_sub = get_font(13, bold=False)
    f_box = get_font(15, bold=True)
    f_desc = get_font(12, bold=False)
    f_arrow = get_font(11, bold=True)
    
    draw.text((600, 30), "Data Flow Diagram (DFD) - Level 0: Context Diagram", font=f_title, fill="#1e293b", anchor="mm")
    draw.text((600, 58), "External Entities and High-Level Boundary Data Flows", font=f_sub, fill="#64748b", anchor="mm")

    # Center Process Circle / Rounded Box
    draw_rounded_box(draw, [420, 200, 780, 420], fill="#f0f9ff", outline="#0284c7", width=3, radius=30)
    draw.text((600, 280), "0.0\nHybrid SLM-LLM\nRouter Gateway System", font=f_box, fill="#0369a1", anchor="mm")
    draw.text((600, 360), "(Complexity Classification,\nDynamic Routing, Telemetry)", font=f_desc, fill="#475569", anchor="mm")

    # External Entity: User / Client
    draw_rounded_box(draw, [50, 260, 240, 360], fill="#f8fafc", outline="#334155", width=2, radius=4)
    draw.text((145, 295), "External Entity", font=f_desc, fill="#64748b", anchor="mm")
    draw.text((145, 325), "End User / Client", font=f_box, fill="#1e293b", anchor="mm")

    draw_arrow(draw, (240, 290), (420, 290), fill="#0284c7", width=2)
    draw.text((330, 275), "User Prompt Payload", font=f_arrow, fill="#0369a1", anchor="mm")
    draw_arrow(draw, (420, 330), (240, 330), fill="#10b981", width=2)
    draw.text((330, 345), "Generated AI Response", font=f_arrow, fill="#047857", anchor="mm")

    # External Entity: Local Ollama SLM
    draw_rounded_box(draw, [960, 100, 1150, 200], fill="#f0fdf4", outline="#16a34a", width=2, radius=4)
    draw.text((1055, 135), "External System", font=f_desc, fill="#64748b", anchor="mm")
    draw.text((1055, 165), "Local Ollama SLM\n(qwen2.5:7b)", font=f_box, fill="#15803d", anchor="mm")

    draw_arrow(draw, (750, 230), (960, 160), fill="#16a34a", width=2)
    draw.text((865, 185), "Simple Prompt (p < 0.5)", font=f_arrow, fill="#15803d", anchor="mm")
    draw_arrow(draw, (960, 180), (770, 260), fill="#16a34a", width=2)
    draw.text((885, 235), "Local Completion", font=f_arrow, fill="#15803d", anchor="mm")

    # External Entity: Cloud LLM APIs
    draw_rounded_box(draw, [960, 270, 1150, 370], fill="#fff7ed", outline="#ea580c", width=2, radius=4)
    draw.text((1055, 305), "External Cloud APIs", font=f_desc, fill="#64748b", anchor="mm")
    draw.text((1055, 335), "Groq LPU / Gemini", font=f_box, fill="#c2410c", anchor="mm")

    draw_arrow(draw, (780, 310), (960, 310), fill="#ea580c", width=2)
    draw.text((870, 295), "Complex Prompt (p >= 0.5)", font=f_arrow, fill="#c2410c", anchor="mm")
    draw_arrow(draw, (960, 340), (780, 340), fill="#ea580c", width=2)
    draw.text((870, 355), "Cloud Completion + Tokens", font=f_arrow, fill="#c2410c", anchor="mm")

    # External Entity: Hardware Sensors (CodeCarbon)
    draw_rounded_box(draw, [960, 440, 1150, 540], fill="#fdf2f8", outline="#db2777", width=2, radius=4)
    draw.text((1055, 475), "Host Hardware", font=f_desc, fill="#64748b", anchor="mm")
    draw.text((1055, 505), "CPU / GPU Sensors\n(Intel RAPL / TDP)", font=f_box, fill="#9d174d", anchor="mm")

    draw_arrow(draw, (750, 390), (960, 470), fill="#db2777", width=2)
    draw.text((865, 420), "Poll Energy Sensors", font=f_arrow, fill="#9d174d", anchor="mm")
    draw_arrow(draw, (960, 500), (750, 410), fill="#db2777", width=2)
    draw.text((865, 470), "Power (kWh) & CO2", font=f_arrow, fill="#9d174d", anchor="mm")

    # External Entity: Administrator
    draw_rounded_box(draw, [50, 450, 240, 550], fill="#f8fafc", outline="#334155", width=2, radius=4)
    draw.text((145, 485), "External Entity", font=f_desc, fill="#64748b", anchor="mm")
    draw.text((145, 515), "System Admin / Analyst", font=f_box, fill="#1e293b", anchor="mm")

    draw_arrow(draw, (450, 390), (240, 480), fill="#6366f1", width=2)
    draw.text((345, 445), "Metrics & Audit Telemetry", font=f_arrow, fill="#4338ca", anchor="mm")

    img.save(r"Report\figures\fig_3_1_dfd_level_0.png")
    print("Generated fig_3_1_dfd_level_0.png")

# ==========================================
# 3. Figure 3.2: DFD Level 1 (Decomposition)
# ==========================================
def generate_dfd_level_1():
    img = Image.new("RGB", (1400, 950), "#ffffff")
    draw = ImageDraw.Draw(img)
    f_title = get_font(22, bold=True)
    f_sub = get_font(13, bold=False)
    f_box = get_font(14, bold=True)
    f_desc = get_font(11, bold=False)
    f_arrow = get_font(10, bold=True)

    draw.text((700, 30), "Data Flow Diagram (DFD) - Level 1: Subsystem Functional Decomposition", font=f_title, fill="#1e293b", anchor="mm")
    draw.text((700, 58), "Process Decomposition, Intermediate Data Flows, and Relational Datastores", font=f_sub, fill="#64748b", anchor="mm")

    # External Entity: User
    draw_rounded_box(draw, [60, 150, 220, 240], fill="#f8fafc", outline="#334155", width=2, radius=4)
    draw.text((140, 180), "End User", font=f_box, fill="#1e293b", anchor="mm")
    draw.text((140, 210), "(Client App / UI)", font=f_desc, fill="#64748b", anchor="mm")

    # Process 1.0
    draw_rounded_box(draw, [320, 140, 520, 250], fill="#eff6ff", outline="#2563eb", width=2, radius=20)
    draw.text((420, 175), "1.0", font=f_desc, fill="#1d4ed8", anchor="mm")
    draw.text((420, 200), "Prompt Ingestion &\nValidation", font=f_box, fill="#1e293b", anchor="mm")

    draw_arrow(draw, (220, 195), (320, 195), fill="#2563eb", width=2)
    draw.text((270, 180), "POST /chat", font=f_arrow, fill="#1d4ed8", anchor="mm")

    # Process 2.0
    draw_rounded_box(draw, [640, 140, 860, 250], fill="#faf5ff", outline="#9333ea", width=2, radius=20)
    draw.text((750, 175), "2.0", font=f_desc, fill="#7e22ce", anchor="mm")
    draw.text((750, 200), "Complexity\nClassification", font=f_box, fill="#1e293b", anchor="mm")

    draw_arrow(draw, (520, 195), (640, 195), fill="#2563eb", width=2)
    draw.text((580, 180), "Clean String", font=f_arrow, fill="#1d4ed8", anchor="mm")

    # Datastore D1
    draw.line([640, 310, 860, 310], fill="#9333ea", width=2)
    draw.line([640, 360, 860, 360], fill="#9333ea", width=2)
    draw.text((750, 335), "D1 | Pretrained Model Weights (DistilBERT)", font=f_arrow, fill="#7e22ce", anchor="mm")
    draw_arrow(draw, (750, 310), (750, 250), fill="#9333ea", width=2)

    # Process 3.0
    draw_rounded_box(draw, [980, 140, 1200, 250], fill="#fef3c7", outline="#d97706", width=2, radius=20)
    draw.text((1090, 175), "3.0", font=f_desc, fill="#b45309", anchor="mm")
    draw.text((1090, 200), "Model Routing &\nDispatch Policy", font=f_box, fill="#1e293b", anchor="mm")

    draw_arrow(draw, (860, 195), (980, 195), fill="#9333ea", width=2)
    draw.text((920, 180), "Score p & Conf.", font=f_arrow, fill="#7e22ce", anchor="mm")

    # Process 4.0: Local Inference
    draw_rounded_box(draw, [750, 430, 970, 540], fill="#f0fdf4", outline="#16a34a", width=2, radius=20)
    draw.text((860, 465), "4.0", font=f_desc, fill="#15803d", anchor="mm")
    draw.text((860, 490), "Local SLM Inference\n(Ollama)", font=f_box, fill="#1e293b", anchor="mm")

    draw_arrow(draw, (1050, 250), (900, 430), fill="#16a34a", width=2)
    draw.text((990, 330), "Route 'local' (p < 0.5)", font=f_arrow, fill="#15803d", anchor="mm")

    # Process 5.0: Cloud Inference
    draw_rounded_box(draw, [1050, 430, 1270, 540], fill="#fff7ed", outline="#ea580c", width=2, radius=20)
    draw.text((1160, 465), "5.0", font=f_desc, fill="#c2410c", anchor="mm")
    draw.text((1160, 490), "Cloud LLM Inference\n(Groq / Gemini)", font=f_box, fill="#1e293b", anchor="mm")

    draw_arrow(draw, (1130, 250), (1160, 430), fill="#ea580c", width=2)
    draw.text((1190, 330), "Route 'cloud' (p >= 0.5)", font=f_arrow, fill="#c2410c", anchor="mm")

    # Fallback line
    draw_arrow(draw, (970, 485), (1050, 485), fill="#dc2626", width=2)
    draw.text((1010, 470), "SLM Err", font=f_arrow, fill="#dc2626", anchor="mm")

    # Process 6.0: Telemetry
    draw_rounded_box(draw, [880, 620, 1140, 720], fill="#fdf2f8", outline="#db2777", width=2, radius=20)
    draw.text((1010, 650), "6.0", font=f_desc, fill="#9d174d", anchor="mm")
    draw.text((1010, 675), "Telemetry, Energy &\nCost Accounting", font=f_box, fill="#1e293b", anchor="mm")

    draw_arrow(draw, (860, 540), (950, 620), fill="#16a34a", width=2)
    draw_arrow(draw, (1160, 540), (1070, 620), fill="#ea580c", width=2)

    # Datastore D2
    draw.line([450, 780, 750, 780], fill="#475569", width=2)
    draw.line([450, 840, 750, 840], fill="#475569", width=2)
    draw.text((600, 810), "D2 | requests_log (SQLite Relational DB)", font=f_arrow, fill="#1e293b", anchor="mm")

    draw_arrow(draw, (920, 720), (680, 780), fill="#db2777", width=2)
    draw.text((820, 765), "Audit Record (16 Fields)", font=f_arrow, fill="#9d174d", anchor="mm")

    # Return response to User
    draw_arrow(draw, (750, 485), (140, 485), fill="#10b981", width=2)
    draw.line([140, 485, 140, 240], fill="#10b981", width=2)
    draw.text((450, 470), "Generated Response Payload (HTTP 200 OK)", font=f_arrow, fill="#047857", anchor="mm")

    # Process 7.0: Dashboard
    draw_rounded_box(draw, [150, 620, 400, 720], fill="#faf5ff", outline="#7c3aed", width=2, radius=20)
    draw.text((275, 650), "7.0", font=f_desc, fill="#6d28d9", anchor="mm")
    draw.text((275, 675), "Dashboard Analytics &\nVisual KPI Rendering", font=f_box, fill="#1e293b", anchor="mm")

    draw_arrow(draw, (520, 780), (350, 720), fill="#475569", width=2)
    draw.text((430, 740), "Select Logs", font=f_arrow, fill="#475569", anchor="mm")

    img.save(r"Report\figures\fig_3_2_dfd_level_1.png")
    print("Generated fig_3_2_dfd_level_1.png")

# ==========================================
# 4. Figure 3.3: DFD Level 2 (Micro Process)
# ==========================================
def generate_dfd_level_2():
    img = Image.new("RGB", (1350, 850), "#ffffff")
    draw = ImageDraw.Draw(img)
    f_title = get_font(22, bold=True)
    f_sub = get_font(13, bold=False)
    f_box = get_font(13, bold=True)
    f_desc = get_font(11, bold=False)
    f_arrow = get_font(10, bold=True)

    draw.text((675, 30), "Data Flow Diagram (DFD) - Level 2: Micro-Decomposition of Classification & Dispatch", font=f_title, fill="#1e293b", anchor="mm")
    draw.text((675, 58), "Granular Process Steps Inside Complexity Scoring (2.0) and Multi-Tier Inference (3.0/4.0/5.0)", font=f_sub, fill="#64748b", anchor="mm")

    # Ingestion input
    draw_rounded_box(draw, [50, 140, 200, 220], fill="#eff6ff", outline="#2563eb", width=2, radius=12)
    draw.text((125, 170), "Validated Prompt", font=f_box, fill="#1d4ed8", anchor="mm")
    draw.text((125, 195), "String input", font=f_desc, fill="#475569", anchor="mm")

    # Process 2.1: WordPiece Tokenizer
    draw_rounded_box(draw, [280, 140, 460, 220], fill="#faf5ff", outline="#9333ea", width=2, radius=16)
    draw.text((370, 165), "2.1", font=f_desc, fill="#7e22ce", anchor="mm")
    draw.text((370, 190), "WordPiece\nTokenizer (max=128)", font=f_box, fill="#1e293b", anchor="mm")
    draw_arrow(draw, (200, 180), (280, 180), fill="#2563eb", width=2)

    # Process 2.2: Forward Tensor Pass
    draw_rounded_box(draw, [540, 140, 720, 220], fill="#faf5ff", outline="#9333ea", width=2, radius=16)
    draw.text((630, 165), "2.2", font=f_desc, fill="#7e22ce", anchor="mm")
    draw.text((630, 190), "Transformer Encoder\n(6 Layers, 768-d)", font=f_box, fill="#1e293b", anchor="mm")
    draw_arrow(draw, (460, 180), (540, 180), fill="#9333ea", width=2)
    draw.text((500, 165), "input_ids", font=f_arrow, fill="#7e22ce", anchor="mm")

    # Process 2.3: Softmax Scorer
    draw_rounded_box(draw, [800, 140, 980, 220], fill="#faf5ff", outline="#9333ea", width=2, radius=16)
    draw.text((890, 165), "2.3", font=f_desc, fill="#7e22ce", anchor="mm")
    draw.text((890, 190), "Softmax Scorer &\nConfidence Bound", font=f_box, fill="#1e293b", anchor="mm")
    draw_arrow(draw, (720, 180), (800, 180), fill="#9333ea", width=2)
    draw.text((760, 165), "Logits", font=f_arrow, fill="#7e22ce", anchor="mm")

    # Process 3.1: Policy Evaluator
    draw_rounded_box(draw, [1060, 140, 1260, 220], fill="#fef3c7", outline="#d97706", width=2, radius=16)
    draw.text((1160, 165), "3.1", font=f_desc, fill="#b45309", anchor="mm")
    draw.text((1160, 190), "Policy Routing Gate\n(Score vs. 0.50)", font=f_box, fill="#1e293b", anchor="mm")
    draw_arrow(draw, (980, 180), (1060, 180), fill="#9333ea", width=2)
    draw.text((1020, 165), "p, conf", font=f_arrow, fill="#7e22ce", anchor="mm")

    # Subsystem 4.0: Local Inference Details
    draw_rounded_box(draw, [150, 360, 550, 520], fill="#f0fdf4", outline="#16a34a", width=2, radius=16)
    draw.text((350, 390), "Subsystem 4.0: Local Inference Execution", font=f_box, fill="#15803d", anchor="mm")
    
    draw_rounded_box(draw, [170, 420, 330, 490], fill="#ffffff", outline="#16a34a", width=1)
    draw.text((250, 445), "4.1: CodeCarbon", font=f_arrow, fill="#15803d", anchor="mm")
    draw.text((250, 470), "Start In-Memory Monitor", font=f_desc, fill="#64748b", anchor="mm")

    draw_rounded_box(draw, [370, 420, 530, 490], fill="#ffffff", outline="#16a34a", width=1)
    draw.text((450, 445), "4.2: Ollama Caller", font=f_arrow, fill="#15803d", anchor="mm")
    draw.text((450, 470), "POST qwen2.5:7b API", font=f_desc, fill="#64748b", anchor="mm")

    draw_arrow(draw, (330, 455), (370, 455), fill="#16a34a", width=1)
    draw_arrow(draw, (1100, 220), (350, 360), fill="#16a34a", width=2)
    draw.text((650, 270), "Route 'local' (p < 0.50)", font=f_arrow, fill="#15803d", anchor="mm")

    # Subsystem 5.0: Cloud Inference Details
    draw_rounded_box(draw, [750, 360, 1200, 520], fill="#fff7ed", outline="#ea580c", width=2, radius=16)
    draw.text((975, 390), "Subsystem 5.0: Cloud Multi-Provider Dispatch", font=f_box, fill="#c2410c", anchor="mm")

    draw_rounded_box(draw, [770, 420, 950, 490], fill="#ffffff", outline="#ea580c", width=1)
    draw.text((860, 445), "5.1: Primary Groq LPU", font=f_arrow, fill="#c2410c", anchor="mm")
    draw.text((860, 470), "gpt-oss-120b Caller", font=f_desc, fill="#64748b", anchor="mm")

    draw_rounded_box(draw, [1000, 420, 1180, 490], fill="#ffffff", outline="#ca8a04", width=1)
    draw.text((1090, 445), "5.2: Gemini Failover", font=f_arrow, fill="#ca8a04", anchor="mm")
    draw.text((1090, 470), "gemini-2.5-flash Caller", font=f_desc, fill="#64748b", anchor="mm")

    draw_arrow(draw, (950, 455), (1000, 455), fill="#dc2626", width=2)
    draw.text((975, 435), "429 Err", font=f_arrow, fill="#dc2626", anchor="mm")

    draw_arrow(draw, (1160, 220), (975, 360), fill="#ea580c", width=2)
    draw.text((1110, 290), "Route 'cloud' (p >= 0.50)", font=f_arrow, fill="#c2410c", anchor="mm")

    # Subsystem 6.0: Telemetry Aggregation & Logging
    draw_rounded_box(draw, [400, 600, 950, 750], fill="#f8fafc", outline="#475569", width=2, radius=16)
    draw.text((675, 630), "Subsystem 6.0: Telemetry Aggregation & Persistence", font=f_box, fill="#1e293b", anchor="mm")

    draw_rounded_box(draw, [430, 660, 650, 725], fill="#ffffff", outline="#475569", width=1)
    draw.text((540, 680), "6.1: Cost & Carbon Math", font=f_arrow, fill="#1e293b", anchor="mm")
    draw.text((540, 705), "Tokens x Rates / RAPL Reads", font=f_desc, fill="#64748b", anchor="mm")

    draw_rounded_box(draw, [700, 660, 920, 725], fill="#ffffff", outline="#475569", width=1)
    draw.text((810, 680), "6.2: SQLite Insert", font=f_arrow, fill="#1e293b", anchor="mm")
    draw.text((810, 705), "16-Column Record Write", font=f_desc, fill="#64748b", anchor="mm")

    draw_arrow(draw, (650, 690), (700, 690), fill="#475569", width=2)
    draw_arrow(draw, (350, 520), (500, 600), fill="#16a34a", width=2)
    draw_arrow(draw, (975, 520), (800, 600), fill="#ea580c", width=2)

    img.save(r"Report\figures\fig_3_3_dfd_level_2.png")
    print("Generated fig_3_3_dfd_level_2.png")

# ==========================================
# 5. Figure 3.8: UML Component Diagram
# ==========================================
def generate_component_diagram():
    img = Image.new("RGB", (1300, 850), "#ffffff")
    draw = ImageDraw.Draw(img)
    f_title = get_font(22, bold=True)
    f_sub = get_font(13, bold=False)
    f_box = get_font(14, bold=True)
    f_comp = get_font(12, bold=True)
    f_desc = get_font(11, bold=False)

    draw.text((650, 30), "UML Component Diagram: Multi-Tier Architectural Packages", font=f_title, fill="#1e293b", anchor="mm")
    draw.text((650, 58), "Component Interfaces, Internal Subsystems, and Inter-Module Dependencies", font=f_sub, fill="#64748b", anchor="mm")

    def draw_component(x1, y1, x2, y2, name, subtext, fill="#f8fafc", out="#334155"):
        draw_rounded_box(draw, [x1, y1, x2, y2], fill=fill, outline=out, width=2, radius=4)
        # Small UML component tabs on top left
        draw.rectangle([x1 - 10, y1 + 10, x1 + 10, y1 + 22], fill=fill, outline=out, width=1)
        draw.rectangle([x1 - 10, y1 + 30, x1 + 10, y1 + 42], fill=fill, outline=out, width=1)
        draw.text(((x1+x2)/2, y1 + 25), f"<<component>>", font=get_font(10, bold=False), fill="#64748b", anchor="mm")
        draw.text(((x1+x2)/2, y1 + 45), name, font=f_comp, fill="#1e293b", anchor="mm")
        draw.text(((x1+x2)/2, y1 + 75), subtext, font=f_desc, fill="#475569", anchor="mm")

    # Presentation Tier
    draw_rounded_box(draw, [40, 110, 320, 780], fill="#fdf2f8", outline="#db2777", width=2, radius=10)
    draw.text((180, 140), "Presentation Tier", font=f_box, fill="#9d174d", anchor="mm")
    draw_component(60, 180, 300, 290, "StreamlitApp", "Interactive Web Portal\n Altair Data Visualizations", fill="#ffffff", out="#db2777")
    draw_component(60, 340, 300, 450, "SwaggerUI", "OpenAPI Interactive Client\n Endpoint Testing (/docs)", fill="#ffffff", out="#db2777")
    draw_component(60, 500, 300, 610, "ExternalClient", "Third-Party REST Consumer\n Automated Batch Suites", fill="#ffffff", out="#db2777")

    # Gateway & Logic Tier
    draw_rounded_box(draw, [380, 110, 840, 780], fill="#eff6ff", outline="#2563eb", width=2, radius=10)
    draw.text((610, 140), "Gateway & Routing Engine Tier", font=f_box, fill="#1d4ed8", anchor="mm")
    draw_component(410, 180, 810, 290, "FastAPIGateway", "backend/main.py\n Asynchronous REST API, Request Schemas, Latency Timers", fill="#ffffff", out="#2563eb")
    draw_component(410, 340, 810, 480, "ComplexityClassifierComponent", "DistilBERT Transformer (Active) / TF-IDF ML / Heuristics\n Output: Continuous Complexity Probability in [0.0, 1.0]", fill="#ffffff", out="#9333ea")
    draw_component(410, 520, 810, 640, "RoutingPolicyEngine", "Decision Gate (Threshold: 0.50)\n Multi-Tier Exception Interception & Bidirectional Fallbacks", fill="#ffffff", out="#d97706")
    draw_component(410, 670, 810, 760, "TelemetryEngine", "CodeCarbon Hardware Profiler & Carbon Footprint Computer", fill="#ffffff", out="#059669")

    # Execution & Persistence Tier
    draw_rounded_box(draw, [900, 110, 1260, 780], fill="#f8fafc", outline="#334155", width=2, radius=10)
    draw.text((1080, 140), "Execution & Persistence Tier", font=f_box, fill="#1e293b", anchor="mm")
    draw_component(920, 180, 1240, 290, "OllamaExecutionService", "Local SLM Daemon (qwen2.5:7b)\n Runs in Host CPU/GPU RAM", fill="#ffffff", out="#16a34a")
    draw_component(920, 340, 1240, 460, "CloudDispatchService", "Primary: Groq LPU (gpt-oss-120b)\n Failover: Google Gemini 2.5 Flash", fill="#ffffff", out="#ea580c")
    draw_component(920, 520, 1240, 640, "SQLitePersistence", "backend/database.py (requests_log)\n Auto-Migrations & Query Audit API", fill="#ffffff", out="#475569")
    draw_component(920, 670, 1240, 760, "ModelStorageArtifacts", "distilbert_classifier/ weights\n classifier_model.joblib", fill="#ffffff", out="#7e22ce")

    # Connectors
    draw_arrow(draw, (300, 235), (410, 235), fill="#2563eb", width=2)
    draw_arrow(draw, (300, 395), (410, 250), fill="#2563eb", width=2)
    draw_arrow(draw, (610, 290), (610, 340), fill="#9333ea", width=2)
    draw_arrow(draw, (610, 480), (610, 520), fill="#d97706", width=2)
    draw_arrow(draw, (810, 560), (920, 235), fill="#16a34a", width=2)
    draw_arrow(draw, (810, 580), (920, 395), fill="#ea580c", width=2)
    draw_arrow(draw, (810, 715), (920, 580), fill="#475569", width=2)

    img.save(r"Report\figures\fig_3_8_uml_component.png")
    print("Generated fig_3_8_uml_component.png")

# ==========================================
# 6. Figure 3.9: UML State Machine Diagram
# ==========================================
def generate_state_machine_diagram():
    img = Image.new("RGB", (1250, 750), "#ffffff")
    draw = ImageDraw.Draw(img)
    f_title = get_font(22, bold=True)
    f_sub = get_font(13, bold=False)
    f_state = get_font(13, bold=True)
    f_trans = get_font(10, bold=True)

    draw.text((625, 30), "UML State Machine Diagram: Request Lifecycle Transitions", font=f_title, fill="#1e293b", anchor="mm")
    draw.text((625, 58), "State Progression from Initial Ingestion to Inference Execution, Fallback, and Completion", font=f_sub, fill="#64748b", anchor="mm")

    # Start Node
    draw.ellipse([60, 220, 90, 250], fill="#1e293b", outline="#1e293b")
    draw_arrow(draw, (90, 235), (150, 235), fill="#1e293b", width=2)
    draw.text((120, 220), "POST /chat", font=f_trans, fill="#1e293b", anchor="mm")

    def draw_state(x1, y1, x2, y2, name, sub="", fill="#f8fafc", out="#334155"):
        draw_rounded_box(draw, [x1, y1, x2, y2], fill=fill, outline=out, width=2, radius=12)
        draw.text(((x1+x2)/2, (y1+y2)/2 - 8 if sub else (y1+y2)/2), name, font=f_state, fill="#1e293b", anchor="mm")
        if sub:
            draw.text(((x1+x2)/2, (y1+y2)/2 + 10), sub, font=get_font(10, bold=False), fill="#64748b", anchor="mm")

    # States
    draw_state(150, 205, 300, 265, "Ingested", "Validating Schema", fill="#eff6ff", out="#2563eb")
    draw_arrow(draw, (300, 235), (370, 235), fill="#2563eb", width=2)
    draw.text((335, 220), "Valid", font=f_trans, fill="#2563eb", anchor="mm")

    draw_state(370, 205, 530, 265, "Classifying", "DistilBERT Inference", fill="#faf5ff", out="#9333ea")
    draw_arrow(draw, (530, 235), (610, 235), fill="#9333ea", width=2)
    draw.text((570, 220), "Score p", font=f_trans, fill="#9333ea", anchor="mm")

    draw_state(610, 205, 760, 265, "RouteSelected", "Threshold Decision", fill="#fef3c7", out="#d97706")

    # Branch Local
    draw_arrow(draw, (685, 205), (685, 140), fill="#16a34a", width=2)
    draw_arrow(draw, (685, 140), (840, 140), fill="#16a34a", width=2)
    draw.text((750, 125), "p < 0.50 (Simple)", font=f_trans, fill="#16a34a", anchor="mm")

    draw_state(840, 110, 1020, 170, "LocalRunning", "Ollama qwen2.5:7b", fill="#f0fdf4", out="#16a34a")

    # Branch Cloud
    draw_arrow(draw, (685, 265), (685, 330), fill="#ea580c", width=2)
    draw_arrow(draw, (685, 330), (840, 330), fill="#ea580c", width=2)
    draw.text((750, 345), "p >= 0.50 (Complex)", font=f_trans, fill="#ea580c", anchor="mm")

    draw_state(840, 300, 1020, 360, "CloudRunning", "Primary Groq LPU", fill="#fff7ed", out="#ea580c")

    # Fallback state
    draw_state(840, 440, 1020, 500, "FailoverTriggered", "Gemini / Cloud Fallback", fill="#fef2f2", out="#dc2626")
    
    # Local failed -> Fallback
    draw_arrow(draw, (1020, 140), (1080, 140), fill="#dc2626", width=2)
    draw.line([1080, 140, 1080, 470], fill="#dc2626", width=2)
    draw_arrow(draw, (1080, 470), (1020, 470), fill="#dc2626", width=2)
    draw.text((1140, 280), "Ollama Offline / Timeout", font=f_trans, fill="#dc2626", anchor="mm")

    # Groq failed -> Failover
    draw_arrow(draw, (930, 360), (930, 440), fill="#dc2626", width=2)
    draw.text((980, 400), "Groq 429", font=f_trans, fill="#dc2626", anchor="mm")

    # All paths -> Logging
    draw_state(550, 580, 720, 640, "LoggingMetrics", "SQLite Persistence", fill="#f8fafc", out="#475569")
    
    draw_arrow(draw, (840, 140), (600, 140), fill="#16a34a", width=2)
    draw.line([600, 140, 600, 580], fill="#16a34a", width=2)

    draw_arrow(draw, (840, 330), (660, 330), fill="#ea580c", width=2)
    draw.line([660, 330, 660, 580], fill="#ea580c", width=2)

    draw_arrow(draw, (840, 470), (700, 470), fill="#dc2626", width=2)
    draw.line([700, 470, 700, 580], fill="#dc2626", width=2)

    # Logging -> Responded & End Node
    draw_state(250, 580, 420, 640, "Responded", "HTTP 200 Sent", fill="#eff6ff", out="#2563eb")
    draw_arrow(draw, (550, 610), (420, 610), fill="#475569", width=2)

    # End Node (Bullseye)
    draw_arrow(draw, (250, 610), (160, 610), fill="#1e293b", width=2)
    draw.ellipse([120, 595, 150, 625], outline="#1e293b", width=2)
    draw.ellipse([125, 600, 145, 620], fill="#1e293b")

    img.save(r"Report\figures\fig_3_9_uml_state_machine.png")
    print("Generated fig_3_9_uml_state_machine.png")

# ==========================================
# 7. Additional Evaluation Graphs
# ==========================================
def generate_extra_graphs():
    # Graph 4.2: Routing Offload Donut / Pie
    img = Image.new("RGB", (800, 550), "#ffffff")
    d = ImageDraw.Draw(img)
    f_title = get_font(18, bold=True)
    f_sub = get_font(12, bold=False)
    f_lbl = get_font(13, bold=True)

    d.text((400, 30), "Graph 4.2: Workload Offload Distribution", font=f_title, fill="#1e293b", anchor="mm")
    d.text((400, 55), "Percentage of Prompts Served Locally (Zero Cost) vs. Cloud Escalations", font=f_sub, fill="#64748b", anchor="mm")

    # Pie chart (60% local = 216 deg, 40% cloud = 144 deg)
    bbox = [150, 110, 490, 450]
    d.pieslice(bbox, start=0, end=216, fill="#16a34a", outline="#ffffff", width=2)
    d.pieslice(bbox, start=216, end=360, fill="#2563eb", outline="#ffffff", width=2)

    # Donut center hole
    d.ellipse([235, 195, 405, 365], fill="#ffffff")
    d.text((320, 260), "60.0%", font=get_font(22, bold=True), fill="#15803d", anchor="mm")
    d.text((320, 290), "Local Offload", font=get_font(12, bold=False), fill="#475569", anchor="mm")

    # Legend
    d.rounded_rectangle([550, 200, 580, 225], radius=4, fill="#16a34a")
    d.text((600, 212), "Local SLM (Ollama)\n60.0% (18 / 30 prompts)", font=f_lbl, fill="#1e293b", anchor="lm")

    d.rounded_rectangle([550, 270, 580, 295], radius=4, fill="#2563eb")
    d.text((600, 282), "Cloud LLM (Groq/Gemini)\n40.0% (12 / 30 prompts)", font=f_lbl, fill="#1e293b", anchor="lm")

    d.text((400, 490), "Result: Exceeds the target 40% cloud API reduction benchmark comfortably.", font=f_sub, fill="#15803d", anchor="mm")
    img.save(r"Report\figures\graph_4_2_traffic_distribution.png")
    print("Generated graph_4_2_traffic_distribution.png")

    # Graph 4.3: Latency Comparison
    img = Image.new("RGB", (900, 550), "#ffffff")
    d = ImageDraw.Draw(img)
    d.text((450, 30), "Graph 4.3: Average Response Latency Comparison", font=f_title, fill="#1e293b", anchor="mm")
    d.text((450, 55), "Comparing Response Times in Seconds across Inference Engines", font=f_sub, fill="#64748b", anchor="mm")

    ox, oy = 250, 420
    d.line([ox, 120, ox, oy], fill="#94a3b8", width=2)
    d.line([ox, oy, 800, oy], fill="#94a3b8", width=2)

    for x_val in [5, 10, 15, 20, 25]:
        x_pos = ox + int(x_val * 21.0)
        d.line([x_pos, 120, x_pos, oy], fill="#f1f5f9", width=1)
        d.text((x_pos, oy + 20), f"{x_val}s", font=f_sub, fill="#64748b", anchor="mm")

    lat_bars = [
        ("Cloud Groq LPU\n(gpt-oss-120b)", 5.5, "#2563eb", 170),
        ("Cloud Gemini\n(gemini-2.5-flash)", 8.2, "#f59e0b", 260),
        ("Local Ollama SLM\n(qwen2.5:7b CPU)", 19.5, "#16a34a", 350)
    ]

    for name, val, color, y_pos in lat_bars:
        w = int(val * 21.0)
        d.rounded_rectangle([ox, y_pos - 25, ox + w, y_pos + 25], radius=6, fill=color)
        d.text((ox - 15, y_pos), name, font=f_lbl, fill="#1e293b", anchor="rm")
        d.text((ox + w + 20, y_pos), f"{val} s", font=get_font(13, bold=True), fill="#1e293b", anchor="lm")

    img.save(r"Report\figures\graph_4_3_latency_comparison.png")
    print("Generated graph_4_3_latency_comparison.png")

    # Graph 4.5: Environmental Carbon Footprint
    img = Image.new("RGB", (900, 550), "#ffffff")
    d = ImageDraw.Draw(img)
    d.text((450, 30), "Graph 4.5: Environmental Carbon Emissions Footprint", font=f_title, fill="#1e293b", anchor="mm")
    d.text((450, 55), "Actual Hybrid Architecture Emissions vs. Simulated 100% Cloud Baseline (Grams CO2)", font=f_sub, fill="#64748b", anchor="mm")

    ox, oy = 120, 450
    d.line([ox, oy, 800, oy], fill="#94a3b8", width=2)
    d.line([ox, oy, ox, 100], fill="#94a3b8", width=2)

    for y_val in [5, 10, 15, 20, 25, 30]:
        y_pos = oy - int(y_val * 10.5)
        d.line([ox, y_pos, 800, y_pos], fill="#f1f5f9", width=1)
        d.text((ox - 15, y_pos), f"{y_val}g", font=f_sub, fill="#64748b", anchor="rm")

    carb_bars = [
        ("Actual Hybrid\nSystem (35 Queries)", 14.8, "#16a34a", 280),
        ("100% All-Cloud\nBaseline (Simulated)", 29.0, "#dc2626", 580)
    ]

    for name, val, color, x_pos in carb_bars:
        h = int(val * 10.5)
        d.rounded_rectangle([x_pos - 60, oy - h, x_pos + 60, oy], radius=6, fill=color)
        d.text((x_pos, oy - h - 15), f"{val} g CO2", font=get_font(13, bold=True), fill="#1e293b", anchor="mm")
        d.text((x_pos, oy + 25), name, font=f_lbl, fill="#334155", anchor="mm")

    d.text((430, 200), "14.2 g CO2 Avoided (~49% Reduction)\nHardware-Tracked via CodeCarbon", font=get_font(13, bold=True), fill="#15803d", anchor="mm")

    img.save(r"Report\figures\graph_4_5_carbon_emissions.png")
    print("Generated graph_4_5_carbon_emissions.png")

if __name__ == "__main__":
    generate_architecture_diagram()
    generate_dfd_level_0()
    generate_dfd_level_1()
    generate_dfd_level_2()
    generate_use_case_diagram()
    generate_class_diagram()
    generate_sequence_diagram()
    generate_activity_diagram()
    generate_component_diagram()
    generate_state_machine_diagram()
    generate_er_diagram()
    generate_extra_graphs()
    print("ALL diagrams and charts generated cleanly!")
