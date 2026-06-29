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

# Unified Data Parameter Matrices Bound Straight From Your Document Panels (Strict ALL CAPS)
US_BASE = [
    ["YOUTUBE", 2110.0, 490.0, 1620.0, 1134.0, 884.5, 539.5],
    ["DISNEY", 1945.0, 1080.0, 865.0, 657.4, 447.0, 228.0],
    ["NETFLIX", 1540.0, 380.0, 1160.0, 846.8, 533.5, 272.1],
    ["TIKTOK", 1480.0, 65.0, 1415.0, 1103.7, 905.0, 660.7],
    ["PARAMOUNT", 1290.0, 810.0, 480.0, 331.2, 195.4, 86.0],
    ["NBCU", 1265.0, 795.0, 470.0, 319.6, 185.4, 76.0],
    ["INSTAGRAM", 1120.0, 110.0, 1010.0, 878.7, 711.7, 391.4],
    ["WBD", 1040.0, 685.0, 355.0, 241.4, 120.7, 50.7],
    ["FACEBOOK", 995.0, 520.0, 475.0, 261.3, 96.7, 18.4],
    ["AMAZON", 635.0, 215.0, 420.0, 344.4, 213.5, 89.7],
    ["FOX", 425.0, 315.0, 110.0, 55.0, 24.8, 5.0]
]

FR_BASE = [
    ["YOUTUBE", 485.0, 95.0, 390.0, 273.0, 212.9, 129.9],
    ["TIKTOK", 335.0, 12.0, 323.0, 251.9, 206.6, 150.8],
    ["NETFLIX", 390.0, 85.0, 305.0, 222.7, 140.3, 71.6],
    ["INSTAGRAM", 215.0, 20.0, 195.0, 169.7, 137.5, 75.6],
    ["TF1", 440.0, 270.0, 170.0, 136.0, 102.0, 51.8],
    ["DISNEY", 180.0, 42.0, 138.0, 104.9, 66.1, 27.3],
    ["FRANCE TV", 510.0, 385.0, 125.0, 102.5, 82.0, 54.2],
    ["ARTE", 120.0, 57.6, 62.4, 48.0, 33.6, 10.1],
    ["GROUP M6", 265.0, 145.0, 120.0, 93.6, 65.5, 29.5],
    ["AMAZON", 155.0, 48.0, 107.0, 87.7, 54.4, 22.8],
    ["WBD", 170.0, 95.0, 75.0, 54.8, 34.5, 14.3],
    ["L'ÉQUIPE", 65.0, 19.5, 45.5, 33.7, 21.6, 8.9],
    ["CANAL+ GROUP", 195.0, 115.0, 80.0, 58.4, 40.9, 13.9],
    ["FACEBOOK", 165.0, 92.0, 73.0, 40.2, 14.9, 2.8],
    ["DAZN", 20.0, 2.0, 18.0, 16.2, 12.8, 7.7]
]
DE_BASE = [
    ["ARD", 710.0, 560.0, 150.0, 115.5, 90.1, 57.6],
    ["YOUTUBE", 625.0, 135.0, 490.0, 343.0, 267.5, 163.2],
    ["ZDF", 615.0, 505.0, 110.0, 84.7, 66.1, 42.2],
    ["RTL GROUP", 510.0, 310.0, 200.0, 150.0, 108.0, 49.0],
    ["NETFLIX", 445.0, 95.0, 350.0, 255.5, 160.9, 82.1],
    ["TIKTOK", 385.0, 14.0, 371.0, 289.4, 237.3, 173.2],
    ["PROSIEBENSAT.1", 340.0, 195.0, 145.0, 107.3, 73.0, 31.2],
    ["INSTAGRAM", 295.0, 28.0, 267.0, 232.3, 188.2, 103.5],
    ["AMAZON", 230.0, 68.0, 162.0, 132.8, 82.3, 34.6],
    ["DISNEY", 195.0, 42.0, 153.0, 116.3, 73.3, 30.3],
    ["WBD", 145.0, 78.0, 67.0, 48.9, 30.8, 12.7],
    ["FACEBOOK", 140.0, 82.0, 58.0, 31.9, 11.8, 2.2]
]

