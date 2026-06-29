import streamlit as st
import pandas as pd
import base64, os, io

def load_text_asset(filename, default_text=""):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content: return content
    return default_text

st.set_page_config(page_title="ESHAP CSAI Dashboard", layout="wide")

# Exact German Parameter Matrix Map Block
DE_BASE = [
    ["ARD", 710.0, 560.0, 150.0, 115.5, 90.1, 57.6],
    ["YOUTUBE", 625.0, 135.0, 490.0, 343.0, 267.5, 163.2],
    ["ZDF", 615.0, 505.0, 110.0, 84.7, 66.1, 42.2],
    ["RTL GROUP", 510.0, 310.0, 200.0, 150.0, 108.0, 49.0],
    ["NETFLIX", 445.0, 95.0, 350.0, 255.5, 160.9, 82.1],
    ["TIKTOK", 385.0, 14.0, 371.0, 289.4, 237.3, 173.2],
    ["PROSIEBENS", 340.0, 195.0, 145.0, 107.3, 73.0, 31.2],
    ["INSTAGRAM", 295.0, 28.0, 267.0, 232.3, 188.2, 103.5],
    ["AMAZON", 230.0, 68.0, 162.0, 132.8, 82.3, 34.6],
    ["DISNEY", 195.0, 42.0, 153.0, 116.3, 73.3, 30.3],
    ["WBD (MAX/I", 145.0, 78.0, 67.0, 48.9, 30.8, 12.7],
    ["FACEBOOK", 140.0, 82.0, 58.0, 31.9, 11.8, 2.2]
]

# Exact Spain Parameters Bound Directly From Your Document Panels
ES_BASE = [
    ["RTVE (Radiot", 395.0, 295.0, 100.0, 77.0, 55.4, 35.5],
    ["ATRESMEDIA", 380.0, 235.0, 145.0, 108.8, 78.3, 39.5],
    ["YOUTUBE", 365.0, 85.0, 280.0, 196.0, 152.9, 93.3],
    ["MEDIASET ES", 320.0, 198.0, 122.0, 91.5, 65.9, 33.3],
    ["TIKTOK", 255.0, 10.0, 245.0, 191.1, 156.7, 114.4],
    ["NETFLIX", 240.0, 52.0, 188.0, 137.2, 86.5, 44.1],
    ["INSTAGRAM", 215.0, 20.0, 195.0, 169.7, 137.5, 75.6],
    ["MOVISTAR+ (", 145.0, 82.0, 63.0, 44.1, 26.5, 11.1],
    ["DISNEY", 115.0, 24.0, 91.0, 69.2, 43.6, 18.0],
    ["WBD (MAX)", 105.0, 55.0, 50.0, 36.5, 23.0, 9.6],
    ["AMAZON", 95.0, 28.0, 67.0, 54.9, 34.0, 14.3],
    ["FACEBOOK", 90.0, 55.0, 35.0, 19.3, 7.1, 1.3]
]

bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    with open("planet_bullet.png", "rb") as b_f: bullet_base64 = base64.b64encode(b_f.read()).decode()
if bullet_base64:
    st.html("""
        <style>
        span[data-testid='stWidgetLabel'] p, 
        button[data-testid='stBaseButton-secondary'] p, 
        [data-baseweb='tab'] p {
            position: relative;
            padding-left: 1.5rem !important;
        }
        span[data-testid='stWidgetLabel'] p::before, 
        button[data-testid='stBaseButton-secondary'] p::before, 
        [data-baseweb='tab'] p::before {
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 16px;
            height: 16px;
            background-size: contain;
            background-repeat: no-repeat;
            background-image: url('data:image/png;base64,""" + bullet_base64 + """') !important;
        }
        </style>
        """)

logo_base64 = ""
if os.path.exists("eshap_map.png"):
    with open("eshap_map.png", "rb") as img_f: logo_base64 = base64.b64encode(img_f.read()).decode()

if logo_base64:
    st.sidebar.html("""
        <style>
        div.sidebar-logo-container {
            width: 100% !important;
            margin: 0 0 1rem 0 !important;
            padding: 0 !important;
            text-align: center !important;
        }
        div.sidebar-logo-container img {
            max-width: 100% !important;
            height: auto !important;
        }
        </style>
        <div class="sidebar-logo-container">
            <img src="data:image/png;base64,""" + logo_base64 + """">
        </div>
        """)

st.html("<style>h1[id='eshap-cross-screen-attention-index-escai'] { white-space: nowrap !important; font-size: 2.25rem !important; }</style>")
st.title("ESHAP Cross-Screen Attention Index (ESCAI)")
st.markdown("<p style='font-size: 0.85rem; font-weight: bold; margin-top: -1rem; margin-bottom: 1.5rem; color: #555555;'>(ESCAI is pronounced \"EE-say\" - the C is silent)</p>", unsafe_allow_html=True)
market_choice = st.sidebar.radio("Territory", ["Germany", "Spain"])
cols = ["Platform/Publisher", "All P13+", "55+ Layer", "13-54 Workforce", "13-44 Youth", "13-34 NextGen", "13-24 Gen Z"]

if market_choice == "Germany": df_matrix = pd.DataFrame(DE_BASE, columns=cols)
else: df_matrix = pd.DataFrame(ES_BASE, columns=cols)

df_matrix[cols[1:]] = df_matrix[cols[1:]].astype(float)
df_static_base = df_matrix.copy()

