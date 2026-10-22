import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import os
import time
import requests
import altair as alt

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "router_logs.db")
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Hybrid SLM-LLM Router Gateway", layout="wide", page_icon="⚡")

# --- CUSTOM CSS WITH ANIMATIONS & MODERN TYPOGRAPHY ---
st.markdown("""
<style>
/* Main Metric Containers */
div[data-testid="metric-container"] {
    background-color: #f8f9fa;
    border: 1px solid #e0e0e0;
    padding: 14px 16px;
    border-radius: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
@media (prefers-color-scheme: dark) {
    div[data-testid="metric-container"] {
        background-color: #1e1e1e;
        border: 1px solid #333;
    }
}

/* Step Headers */
.step-header {
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 24px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.step-caption {
    color: #666;
    font-size: 0.88rem;
    margin-bottom: 14px;
}
@media (prefers-color-scheme: dark) {
    .step-caption {
        color: #aaa;
    }
}

/* Status Bar & Pills */
.status-pill {
    background: #ffffff;
    border: 1px solid #ddd;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
}
@media (prefers-color-scheme: dark) {
    .status-pill {
        background: #262626;
        border: 1px solid #444;
        color: #eee;
    }
}

/* Base Journey Card */
.journey-card {
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px 10px;
    text-align: center;
    min-height: 115px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: transform 0.2s ease;
}
@media (prefers-color-scheme: dark) {
    .journey-card {
        background-color: #242424;
        border: 1px solid #444;
    }
}

/* Keyframe Animations for Active Routing Paths */
@keyframes pulseGreenGlow {
    0% { box-shadow: 0 0 0 0 rgba(46, 123, 50, 0.7); transform: translateY(0); }
    50% { box-shadow: 0 0 16px 3px rgba(46, 123, 50, 0.45); transform: translateY(-2px); }
    100% { box-shadow: 0 0 0 0 rgba(46, 123, 50, 0.7); transform: translateY(0); }
}
@keyframes pulseBlueGlow {
    0% { box-shadow: 0 0 0 0 rgba(21, 101, 192, 0.7); transform: translateY(0); }
    50% { box-shadow: 0 0 16px 3px rgba(21, 101, 192, 0.45); transform: translateY(-2px); }
    100% { box-shadow: 0 0 0 0 rgba(21, 101, 192, 0.7); transform: translateY(0); }
}
@keyframes pulseOrangeGlow {
    0% { box-shadow: 0 0 0 0 rgba(230, 81, 0, 0.7); transform: translateY(0); }
    50% { box-shadow: 0 0 16px 3px rgba(230, 81, 0, 0.45); transform: translateY(-2px); }
    100% { box-shadow: 0 0 0 0 rgba(230, 81, 0, 0.7); transform: translateY(0); }
}
@keyframes processingPulse {
    0% { background-color: rgba(230, 81, 0, 0.05); border-color: rgba(230, 81, 0, 0.4); }
    50% { background-color: rgba(230, 81, 0, 0.16); border-color: rgba(230, 81, 0, 0.9); box-shadow: 0 0 14px rgba(230, 81, 0, 0.4); }
    100% { background-color: rgba(230, 81, 0, 0.05); border-color: rgba(230, 81, 0, 0.4); }
}
@keyframes shimmerArrow {
    0% { opacity: 0.25; transform: translateX(-4px); }
    50% { opacity: 1; transform: translateX(4px); }
    100% { opacity: 0.25; transform: translateX(-4px); }
}
@keyframes beaconPulse {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(1.3); }
    100% { opacity: 1; transform: scale(1); }
}

.animated-arrow-col {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 115px;
}
.animated-arrow {
    display: inline-block;
    animation: shimmerArrow 1.5s infinite ease-in-out;
    color: #1976d2;
    font-size: 20px;
    font-weight: 900;
}

.journey-highlight-local {
    border: 2.5px solid #2e7b32 !important;
    background-color: rgba(46, 123, 50, 0.12) !important;
    animation: pulseGreenGlow 2.2s infinite ease-in-out !important;
}
.journey-highlight-cloud {
    border: 2.5px solid #1565c0 !important;
    background-color: rgba(21, 101, 192, 0.12) !important;
    animation: pulseBlueGlow 2.2s infinite ease-in-out !important;
}
.journey-highlight-fallback {
    border: 2.5px solid #e65100 !important;
    background-color: rgba(230, 81, 0, 0.14) !important;
    animation: pulseOrangeGlow 2.2s infinite ease-in-out !important;
}
.journey-processing-card {
    border: 2px dashed #e65100 !important;
    animation: processingPulse 1.4s infinite ease-in-out !important;
}

/* Branch Pathway Map */
.pathway-box {
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 6px;
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1px solid #e0e0e0;
    background: #fbfbfb;
}
@media (prefers-color-scheme: dark) {
    .pathway-box {
        background: #1e1e1e;
        border: 1px solid #333;
    }
}
.pathway-active {
    font-weight: bold;
}
.pathway-active-local {
    border: 2px solid #2e7b32 !important;
    background-color: rgba(46, 123, 50, 0.1) !important;
    color: #2e7b32 !important;
}
.pathway-active-cloud {
    border: 2px solid #1565c0 !important;
    background-color: rgba(21, 101, 192, 0.1) !important;
    color: #1565c0 !important;
}
.pathway-active-fallback {
    border: 2px solid #e65100 !important;
    background-color: rgba(230, 81, 0, 0.1) !important;
    color: #e65100 !important;
}
.beacon-dot {
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    margin-right: 6px;
    animation: beaconPulse 1.2s infinite ease-in-out;
}

/* Full Generated Response Viewer */
.answer-box {
    border-radius: 10px;
    padding: 18px 22px;
    margin-top: 10px;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
}
@media (prefers-color-scheme: dark) {
    .answer-box {
        background-color: #1a1a1a;
        border: 1px solid #333;
        color: #f0f0f0;
    }
}
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("⚡ Hybrid SLM-LLM Router Gateway")
st.caption("Intelligent Prompt Complexity Evaluation • Zero-Cost Local Inference • Automated Cloud LLM Failover")

# --- LOAD DATABASE RECORDS ---
def load_data():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM requests_log ORDER BY id DESC", conn)
    conn.close()
    return df

df = load_data()

# Ensure all columns exist for old DB backward compatibility
for col in ['cloud_provider', 'co2_grams', 'energy_kwh', 'fallback_reason', 'classifier_confidence', 'classify_ms', 'inference_ms', 'model_name']:
    if col not in df.columns:
        df[col] = None

gemini_failovers_count = len(df[df['cloud_provider'] == 'gemini']) if not df.empty else 0
fallbacks_count = len(df[df['fallback_reason'].isin(['local_slm_unavailable', 'cloud_llm_unavailable'])]) if not df.empty else 0

# --- SLEEK SYSTEM CONNECTIVITY STATUS BAR ---
def fetch_health():
    # Primary target is 127.0.0.1 to avoid Windows IPv6 resolution latency
    targets = [BACKEND_URL]
    if "127.0.0.1" not in BACKEND_URL:
        targets.append("http://127.0.0.1:8000")
    for target in targets:
        try:
            r = requests.get(f"{target}/health", timeout=4.5)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
    return None

health_data = fetch_health()

if health_data:
    ollama_icon = "🟢" if health_data.get("ollama_up") else "🔴"
    groq_icon = "🟢" if health_data.get("groq_key_configured") else "🔴"
    gemini_icon = "🟢" if health_data.get("gemini_key_configured") else "🔴"
    distilbert_icon = "🟢" if health_data.get("distilbert_loaded") else "⚪"
    mode_text = health_data.get("classifier_mode", "distilbert").upper()
    thresh_val = health_data.get("threshold", 0.5)

    st.markdown(f"""
    <div style="background: rgba(46, 123, 50, 0.07); border: 1px solid rgba(46, 123, 50, 0.25); border-left: 5px solid #2e7b32; border-radius: 8px; padding: 10px 16px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <div>
            <span style="font-weight: 700; color: #2e7b32; font-size: 14px;">🟢 Gateway Backend Online</span>
            <span style="font-size: 12px; color: #555; margin-left: 8px;">Active Mode: <b>{mode_text}</b> | Threshold: <b>{thresh_val}</b></span>
        </div>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            <span class="status-pill">{ollama_icon} Ollama ({'Online' if health_data.get('ollama_up') else 'Offline'})</span>
            <span class="status-pill">{groq_icon} Groq ({'Configured' if health_data.get('groq_key_configured') else 'No Key'})</span>
            <span class="status-pill">{gemini_icon} Gemini ({'Configured' if health_data.get('gemini_key_configured') else 'No Key'})</span>
            <span class="status-pill">{distilbert_icon} DistilBERT ({'Loaded' if health_data.get('distilbert_loaded') else 'Standby'})</span>
            <span class="status-pill" style="color: #6a1b9a;">✨ Failovers: <b>{gemini_failovers_count}</b></span>
            <span class="status-pill" style="color: #e65100;">⚠️ Fallbacks: <b>{fallbacks_count}</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style="background: rgba(255, 152, 0, 0.08); border: 1px solid rgba(255, 152, 0, 0.35); border-left: 5px solid #ff9800; border-radius: 8px; padding: 10px 16px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <div>
            <span style="font-weight: 700; color: #e65100; font-size: 14px;">⚡ Backend Server Standby ({BACKEND_URL})</span>
            <span style="font-size: 12px; color: #666; margin-left: 8px;">Run backend with: <code>uvicorn backend.main:app --port 8000 --reload</code>. Showing historical records from <code>router_logs.db</code>.</span>
        </div>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            <span class="status-pill" style="color: #777;">⚪ Ollama (Standby)</span>
            <span class="status-pill" style="color: #777;">⚪ Cloud API (Standby)</span>
            <span class="status-pill" style="color: #6a1b9a;">✨ Failovers: <b>{gemini_failovers_count}</b></span>
            <span class="status-pill" style="color: #e65100;">⚠️ Fallbacks: <b>{fallbacks_count}</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# STEP 1: INTERACTIVE PROMPT ROUTING PLAYGROUND & REQUEST JOURNEY
# ============================================================================
st.markdown('<div class="step-header">🎮 Step 1: Interactive Prompt Routing Playground</div>', unsafe_allow_html=True)
st.markdown('<div class="step-caption">Submit a custom prompt or trigger a benchmark batch to watch the router evaluate complexity and execute the optimal compute route live.</div>', unsafe_allow_html=True)

prompt_col, action_col = st.columns([3, 1])

with prompt_col:
    user_prompt = st.text_area(
        "Enter a prompt to test the hybrid router live:",
        placeholder="e.g. 'What is the boiling point of water?' or 'Write a complete Python implementation of an LRU cache with O(1) ops.'",
        height=85,
        label_visibility="collapsed"
    )
    with st.expander("🎯 Curated Demo Testing Prompts (Click to copy & test live)", expanded=False):
        c_sim, c_cpx = st.columns(2)
        with c_sim:
            st.markdown("**🟢 Simple Queries (Target: Local SLM `qwen2.5:7b`):**")
            st.code("What is the boiling point of water in Celsius?", language="text")
            st.code("Convert 150 miles per hour to kilometers per hour.", language="text")
            st.code("Name three primary colors and their complementary pairs.", language="text")
        with c_cpx:
            st.markdown("**🔵 Complex Queries (Target: Cloud LLM `gpt-oss-120b`):**")
            st.code("Write a complete Python implementation of an LRU Cache with O(1) get and put operations.", language="text")
            st.code("Analyze how quantum error correction surface codes protect logical qubits against depolarizing noise.", language="text")
            st.code("Design a fault-tolerant distributed consensus protocol using a two-phase commit with Raft leader election.", language="text")
        st.markdown("**🛡️ Resilient Failover & Fallback Scenarios to Demo:**")
        st.caption("1. **Local ➔ Cloud Fallback (Path D):** Stop Ollama (`ollama stop` or close app) and send a simple prompt. Router detects Ollama offline and automatically routes to Cloud LLM.")
        st.caption("2. **Cloud ➔ Local Fallback (Path E):** Disconnect internet or provide invalid Cloud keys and send a complex prompt. Router detects Cloud unavailable and automatically routes to Local SLM.")
        st.caption("3. **Cloud Failover (Path C):** Groq rate limit / timeout automatically falls over to Google Gemini Flash.")

with action_col:
    st.write("")
    send_clicked = st.button("🚀 Route Prompt", use_container_width=True)
    batch_clicked = st.button("⚡ Run 20-Prompt Benchmark", use_container_width=True)
    reset_db_clicked = st.button("🗑️ Reset DB for Demo", use_container_width=True, help="Empties requests_log table so you can start a clean live demo.")

# Placeholder where the Request Journey & Generated Answer will render
journey_container = st.empty()

# Helper function to render the Request Journey & Answer panel
def render_journey_panel(target_container, state="completed", req_data=None, prompt_text=""):
    with target_container.container():
        st.markdown("**🧭 Execution Journey & Active Routing Pathway:**")

        if state == "processing":
            # --- LIVE IN-FLIGHT ANIMATED PROCESSING STATE ---
            st.caption("⚡ **Live Pipeline Progression:** Evaluating complexity score ➔ Computing route gate ➔ Invoking model...")
            st.progress(0.45)

            col1, a1, col2, a2, col3, a3, col4, a4, col5, a5, col6 = st.columns([2.0, 0.35, 2.0, 0.35, 2.0, 0.35, 2.4, 0.35, 2.0, 0.35, 1.8])

            col1.markdown(f"""
            <div class="journey-card">
                <b>1. Prompt</b>
                <span style="font-size:12px; color:#777;">{len(prompt_text.split())} words</span>
                <span style="font-size:11px; margin-top:4px;">"{prompt_text[:28]}..."</span>
            </div>
            """, unsafe_allow_html=True)

            a1.markdown('<div class="animated-arrow-col"><span class="animated-arrow">➔</span></div>', unsafe_allow_html=True)

            col2.markdown("""
            <div class="journey-card journey-processing-card">
                <b>2. Classifier</b>
                <span style="font-size:12px; font-weight:bold; color:#e65100;">Evaluating...</span>
                <span style="font-size:11px; color:#e65100;">Scoring reasoning</span>
            </div>
            """, unsafe_allow_html=True)

            a2.markdown('<div class="animated-arrow-col"><span class="animated-arrow">➔</span></div>', unsafe_allow_html=True)

            col3.markdown("""
            <div class="journey-card journey-processing-card">
                <b>3. Decision</b>
                <span style="font-size:12px; color:#e65100;">Calculating...</span>
                <span style="font-size:11px; color:#777;">Threshold: 0.50</span>
            </div>
            """, unsafe_allow_html=True)

            a3.markdown('<div class="animated-arrow-col"><span class="animated-arrow">➔</span></div>', unsafe_allow_html=True)

            col4.markdown("""
            <div class="journey-card journey-processing-card">
                <b>4. Model Used</b>
                <span style="font-size:12px; color:#e65100;">Dispatching...</span>
                <span style="font-size:11px; color:#777;">SLM or Cloud LLM</span>
            </div>
            """, unsafe_allow_html=True)

            a4.markdown('<div class="animated-arrow-col"><span class="animated-arrow">➔</span></div>', unsafe_allow_html=True)

            col5.markdown("""
            <div class="journey-card">
                <b>5. Response</b>
                <span style="font-size:12px; color:#999;">Awaiting...</span>
                <span style="font-size:11px; color:#999;">Generating tokens</span>
            </div>
            """, unsafe_allow_html=True)

            a5.markdown('<div class="animated-arrow-col"><span class="animated-arrow">➔</span></div>', unsafe_allow_html=True)

            col6.markdown("""
            <div class="journey-card">
                <b>6. Logged</b>
                <span style="font-size:12px; color:#999;">Pending...</span>
                <span style="font-size:11px; color:#999;">SQLite</span>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            st.info("⚡ Prompt is executing across the routing middleware. The decision tree and generated answer will appear below momentarily...")

        elif state == "completed" and req_data:
            # --- COMPLETED FINAL ROUTING STATE ---
            route_val = str(req_data.get("route", "local")).lower()
            fallback_val = req_data.get("fallback_reason")
            provider_val = str(req_data.get("cloud_provider", "")).lower()

            card_cls = "journey-card"
            if fallback_val == "local_slm_unavailable":
                highlight_cls = "journey-card journey-highlight-fallback"
                path_label = "⚠️ Local Fallback → Cloud"
                active_branch = "fallback"
                theme_color = "#e65100"
            elif fallback_val == "cloud_llm_unavailable":
                highlight_cls = "journey-card journey-highlight-fallback"
                path_label = "⚠️ Cloud Fallback → Local SLM"
                active_branch = "cloud_fallback"
                theme_color = "#e65100"
            elif route_val == "local":
                highlight_cls = "journey-card journey-highlight-local"
                path_label = "💻 Local Path (Ollama)"
                active_branch = "local"
                theme_color = "#2e7b32"
            elif provider_val == "gemini":
                highlight_cls = "journey-card journey-highlight-cloud"
                path_label = "✨ Gemini Failover Path"
                active_branch = "gemini"
                theme_color = "#6a1b9a"
            else:
                highlight_cls = "journey-card journey-highlight-cloud"
                path_label = "⚡ Groq Cloud Path"
                active_branch = "groq"
                theme_color = "#1565c0"

            st.caption(f"Active Request Progression: Stage 1 ➔ Stage 2 ➔ Stage 3 ➔ Stage 4 ➔ Stage 5 ➔ Stage 6 (**100% Completed**)")
            st.progress(1.0)

            col1, a1, col2, a2, col3, a3, col4, a4, col5, a5, col6 = st.columns([2.0, 0.35, 2.0, 0.35, 2.0, 0.35, 2.4, 0.35, 2.0, 0.35, 1.8])

            p_txt = str(req_data.get("prompt", ""))
            col1.markdown(f"""
            <div class="{card_cls}">
                <b>1. Prompt</b>
                <span style="font-size:12px; color:#777;">{len(p_txt.split())} words</span>
                <span style="font-size:11px; margin-top:4px;">"{p_txt[:28]}..."</span>
            </div>
            """, unsafe_allow_html=True)

            a1.markdown('<div class="animated-arrow-col"><span class="animated-arrow">➔</span></div>', unsafe_allow_html=True)

            c_score = float(req_data.get("complexity_score", 0.0) or 0.0)
            c_conf = float(req_data.get("classifier_confidence", 0.0) or 0.0)
            col2.markdown(f"""
            <div class="{card_cls}">
                <b>2. Classifier</b>
                <span style="font-size:13px; font-weight:bold; color:#e65100;">Score: {c_score:.2f}</span>
                <span style="font-size:12px; color:#555;">Conf: {c_conf * 100:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)

            a2.markdown('<div class="animated-arrow-col"><span class="animated-arrow">➔</span></div>', unsafe_allow_html=True)

            thresh = float(req_data.get("threshold", 0.5))
            col3.markdown(f"""
            <div class="{card_cls}">
                <b>3. Decision</b>
                <span style="font-size:14px; font-weight:bold; color:{'#2e7b32' if route_val=='local' else '#1565c0'};">{route_val.upper()}</span>
                <span style="font-size:11px; color:#777;">Threshold: {thresh}</span>
            </div>
            """, unsafe_allow_html=True)

            a3.markdown('<div class="animated-arrow-col"><span class="animated-arrow">➔</span></div>', unsafe_allow_html=True)

            model_display = req_data.get("model_name") or "qwen2.5:7b"
            total_lat = float(req_data.get("latency_ms", 0.0) or 0.0)
            col4.markdown(f"""
            <div class="{highlight_cls}">
                <b>4. Model Used</b>
                <span style="font-size:12px; font-weight:bold;">{model_display}</span>
                <span style="font-size:11px;">{path_label}</span>
                <span style="font-size:11px; color:#555;">Latency: {total_lat:.0f} ms</span>
            </div>
            """, unsafe_allow_html=True)

            a4.markdown('<div class="animated-arrow-col"><span class="animated-arrow">➔</span></div>', unsafe_allow_html=True)

            resp_preview = str(req_data.get("response", ""))[:35]
            col5.markdown(f"""
            <div class="{card_cls}">
                <b>5. Response</b>
                <span style="font-size:11px; color:#555;">Generated:</span>
                <span style="font-size:11px;">"{resp_preview}..."</span>
            </div>
            """, unsafe_allow_html=True)

            a5.markdown('<div class="animated-arrow-col"><span class="animated-arrow">➔</span></div>', unsafe_allow_html=True)

            col6.markdown(f"""
            <div class="{card_cls}">
                <b>6. Logged</b>
                <span style="font-size:13px; font-weight:bold; color:#2e7b32;">SQLite ✅</span>
                <span style="font-size:11px; color:#666;">ID: {req_data.get('id', 'N/A')}</span>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            # Visual Branch Pathway Map & Timing Bar
            col_path_map, col_timing_bar = st.columns([1.2, 1.0])

            with col_path_map:
                st.markdown("**Routing Path Decision Tree:**")

                b_local = "pathway-box pathway-active pathway-active-local" if active_branch == "local" else "pathway-box"
                b_groq = "pathway-box pathway-active pathway-active-cloud" if active_branch == "groq" else "pathway-box"
                b_gemini = "pathway-box pathway-active pathway-active-cloud" if active_branch == "gemini" else "pathway-box"
                b_fallback = "pathway-box pathway-active pathway-active-fallback" if active_branch == "fallback" else "pathway-box"
                b_cloud_fallback = "pathway-box pathway-active pathway-active-fallback" if active_branch == "cloud_fallback" else "pathway-box"

                beacon_local = '<span class="beacon-dot" style="background:#2e7b32;"></span>' if active_branch == "local" else '⚪'
                beacon_groq = '<span class="beacon-dot" style="background:#1565c0;"></span>' if active_branch == "groq" else '⚪'
                beacon_gemini = '<span class="beacon-dot" style="background:#6a1b9a;"></span>' if active_branch == "gemini" else '⚪'
                beacon_fallback = '<span class="beacon-dot" style="background:#e65100;"></span>' if active_branch == "fallback" else '⚪'
                beacon_cloud_fallback = '<span class="beacon-dot" style="background:#e65100;"></span>' if active_branch == "cloud_fallback" else '⚪'

                tag_local = "<b>[● ACTIVE ROUTE]</b>" if active_branch == "local" else "<span style='color:#888;'>Idle</span>"
                tag_groq = "<b>[● ACTIVE ROUTE]</b>" if active_branch == "groq" else "<span style='color:#888;'>Idle</span>"
                tag_gemini = "<b>[● ACTIVE ROUTE]</b>" if active_branch == "gemini" else "<span style='color:#888;'>Idle</span>"
                tag_fallback = "<b>[● ACTIVE ROUTE]</b>" if active_branch == "fallback" else "<span style='color:#888;'>Idle</span>"
                tag_cloud_fallback = "<b>[● ACTIVE ROUTE]</b>" if active_branch == "cloud_fallback" else "<span style='color:#888;'>Idle</span>"

                st.markdown(f"""
                <div class="{b_local}">
                    <span>{beacon_local} <b>Path A: Local SLM (Score &lt; 0.50)</b> → <code>qwen2.5:7b</code></span>
                    <span>{tag_local}</span>
                </div>
                <div class="{b_groq}">
                    <span>{beacon_groq} <b>Path B: Primary Cloud (Score &ge; 0.50)</b> → <code>gpt-oss-120b</code></span>
                    <span>{tag_groq}</span>
                </div>
                <div class="{b_gemini}">
                    <span>{beacon_gemini} <b>Path C: Cloud Failover</b> → <code>gemini-3.8-flash</code></span>
                    <span>{tag_gemini}</span>
                </div>
                <div class="{b_fallback}">
                    <span>{beacon_fallback} <b>Path D: Local Fallback</b> → Ollama Offline ➔ Cloud LLM</span>
                    <span>{tag_fallback}</span>
                </div>
                <div class="{b_cloud_fallback}">
                    <span>{beacon_cloud_fallback} <b>Path E: Reverse Cloud Fallback</b> → Cloud Offline ➔ Local SLM (Ollama)</span>
                    <span>{tag_cloud_fallback}</span>
                </div>
                """, unsafe_allow_html=True)

            with col_timing_bar:
                st.markdown("**Latency Breakdown (Classify vs Inference):**")
                cls_ms = float(req_data.get("classify_ms") or 0.0)
                inf_ms = float(req_data.get("inference_ms") or 0.0)

                if cls_ms > 0 or inf_ms > 0:
                    timing_df = pd.DataFrame([
                        {"Stage": f"1. Classification ({cls_ms:.1f} ms)", "Duration (ms)": cls_ms, "Order": 1},
                        {"Stage": f"2. Model Inference ({inf_ms:.1f} ms)", "Duration (ms)": inf_ms, "Order": 2}
                    ])
                    timing_chart = alt.Chart(timing_df).mark_bar(height=26, cornerRadius=3).encode(
                        x=alt.X('Duration (ms):Q', stack='zero', axis=alt.Axis(title="Milliseconds (ms)")),
                        color=alt.Color('Stage:N', scale=alt.Scale(range=['#e65100', '#1565c0']), legend=alt.Legend(orient="bottom", title="Component")),
                        tooltip=['Stage', 'Duration (ms)']
                    ).properties(height=110)
                    st.altair_chart(timing_chart, use_container_width=True)
                else:
                    st.info("Timing breakdown will update on next request.")

            # --- PROMINENT FULL GENERATED ANSWER SECTION ---
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"**📝 Full Generated Answer ({model_display}):**")

            full_ans = str(req_data.get("response", "")).strip()
            if not full_ans:
                full_ans = "*(No response text returned)*"

            # Render complete markdown output (renders code blocks, lists, equations)
            answer_container = st.container()
            with answer_container:
                st.markdown(f"""
                <div class="answer-box" style="border-left: 6px solid {theme_color};">
                    <div style="font-size: 13px; font-weight: bold; color: {theme_color}; margin-bottom: 8px;">
                        ROUTE: {route_val.upper()} | MODEL: {model_display} | LATENCY: {total_lat:.0f} ms
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(full_ans)

# Handle single prompt submission
if send_clicked:
    if not user_prompt.strip():
        st.warning("Please enter a non-empty prompt.")
    else:
        # Step A: Show live animated in-flight routing state directly in the Request Journey panel
        render_journey_panel(journey_container, state="processing", prompt_text=user_prompt.strip())

        try:
            # Step B: Call backend
            resp = requests.post(f"{BACKEND_URL}/chat", json={"prompt": user_prompt.strip()}, timeout=120)
            resp.raise_for_status()
            result = resp.json()
            st.session_state["last_result"] = result
            df = load_data()  # Reload so charts include the new request immediately

            # Step C: Show completed routing state and full generated answer
            render_journey_panel(journey_container, state="completed", req_data=result)
            st.success(f"Prompt processed! Routed to **{result.get('route', '').upper()}** via **{result.get('model_name', result.get('cloud_provider', ''))}** in {result.get('latency_ms', 0):.0f} ms.")
        except requests.exceptions.RequestException as e:
            journey_container.error(f"⚠️ Backend is unreachable at `{BACKEND_URL}`. Please start the backend (`uvicorn backend.main:app --port 8000`). Details: {e}")

# Sample batch of 20 prompts (10 simple, 10 complex, NONE from training_final.csv)
SAMPLE_BATCH_PROMPTS = [
    # 10 Simple Prompts
    "What is the boiling point of water in Celsius?",
    "Name three primary colors.",
    "How many continents are there on Earth?",
    "What is the opposite of hot?",
    "Who wrote the play Romeo and Juliet?",
    "Convert 100 centimeters to meters.",
    "What is the currency of Japan?",
    "Spell the word environment backwards.",
    "Give me a friendly morning greeting.",
    "What gas do plants absorb during photosynthesis?",
    # 10 Complex Prompts
    "Design a fault-tolerant distributed consensus protocol using a two-phase commit with Raft leader election.",
    "Write a complete Python implementation of Dijkstra algorithm using an indexed binary heap with decrease-key operation.",
    "Explain the mathematical derivation of backpropagation in a deep transformer self-attention head with layer normalization.",
    "Analyze how quantum error correction surface codes protect logical qubits against depolarizing noise.",
    "Construct an econometric time-series forecast model for inflation using vector autoregression and cointegration analysis.",
    "Implement a thread-safe lock-free concurrent ring buffer in C++ using atomic memory order acquire and release semantics.",
    "Evaluate the legal and geopolitical implications of the United Nations Convention on the Law of the Sea regarding deep-sea mining in international waters.",
    "Derive the asymptotic computational complexity of the Fast Fourier Transform using the Cooley-Tukey divide-and-conquer recurrence relation.",
    "Design an end-to-end microservices event sourcing architecture using Kafka, CQRS, and transactional outbox pattern.",
    "Prove that the language L = {a^n b^n c^n | n >= 0} is not context-free using the Ogden lemma."
]

if batch_clicked:
    with journey_container.container():
        st.subheader("⚡ Running 20-Prompt Benchmark Batch (10 Simple + 10 Complex)...")
        batch_prog = st.progress(0.0)
        batch_status_text = st.empty()
        success_count = 0
        try:
            for idx, prompt_text in enumerate(SAMPLE_BATCH_PROMPTS, 1):
                batch_status_text.markdown(f"**Routing Prompt [{idx}/20]:** *\"{prompt_text[:50]}...\"*")
                r = requests.post(f"{BACKEND_URL}/chat", json={"prompt": prompt_text}, timeout=120)
                if r.status_code == 200:
                    success_count += 1
                    st.session_state["last_result"] = r.json()
                batch_prog.progress(idx / len(SAMPLE_BATCH_PROMPTS))
            st.success(f"✅ Batch completed! Successfully routed {success_count}/20 requests.")
            df = load_data()
            st.rerun()
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Batch processing interrupted: Backend unreachable at `{BACKEND_URL}` ({e}).")

if reset_db_clicked:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM requests_log")
        try:
            conn.execute("DELETE FROM sqlite_sequence WHERE name='requests_log'")
        except Exception:
            pass
        conn.commit()
        conn.close()
        st.session_state["last_result"] = None
        st.success("✅ Database emptied successfully! Clean slate ready for demo.")
        df = load_data()
        st.rerun()
    except Exception as e:
        st.error(f"Error resetting database: {e}")

# If page loaded and not currently handling a fresh click, render the existing last request
if not send_clicked and not batch_clicked and not reset_db_clicked:
    last_req = st.session_state.get("last_result")
    if not last_req and not df.empty:
        latest_row = df.iloc[0]
        last_req = {
            "prompt": latest_row.get("prompt", ""),
            "complexity_score": float(latest_row.get("complexity_score", 0.0) or 0.0),
            "classifier_confidence": float(latest_row.get("classifier_confidence", 0.0) or 0.0),
            "threshold": 0.5,
            "route": latest_row.get("route_taken", "local"),
            "model_name": latest_row.get("model_name") or ("qwen2.5:7b" if latest_row.get("route_taken") == "local" else latest_row.get("cloud_provider", "groq")),
            "cloud_provider": latest_row.get("cloud_provider", "none"),
            "fallback_reason": latest_row.get("fallback_reason"),
            "latency_ms": float(latest_row.get("latency_ms", 0.0) or 0.0),
            "classify_ms": float(latest_row.get("classify_ms", 0.0) or 0.0),
            "inference_ms": float(latest_row.get("inference_ms", 0.0) or 0.0),
            "response": latest_row.get("response_preview", ""),
            "id": latest_row.get("id", "latest")
        }

    if last_req:
        render_journey_panel(journey_container, state="completed", req_data=last_req)

st.divider()

# ============================================================================
# STEP 2: AGGREGATE OPERATIONAL PERFORMANCE & COST EFFICIENCY (KPIs)
# ============================================================================
st.markdown('<div class="step-header">📊 Step 2: System-Wide Operational KPIs & Cost Savings</div>', unsafe_allow_html=True)
st.markdown('<div class="step-caption">Real-time aggregate telemetry comparing actual execution costs against a hypothetical baseline where 100% of traffic is sent to cloud LLMs.</div>', unsafe_allow_html=True)

if df.empty:
    st.info("No data in router_logs.db yet. Use the prompt box above or click 'Run 20-Prompt Benchmark' to populate!")
else:
    # Convert units: USD to INR (approx 83.5) and ms to seconds
    df['estimated_cost_inr'] = df['estimated_cost_usd'] * 83.5
    df['latency_s'] = df['latency_ms'] / 1000.0

    # Clean numeric fields
    df['complexity_score'] = pd.to_numeric(df['complexity_score'], errors='coerce').fillna(0.0)
    df['classifier_confidence'] = pd.to_numeric(df['classifier_confidence'], errors='coerce').fillna(0.5)

    total_queries = len(df)
    local_df = df[df['route_taken'] == 'local']
    cloud_df = df[df['route_taken'] == 'cloud']

    local_count = len(local_df)
    cloud_count = len(cloud_df)

    groq_count = len(df[df['cloud_provider'] == 'groq'])
    gemini_count = len(df[df['cloud_provider'] == 'gemini'])
    local_fallback_count = len(df[df['fallback_reason'] == 'local_slm_unavailable'])

    # Cost Estimation in INR
    avg_cloud_cost = cloud_df['estimated_cost_inr'].mean() if not cloud_df.empty else 0.001
    actual_cost = df['estimated_cost_inr'].sum()
    potential_total_cost = actual_cost + (local_count * avg_cloud_cost)
    cost_saved = potential_total_cost - actual_cost

    # Cloud Calls Avoided share
    avoided_pct = (local_count / total_queries * 100) if total_queries > 0 else 0.0
    target_met = avoided_pct >= 40.0
    avoided_delta = "Target ≥40% (Met ✅)" if target_met else "Target ≥40% (Not Met ⚠️)"
    avoided_delta_color = "normal" if target_met else "inverse"

    # Dynamic delta label for Cloud Provider breakdown
    delta_parts = []
    if groq_count > 0:
        delta_parts.append(f"⚡ Groq: {groq_count}")
    if gemini_count > 0:
        delta_parts.append(f"✨ Gemini: {gemini_count}")
    if local_fallback_count > 0:
        delta_parts.append(f"⚠️ Fallbacks: {local_fallback_count}")
    cloud_delta = " | ".join(delta_parts) if delta_parts else "API Cost Incurred"
    cloud_delta_color = "normal" if gemini_count > 0 or local_fallback_count > 0 else "inverse"

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Requests", total_queries)
    m2.metric("Routed Local (SLM)", local_count, delta="Zero Cost (₹0.00)", delta_color="normal")
    m3.metric("Routed Cloud (LLM)", cloud_count, delta=cloud_delta, delta_color=cloud_delta_color)
    m4.metric("Total Cost Saved", f"₹{cost_saved:.4f}", delta="Estimated Net Savings", delta_color="normal")
    m5.metric("Cloud Calls Avoided", f"{avoided_pct:.1f}%", delta=avoided_delta, delta_color=avoided_delta_color)
    st.caption("ℹ️ **Cloud API Calls Avoided:** Share of requests handled locally by Ollama without incurring cloud API billing.")

    st.divider()

    # ============================================================================
    # STEP 3: COMPLEXITY CLASSIFIER ANALYSIS & BOUNDARIES
    # ============================================================================
    st.markdown('<div class="step-header">🎯 Step 3: Complexity Classification Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-caption">Visualizing the continuous complexity distribution [0.0 - 1.0]. Prompts at or above the 0.50 threshold gate are sent to Cloud LLMs; prompts below are served locally.</div>', unsafe_allow_html=True)

    col_class_chart, col_class_meta = st.columns([3, 1])

    with col_class_chart:
        plot_df = df.copy().sort_values('id')
        plot_df['Request Index'] = range(1, len(plot_df) + 1)
        plot_df['Confidence %'] = (plot_df['classifier_confidence'] * 100).round(1)

        scatter_points = alt.Chart(plot_df).mark_circle(size=75).encode(
            x=alt.X('Request Index:Q', title="Request Sequence (Chronological)"),
            y=alt.Y('complexity_score:Q', title="Complexity Score [0.0 - 1.0]", scale=alt.Scale(domain=[0.0, 1.05])),
            color=alt.Color('route_taken:N', scale=alt.Scale(domain=['local', 'cloud'], range=['#2e7b32', '#1565c0']), legend=alt.Legend(title="Assigned Route", orient="top")),
            tooltip=['id', 'prompt', 'complexity_score', 'Confidence %', 'route_taken', 'cloud_provider']
        )

        threshold_line = alt.Chart(pd.DataFrame({'y': [0.5]})).mark_rule(
            color='#d32f2f', strokeDash=[6, 4], strokeWidth=2
        ).encode(y='y:Q')

        combined_class_chart = (scatter_points + threshold_line).properties(height=280)
        st.altair_chart(combined_class_chart, use_container_width=True)
        st.caption("ℹ️ **Scores at or above the red line (0.50) go to the cloud.** Scores below 0.50 are routed to the local SLM.")

    with col_class_meta:
        latest_conf = float(df.iloc[0]['classifier_confidence']) if not df.empty else 0.5
        st.metric("Latest Classifier Confidence", f"{latest_conf * 100:.1f}%", delta="Confidence in Route", delta_color="normal")
        avg_score = df['complexity_score'].mean()
        st.metric("Average Complexity Score", f"{avg_score:.3f}", delta="Across All Logs", delta_color="off")
        active_mode = health_data.get("classifier_mode", "distilbert").upper() if health_data else "DISTILBERT"
        st.caption(f"Confidence represents model certainty `max(p, 1-p)`. Active classifier engine: **{active_mode}**.")

    st.divider()

    # ============================================================================
    # STEP 4: FINANCIAL & ENVIRONMENTAL IMPACT ANALYSIS
    # ============================================================================
    st.markdown('<div class="step-header">💰 Step 4: Financial & Environmental Impact Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-caption">Quantifying tangible savings in Indian Rupees (₹) and CO₂ emissions (grams) achieved by diverting routine traffic away from cloud clusters.</div>', unsafe_allow_html=True)

    # A. Cumulative Savings Trends
    st.markdown("**Cumulative Savings Trends (vs Sending 100% of Traffic to Cloud):**")
    trend_df = df.copy().sort_values('id')
    avg_cloud_co2 = cloud_df['co2_grams'].mean() if (not cloud_df.empty and cloud_df['co2_grams'].mean() > 0) else 0.35

    trend_df['step_cost_saved'] = trend_df['route_taken'].apply(lambda r: avg_cloud_cost if r == 'local' else 0.0)
    trend_df['cum_cost_saved'] = trend_df['step_cost_saved'].cumsum()

    trend_df['step_co2_saved'] = trend_df['route_taken'].apply(lambda r: avg_cloud_co2 if r == 'local' else 0.0)
    trend_df['cum_co2_saved'] = trend_df['step_co2_saved'].cumsum()

    trend_df['Request Seq'] = range(1, len(trend_df) + 1)

    col_trend1, col_trend2 = st.columns(2)
    with col_trend1:
        cost_trend_chart = alt.Chart(trend_df).mark_area(
            line={'color': '#2e7b32'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='#2e7b32', offset=0),
                       alt.GradientStop(color='rgba(46, 123, 50, 0.05)', offset=1)],
                x1=1, x2=1, y1=1, y2=0
            )
        ).encode(
            x=alt.X('Request Seq:Q', title="Request Sequence"),
            y=alt.Y('cum_cost_saved:Q', title="Cumulative Cost Saved (₹)"),
            tooltip=['Request Seq', alt.Tooltip('cum_cost_saved:Q', format='.4f', title='Cost Saved (₹)')]
        ).properties(height=220)
        st.altair_chart(cost_trend_chart, use_container_width=True)

    with col_trend2:
        co2_trend_chart = alt.Chart(trend_df).mark_area(
            line={'color': '#00897b'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='#00897b', offset=0),
                       alt.GradientStop(color='rgba(0, 137, 123, 0.05)', offset=1)],
                x1=1, x2=1, y1=1, y2=0
            )
        ).encode(
            x=alt.X('Request Seq:Q', title="Request Sequence"),
            y=alt.Y('cum_co2_saved:Q', title="Cumulative CO₂ Saved (Grams)"),
            tooltip=['Request Seq', alt.Tooltip('cum_co2_saved:Q', format='.3f', title='CO₂ Saved (g)')]
        ).properties(height=220)
        st.altair_chart(co2_trend_chart, use_container_width=True)

    st.write("")

    # B. Comparative Breakdown Charts
    col_chart1, col_chart2, col_chart3 = st.columns(3)

    with col_chart1:
        st.markdown("**Traffic Route Share:**")
        route_data = pd.DataFrame({
            'Route': ['Local (SLM)', 'Cloud (LLM)'],
            'Count': [local_count, cloud_count]
        })
        base = alt.Chart(route_data).encode(
            theta=alt.Theta("Count:Q", stack=True),
            color=alt.Color("Route:N", scale=alt.Scale(domain=['Local (SLM)', 'Cloud (LLM)'], range=['#2e7b32', '#1565c0']), legend=alt.Legend(title="Route Path", orient="bottom")),
            tooltip=['Route', 'Count']
        )
        pie = base.mark_arc(innerRadius=65, stroke="#fff")
        st.altair_chart(pie, use_container_width=True)

    with col_chart2:
        st.markdown("**Financial Impact (₹):**")
        cost_data = pd.DataFrame({
            'Scenario': ['Actual Cost', 'Cost if 100% Cloud'],
            'Cost (₹)': [actual_cost, potential_total_cost]
        })
        bar_chart = alt.Chart(cost_data).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
            x=alt.X('Scenario:N', axis=alt.Axis(labelAngle=0, title="")),
            y=alt.Y('Cost (₹):Q', axis=alt.Axis(title="Rupees (₹)")),
            color=alt.Color('Scenario:N', scale=alt.Scale(domain=['Actual Cost', 'Cost if 100% Cloud'], range=['#43a047', '#e53935']), legend=None),
            tooltip=['Scenario', 'Cost (₹)']
        ).properties(height=300)
        st.altair_chart(bar_chart, use_container_width=True)

    with col_chart3:
        st.markdown("**Average Latency (Seconds):**")
        avg_local_lat = local_df['latency_s'].mean() if not local_df.empty else 0
        avg_cloud_lat = cloud_df['latency_s'].mean() if not cloud_df.empty else 0

        latency_data = pd.DataFrame({
            'Route': ['Local (SLM)', 'Cloud (LLM)'],
            'Latency (s)': [avg_local_lat, avg_cloud_lat]
        })
        lat_chart = alt.Chart(latency_data).mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5).encode(
            y=alt.Y('Route:N', axis=alt.Axis(title="", labelAngle=0)),
            x=alt.X('Latency (s):Q', axis=alt.Axis(title="Seconds")),
            color=alt.Color('Route:N', scale=alt.Scale(domain=['Local (SLM)', 'Cloud (LLM)'], range=['#2e7b32', '#1565c0']), legend=None),
            tooltip=['Route', 'Latency (s)']
        ).properties(height=300)
        st.altair_chart(lat_chart, use_container_width=True)

    # C. Environmental Emissions Section
    actual_co2 = df['co2_grams'].sum()
    potential_cloud_co2 = actual_co2 + (local_count * avg_cloud_co2)
    co2_saved = potential_cloud_co2 - actual_co2
    total_energy = df['energy_kwh'].sum()

    st.write("")
    col_env1, col_env2 = st.columns([1, 2])
    with col_env1:
        st.markdown("**Environmental Carbon Telemetry:**")
        st.metric("Total CO₂ Saved", f"{co2_saved:.3f} g", delta="Estimated Net Savings vs 100% Cloud", delta_color="normal")
        st.metric("Total Energy Consumed", f"{total_energy:.6f} kWh", delta="Hardware Tracked + Cloud Est.", delta_color="off")
        st.caption("ℹ️ **Methodology:** Local SLM energy is directly measured via CodeCarbon hardware tracking. Cloud LLM emissions are statistically estimated (~0.35g CO₂ / 1,000 tokens) based on published data center research.")

    with col_env2:
        st.markdown("**Emissions Comparison (Grams CO₂):**")
        co2_data = pd.DataFrame({
            'Scenario': ['Actual Emissions', 'Emissions if 100% Cloud (Estimated)'],
            'CO2 (Grams)': [actual_co2, potential_cloud_co2]
        })
        co2_chart = alt.Chart(co2_data).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
            x=alt.X('Scenario:N', axis=alt.Axis(labelAngle=0, title="")),
            y=alt.Y('CO2 (Grams):Q', axis=alt.Axis(title="CO₂ (Grams)")),
            color=alt.Color('Scenario:N', scale=alt.Scale(domain=['Actual Emissions', 'Emissions if 100% Cloud (Estimated)'], range=['#2e7b32', '#e53935']), legend=None),
            tooltip=['Scenario', 'CO2 (Grams)']
        ).properties(height=230)
        st.altair_chart(co2_chart, use_container_width=True)

    st.divider()

    # ============================================================================
    # STEP 5: HISTORICAL AUDIT LOG & REQUEST TELEMETRY
    # ============================================================================
    st.markdown('<div class="step-header">📜 Step 5: Historical Request Audit Log</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-caption">Granular database audit of all logged requests in <code>router_logs.db</code>, capturing model resolution, costs, hardware carbon emissions, and latency.</div>', unsafe_allow_html=True)

    display_df = df.copy()
    display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%H:%M:%S')

    display_df['route_taken'] = display_df['route_taken'].apply(
        lambda x: '💻 Local (SLM)' if str(x).lower() == 'local' else '☁️ Cloud (LLM)'
    )

    def format_provider(row):
        route = row['route_taken']
        provider = str(row.get('cloud_provider', '')).lower()
        fallback = row.get('fallback_reason')
        model = row.get('model_name')
        if pd.notna(fallback) and str(fallback).strip() == 'local_slm_unavailable':
            prov_name = 'Gemini' if provider == 'gemini' else 'Groq'
            return f'⚠️ Local Fallback → Cloud ({prov_name})'
        if pd.notna(fallback) and str(fallback).strip() == 'cloud_llm_unavailable':
            return f'⚠️ Cloud Fallback → Local (Ollama)'
        if 'Local' in route:
            return f'💻 Ollama ({model or "qwen2.5:7b"})'
        elif provider == 'gemini':
            return f'✨ Gemini ({model or "gemini-3.8-flash"})'
        else:
            return f'⚡ Groq ({model or "gpt-oss-120b"})'

    display_df['Resolved Model / Provider'] = display_df.apply(format_provider, axis=1)

    def style_route(val):
        color = '#2e7b32' if 'Local' in str(val) else '#1565c0'
        return f'color: {color}; font-weight: bold'

    def style_provider(val):
        sval = str(val)
        if '⚠️' in sval:
            return 'color: #e65100; font-weight: bold'
        elif 'Gemini' in sval:
            return 'color: #6a1b9a; font-weight: bold'
        elif 'Groq' in sval:
            return 'color: #1565c0; font-weight: bold'
        elif 'Ollama' in sval:
            return 'color: #2e7b32; font-weight: bold'
        return ''

    styled_df = display_df.rename(columns={
        'timestamp': 'Time',
        'route_taken': 'Route',
        'complexity_score': 'Complexity',
        'classifier_confidence': 'Confidence',
        'latency_s': 'Latency (s)',
        'estimated_cost_inr': 'Cost (₹)',
        'co2_grams': 'CO₂ (g)',
        'prompt': 'Prompt',
        'response_preview': 'Response'
    })

    available_cols = [c for c in ['Time', 'Prompt', 'Complexity', 'Confidence', 'Route', 'Resolved Model / Provider', 'Cost (₹)', 'CO₂ (g)', 'Latency (s)', 'Response'] if c in styled_df.columns]

    st.dataframe(
        styled_df[available_cols].style
            .map(style_route, subset=['Route'] if 'Route' in available_cols else [])
            .map(style_provider, subset=['Resolved Model / Provider'] if 'Resolved Model / Provider' in available_cols else []),
        use_container_width=True,
        hide_index=True,
        height=360
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# STEP 6: ARCHITECTURE & METHODOLOGY REFERENCE
# ============================================================================
with st.expander("ℹ️ Step 6: Architecture & Methodology Reference", expanded=False):
    st.markdown("""
    ### The 6-Step Execution Lifecycle
    1. **Client Submission:** The client or UI submits a prompt (`ChatRequest`) to `POST /chat`.
    2. **Real-Time Complexity Scoring:**
       - Based on `CLASSIFIER_MODE` (`heuristic`, `ml`, or `distilbert`), a complexity score between `0.0` (purely factual / simple) and `1.0` (deep reasoning / algorithmic) is generated along with classification latency (`classify_ms`) and model confidence (`max(p, 1-p)`).
    3. **Threshold-Based Routing:**
       - **Score < 0.50:** Dispatched to the **Local SLM Pipeline**.
       - **Score ≥ 0.50:** Dispatched to the **Cloud LLM Pipeline**.
    4. **Resilient Local Execution & Hardware Telemetry:**
       - Local queries run on `qwen2.5:7b` via Ollama at **₹0 API cost**.
       - The `CodeCarbon` in-memory tracker samples real CPU/GPU power registers to compute true electrical energy consumed (kWh) and hardware CO₂ emissions (grams).
       - *Resilient Tier-1 Fallback:* If Ollama is offline, unreachable, or errors out, the request is caught and immediately rerouted to the Cloud LLM pipeline with `fallback_reason = "local_slm_unavailable"`.
    5. **High-Performance Cloud Execution & Provider Failover:**
       - Cloud requests hit **Groq** (`openai/gpt-oss-120b`) for sub-second LPU inference.
       - *Resilient Tier-2 Failover:* If Groq hits rate limits (HTTP 429), timeouts, or API outages, the request automatically falls over to **Google Gemini** (`gemini-3.8-flash`).
       - Cloud emissions are calculated using published data center averages (0.35g CO₂ and 0.0004 kWh per 1,000 tokens).
    6. **Audit Logging & Live Dashboard Telemetry:**
       - All operational metrics (route, model name, confidence, latency, cost, emissions, fallback reasons) are persisted to `requests_log` in `router_logs.db` with self-healing schema migrations.
    """)

if st.button("🔄 Refresh Dashboard Data", use_container_width=True):
    st.rerun()
