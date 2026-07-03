import streamlit as st
import pandas as pd
import base64, os, io

# Universal Token Matrix for System Initialization Mapping
CORE_TOKENS = ["us", "fr", "uk", "it", "de", "sp", "br", "mx"]

# Instant Memory Cache Bootstrapper: Reads the filesystem once and retains data permanently in RAM
if "text_memory_cache" not in st.session_state:
    st.session_state.text_memory_cache = {}
    for token in CORE_TOKENS:
        for prefix in ["methodology", "sources"]:
            filename = f"{prefix}_{token}.txt"
            content = ""
            if os.path.exists(filename):
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        content = str(f.read().strip())
                except Exception:
                    content = ""
            st.session_state.text_memory_cache[filename] = content

def load_text_asset(filename, default_text=""):
    cached_content = st.session_state.text_memory_cache.get(filename, "")
    return cached_content if cached_content else default_text

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
    ["ITV PLC", 510.0, 335.0, 175.0, 113.8, 75.1, 36.8],
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

MX_BASE = [
    ["TELEVISAUNIVISION", 1640.0, 685.0, 955.0, 744.9, 558.7, 284.9],
    ["YOUTUBE", 1390.0, 115.0, 1275.0, 905.2, 733.2, 476.6],
    ["TIKTOK", 860.0, 12.0, 848.0, 695.3, 591.0, 461.0],
    ["INSTAGRAM", 695.0, 18.0, 677.0, 602.5, 518.1, 305.7],
    ["NETFLIX", 635.0, 54.0, 581.0, 447.4, 295.3, 156.4],
    ["TV AZTECA", 485.0, 245.0, 240.0, 180.0, 122.4, 52.8],
    ["AMAZON", 245.0, 32.0, 213.0, 176.8, 116.7, 52.5],
    ["DISNEY", 220.0, 25.0, 195.0, 152.1, 100.4, 46.2],
    ["WBD", 195.0, 42.0, 153.0, 113.2, 72.4, 33.3],
    ["FACEBOOK", 180.0, 78.0, 102.0, 59.2, 23.1, 4.6]
]

BR_BASE = [
    ["GRUPO GLOBO", 2210.0, 1015.0, 1195.0, 920.2, 680.9, 354.1],
    ["YOUTUBE", 1980.0, 260.0, 1720.0, 1221.2, 976.9, 625.2],
    ["TIKTOK", 1150.0, 28.0, 1122.0, 908.8, 763.4, 587.8],
    ["INSTAGRAM", 1040.0, 52.0, 988.0, 879.3, 747.4, 433.5],
    ["NETFLIX", 915.0, 120.0, 795.0, 604.2, 398.7, 211.3],
    ["GROUPO RECORD", 620.0, 365.0, 255.0, 186.1, 122.8, 54.8],
    ["SBT (SISTEMA BRASILEIRO DE TELEVISAO)", 515.0, 290.0, 225.0, 168.7, 115.8, 53.2],
    ["AMAZON", 390.0, 65.0, 325.0, 266.5, 173.2, 77.9],
    ["DISNEY", 325.0, 48.0, 277.0, 213.3, 139.3, 64.0],
    ["WBD (MAX)", 290.0, 82.0, 208.0, 151.8, 95.6, 43.0],
    ["FACEBOOK", 285.0, 135.0, 150.0, 85.5, 32.4, 6.3],
    ["BAND (GRUPO)", 210.0, 122.0, 88.0, 61.6, 38.7, 15.4]
]
bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    with open("planet_bullet.png", "rb") as b_f: bullet_base64 = base64.b64encode(b_f.read()).decode()

# Mobile Viewport Optimization Shield: Injects global style markers to force seamless horizontal scrolling
st.html("""
    <style>
    span[data-testid='stWidgetLabel'] p, button[data-testid='stBaseButton-secondary'] p, [data-baseweb='tab'] p {
        position: relative; padding-left: 1.5rem !important;
    }
    """ + (f"""span[data-testid='stWidgetLabel'] p::before, button[data-testid='stBaseButton-secondary'] p::before, [data-baseweb='tab'] p::before {{
        content: ''; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; background-size: contain; background-repeat: no-repeat;
        background-image: url('data:image/png;base64,{bullet_base64}') !important;
    }}""" if bullet_base64 else "") + """
    /* Force unclipped mobile-responsive frames on data frames to let smartphone users swipe naturally */
    div[data-testid="stDataFrame"] {
        width: 100% !important;
        overflow-x: auto !important;
    }
    div[data-testid="stDataFrame"] data-grid {
        min-width: 820px !important;
    }
    </style>
    """)

# Clean Sidebar Pronunciation Line: Stripped cleanly of bold/italic properties to sit subtly at sidebar apex
st.sidebar.markdown(
    "<p style='font-size: 0.82rem; font-weight: normal; font-style: normal; color: #dddddd; margin-bottom: 0.75rem; text-align: center; letter-spacing: 0.05em;'> "
    "ECSAI: pronounced EE-say"
    "</p>", 
    unsafe_allow_html=True
)

logo_base64 = ""
if os.path.exists("eshap_map.png"):
    with open("eshap_map.png", "rb") as img_f: logo_base64 = base64.b64encode(img_f.read()).decode()
if logo_base64:
    # Sidebar Map Anchor Lock: Explicitly routes the map logo layout directly to the Substack maps link tree
    st.sidebar.html("""
        <style>
        div.sidebar-logo-container { width: 100% !important; margin: 0 0 0.5rem 0 !important; padding: 0 !important; text-align: center !important; }
        div.sidebar-logo-container img { max-width: 100% !important; height: auto !important; }
        </style>
        <div class="sidebar-logo-container"><a href="https://eshap.substack.com/p/media-universe-maps-2020-2026" target="_blank"><img src="data:image/png;base64,""" + logo_base64 + """"></a></div>
        """)

