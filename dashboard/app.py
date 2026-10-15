import streamlit as st
import sqlite3
import pandas as pd
import os
import altair as alt

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "router_logs.db")

st.set_page_config(page_title="Hybrid SLM-LLM Router", layout="wide", page_icon="⚡")

# --- HEADER SECTION ---
st.title("⚡ Hybrid SLM-LLM Router")
st.caption("Dynamic Request Routing with Automatic Failover & Environmental Carbon Tracking")

# Custom CSS for the metric cards to give them a shadow/border
st.markdown("""
<style>
div[data-testid="metric-container"] {
    background-color: #f8f9fa;
    border: 1px solid #e0e0e0;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
}
/* For dark mode compatibility */
@media (prefers-color-scheme: dark) {
    div[data-testid="metric-container"] {
        background-color: #1e1e1e;
        border: 1px solid #333;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

def load_data():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM requests_log ORDER BY id DESC", conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.info("Waiting for data... Run your test script to populate the dashboard!")
else:
    # Ensure new columns exist even if reading an older database
    if 'cloud_provider' not in df.columns:
        df['cloud_provider'] = 'none'
    if 'co2_grams' not in df.columns:
        df['co2_grams'] = 0.0
    if 'energy_kwh' not in df.columns:
        df['energy_kwh'] = 0.0

    # Convert units: USD to INR (approx 83.5) and ms to seconds
    df['estimated_cost_inr'] = df['estimated_cost_usd'] * 83.5
    df['latency_s'] = df['latency_ms'] / 1000.0

    # --- TOP METRICS ---
    total_queries = len(df)
    local_df = df[df['route_taken'] == 'local']
    cloud_df = df[df['route_taken'] == 'cloud']
    
    local_count = len(local_df)
    cloud_count = len(cloud_df)
    
    # Provider breakdown for cloud calls
    groq_count = len(df[df['cloud_provider'] == 'groq'])
    gemini_count = len(df[df['cloud_provider'] == 'gemini'])
    
    # Cost Estimation in INR
    avg_cloud_cost = cloud_df['estimated_cost_inr'].mean() if not cloud_df.empty else 0.001
    actual_cost = df['estimated_cost_inr'].sum()
    
    potential_total_cost = actual_cost + (local_count * avg_cloud_cost)
    cost_saved = potential_total_cost - actual_cost
    
    # Dynamic delta label for Cloud Provider breakdown
    if gemini_count > 0:
        cloud_delta = f"⚡ Groq: {groq_count} | ✨ Gemini: {gemini_count} (Failover)"
        cloud_delta_color = "normal"
    else:
        cloud_delta = f"⚡ Groq: {groq_count}" if groq_count > 0 else "API Cost Incurred"
        cloud_delta_color = "inverse"

    # Top metric cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Requests", total_queries)
    m2.metric("Routed Local (SLM)", local_count, delta="Zero Cost", delta_color="normal")
    m3.metric("Routed Cloud (LLM)", cloud_count, delta=cloud_delta, delta_color=cloud_delta_color)
    m4.metric("Total Cost Saved", f"₹{cost_saved:.4f}", delta="Estimated", delta_color="normal")
    
    st.divider()
    
    # --- VISUALIZATIONS ---
    col_chart1, col_chart2, col_chart3 = st.columns(3)
    
    with col_chart1:
        st.subheader("Traffic Routing Distribution")
        route_data = pd.DataFrame({
            'Route': ['Local (SLM)', 'Cloud (LLM)'],
            'Count': [local_count, cloud_count]
        })
        base = alt.Chart(route_data).encode(
            theta=alt.Theta("Count:Q", stack=True),
            color=alt.Color("Route:N", scale=alt.Scale(domain=['Local (SLM)', 'Cloud (LLM)'], range=['#2e7b32', '#1565c0']), legend=alt.Legend(title="Route Path", orient="bottom")),
            tooltip=['Route', 'Count']
        )
        pie = base.mark_arc(innerRadius=70, stroke="#fff")
        st.altair_chart(pie, use_container_width=True)
        
    with col_chart2:
        st.subheader("Financial Impact")
        cost_data = pd.DataFrame({
            'Scenario': ['Actual Cost', 'Cost if 100% Cloud'],
            'Cost (₹)': [actual_cost, potential_total_cost]
        })
        bar_chart = alt.Chart(cost_data).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
            x=alt.X('Scenario:N', axis=alt.Axis(labelAngle=0, title="")),
            y=alt.Y('Cost (₹):Q', axis=alt.Axis(title="Rupees (₹)")),
            color=alt.Color('Scenario:N', scale=alt.Scale(domain=['Actual Cost', 'Cost if 100% Cloud'], range=['#43a047', '#e53935']), legend=None),
            tooltip=['Scenario', 'Cost (₹)']
        ).properties(height=350)
        st.altair_chart(bar_chart, use_container_width=True)
        
    with col_chart3:
        st.subheader("Average Speed (Latency)")
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
        ).properties(height=350)
        st.altair_chart(lat_chart, use_container_width=True)
        
    st.divider()

    # --- ENVIRONMENTAL IMPACT SECTION (CodeCarbon) ---
    st.subheader("🌱 Environmental Impact (Carbon Footprint)")
    
    actual_co2 = df['co2_grams'].sum()
    avg_cloud_co2 = cloud_df['co2_grams'].mean() if (not cloud_df.empty and cloud_df['co2_grams'].mean() > 0) else 0.35
    potential_cloud_co2 = actual_co2 + (local_count * avg_cloud_co2)
    co2_saved = potential_cloud_co2 - actual_co2
    total_energy = df['energy_kwh'].sum()

    col_env1, col_env2 = st.columns([1, 2])
    with col_env1:
        st.metric("Total CO₂ Saved", f"{co2_saved:.3f} g", delta="Estimated Savings vs 100% Cloud", delta_color="normal")
        st.metric("Total Energy Consumed", f"{total_energy:.6f} kWh", delta="Hardware Tracked + Cloud Est.", delta_color="off")
        st.caption("ℹ️ **Measurement Methodology:** Local SLM energy is directly measured via CodeCarbon hardware tracking. Cloud LLM emissions are statistically estimated (~0.35g CO₂ / 1,000 tokens) based on published data center research.")

    with col_env2:
        co2_data = pd.DataFrame({
            'Scenario': ['Actual Emissions', 'Emissions if 100% Cloud (Estimated)'],
            'CO2 (Grams)': [actual_co2, potential_cloud_co2]
        })
        co2_chart = alt.Chart(co2_data).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
            x=alt.X('Scenario:N', axis=alt.Axis(labelAngle=0, title="")),
            y=alt.Y('CO2 (Grams):Q', axis=alt.Axis(title="CO₂ (Grams)")),
            color=alt.Color('Scenario:N', scale=alt.Scale(domain=['Actual Emissions', 'Emissions if 100% Cloud (Estimated)'], range=['#2e7b32', '#e53935']), legend=None),
            tooltip=['Scenario', 'CO2 (Grams)']
        ).properties(height=260)
        st.altair_chart(co2_chart, use_container_width=True)

    st.divider()

    # --- TRAFFIC MONITOR CHART ---
    st.subheader("Live Traffic Monitor")
    
    monitor_df = df.copy().sort_values('id')
    monitor_df['Request ID'] = monitor_df['id'].astype(str)
    
    traffic_chart = alt.Chart(monitor_df).mark_bar(size=20, cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X('Request ID:N', sort=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y('latency_s:Q', axis=alt.Axis(title="Latency (s)")),
        color=alt.Color('route_taken:N', scale=alt.Scale(domain=['local', 'cloud'], range=['#2e7b32', '#1565c0']), legend=alt.Legend(title="Route", orient="top")),
        tooltip=['prompt', 'latency_s', 'route_taken', 'cloud_provider']
    ).properties(height=250)
    
    st.altair_chart(traffic_chart, use_container_width=True)
    
    st.divider()

    # --- RAW DATA SECTION ---
    st.subheader("Live Request Log")
    
    display_df = df.copy()
    display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%H:%M:%S')
    
    # Add visual icons to the routing
    display_df['route_taken'] = display_df['route_taken'].apply(
        lambda x: '💻 Local (SLM)' if x.lower() == 'local' else '☁️ Cloud (LLM)'
    )

    # Format cloud provider display
    def format_provider(row):
        route = row['route_taken']
        provider = str(row['cloud_provider']).lower()
        if 'Local' in route:
            return '💻 Ollama (Local)'
        elif provider == 'gemini':
            return '✨ Gemini (Failover)'
        else:
            return '⚡ Groq (Primary)'

    display_df['Provider'] = display_df.apply(format_provider, axis=1)
    
    # Style the dataframe: color the route column
    def style_route(val):
        color = '#2e7b32' if 'Local' in str(val) else '#1565c0'
        return f'color: {color}; font-weight: bold'
        
    styled_df = display_df.rename(columns={
        'timestamp': 'Time',
        'route_taken': 'Route',
        'complexity_score': 'Complexity',
        'latency_s': 'Latency (s)',
        'estimated_cost_inr': 'Cost (₹)',
        'co2_grams': 'CO₂ (g)',
        'prompt': 'Prompt',
        'response_preview': 'Response'
    })
    
    st.dataframe(
        styled_df[['Time', 'Prompt', 'Complexity', 'Route', 'Provider', 'Cost (₹)', 'CO₂ (g)', 'Latency (s)', 'Response']].style.map(style_route, subset=['Route']),
        use_container_width=True,
        hide_index=True,
        height=400
    )

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 Refresh Data", use_container_width=True):
    st.rerun()
