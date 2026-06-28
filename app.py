import streamlit as st
import pandas as pd
import base64
import os

def load_text_asset(filename, default_text=""):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content: return content
    return default_text

st.set_page_config(page_title="ESHAP CSAI Dashboard", layout="wide")

@st.cache_data
def fetch_complete_matrix_from_excel(file_path, sheet_name):
    fb = pd.DataFrame(columns=["Platform/Publisher", "All P13+", "55+ GenX+", "13-54 Workforce", "13-44 Youth", "13-34 NextGen", "13-24 Gen A/Z"])
    if not os.path.exists(file_path): return fb
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df.columns = df.columns.str.strip()
        cl = {}
        for col in df.columns:
            low = col.lower()
            if "platform" in low or "publisher" in low or "entity" in low: cl[col] = "Platform/Publisher"
            elif "p13" in low or "all" in low: cl[col] = "All P13+"
            elif "55+" in low or "layer" in low or "retirement" in low or "genx" in low: cl[col] = "55+ GenX+"
            elif "13-54" in low or "workforce" in low or "labor" in low: cl[col] = "13-54 Workforce"
            elif "13-44" in low or "youth" in low: cl[col] = "13-44 Youth"
            elif "13-34" in low or "core" in low or "nextgen" in low: cl[col] = "13-34 NextGen"
            elif "13-24" in low or "z" in low or "a/z" in low: cl[col] = "13-24 Gen A/Z"
        df = df.rename(columns=cl)
        if "Platform/Publisher" in df.columns:
            df["Platform/Publisher"] = df["Platform/Publisher"].astype(str).str.strip().str.upper()
        num_cols = ["All P13+", "55+ GenX+", "13-54 Workforce", "13-44 Youth", "13-34 NextGen", "13-24 Gen A/Z"]
        for c in num_cols:
            if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)
        return df[["Platform/Publisher"] + [col for col in num_cols if col in df.columns]]
    except: return fb

bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    with open("planet_bullet.png", "rb") as b_f: bullet_base64 = base64.b64encode(b_f.read()).decode()
if bullet_base64:
    st.html("<style>span[data-testid='stWidgetLabel'] p, button[data-testid='stBaseButton-secondary'] p, [data-baseweb='tab'] p { position: relative; padding-left: 1.5rem !important; } span[data-testid='stWidgetLabel'] p::before, button[data-testid='stBaseButton-secondary'] p::before, [data-baseweb='tab'] p::before { content: ''; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; background-size: contain; background-repeat: no-repeat; background-image: url('data:image/png;base64," + bullet_base64 + "') !important; }</style>")

logo_base64 = ""
if os.path.exists("eshap_map.png"):
    with open("eshap_map.png", "rb") as img_f: logo_base64 = base64.b64encode(img_f.read()).decode()
if logo_base64:
    st.markdown(f"<div style='display: flex; align-items: center; justify-content: space-between; gap: 1rem; width: 100%;'><h1 style='margin: 0; padding: 0;'>ESHAP Cross-Screen Attention Index (CSAI)</h1><img src='data:image/png;base64,{logo_base64}' style='max-width: 15%; height: auto; object-fit: contain;' /></div>", unsafe_allow_html=True)
else: st.title("ESHAP Cross-Screen Attention Index (CSAI)")
st.write("")

market_choice = st.sidebar.radio("Select Market Territory Component", ["United States", "France", "United Kingdom", "Italy"])
df_matrix = fetch_complete_matrix_from_excel("eshap_index_data.xlsx", market_choice)

st.sidebar.markdown("### Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated\n## **MILLIONS OF HOURS**")
user_shifts = {}
if not df_matrix.empty and "Platform/Publisher" in df_matrix.columns:
    for entity in df_matrix["Platform/Publisher"].unique():
        user_shifts[entity] = st.sidebar.slider(f"{entity} Shift Impact", min_value=-200.0, max_value=200.0, value=0.0, step=5.0, key=f"{entity}_{st.session_state.get('reset_id', 0)}")