# Global Unconditional Sidebar Toggle: Activated and visible across all territory ledger grids uniformly
merge_meta = st.sidebar.toggle("Consolidate Instagram/Facebook into Meta", value=False, key="meta_toggle_top")
st.sidebar.markdown("<div style='margin-bottom: 0.75rem;'></div>", unsafe_allow_html=True)

st.html("""
    <style>
    section[data-testid="stSidebar"] { background-color: #4A4A4A !important; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div, div[data-testid="stWidgetLabel"] > label p { color: #ffffff !important; }
    g[class*="role-axis"] text { font-weight: bold !important; font-size: 11px !important; }
    
    /* Fixed Selector Shield: Injects the branded red style properties straight to the subhead class */
    .eshap-subhead-text { color: #FF0000 !important; }
    </style>
    """)

st.header("ESHAP Cross Screen Attention Index (ECSAI)")

# Main Scale Subhead Block: Class rule will now natively enforce the bright red anchor color across all themes
st.markdown(
    "<p class='eshap-subhead-text' style='font-size: 0.9rem; font-weight: bold; margin-top: -1rem; margin-bottom: 0.5rem; font-style: normal;'>"
    "The Definitive Zero-Sum Scale For Total Attention From Media's Official Cartographer"
    "</p>", 
    unsafe_allow_html=True
)

# Permanent Link Markdown Lock: Native un-sanitized notation forcing absolute target subdomain security
st.markdown("This index will update monthly, on a rolling six months basis. Each month, we will also drop our analysis of the latest data on **[Media War & Peace](https://eshap.substack.com/)**.", unsafe_allow_html=True)

st.html("<style>div[data-testid='stSidebarNav'] + div, div[data-testid='stRadio'] > div { gap: 0.25rem !important; padding: 0 !important; } div[data-testid='stRadio'] label p { font-size: 0.88rem !important; margin: 0 !important; }</style>")


st.html("<style>div[data-testid='stSidebarNav'] + div, div[data-testid='stRadio'] > div { gap: 0.25rem !important; padding: 0 !important; } div[data-testid='stRadio'] label p { font-size: 0.88rem !important; margin: 0 !important; }</style>")
# Callback Shield: Programmatically wipes memory states cleanly without using loop rerun overhead
def handle_market_switch_callback():
    st.session_state.reset_id = st.session_state.get('reset_id', 0) + 1

market_choice = st.sidebar.radio(
    "Territory", 
    ["United States", "Brazil", "Mexico", "Germany", "United Kingdom", "France", "Italy", "Spain"], 
    key="market_choice_sync",
    on_change=handle_market_switch_callback
)

cols = ["Platform/Publisher", "P13+", "55+ GenX+", "13-54 Majority", "13-44 NextGen", "13-34 Youth", "13-24 GenA/Z"]

if market_choice == "United States": df_matrix = pd.DataFrame(US_BASE, columns=cols)
elif market_choice == "France": df_matrix = pd.DataFrame(FR_BASE, columns=cols)
elif market_choice == "United Kingdom": df_matrix = pd.DataFrame(UK_BASE, columns=cols)
elif market_choice == "Italy": df_matrix = pd.DataFrame(IT_BASE, columns=cols)
elif market_choice == "Germany": df_matrix = pd.DataFrame(DE_BASE, columns=cols)
elif market_choice == "Spain": df_matrix = pd.DataFrame(ES_BASE, columns=cols)
elif market_choice == "Brazil": df_matrix = pd.DataFrame(BR_BASE, columns=cols)
else: df_matrix = pd.DataFrame(MX_BASE, columns=cols)

if merge_meta:
    meta_rows = df_matrix[df_matrix["Platform/Publisher"].isin(["INSTAGRAM", "FACEBOOK"])]
    non_meta_df = df_matrix[~df_matrix["Platform/Publisher"].isin(["INSTAGRAM", "FACEBOOK"])]
    if not meta_rows.empty:
        summed_vals = meta_rows[cols[1:]].sum().tolist()
        combined_row = [["META"] + summed_vals]
        df_matrix = pd.concat([non_meta_df, pd.DataFrame(combined_row, columns=cols)], ignore_index=True)
        df_matrix = df_matrix.sort_values(by="P13+", ascending=False).reset_index(drop=True)

# Enforce float casting immediately at start to prevent calculation mismatch value errors
df_matrix[cols[1:]] = df_matrix[cols[1:]].astype(float)

# Uniformize data presentation layer text across ledger, CSV export, and charting arrays
df_matrix["Platform/Publisher"] = df_matrix["Platform/Publisher"].replace({
    "TELEVISAUNIVISION": "TVSA/UNI",
    "SBT (SISTEMA BRASILEIRO DE TELEVISAO)": "SBT (BRAZIL)",
    "MEDIASET ESPANA": "MEDIASET ES",
    "MFE (MEDIASET)": "MFE",
    "GROUPO RECORD": "GROUPO RECORD"
})

df_static_base = df_matrix.copy()

# Sidebar Branded Units Label: Updates text block to point straight to bright red (#FF0000)
st.sidebar.markdown("### Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated")
st.sidebar.markdown("<h2 style='color: #FF0000; margin-top: -0.5rem; margin-bottom: 0.5rem;'>MILLIONS OF HOURS</h2>", unsafe_allow_html=True)