ES_BASE = [
    ["RTVE", 395.0, 295.0, 100.0, 77.0, 55.4, 35.5],
    ["ATRESMEDIA", 380.0, 235.0, 145.0, 108.8, 78.3, 39.5],
    ["YOUTUBE", 365.0, 85.0, 280.0, 196.0, 152.9, 93.3],
    ["MEDIASET ESPANA", 320.0, 198.0, 122.0, 91.5, 65.9, 33.3],
    ["TIKTOK", 255.0, 10.0, 245.0, 191.1, 156.7, 114.4],
    ["NETFLIX", 240.0, 52.0, 188.0, 137.2, 86.5, 44.1],
    ["INSTAGRAM", 215.0, 20.0, 195.0, 169.7, 137.5, 75.6],
    ["MOVISTAR+", 145.0, 82.0, 63.0, 44.1, 26.5, 11.1],
    ["DISNEY", 115.0, 24.0, 91.0, 69.2, 43.6, 18.0],
    ["WBD (MAX)", 105.0, 55.0, 50.0, 36.5, 23.0, 9.6],
    ["AMAZON", 95.0, 28.0, 67.0, 54.9, 34.0, 14.3],
    ["FACEBOOK", 90.0, 55.0, 35.0, 19.3, 7.1, 1.3]
]

UK_BASE = [
    ["BBC", 640.0, 460.0, 180.0, 122.4, 85.7, 45.4],
    ["YOUTUBE", 590.0, 110.0, 480.0, 336.0, 262.1, 159.9],
    ["ITV", 510.0, 335.0, 175.0, 113.8, 75.1, 36.8],
    ["NETFLIX", 495.0, 105.0, 390.0, 284.7, 179.4, 91.5],
    ["TIKTOK", 410.0, 18.0, 392.0, 305.8, 250.7, 183.0],
    ["SKY GROUP", 385.0, 210.0, 175.0, 119.0, 70.2, 28.8],
    ["INSTAGRAM", 275.0, 28.0, 247.0, 214.9, 174.1, 95.8],
    ["PARAMOUNT", 245.0, 155.0, 90.0, 61.2, 36.1, 14.8],
    ["DISNEY", 235.0, 52.0, 183.0, 139.1, 87.6, 36.2],
    ["WBD", 220.0, 128.0, 92.0, 62.6, 31.3, 13.1],
    ["FACEBOOK", 210.0, 115.0, 95.0, 52.3, 19.3, 3.7],
    ["AMAZON", 195.0, 62.0, 133.0, 109.1, 67.6, 28.4]
]

IT_BASE = [
    ["RAI", 520.0, 415.0, 105.0, 80.9, 58.2, 37.2],
    ["YOUTUBE", 440.0, 110.0, 330.0, 231.0, 180.2, 109.9],
    ["MFE (MEDIASET)", 415.0, 265.0, 150.0, 112.5, 81.0, 40.8],
    ["TIKTOK", 295.0, 12.0, 283.0, 220.7, 181.0, 132.1],
    ["NETFLIX", 310.0, 70.0, 240.0, 175.2, 110.4, 56.3],
    ["INSTAGRAM", 250.0, 25.0, 225.0, 195.8, 158.6, 87.2],
    ["SKY ITALIA", 175.0, 102.0, 73.0, 50.4, 29.7, 12.2],
    ["DISNEY", 170.0, 38.0, 132.0, 100.3, 63.2, 26.1],
    ["WBD", 165.0, 92.0, 73.0, 51.1, 31.7, 12.9],
    ["FACEBOOK", 160.0, 101.0, 59.0, 32.5, 12.0, 2.3],
    ["AMAZON", 140.0, 42.0, 98.0, 80.4, 49.8, 20.9]
]

bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    with open("planet_bullet.png", "rb") as b_f: bullet_base64 = base64.b64encode(b_f.read()).decode()
if bullet_base64:
    st.html("""
        <style>
        span[data-testid='stWidgetLabel'] p, button[data-testid='stBaseButton-secondary'] p, [data-baseweb='tab'] p {
            position: relative; padding-left: 1.5rem !important;
        }
        span[data-testid='stWidgetLabel'] p::before, button[data-testid='stBaseButton-secondary'] p::before, [data-baseweb='tab'] p::before {
            content: ''; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; background-size: contain; background-repeat: no-repeat;
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
        div.sidebar-logo-container { width: 100% !important; margin: 0 0 1rem 0 !important; padding: 0 !important; text-align: center !important; }
        div.sidebar-logo-container img { max-width: 100% !important; height: auto !important; }
        </style>
        <div class="sidebar-logo-container"><img src="data:image/png;base64,""" + logo_base64 + """"></div>
        """)