if st.sidebar.button("Reset Defaults"):
    st.session_state.reset_id = st.session_state.get('reset_id', 0) + 1
    st.rerun()

# FIXED: Standardized matrix adjustments to properly mutate float scalar rows
if not df_matrix.empty and user_shifts:
    for entity, shift_val in user_shifts.items():
        if shift_val != 0.0:
            idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
            if len(idx) > 0:
                p13_orig = float(df_matrix.loc[idx[0], "All P13+"])
                if p13_orig > 0:
                    adj_p13 = max(0.0, p13_orig + shift_val)
                    ratio = adj_p13 / p13_orig
                    df_matrix.loc[idx[0], "All P13+"] = adj_p13
                    df_matrix.loc[idx[0], "13-54 Workforce"] = max(0.0, adj_p13 - float(df_matrix.loc[idx[0], "55+ GenX+"]))
                    df_matrix.loc[idx[0], "13-44 Youth"] = max(0.0, float(df_matrix.loc[idx[0], "13-44 Youth"]) * ratio)
                    df_matrix.loc[idx[0], "13-34 NextGen"] = max(0.0, float(df_matrix.loc[idx[0], "13-34 NextGen"]) * ratio)
                    df_matrix.loc[idx[0], "13-24 Gen A/Z"] = max(0.0, float(df_matrix.loc[idx[0], "13-24 Gen A/Z"]) * ratio)

net_balance = sum(user_shifts.values()) if user_shifts else 0.0
if abs(net_balance) > 0.001: st.sidebar.warning(f"Simulated Shift Imbalance: {net_balance:+.1f}M Hours")
else: st.sidebar.success("Zero-Sum Balance Maintained")

tab1, tab2 = st.tabs(["CSAI Interactive Index Matrix", "Index Architecture & Methodology"])
with tab1:
    st.subheader(f"Cross-Screen Attention Allocation Ledger — {market_choice}")
    st.markdown("<p style='font-size: 0.85rem; font-weight: bold; margin-top: -0.75rem; margin-bottom: 1rem; color: #555555;'>Click Header To Reorder By Column</p>", unsafe_allow_html=True)
    st.dataframe(df_matrix.style.format({col: "{:,.1f}" for col in df_matrix.columns if col != "Platform/Publisher"}), use_container_width=True, hide_index=True)
    if st.download_button(label="Export Current Ledger to CSV", data=df_matrix.to_csv(index=False).encode('utf-8'), file_name=f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv", mime="text/csv", use_container_width=True): pass
    st.write("")
    st.markdown("#### Interactive Visual Share Map")
    demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
    selected_demo = st.radio("Select Demographic Cohort to Isolate in Bar Chart:", options=["Show All Cohorts Overlaid"] + demo_columns, horizontal=True)
    chart_df = df_matrix.set_index("Platform/Publisher")
    chart_metrics = ["All P13+", "13-54 Workforce", "55+ GenX+"] if selected_demo == "Show All Cohorts Overlaid" else [selected_demo]
    st.bar_chart(chart_df[chart_metrics], horizontal=True, height=380)

with tab2:
    sub_method, sub_source = st.tabs(["Methodology Framework", "Sourcing Matrix"])
    with sub_method:
        st.markdown("### METHODOLOGY")
        w_map = {"United States": ("64.2%", "35.8%", "us"), "France": ("65.1%", "34.9%", "fr"), "United Kingdom": ("63.8%", "36.2%", "uk"), "Italy": ("59.8%", "40.2%", "it")}
        weight_info = w_map.get(market_choice, ("64.2%", "35.8%", "us"))
        st.markdown(f"**Territorial Demographic Weight:** {weight_info[0]} of Population is ≤ 54 Years Old ({weight_info[1]} is ≥ 55)")
        st.write(load_text_asset(f"methodology_{weight_info[2]}.txt", f"{market_choice} methodology asset file missing."))
    with sub_source:
        st.markdown("### DATA SOURCES")
        st.write(load_text_asset(f"sources_{w_map.get(market_choice, ('','','us'))[2]}.txt", f"{market_choice} sources asset file missing."))
