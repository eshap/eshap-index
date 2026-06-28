import streamlit as st
import pandas as pd
import base64, os

def load_text_asset(filename, default_text=""):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content: return content
    return default_text

st.set_page_config(page_title="ESHAP CSAI Dashboard", layout="wide")

# Compressed Parameter Arrays Encoded Directly From Document Panels
US_BASE = [["YOUTUBE",2110,490,1620,1134,884.5,539.5],["DISNEY",1945,1080,865,657.4,447,228],["NETFLIX",1540,380,1160,846.8,533.5,272.1],["TIKTOK",1480,65,1415,1103.7,905,660.7],["PARAMOUNT",1290,810,480,331.2,195.4,86],["NBCU",1265,795,470,319.6,185.4,76],["INSTAGRAM",1120,110,1010,878.7,711.7,391.4],["WBD",1040,685,355,241.4,120.7,50.7],["FACEBOOK",995,520,475,261.3,96.7,18.4],["AMAZON",635,215,420,344.4,213.5,89.7],["FOX",425,315,110,55,24.8,5.0]]
FR_BASE = [["YOUTUBE",485,95,390,273,212.9,129.9],["TIKTOK",335,12,323,251.9,206.6,150.8],["NETFLIX",390,85,305,222.7,140.3,71.6],["INSTAGRAM",215,20,195,169.7,137.5,75.6],["TF1",440,270,170,136,102,51.8],["DISNEY",180,42,138,104.9,66.1,27.3],["FRANCE TV",510,385,125,102.5,82,54.2],["ARTE",120,57.6,62.4,48,33.6,10.1],["GROUP M6",265,145,120,93.6,65.5,29.5],["AMAZON",155,48,107,87.7,54.4,22.8],["WBD",170,95,75,54.8,34.5,14.3],["L'ÉQUIPE",65,19.5,45.5,33.7,21.6,8.9],["CANAL+ GROUP",195,115,80,58.4,40.9,13.9],["FACEBOOK",165,92,73,40.2,14.9,2.8],["DAZN",20,2,18,16.2,12.8,7.7]]
UK_BASE = [["BBC",640,460,180,122.4,85.7,45.4],["YOUTUBE",590,110,480,336,262.1,159.9],["ITV",510,335,175,113.8,75.1,36.8],["NETFLIX",495,105,390,284.7,179.4,91.5],["TIKTOK",410,18,392,305.8,250.7,183.0],["SKY GROUP",385,210,175,119,70.2,28.8],["INSTAGRAM",275,28,247,214.9,174.1,95.8],["PARAMOUNT",245,155,90,61.2,36.1,14.8],["DISNEY",235,52,183,139.1,87.6,36.2],["WBD",220,128,92,62.6,31.3,13.1],["FACEBOOK",210,115,95,52.3,19.3,3.7],["AMAZON",195,62,133,109.1,67.6,28.4]]
IT_BASE = [["Rai",520,415,105,80.9,58.2,37.2],["YOUTUBE",440,110,330,231,180.2,109.9],["MFE (Mediaset)",415,265,150,112.5,81.0,40.8],["TIKTOK",295,12,283,220.7,181.0,132.1],["NETFLIX",310,70,240,175.2,110.4,56.3],["INSTAGRAM",250,25,225,195.8,158.6,87.2],["SKY ITALIA",175,102,73,50.4,29.7,12.2],["DISNEY",170,38,132,100.3,63.2,26.1],["WBD",165,92,73,51.1,31.7,12.9],["FACEBOOK",160,101,59,32.5,12.0,2.3],["AMAZON",140,42,98,80.4,49.8,20.9]]

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
cols = ["Platform/Publisher", "All P13+", "55+ Layer", "13-54 Workfc", "13-44 Youth", "13-34 Core", "13-24 Gen Z"]