# Mid-Gray Sidebar Style Matrix & Global Typography Canvas Overrides
st.html("""
    <style>
    section[data-testid="stSidebar"] {
        background-color: #4A4A4A !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div, div[data-testid="stWidgetLabel"] > label p {
        color: #ffffff !important;
    }
    h1 {
        white-space: nowrap !important;
        font-size: 2.25rem !important;
        color: #000000 !important;
        display: block !important;
        visibility: visible !important;
    }
    div[data-testid="stMain"] p, div[data-testid="stMain"] span, div[data-testid="stMain"] label, 
    div[data-testid="stMain"] h3, div[data-testid="stMain"] h4 {
        color: #000000 !important;
    }
    g[class*="role-axis"] text {
        font-weight: bold !important;
        font-size: 11px !important;
    }
    </style>
    """)
# Exact Mexico Parameters Bound Straight From Your Document Sheets (Strict ALL CAPS Alignment)
MX_BASE = [
    ["TELEVISAUNIVISION", 1640.0, 685.0, 955.0, 744.9, 558.7, 284.9],
    ["YOUTUBE", 1390.0, 115.0, 1275.0, 905.2, 733.2, 476.6],
    ["TIKTOK", 860.0, 12.0, 848.0, 695.3, 591.0, 461.0],
    ["INSTAGRAM", 695.0, 18.0, 677.0, 602.5, 518.1, 305.7],
    ["NETFLIX", 635.0, 54.0, 581.0, 447.4, 295.3, 156.4],
    ["TV AZTECA", 485.0, 245.0, 240.0, 180.0, 122.4, 52.8],
    ["AMAZON", 245.0, 32.0, 213.0, 176.8, 116.7, 52.5],
    ["DISNEY", 220.0, 25.0, 195.0, 152.1, 100.4, 46.2],
    ["WBD (MAX)", 195.0, 42.0, 153.0, 113.2, 72.4, 33.3],
    ["FACEBOOK", 180.0, 78.0, 102.0, 59.2, 23.1, 4.6]
]

# Exact Complete Brazil Matrix Bound Straight From Your Audited Document Panels (Strict ALL CAPS Alignment)
BR_BASE = [
    ["GRUPO GLOBO", 2210.0, 1015.0, 1195.0, 920.2, 680.9, 354.1],
    ["YOUTUBE", 1980.0, 260.0, 1720.0, 1221.2, 976.9, 625.2],
    ["TIKTOK", 1150.0, 28.0, 1122.0, 908.8, 763.4, 587.8],
    ["INSTAGRAM", 1040.0, 52.0, 988.0, 879.3, 747.4, 433.5],
    ["NETFLIX", 915.0, 120.0, 795.0, 604.2, 398.7, 211.3],
    ["RECORD GRUPO", 620.0, 365.0, 255.0, 186.1, 122.8, 54.8],
    ["SBT (SISTEMA BRASILEIRO DE TELEVISAO)", 515.0, 290.0, 225.0, 168.7, 115.8, 53.2],
    ["AMAZON", 390.0, 65.0, 325.0, 266.5, 173.2, 77.9],
    ["DISNEY", 325.0, 48.0, 277.0, 213.3, 139.3, 64.0],
    ["WBD (MAX)", 290.0, 82.0, 208.0, 151.8, 95.6, 43.0],
    ["FACEBOOK", 285.0, 135.0, 150.0, 85.5, 32.4, 6.3],
    ["BAND (GRUPO)", 210.0, 122.0, 88.0, 61.6, 38.7, 15.4]
]

st.title("ESHAP Cross-Screen Attention Index (ESCAI)")
st.markdown("<p style='font-size: 0.9rem; font-weight: bold; margin-top: -1rem; margin-bottom: 1.5rem; color: #333333;'>The Definitive Zero-Sum Cross-Screen Attention Scale</p>", unsafe_allow_html=True)

