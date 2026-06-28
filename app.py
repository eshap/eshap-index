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

# Standardized baseline data parameters: { Platform: (All P13+, 55+ Layer) }
US_RAW = {
    "YOUTUBE": (2110.0, 490.0), "DISNEY": (1945.0, 1080.0), "NETFLIX": (1540.0, 380.0),
    "TIKTOK": (1480.0, 65.0), "PARAMOUNT": (1290.0, 810.0), "NBCU": (1265.0, 795.0),
    "INSTAGRAM": (1120.0, 110.0), "WBD": (1040.0, 685.0), "FACEBOOK": (995.0, 520.0),
    "AMAZON": (635.0, 215.0), "FOX": (425.0, 315.0)
}
FR_RAW = {
    "YOUTUBE": (485.0, 95.0), "TIKTOK": (335.0, 12.0), "NETFLIX": (390.0, 85.0),
    "INSTAGRAM": (215.0, 20.0), "TF1": (440.0, 270.0), "DISNEY": (180.0, 42.0),
    "FRANCE TV": (510.0, 385.0), "ARTE": (120.0, 57.6), "GROUP M6": (265.0, 145.0),
    "AMAZON": (155.0, 48.0), "WBD": (170.0, 95.0), "L'ÉQUIPE": (65.0, 19.5),
    "CANAL+ GROUP": (195.0, 115.0), "FACEBOOK": (165.0, 92.0), "DAZN": (20.0, 2.0)
}
UK_RAW = {
    "BBC": (640.0, 460.0), "YOUTUBE": (590.0, 110.0), "ITV": (510.0, 335.0),
    "NETFLIX": (495.0, 105.0), "TIKTOK": (410.0, 18.0), "SKY GROUP": (385.0, 210.0),
    "INSTAGRAM": (275.0, 28.0), "PARAMOUNT": (245.0, 155.0), "DISNEY": (235.0, 52.0),
    "WBD": (220.0, 128.0), "FACEBOOK": (210.0, 115.0), "AMAZON": (195.0, 62.0)
}
IT_RAW = {
    "Rai": (520.0, 415.0), "YOUTUBE": (440.0, 110.0), "MFE (Mediaset)": (415.0, 265.0),
    "TIKTOK": (295.0, 12.0), "NETFLIX": (310.0, 70.0), "INSTAGRAM": (250.0, 25.0),
    "SKY ITALIA": (175.0, 102.0), "DISNEY": (170.0, 38.0), "WBD": (165.0, 92.0),
    "FACEBOOK": (160.0, 101.0), "AMAZON": (140.0, 42.0)
}

DECAY = {"13-44": 0.78, "13-34": 0.54, "13-24": 0.32}

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
raw_set = {"United States": US_RAW, "France": FR_RAW, "United Kingdom": UK_RAW, "Italy": IT_RAW}.get(market_choice, US_RAW)

st.sidebar.markdown("### Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated\n## **MILLIONS OF HOURS**")
user_shifts = {}
for entity in raw_set.keys():
    user_shifts[entity] = st.sidebar.slider(f"{entity} Shift Impact", min_value=-200.0, max_value=200.0, value=0.0, step=5.0, key=f"{entity}_{st.session_state.get('reset_id', 0)}")

if st.sidebar.button("Reset Defaults"):
    st.session_state.reset_id = st.session_state.get('reset_id', 0) + 1
    st.rerun()

# AUTOMATED COMPACT PRO-RATA REALLOCATION ENGINE
matrix_data = []
active_shifts = {k: v for k, v in user_shifts.items() if v != 0.0}
total_shifted = sum(active_shifts.values())
non_shifted_pool = sum([v[0] for k, v in raw_set.items() if k not in active_shifts])

for entity, (p13, p55) in raw_set.items():
    if entity in active_shifts:
        adj_p13 = max(0.0, p13 + active_shifts[entity])
    else:
        share_weight = p13 / non_shifted_pool if non_shifted_pool > 0 else 0.0
        adj_p13 = max(0.0, p13 + (-total_shifted * share_weight))
    
    w54 = max(0.0, adj_p13 - p55)
    matrix_data.append({
        "Platform/Publisher": entity, "All P13+": adj_p13, "55+ Layer": p55,
        "13-54 Workforce": min(w54, adj_p13),
        "13-44 Youth": min(w54 * DECAY["13-44"], w54),
        "13-34 Core": min(w54 * DECAY["13-34"], w54 * DECAY["13-44"]),
        "13-24 Gen Z": min(w54 * DECAY["13-24"], w54 * DECAY["13-34"])
    })
df_matrix = pd.DataFrame(matrix_data)

net_balance = df_matrix["All P13+"].sum() - sum([v[0] for v in raw_set.values()])
if abs(net_balance) > 0.1: st.sidebar.warning(f"Simulated Shift Imbalance: {net_balance:+.1f}M Hours")
else: st.sidebar.success("Zero-Sum Balance Maintained")

tab1, tab2 = st.tabs(["CSAI Interactive Index Matrix", "Index Architecture & Methodology"])
with tab1:
    st.subheader(f"Cross-Screen Attention Allocation Ledger — {market_choice}")
    st.markdown("<p style='font-size: 0.85rem; font-weight: bold; margin-top: -0.75rem; margin-bottom: 1rem; color: #555555;'>Click Header To Reorder By Column</p>", unsafe_allow_html=True)
    st.dataframe(df_matrix.style.format({col: "{:,.1f}" for col in df_matrix.columns if col != "Platform/Publisher"}), use_container_width=True, hide_index=True)
    st.download_button(label="Export Current Ledger to CSV", data=df_matrix.to_csv(index=False).encode('utf-8'), file_name=f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv", mime="text/csv", use_container_width=True)
    st.write("")
    st.markdown("#### Interactive Visual Share Map")
    demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
    selected_demo = st.radio("Select Demographic Cohort to Isolate in Bar Chart:", options=["Show All Cohorts Overlaid"] + demo_columns, horizontal=True)
    chart_df = df_matrix.set_index("Platform/Publisher")
    chart_metrics = ["All P13+", "13-54 Workforce", "55+ Layer"] if selected_demo == "Show All Cohorts Overlaid" else [selected_demo]
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