user_shifts = {}
for entity in df_matrix["Platform/Publisher"].unique():
    user_shifts[entity] = st.sidebar.slider(f"{entity} Shift Impact", min_value=-200.0, max_value=200.0, value=0.0, step=5.0, key=f"{entity}_{st.session_state.get('reset_id', 0)}")

if st.sidebar.button("Reset Defaults"):
    st.session_state.reset_id = st.session_state.get('reset_id', 0) + 1
    st.rerun()

st.sidebar.markdown("<p style='font-size: 0.8rem; font-style: italic; color: #dddddd; margin-top: 1.5rem; line-height: 1.45;'>Time is not infinite. In a snapshot -- this index -- where population and time are constants, when attention shifts to one platform, it must come from somewhere else. These sliders adjust the whole based on adjustments made to any one.</p>", unsafe_allow_html=True)

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

if abs(total_shifted_hours) > 0.01:
    non_shifted_mask = ~df_matrix["Platform/Publisher"].isin(active_shifts.keys())
    total_non_shifted_pool = float(df_static_base[non_shifted_mask]["P13+"].sum())

    if total_non_shifted_pool > 0.0:
        for entity in df_static_base[non_shifted_mask]["Platform/Publisher"].unique():
            idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
            
            # Extract raw float scalar value from array to prevent type conversion errors
            p13_orig_val = float(df_static_base.loc[idx, "P13+"].values)
            pro_rata_weight = p13_orig_val / total_non_shifted_pool
            absorbed_share = -total_shifted_hours * pro_rata_weight
            
            # Absolute Max Guard: Safely handles single float values to block negative entries
            adj_p13 = max(0.0, p13_orig_val + absorbed_share)
            ratio = adj_p13 / p13_orig_val if p13_orig_val > 0.0 else 1.0
            
            df_matrix.loc[idx, "P13+"] = adj_p13
            df_matrix.loc[idx, "13-54 Majority"] = max(0.0, adj_p13 - float(df_static_base.loc[idx, "55+ GenX+"].values))
            df_matrix.loc[idx, "13-44 NextGen"] = float(df_static_base.loc[idx, "13-44 NextGen"].values) * ratio
            df_matrix.loc[idx, "13-34 Youth"] = float(df_static_base.loc[idx, "13-34 Youth"].values) * ratio
            df_matrix.loc[idx, "13-24 GenA/Z"] = float(df_static_base.loc[idx, "13-24 GenA/Z"].values) * ratio

df_matrix[cols[1:]] = df_matrix[cols[1:]].round(1)
net_balance = df_matrix["P13+"].sum() - df_static_base["P13+"].sum()
if abs(net_balance) > 0.1: st.sidebar.warning(f"Simulated Shift Imbalance: {net_balance:+.1f}M Hours")
else: st.sidebar.success("Zero-Sum Balance Maintained")

f_map = {"United States": "🇺🇸", "Germany": "🇩🇪", "United Kingdom": "🇬🇧", "France": "🇫🇷", "Italy": "🇮🇹", "Spain": "🇪🇸", "Brazil": "🇧🇷", "Mexico": "🇲🇽"}
active_flag = f_map.get(market_choice, "🇺🇸")