market_choice = st.sidebar.radio("Territory", ["United States", "Brazil", "Mexico", "Germany", "United Kingdom", "France", "Italy", "Spain"])
cols = ["Platform/Publisher", "P13+", "55+ GenX+", "13-54 Majority", "13-44 NextGen", "13-34 Youth", "13-24 GenA/Z"]

if market_choice == "United States": df_matrix = pd.DataFrame(US_BASE, columns=cols)
elif market_choice == "France": df_matrix = pd.DataFrame(FR_BASE, columns=cols)
elif market_choice == "United Kingdom": df_matrix = pd.DataFrame(UK_BASE, columns=cols)
elif market_choice == "Italy": df_matrix = pd.DataFrame(IT_BASE, columns=cols)
elif market_choice == "Germany": df_matrix = pd.DataFrame(DE_BASE, columns=cols)
elif market_choice == "Spain": df_matrix = pd.DataFrame(ES_BASE, columns=cols)
elif market_choice == "Brazil": df_matrix = pd.DataFrame(BR_BASE, columns=cols)
else: df_matrix = pd.DataFrame(MX_BASE, columns=cols)

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
            p13_orig = df_static_base.loc[idx, "P13+"].values
            adj_p13 = max(0.0, p13_orig + shift_val)
            ratio = adj_p13 / p13_orig if p13_orig > 0 else 1.0
            df_matrix.loc[idx, "P13+"] = adj_p13
            df_matrix.loc[idx, "13-54 Majority"] = max(0.0, adj_p13 - df_static_base.loc[idx, "55+ GenX+"].values)
            df_matrix.loc[idx, "13-44 NextGen"] = df_static_base.loc[idx, "13-44 NextGen"].values * ratio
            df_matrix.loc[idx, "13-34 Youth"] = df_static_base.loc[idx, "13-34 Youth"].values * ratio
            df_matrix.loc[idx, "13-24 GenA/Z"] = df_static_base.loc[idx, "13-24 GenA/Z"].values * ratio

    total_shifted_hours = sum(active_shifts.values())
    non_shifted_df = df_static_base[~df_static_base["Platform/Publisher"].isin(active_shifts.keys())]
    total_non_shifted_pool = non_shifted_df["P13+"].sum()

    if total_non_shifted_pool > 0 and abs(total_shifted_hours) > 0.01:
        for entity in non_shifted_df["Platform/Publisher"].unique():
            idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
            p13_orig = df_static_base.loc[idx, "P13+"].values
            pro_rata_weight = p13_orig / total_non_shifted_pool
            absorbed_share = -total_shifted_hours * pro_rata_weight
            adj_p13 = max(0.0, p13_orig + absorbed_share)
            ratio = adj_p13 / p13_orig if p13_orig > 0 else 1.0
            df_matrix.loc[idx, "P13+"] = adj_p13
            df_matrix.loc[idx, "13-54 Majority"] = max(0.0, adj_p13 - df_static_base.loc[idx, "55+ GenX+"].values)
            df_matrix.loc[idx, "13-44 NextGen"] = df_static_base.loc[idx, "13-44 NextGen"].values * ratio
            df_matrix.loc[idx, "13-34 Youth"] = df_static_base.loc[idx, "13-34 Youth"].values * ratio
            df_matrix.loc[idx, "13-24 GenA/Z"] = df_static_base.loc[idx, "13-24 GenA/Z"].values * ratio

df_matrix[cols[1:]] = df_matrix[cols[1:]].round(1)
net_balance = df_matrix["P13+"].sum() - df_static_base["P13+"].sum()
if abs(net_balance) > 0.1: st.sidebar.warning(f"Simulated Shift Imbalance: {net_balance:+.1f}M Hours")
else: st.sidebar.success("Zero-Sum Balance Maintained")

f_map = {
    "United States": "🇺🇸", "Germany": "🇩🇪", "United Kingdom": "🇬🇧",
    "France": "🇫🇷", "Italy": "🇮🇹", "Spain": "🇪🇸", "Brazil": "🇧🇷", "Mexico": "🇲🇽"
}
active_flag = f_map.get(market_choice, "🇺🇸")