st.sidebar.markdown("### Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated\n## **MILLIONS OF HOURS**")
user_shifts = {}
for entity in df_matrix["Platform/Publisher"].unique():
    user_shifts[entity] = st.sidebar.slider(f"{entity} Shift Impact", min_value=-200.0, max_value=200.0, value=0.0, step=5.0, key=f"{entity}_{st.session_state.get('reset_id', 0)}")

if st.sidebar.button("Reset Defaults"):
    st.session_state.reset_id = st.session_state.get('reset_id', 0) + 1
    st.rerun()

active_shifts = {k: float(v) for k, v in user_shifts.items() if v != 0.0}
if active_shifts:
    for entity, shift_val in active_shifts.items():
        idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
        if len(idx) > 0:
            p13_orig = df_static_base.loc[idx, "All P13+"].values
            adj_p13 = max(0.0, p13_orig + shift_val)
            ratio = adj_p13 / p13_orig if p13_orig > 0 else 1.0
            df_matrix.loc[idx, "All P13+"] = adj_p13
            df_matrix.loc[idx, "13-54 Workforce"] = max(0.0, adj_p13 - df_static_base.loc[idx, "55+ Layer"].values)
            df_matrix.loc[idx, "13-44 Youth"] = df_static_base.loc[idx, "13-44 Youth"].values * ratio
            df_matrix.loc[idx, "13-34 NextGen"] = df_static_base.loc[idx, "13-34 NextGen"].values * ratio
            df_matrix.loc[idx, "13-24 Gen Z"] = df_static_base.loc[idx, "13-24 Gen Z"].values * ratio

    total_shifted_hours = sum(active_shifts.values())
    non_shifted_df = df_static_base[~df_static_base["Platform/Publisher"].isin(active_shifts.keys())]
    total_non_shifted_pool = non_shifted_df["All P13+"].sum()

    if total_non_shifted_pool > 0 and abs(total_shifted_hours) > 0.01:
        for entity in non_shifted_df["Platform/Publisher"].unique():
            idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
            p13_orig = df_static_base.loc[idx, "All P13+"].values
            pro_rata_weight = p13_orig / total_non_shifted_pool
            absorbed_share = -total_shifted_hours * pro_rata_weight
            adj_p13 = max(0.0, p13_orig + absorbed_share)
            ratio = adj_p13 / p13_orig if p13_orig > 0 else 1.0
            df_matrix.loc[idx, "All P13+"] = adj_p13
            df_matrix.loc[idx, "13-54 Workforce"] = max(0.0, adj_p13 - df_static_base.loc[idx, "55+ Layer"].values)
            df_matrix.loc[idx, "13-44 Youth"] = df_static_base.loc[idx, "13-44 Youth"].values * ratio
            df_matrix.loc[idx, "13-34 NextGen"] = df_static_base.loc[idx, "13-34 NextGen"].values * ratio
            df_matrix.loc[idx, "13-24 Gen Z"] = df_static_base.loc[idx, "13-24 Gen Z"].values * ratio

df_matrix[cols[1:]] = df_matrix[cols[1:]].round(1)
net_balance = df_matrix["All P13+"].sum() - df_static_base["All P13+"].sum()
if abs(net_balance) > 0.1: st.sidebar.warning(f"Simulated Shift Imbalance: {net_balance:+.1f}M Hours")
else: st.sidebar.success("Zero-Sum Balance Maintained")

tab1, tab2 = st.tabs(["CSAI Interactive Index Matrix", "Index Architecture & Methodology"])
with tab1:
    st.subheader(f"Cross-Screen Attention Allocation Ledger — {market_choice}")
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
    st.download_button(label="Export Current Ledger to CSV", data=df_matrix.to_csv(index=False).encode('utf-8'), file_name=f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv", mime="text/csv", use_container_width=True)
    st.write("")
    st.markdown("#### Interactive Visual Share Map")
    
    st.html("<style>div[data-testid='stRadio'] > div { gap: 1.5rem !important; } div[data-testid='stRadio'] label p { font-size: 0.95rem !important; white-space: nowrap !important; }</style>")
    
    demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
    selected_demo = st.radio("Select Demographic Cohort to Isolate in Bar Chart:", options=["All Cohorts Overlaid"] + demo_columns, horizontal=True)
    chart_df = df_matrix.set_index("Platform/Publisher")
    
    chart_metrics = ["All P13+", "13-54 Workforce", "55+ Layer"] if selected_demo == "All Cohorts Overlaid" else [selected_demo]
    st.bar_chart(chart_df[chart_metrics], horizontal=True, height=380)

with tab2:
    sub_method, sub_source = st.tabs(["Methodology Framework", "Sourcing Matrix"])
    w_map = {"Germany": ("61.5%", "38.5%", "de"), "Spain": ("62.0%", "38.0%", "sp")}
    weight_info = w_map.get(market_choice, ("61.5%", "38.5%", "de"))
    with sub_method:
        st.markdown("### METHODOLOGY: CARTOGRAPHER'S BLUEPRINT")
        st.markdown(f"**Territorial Demographic Weight:** {weight_info[0]} of Population is ≤ 54 Years Old ({weight_info[1]} is ≥ 55)")
        st.write(load_text_asset(f"methodology_{weight_info[2]}.txt", f"{market_choice} methodology text loading..."))
    with sub_source:
        st.markdown("### DATA SOURCES")
        st.write(load_text_asset(f"sources_{weight_info[2]}.txt", f"{market_choice} sourcing data loading..."))