if market_choice == "United States": df_matrix = pd.DataFrame(US_BASE, columns=cols)
elif market_choice == "France": df_matrix = pd.DataFrame(FR_BASE, columns=cols)
elif market_choice == "United Kingdom": df_matrix = pd.DataFrame(UK_BASE, columns=cols)
else: df_matrix = pd.DataFrame(IT_BASE, columns=cols)

df_static_base = df_matrix.copy()

st.sidebar.markdown("### Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated\n## **MILLIONS OF HOURS**")
user_shifts = {}
for entity in df_matrix["Platform/Publisher"].unique():
    user_shifts[entity] = st.sidebar.slider(f"{entity} Shift Impact", min_value=-200.0, max_value=200.0, value=0.0, step=5.0, key=f"{entity}_{st.session_state.get('reset_id', 0)}")

if st.sidebar.button("Reset Defaults"):
    st.session_state.reset_id = st.session_state.get('reset_id', 0) + 1
    st.rerun()

# TRUE PRO-RATA ZERO-SUM CALCULATION LOGIC
active_shifts = {k: v for k, v in user_shifts.items() if v != 0.0}
if active_shifts:
    for entity, shift_val in active_shifts.items():
        idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
        if len(idx) > 0:
            p13_orig = float(df_static_base.loc[idx, "All P13+"].values[0])
            adj_p13 = max(0.0, p13_orig + shift_val)
            ratio = adj_p13 / p13_orig if p13_orig > 0 else 1.0
            df_matrix.loc[idx, "All P13+"] = adj_p13
            df_matrix.loc[idx, "13-54 Workfc"] = max(0.0, adj_p13 - float(df_static_base.loc[idx, "55+ Layer"].values[0]))
            df_matrix.loc[idx, "13-44 Youth"] = max(0.0, float(df_static_base.loc[idx, "13-44 Youth"].values[0]) * ratio)
            df_matrix.loc[idx, "13-34 Core"] = max(0.0, float(df_static_base.loc[idx, "13-34 Core"].values[0]) * ratio)
            df_matrix.loc[idx, "13-24 Gen Z"] = max(0.0, float(df_static_base.loc[idx, "13-24 Gen Z"].values[0]) * ratio)

    total_shifted_hours = sum(active_shifts.values())
    non_shifted_df = df_static_base[~df_static_base["Platform/Publisher"].isin(active_shifts.keys())]
    total_non_shifted_pool = non_shifted_df["All P13+"].sum()

    if total_non_shifted_pool > 0 and abs(total_shifted_hours) > 0.01:
        for entity in non_shifted_df["Platform/Publisher"].unique():
            idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
            p13_orig = float(df_static_base.loc[idx, "All P13+"].values[0])
            pro_rata_weight = p13_orig / total_non_shifted_pool
            absorbed_share = -total_shifted_hours * pro_rata_weight
            adj_p13 = max(0.0, p13_orig + absorbed_share)
            ratio = adj_p13 / p13_orig if p13_orig > 0 else 1.0
            df_matrix.loc[idx, "All P13+"] = adj_p13
            df_matrix.loc[idx, "13-54 Workfc"] = max(0.0, adj_p13 - float(df_static_base.loc[idx, "55+ Layer"].values[0]))
            df_matrix.loc[idx, "13-44 Youth"] = max(0.0, float(df_static_base.loc[idx, "13-44 Youth"].values[0]) * ratio)
            df_matrix.loc[idx, "13-34 Core"] = max(0.0, float(df_static_base.loc[idx, "13-34 Core"].values[0]) * ratio)
            df_matrix.loc[idx, "13-24 Gen Z"] = max(0.0, float(df_static_base.loc[idx, "13-24 Gen Z"].values[0]) * ratio)

net_balance = df_matrix["All P13+"].sum() - df_static_base["All P13+"].sum()
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
    chart_metrics = ["All P13+", "13-54 Workfc", "55+ Layer"] if selected_demo == "Show All Cohorts Overlaid" else [selected_demo]
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