tab1, tab2 = st.tabs(["CSAI Interactive Index Matrix", "Index Architecture & Methodology"])
with tab1:
    st.subheader(f"Cross-Screen Attention Allocation Ledger: {active_flag} {market_choice}")
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
    st.write("")
    st.markdown("#### Interactive Visual Share Map")
    st.html("<style>div[data-testid='stRadio'] > div { gap: 1.5rem !important; } div[data-testid='stRadio'] label p { font-size: 0.95rem !important; white-space: nowrap !important; }</style>")
    demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
    selected_demo = st.radio("Select Demographic Cohort to Isolate in Bar Chart:", options=["Cohorts Overlaid"] + demo_columns, horizontal=True)
    
    chart_df = df_matrix.copy()
    chart_df["Platform/Publisher"] = chart_df["Platform/Publisher"].replace({
        "TELEVISAUNIVISION": "TVSA/UNI",
        "SBT (SISTEMA BRASILEIRO DE TELEVISAO)": "SBT (BRAZIL)",
        "MEDIASET ESPANA": "MEDIASET ES",
        "MFE (MEDIASET)": "MFE",
        "RECORD GRUPO": "RECORD"
    })
    chart_df = chart_df.set_index("Platform/Publisher")
    chart_metrics = ["P13+", "13-54 Majority", "55+ GenX+"] if selected_demo == "Cohorts Overlaid" else [selected_demo]
    
    st.bar_chart(chart_df[chart_metrics], horizontal=True, height=380, use_container_width=True)
    
    if market_choice == "Brazil":
        st.markdown("<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross-Screen Attention Allocation Ledger: BRAZIL</strong><br>Platform totals represent unified corporate parent structures. Grupo Globo incorporates all Globoplay streaming telemetry. WBD fully encapsulates Max sessions and TNT Sports premium footprints. Concurrent multi-screening duplication and passive device use discounted.</p>", unsafe_allow_html=True)
    elif market_choice == "Mexico":
        st.markdown("<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross-Screen Attention Allocation Ledger: MEXICO</strong><br>Platform totals represent unified corporate parent structures. TelevisaUnivision incorporates all ViX streaming telemetry. YouTube and mobile digital baselines natively absorb all open-distribution and telco-bundled attention siphons, including consolidated cross-screen volumes for Claro Sports and Uno TV. Concurrent multi-screening duplication and passive device use discounted.</p>", unsafe_allow_html=True)
        
    st.download_button(label="Export Current Ledger to CSV", data=df_matrix.to_csv(index=False).encode('utf-8'), file_name=f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv", mime="text/csv", use_container_width=True)

with tab2:
    sub_method, sub_source = st.tabs(["Methodology Framework", "Sourcing Matrix"])
    w_map = {
        "United States": "us", "France": "fr", "United Kingdom": "uk",
        "Italy": "it", "Germany": "de", "Spain": "sp", "Brazil": "br", "Mexico": "mx"
    }
    t_map = {
        "United States": ("64.2%", "35.8%"), "France": ("65.1%", "34.9%"), "United Kingdom": ("63.8%", "36.2%"),
        "Italy": ("59.8%", "40.2%"), "Germany": ("61.5%", "38.5%"), "Spain": ("62.0%", "38.0%"),
        "Brazil": ("68.5%", "31.5%"), "Mexico": ("71.0%", "29.0%")
    }
    f_token = w_map.get(market_choice, "us")
    w1, w2 = t_map.get(market_choice, ("64.2%", "35.8%"))
    with sub_method:
        st.markdown(f"### METHODOLOGY: CARTOGRAPHER'S BLUEPRINT ({active_flag} {market_choice.upper()})")
        st.markdown(f"**Territorial Demographic Weight:** {w1} is ≤ 54 / {w2} is ≥ 55")
        st.write(load_text_asset(f"methodology_{f_token}.txt", f"{market_choice} methodology text loading..."))
    with sub_source:
        st.markdown("### DATA SOURCES ({active_flag})")
        st.write(load_text_asset(f"sources_{f_token}.txt", f"{market_choice} sourcing data loading..."))