# Programmatic Tab Interface Engine Initialization
tab1, tab2, tab3, tab4 = st.tabs(["CSAI Interactive Index Matrix", "Why ECSAI?", "ECSAI FAQs", "Index Architecture & Methodology"])
with tab1:
    st.subheader(f"Cross-Screen Attention Tracker: {active_flag} {market_choice}")
    
    # 1. VISUAL SHARE MAP: Chart-First Architecture
    st.markdown("#### Interactive Visual Share Map")
    st.markdown("<p style='font-size: 0.92rem; font-weight: bold; font-style: italic; color: #FF0000; margin-top: -0.5rem; margin-bottom: 0.75rem;'>MILLIONS OF HOURS</p>", unsafe_allow_html=True)
    
    st.html("<style>div[data-testid='stRadio'] > div { gap: 1.5rem !important; } div[data-testid='stRadio'] label p { font-size: 0.95rem !important; white-space: nowrap !important; }</style>")
    demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
    selected_demo = st.radio("Select Demographic Cohort to Isolate in Bar Chart:", options=demo_columns, horizontal=True)
    
    chart_df = df_matrix.copy()
    chart_df["Platform/Publisher"] = chart_df["Platform/Publisher"].replace({"GROUPO RECORD": "RECORD"})
    chart_df = chart_df.set_index("Platform/Publisher")
    
    chart_metrics = [selected_demo]
    st.bar_chart(chart_df[chart_metrics], horizontal=True, height=380, use_container_width=True, color="#FF0000")
    
    st.write("---")
    
    # 2. TABULAR LEDGER MATRIX: Repositioned below chart canvas
    st.markdown("#### Cross Screen Attention Ledger")
    st.markdown("<p style='font-size: 0.92rem; font-weight: bold; font-style: italic; color: #FF0000; margin-top: -0.5rem; margin-bottom: 0.75rem;'>MILLIONS OF HOURS</p>", unsafe_allow_html=True)
    
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
    st.write("")
    
    if market_choice == "Brazil":
        st.markdown("<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross Screen Attention Ledger: BRAZIL</strong><br>Platform totals represent unified corporate parent structures. Grupo Globo incorporates all Globoplay streaming telemetry. WBD fully encapsulates Max sessions and TNT Sports premium footprints. Concurrent multi-screening duplication and passive device use discounted.</p>", unsafe_allow_html=True)
    elif market_choice == "Mexico":
        st.markdown("<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross Screen Attention Ledger: MEXICO</strong><br>Platform totals represent unified corporate parent structures. TelevisaUnivision incorporates all ViX streaming telemetry. YouTube and mobile digital baselines natively absorb all open-distribution and telco-bundled attention siphons, including consolidated cross-screen volumes for Claro Sports and Uno TV. Concurrent multi-screening duplication and passive device use discounted.</p>", unsafe_allow_html=True)
    elif market_choice in ["France", "Germany", "United Kingdom", "Italy", "Spain"]:
        st.markdown(f"<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross Screen Attention Ledger: {market_choice.upper()}</strong><br>Platform totals represent unified holding corporate structures. Traditional TV volumes are scaled using audited single-screen panel metrics from regional state-backed systems (including BARB, Médiamétrie, and Agf/Gfk) and balanced against hardware-level handset logs. Multi-screening and background device noise programmatically flattened through duplication discounts to retain zero-sum integrity.</p>", unsafe_allow_html=True)
        
    st.download_button(label="Export Current Ledger to CSV", data=df_matrix.to_csv(index=False).encode('utf-8'), file_name=f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv", mime="text/csv", use_container_width=True)
with tab2:
    # High-impact centered typography header block utilizing tight line-height spacing and branded red
    st.markdown(
        "<div style='text-align: center; line-height: 0.95; margin-bottom: 1.5rem;'>\n"
        "<h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold;'>WHY THE ECSAI?</h2>\n"
        "<h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold; color: #FF0000;'>BECAUSE HUMAN ATTENTION IS FINITE.</h2>\n"
        "<h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold;'>WE REALLY NEED TO TRACK IT THAT WAY.</h2>\n"
        "</div>",
        unsafe_allow_html=True
    )
    
    st.markdown("Let's face the raw reality of modern media consumption: our entire multi-billion-dollar industry is navigating by a map that does not match the earth.")
    st.markdown("For years, the measurement establishment has relied on a self-serving mythology called \"premium attention quality\" to protect hyper-inflated television CPMs. They want you to believe that a 75-inch living room screen playing high-end drama possesses an inherent, elite cognitive impact. But look at what is actually happening under that roof. While the expensive television glass functions as background wallpaper to an empty sofa, the human being you are trying to reach is in the toilet, actively holding, scrolling, unmuting, and binging vertical video on a smartphone feed.")
    st.markdown("Traditional currencies track the device canvas; they do not track the human. They count a television playing to a room as an absolute hit, while treating a high-intensity mobile session that requires active thumb-and-eye engagement to exist as \"low-tier digital noise.\" This is a collective industry blindness. Legacy tracking systems want you to look at media through isolated reach silos—treating an open screen in an empty room as equal to an active, single-screen consumer focus.")
    st.markdown("When other industry signposts try to offer insight into this cross-screen crisis, they show up with a mallet rather than a magnifying glass. They aggregate soft consumer diaries, build clunky additive charts where the human daily clock magically stretches past 24 hours, or offer micro-level campaign widgets that count how many seconds an ad was technically \"on screen.\" They are handing you a shovel to look at individual twigs while your entire forest is burning to the ground.")
    
    # Red Strategic Compass Lines: Separated into three individual, tightly stacked bold lines in bright red
    st.markdown(
        "<div style='text-align: center; line-height: 1.1; margin-top: 1rem; margin-bottom: 1.5rem;'>\n"
        "<p style='color: #FF0000; font-weight: bold; margin: 0; font-size: 1.05rem;'>TO BE CLEAR:</p>\n"
        "<p style='color: #FF0000; font-weight: bold; margin: 0; font-size: 1.05rem;'>THIS IS NOT A MEDIA BUYING MECHANISM.</p>\n"
        "<p style='color: #FF0000; font-weight: bold; margin: 0; font-size: 1.05rem;'>IT'S A STRATEGIC AND FISCAL PLANNING COMPASS.</p>\n"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown("The data is also clear: Since COVID and the arrival of TikTok, the phone has replaced the television as the center of video gravity. 60% of the world's video attention is now on mobile phones. If you are a media company and you are investing 100% of your budget on tv sets, you are mapping your course to irrelevancy and/or bankruptcy.")
    st.markdown("So much of our measurement investment is spent on measuring television viewing - even when the TV is not being watched!")
    st.markdown("As a result, the Media Industrial complex spends a disproportionate amount of time, energy and resources fighting over control of a screen that ONLY captures 40% of video consumption. That's not just bad business; it's a suicide mission.")
    
    if os.path.exists("eshap_us_devices.png"): 
        st.image("eshap_us_devices.png", caption="Video Consumption Share By Device Ecosystem (US Baseline Panel)", use_container_width=True)
    else: 
        st.info("💡 *[Placeholder for eshap_us_devices.png: In recent telemetry tracking profiles like the MX8 index baseline, 59% of people point to their phone as the primary vehicle they use to watch video. Just 28% name the TV screen]*")
    st.markdown("This real-world divergence isn't a theory; it is a measurable baseline.")
    st.markdown("When tracking video share by device among US consumers, 59% of people point to their phone as the primary vehicle they use to watch video. Just 28% name the TV screen. When you pull back the demographic layers and look under the age of 55, this gap becomes a generational chasm. Two thirds of the video consumption by consumers under 55 is on smartphones, not TVs.")
    st.markdown("The ESHAP Cross-Screen Attention Index (ESCAI) introduces a completely new analytical paradigm to capture this shift. We didn't build a local programmatic tool to place an individual ad spot next Tuesday. To look at this index and ask how to execute a DSP trade is to confuse a compass with a shovel.")
    st.markdown("This scale is a macroeconomic strategy engine engineered for the C-suite to audit structural enterprise risk and investment. If your brand is allocating 60% of its capital to traditional glass viewing while our closed census time budget proves your active workforce demographic has permanently migrated its conscious time to a personal screen, that is an organizational asset failure.")
    st.markdown("ESCAI enforces the absolute laws of human physics. Human time is a non-elastic, zero-sum commodity—a closed market sponge. Every single hour gained by an algorithm is an hour permanently destroyed for a broadcast tower.")
    st.markdown("### THE ZERO-SUM SQUEEZE AND DIARY DE-DUPLICATION")
    
    if os.path.exists("ecsai_flow.png"):
        st.image("ecsai_flow.png", caption="ESHAP Cross-Screen Attention Index Production Workflow Map", use_container_width=True)
    else:
        st.info("💡 *[Placeholder for ecsai_flow.png: Baseline Ingestion, Squeeze Dynamics, and Closed Capacity Ceiling Workflow Layout]*")

    st.markdown("This zero-sum squeeze is where the smooth, cross-screen blending actually happens. If we simply added the television hours to the digital hours, the market sponge would explode past the census ceiling due to concurrent multi-screening—a consumer scrolling on TikTok while the television plays a broadcast in the background. Our index model applies localized duplication coefficients derived from GWI Consumer Diaries and verified attention panels. These diaries track the exact percentage of a cohort that multi-screens daily (e.g., 77% of Gen Z in France).")
    st.markdown("The model uses this percentage to calculate a duplication discount factor. It treats human attention as a finite zero-sum resource: if the eye is looking at a smartphone screen, that fraction of time is physically subtracted from the traditional television glass volume. The digital hours (which require active, focused scrolling on a handheld device) are treated as hard, primary attention blocks. The background television glass hours are programmatically squeezed down until the entire multi-screen overlap is flattened and the duplication is erased. This prioritized single-screen eye focus is a primary reason background audio is not covered in this index.")
    st.markdown("### THE SEPARATION OF POWERS")
    st.markdown("To achieve this, the index operates on a strict Separation of Powers. We use a Sovereign Boundary Model where the hard quantitative ceilings are locked down entirely by currency-grade, telemetry logs (Nielsen, BARB, Médiamétrie, Comscore). The index does not ask consumers how many hours they watched; it uses codified telemetry to establish total volume.")
    st.markdown("Behavioral data from GWI Consumer Diaries is introduced strictly as a coefficient matrix to calculate the mathematical overlap when two devices are running in the same room. We use behavioral data solely to map the friction points where those macro volumes intersect. Legacy currencies rely on passive boxes in empty rooms, counting a television playing to an empty sofa as a hit. We use behavioral data to verify human presence and device co-activity, injecting human reality back into blind hardware metrics.")
    
    st.markdown("### PLEASE LOOK AT THE METHODOLOGY BLUEPRINTS AND SOURCE MATRICES FOR MORE DETAILS ON HOW WE BUILT THIS MODEL.")
    st.markdown("Perhaps the most important point for our industry: We didn't invent new numbers, and we didn't hide our math inside a proprietary black box. Every data point used to build this scale sits legitimately out in the open public domain, scattered across public broadcaster annual disclosures, investor relations filings, and sovereign regulatory white papers. Anyone could theoretically download these records and combine them to see the true division of human time for which they are competing. Until now, however, no one has.")
    st.markdown("Why? Because our industry incentivizes legacy silos. Because, among the most traditional of media and measurement experts, there is widespread fear of finding out how our consumers are actually spending their time and which half of their budgets are being wasted. The current system of content distribution and measurement is built by and for those who profit directly from it, whether or not it actually works.")
    st.markdown("We have built what we believe is the ultimate \"Attention Model,” the first index to track the actual behavior of humans across all the screens they use and account for their attention in a way that helps us all map a course for the future of media.")
    
    # Permanent Markdown Link Lock: Enforces absolute target routing security directly to your domain
    st.markdown("This index will update monthly, on a rolling six months basis. And each month, we will also drop our analysis of the latest data on **[Media War & Peace](https://eshap.substack.com/)**.")
    st.markdown("This is a FREE platform. This is a public project. We are VERY open to your feedback and critique and will continually strive to adapt and improve this product to meet the actual needs of the media community.")
    st.markdown("Thanks for your attention!")
    st.markdown("**ESHAP**")
with tab3:
    st.subheader("ECSAI Frequently Asked Questions (FAQs)")
    
    st.markdown("#### Q: HOW DID WE CHOOSE THE VARIOUS COMBINATION OF SOURCES FOR THE INDEX ACROSS THE REGIONS?")
    st.markdown("To establish an unassailable cross-border baseline, data sources for each country were selected based on three strict criteria: sovereign regulatory authority, parent corporate transparency, and audited single-screen telemetry. Rather than relying on soft consumer opinion surveys, the index exclusively ingests data from official state census registries (such as INSEE, Destatis, and the ONS) for macro population controls, alongside published annual disclosures from public service broadcasters and quarterly investor relations filings from publicly traded tech titans. To bridge the traditional glass and mobile screen gap, these baselines are matched against the hardware-level device telemetry of globally recognized digital tracking firms and local regulatory media white papers. This ensures that every source component sits legitimately in the open public domain, provides absolute consistency in tracking parent corporate holding structures, and natively supports the normalization of disparate metrics into absolute hours of focused human attention.")
    
    st.markdown("#### Q: THE INDEX LISTS ENTERPRISE SUBSCRIPTION SYSTEMS LIKE SENSOR TOWER AND COMSCORE MOBILE METRIX—HOW IS THIS DATA LEGITIMATELY ACCESSED AND DEPLOYED WITHOUT A PAYWALL SUBSCRIPTION?")
    st.markdown("To be entirely clear: ESHAP does not maintain an enterprise terminal contract with Comscore or Sensor Tower, and our open-source methodology explicitly rejects data hidden behind corporate paywalls. Instead, we utilize a reverse-engineering loop built on public-domain telemetry disclosures. Sensor Tower, data.ai, and Comscore Mobile Metrix frequently release exhaustive public data sets, white papers, market intelligence briefs, regulatory antitrust filings, and quarterly macroeconomic charts. Furthermore, public regulatory audits from sovereign media bodies natively ingest and list these exact hardware-level application session counts and time-spent parameters within their free, open-source documentation. ESCAI intercepts these distributed public reports, extracts the specific country-level application session lengths and active monthly user metrics, and applies a localized territory footprint weight. We are not paying for proprietary access to their systems; we are systematically doing the architectural work of gathering, normalizing, and blending their publicly disclosed secondary datasets into a unified human daily clock.")
    st.markdown("#### Q: HOW DO YOU BLEND THE VARIOUS INPUTS - GLASS DATA, CENSUS, DIARIES - INTO ONE SMOOTH INDEX FOR EACH COUNTRY, CUTTING ACROSS DEMOS BASED ONLY ON PUBLICLY AVAILABLE DATA?")
    st.markdown("To blend these completely disparate public inputs into a single, seamless cross-screen index for each territory, our model runs a three-step mathematical normalization loop that forces apples-and-oranges data into a strict, logic-enforced daily time budget. Because we use free, un-siloed data scattered across corporate and government reports, our system treats each country as a closed market sponge where total population and total available hours are hard constants.")
    st.markdown("Here is the exact step-by-step math mechanics of how the index blends glass data, census records, and consumer diaries into a single smooth number for each demographic cohort:")
    st.markdown("**• Census Denominator Lock (The Total Volume Ceiling)**<br>The entire model is anchored on the local state census registry (such as INSEE, Destatis, ISTAT, or the U.S. Census Bureau). The index takes the total population headcount for the territory, filters for the P13+ universe. It then establishes a Total Available Awake Hours Budget per month (assuming a standardized 16-hour active day). This number is our absolute ceiling. It represents the total size of the market sponge. No matter how many apps or TV channels claim massive usage, the combined monthly hours in our index can never exceed this hard, census-backed population budget.", unsafe_allow_html=True)
    st.markdown("**• Normalizing Metrics into 'Absolute Attention Hours'**<br>Next, our model takes the fragmented public data points and converts them into a singular currency: Millions of Attention Hours per Month. Blending the Glass and Feed Data: Traditional linear TV currencies (like Médiamétrie or BARB) publish reach and 'Time Spent Viewing' (TSV) per day. The model takes the average daily TSV for a specific cohort, multiplies it by the demographic population weight from the census, and scales it to 30 days to find total linear hours. Big Tech investor filings and regulatory white papers present usage in 'Daily Active Users' (DAUs) or 'Monthly Active Users' (MAUs) paired with global or regional average session lengths. The model intercepts these ratios, applies the local territory footprint weight, and multiplies active users by daily active minutes to extract total digital hours. We take the stated number of users per digital platforms, apportion them by region/populations, then using diaries, surveys, public reports, and other regional research data, the model assigns pro rata usage hours per day in those regions.", unsafe_allow_html=True)
    st.markdown("#### Q: THE ZERO-SUM SQUEEZE AND DIARY DE-DUPLICATION")
    
    if os.path.exists("ecsai_flow.png"):
        st.image("ecsai_flow.png", caption="ESHAP Cross-Screen Attention Index Production Workflow Map", use_container_width=True)
    else:
        st.info("💡 *[Placeholder for ecsai_flow.png: Baseline Ingestion, Squeeze Dynamics, and Closed Capacity Ceiling Workflow Layout]*")
        
    st.markdown("This zero-sum squeeze is where the smooth, cross-screen blending actually happens. If we simply added the television hours to the digital hours, the market sponge would explode past the census ceiling. This over-allocation happens because of concurrent multi-screening -- a consumer scrolling on TikTok while the television plays a telenovela or news broadcast in the background. The Diary Filter: Our index model applies localized duplication coefficients derived from GWI Consumer Diaries and Dentsu/Lumen attention panels. These diaries track the percentage of a cohort that multi-screens daily (e.g., 77% of Gen Z in France). The Squeeze: The model uses this percentage to calculate a duplication discount factor. It treats human attention as a finite zero-sum resource: if the eye is looking at a smartphone screen, that fraction of time is physically subtracted from the traditional television glass volume. The digital hours (which require active, focused scrolling on a handheld device) are treated as hard, primary attention blocks. The background television glass hours are programmatically squeezed down until the entire multi-screen overlap is flattened, the duplication is erased, and the final platform columns perfectly fit the closed census ceiling. This is a big reason audio is not covered in this index.")

    st.markdown("#### Q: DOESN'T BLENDING 'SOFT' SURVEY RECALL WITH 'HARD' DEVICE TELEMETRY CORRUPT THE DATA FOUNDATION?")
    st.markdown("The index operates on a strict Separation of Powers. We use a Sovereign Boundary Model where the hard quantitative ceilings are locked down entirely by currency-grade, hard telemetry logs (Nielsen, BARB, Médiamétrie, Comscore). The index does not ask consumers how many hours they watched; it uses hard regulatory telemetry to establish total volume. Behavioral data from GWI Consumer Diaries is introduced strictly as a coefficient matrix to calculate the mathematical overlap when two devices are running in the same room. We use behavioral data solely to map the friction points where those macro volumes intersect. Legacy currencies rely on passive boxes in empty rooms, counting a television playing to an empty sofa as a hit. We use behavioral data to verify human presence and device co-activity, injecting human reality back into blind hardware metrics.")
    
    st.markdown("#### Q: ISN'T IT AN 'EQUIVALENCY FALLACY' TO TREAT A SMALL MOBILE SCREEN THE SAME AS A 75-INCH LIVING ROOM TV?")
    st.markdown("The legacy definition of 'premium attention' is a self-serving myth designed to protect high television CPMs. Screen size does not equal cognitive impact. A living room television screen frequently functions as ambient, household background noise. Conversely, a smartphone screen requires active physical interaction—holding, scrolling, unmuting—to maintain the media stream. This index does not flatten attention; it democratizes conscious eye-hours. Our Attention Index (ECSAI, pronounced EE-say) strips away the unearned premium of the living room glass, exposing how mobile feeds capture high-intensity, active physical engagement while traditional TVs increasingly serve as expensive domestic wallpaper. If the eye is on the phone screen, that fraction of time is physically subtracted from the television volume, regardless of how large the TV glass is.")
    st.markdown("#### Q: IF A MEDIA BUYER CANNOT USE THIS HIGH-LEVEL DASHBOARD TO EXECUTE AN AD PLACEMENT ON A DSP, ISN'T THE DATA TOO COARSE FOR REAL-WORLD BUYING?")
    st.markdown("To criticize ESCAI for not executing programmatic ad trades is to mistake a compass for a shovel. This app is a macroeconomic strategy engine, not a trading desk. It is built specifically for the C-suite and Chief Marketing Officers to audit structural enterprise asset risk. Media buyers measure individual twigs; CEOs use this index to see that their entire forest is on fire. If your enterprise allocates 60% of its budget to a legacy channel that commands only 15% of your target workforce demographic's finite daily time budget, that is an enterprise failure. This scale is built to align multi-million-dollar corporate capital allocations with human reality, not to execute a local programmatic trade.")
    
    st.markdown("#### Q: HOW DOES THE INDEX HANDLE MAJOR LIVE EVENT SPIKES, LIKE THE WORLD CUP, THE OLYMPICS, OR A MASSIVE LOCAL ELECTION CYCLE?")
    st.markdown("The ESCAI tracks the stabilized structural baseline of media consumption across a rolling multi-month cycle (currently, for the December 2025 through May 2026 window). While individual live sports or news events create temporary 48-hour spikes on linear glass or premium streaming platforms, the zero-sum math proves these hours are highly volatile siphons. They do not permanently alter the baseline habits of the workforce. When the event ends, the consumer immediately reverts to their core digital utility habits, meaning seasonal spikes do not change the long-term demographic decline of the legacy infrastructure.")
    
    st.markdown("#### Q: IF YOUR MODEL RELIES ON PUBLIC DATA, HOW QUICKLY CAN IT ADAPT WHEN A BRAND-NEW PLATFORM LAUNCHES AND STARTS STEALING ATTENTION?")
    st.markdown("Because the index is built as a strict closed time budget, focused on the consumer, it adapts with consumer attention. If a new platform experiences a sudden user growth explosion, its daily active user metrics and time-spent parameters will show up in public regulatory papers and quarterly financial investor filings. Is there a lag? Yes. Welcome to measurement. When that new platform line-item is introduced to the index, the pro-rata redistribution algorithm automatically squeezes the existing rows down to make room for it. The zero-sum daily clock allows for new platform gains by subtracting from the rest of the market budget, based on the combination of corporate earnings, public records, and ongoing panel diaries.")
    st.markdown("#### Q: HOW DID YOU CHOOSE THESE REGIONS TO INCLUDE FIRST, AND WHY NOT ASIA OR A WIDER FOOTPRINT ACROSS LATIN AMERICA?")
    st.markdown("The selection of these eight territories for the initial rollout was driven by a two-part economic framework: macro-advertising scale and demographic diversity. Rather than picking markets at random, we prioritized the absolute largest media-buying engines on earth alongside the core European and Latin American bellwethers that dictate global distribution strategies. The index natively anchors itself in the highest-monetized ad economies in the Western hemisphere. The United States stands as the undisputed global capital of ad-supported media volume. The United Kingdom represents the most digitally advanced, frictionless English-speaking market in Europe, while Germany commands the absolute largest total advertising and consumer economy on the European continent. The index must be stress-tested against markets that actively resist international digital migration through aggressive state intervention and distinct cultural infrastructure, such as Italy, France, and Spain. By forcing the zero-sum model to process these three protectionist territories, by engineering specialized local policy friction curves to honor their defensive cushions, the index can be a flexible global tool, not just a cookie-cutter American proxy. To balance the inverted, aging demographic pyramids of Europe, the index integrates the two heavyweights of Latin America. Brazil and Mexico represent massive, youth-heavy populations that boast some of the highest daily smartphone video consumption lengths on earth. Including these territories allows us to visualize the absolute opposite end of the media lifecycle: markets where traditional pay-TV infrastructures are entirely bypassable, mobile-velocity acceleration is absolute, and tech utilities operate at an unprecedented 97% to 98% workforce density. We did not include Asia or a wider Latin American footprint in this initial launch for one reason: data maturity and local currency standardization. To deliver a logic-enforced zero-sum matrix, the index requires every country baseline to sit completely transparently in the public domain. The foundational data layers - specifically, open regulatory white papers, audited public broadcaster disclosures, and standardized local device telemetry panels - must possess structural transparency. Markets like Japan, South Korea, India, and smaller Latin American territories currently operate on highly fragmented, proprietary, or state-cloaked measurement silos. Trying to force those opaque systems into a strict human daily clock, right now, requires speculative modeling that compromises the index's standard of data integrity. There is more to come - more regions are actively being built into our pipelines systematically as local sovereign data layers mature.")
    st.markdown("#### Q: LOCAL NETWORKS IN EUROPE AND LATIN AMERICA ARE AGGRESSIVELY PUSHING LOCAL CATCH-UP APPS AND HYBRID SERVICES (LIKE FRANCE.TV, VIX, GLOBOPLAY, ATRESPLAYER, AND JOYN). DOES THE INDEX IGNORE THIS STREAMING MIGRATION?")
    st.markdown("Absolutely not. Local catch-up applications, direct-to-consumer streaming hubs, ad-supported tiers, and premium digital storefronts are natively absorbed and completely accounted for directly inside their parent corporate row items. When you look at the matrix, FRANCE TV includes france.tv; TELEVISAUNIVISION completely captures ViX; GRUPO GLOBO encapsulates Globoplay; ATRESMEDIA holds Atresplayer Premium; and PROSIEBENSAT.1 absorbs Joyn. We have granted these local networks every single drop of digital padding their state-mandated ecosystems can buy. The terrifying reality for these broadcasters is that when you roll up all their premium digital streaming hours into their core corporate rows, the combined weight still looks catastrophic next to the un-elastic velocity of the mobile personal screen.")
    
    st.markdown("#### Q: WHY ARE FAST CHANNELS AND NATIVE STREAMING EXTENSIONS LIKE TUBI, PLUTO TV, OR ROKU CHANNEL LOGGED SEPARATELY IN SOME REPORTS BUT CONSOLIDATED HERE?")
    st.markdown("In the zero-sum marketplace, we follow the money back to the ultimate corporate gatekeeper. Therefore, Tubi is programmatically unified with FOX; Pluto TV, Paramount+, and Channel 5 are collapsed into PARAMOUNT; and Peacock is completely integrated into NBCU. We do this specifically to test the total consolidated structural health of these legacy media empires.")
    
    st.markdown("#### Q: WHY IS BACKGROUND AUDIO, SUCH AS SPOTIFY, NATIVE RADIO REGS, OR APPLE MUSIC, COMPLETELY OMITTED FROM THIS SCALE?")
    st.markdown("Because this index explicitly measures the physical limits of single-screen eye focus, not passive background sound. Human attention is a zero-sum, non-elastic commodity, and to maintain an active video or social media stream on a modern mobile device requires active, physical eye-and-thumb engagement to keep scrolling, holding, and unmuting. Background, on the other hand, audio operates on a parallel, split-cognitive layer—a consumer can listen to a podcast or a music stream while actively focusing their eyes on a TikTok feed or a TV screen. If we attempted to smush ambient, passive ear-hours into a strict human daily awake ceiling, we would break the laws of physics and inflate the market sponge past the census ceiling. This index tracks where the conscious eye goes, because that is where absolute enterprise value is won or lost.")
    
    st.write("---")
    st.markdown(
        "<p style='font-size: 0.92rem; font-weight: bold; line-height: 1.5; color: var(--text-color, inherit); font-style: normal;'>\n"
        "There is more to come &ndash; more regions, more detailed data cuts, more!<br><br>\n"
        "We would love to know what you think. Please send your feedback and questions to \n"
        "<a href='mailto:info@eshap.tv' style='color: #007bff; text-decoration: underline; font-weight: bold;'>info@eshap.tv</a>.<br><br>\n"
        "Cheers!<br><br>\n"
        "ESHAP\n"
        "</p>", 
        unsafe_allow_html=True
    )

with tab4:
    sub_method, sub_source = st.tabs(["Methodology Blueprint", "Sourcing Matrix"])
    w_map = {"United States": "us", "France": "fr", "United Kingdom": "uk", "Italy": "it", "Germany": "de", "Spain": "sp", "Brazil": "br", "Mexico": "mx"}
    t_map = {"United States": ("64.2%", "35.8%"), "France": ("65.1%", "34.9%"), "United Kingdom": ("63.8%", "36.2%"), "Italy": ("59.8%", "40.2%"), "Germany": ("61.5%", "38.5%"), "Spain": ("62.0%", "38.0%"), "Brazil": ("68.5%", "31.5%"), "Mexico": ("71.0%", "29.0%")}
    f_token = w_map.get(market_choice, "us")
    w1, w2 = t_map.get(market_choice, ("64.2%", "35.8%"))
    
    with sub_method:
        st.markdown(f"### METHODOLOGY: CARTOGRAPHER'S BLUEPRINT ({active_flag} {market_choice.upper()})")
        st.markdown(f"**Territorial Demographic Weight:** {w1} is &le; 54 / {w2} is &ge; 55")
        st.write(load_text_asset(f"methodology_{f_token}.txt", f"{market_choice} methodology text loading..."))
    with sub_source:
        st.markdown(f"### DATA SOURCES ({active_flag} {market_choice.upper()})")
        st.write(load_text_asset(f"sources_{f_token}.txt", f"{market_choice} sourcing data loading..."))
