import streamlit as st
import pandas as pd
import base64, os, io

CORE_TOKENS = ["us", "fr", "uk", "it", "de", "sp", "br", "mx"]

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
    return st.session_state.text_memory_cache.get(filename, default_text)

st.set_page_config(page_title="ESHAP CSAI Dashboard", layout="wide")

# Hardcoded United States Matrix Array with OTHER Long-Tail Layer Integrated
US_BASE = [
    ["YOUTUBE", 2110.0, 490.0, 1620.0, 1134.0, 884.5, 539.5],
    ["OTHER", 1120.0, 210.0, 910.0, 780.0, 620.0, 310.0],
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
    ["FRANCE TV", 510.0, 385.0, 125.0, 102.5, 82.0, 54.2],
    ["YOUTUBE", 485.0, 95.0, 390.0, 273.0, 212.9, 129.9],
    ["TF1", 440.0, 270.0, 170.0, 136.0, 102.0, 51.8],
    ["NETFLIX", 390.0, 85.0, 305.0, 222.7, 140.3, 71.6],
    ["TIKTOK", 335.0, 12.0, 323.0, 251.9, 206.6, 150.8],
    ["GROUP M6", 265.0, 145.0, 120.0, 93.6, 65.5, 29.5],
    ["INSTAGRAM", 215.0, 20.0, 195.0, 169.7, 137.5, 75.6],
    ["OTHER", 210.4, 75.0, 135.4, 98.0, 65.0, 24.0],
    ["CANAL+ GROUP", 195.0, 115.0, 80.0, 58.4, 40.9, 13.9],
    ["DISNEY", 180.0, 42.0, 138.0, 104.9, 66.1, 27.3],
    ["WBD", 170.0, 95.0, 75.0, 54.8, 34.5, 14.3],
    ["FACEBOOK", 165.0, 92.0, 73.0, 40.2, 14.9, 2.8],
    ["AMAZON", 155.0, 48.0, 107.0, 87.7, 54.4, 22.8],
    ["ARTE", 120.0, 57.6, 62.4, 48.0, 33.6, 10.1],
    ["L'ÉQUIPE", 65.0, 19.5, 45.5, 33.7, 21.6, 8.9],
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
    ["OTHER", 325.0, 110.0, 215.0, 160.0, 115.0, 52.0],
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
    ["OTHER", 215.0, 82.0, 133.0, 90.0, 58.0, 21.0],
    ["INSTAGRAM", 215.0, 20.0, 195.0, 169.7, 137.5, 75.6],
    ["MOVISTAR+", 145.0, 82.0, 63.0, 44.1, 26.5, 11.1],
    ["DISNEY", 115.0, 24.0, 91.0, 69.2, 43.6, 18.0],
    ["WBD (MAX)", 105.0, 55.0, 50.0, 36.5, 23.0, 9.6],
    ["AMAZON", 95.0, 28.0, 67.0, 54.9, 34.0, 14.3],
    ["FACEBOOK", 90.0, 55.0, 35.0, 19.3, 7.1, 1.3]
]
UK_BASE = [
    ["BBC", 640.0, 460.0, 180.0, 122.4, 85.7, 45.4],
    ["OTHER", 640.0, 480.0, 160.0, 95.0, 50.0, 15.0],
    ["YOUTUBE", 590.0, 110.0, 480.0, 336.0, 262.1, 159.9],
    ["ITV", 510.0, 335.0, 175.0, 113.8, 75.1, 36.8],
    ["NETFLIX", 495.0, 105.0, 390.0, 284.7, 179.4, 91.5],
    ["TIKTOK", 410.0, 18.0, 392.0, 305.8, 250.7, 183.0],
    ["SKY", 385.0, 210.0, 175.0, 119.0, 70.2, 28.8],
    ["INSTAGRAM", 275.0, 28.0, 247.0, 214.9, 174.1, 95.8],
    ["PARAMOUNT", 245.0, 155.0, 90.0, 61.2, 36.1, 14.8],
    ["WBD", 220.0, 128.0, 92.0, 62.6, 31.3, 13.1],
    ["CHANNEL4", 290.0, 165.0, 125.0, 85.0, 50.2, 20.6],
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
    ["OTHER", 230.0, 95.0, 135.0, 92.0, 60.0, 22.0],
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
    ["OTHER", 315.0, 85.0, 230.0, 185.0, 140.0, 65.0],
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
    ["OTHER", 490.0, 115.0, 375.0, 290.0, 210.0, 95.0],
    ["AMAZON", 390.0, 65.0, 325.0, 266.5, 173.2, 77.9],
    ["DISNEY", 325.0, 48.0, 277.0, 213.3, 139.3, 64.0],
    ["WBD (MAX)", 290.0, 82.0, 208.0, 151.8, 95.6, 43.0],
    ["FACEBOOK", 285.0, 135.0, 150.0, 85.5, 32.4, 6.3],
    ["BAND (GRUPO)", 210.0, 122.0, 88.0, 61.6, 38.7, 15.4]
]

bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    with open("planet_bullet.png", "rb") as b_f: bullet_base64 = base64.b64encode(b_f.read()).decode()
st.html("""
    <style>
    span[data-testid='stWidgetLabel'] p, button[data-testid='stBaseButton-secondary'] p, [data-baseweb='tab'] p {
        position: relative; padding-left: 1.5rem !important;
    }
    """ + (f"""span[data-testid='stWidgetLabel'] p::before, button[data-testid='stBaseButton-secondary'] p::before, [data-baseweb='tab'] p::before {{
        content: ''; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; background-size: contain; background-repeat: no-repeat;
        background-image: url('data:image/png;base64,{bullet_base64}') !important;
    }}""" if bullet_base64 else "") + """
    div[data-testid="stDataFrame"] {
        width: 100% !important;
        overflow-x: auto !important;
    }
    div[data-testid="stDataFrame"] data-grid {
        min-width: 820px !important;
    }
    </style>
    """)

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
    st.sidebar.html("""
        <style>
        div.sidebar-logo-container { width: 100% !important; margin: 0 0 0.5rem 0 !important; padding: 0 !important; text-align: center !important; }
        div.sidebar-logo-container img { max-width: 100% !important; height: auto !important; }
        </style>
        <div class="sidebar-logo-container"><a href="https://eshap.substack.com" target="_blank"><img src="data:image/png;base64,""" + logo_base64 + """"></a></div>
        """)

merge_meta = st.sidebar.toggle("Consolidate Instagram/Facebook into Meta", value=False, key="meta_toggle_top")
st.sidebar.markdown("<div style='margin-bottom: 0.75rem;'></div>", unsafe_allow_html=True)
st.html("""
    <style>
    section[data-testid="stSidebar"] { background-color: #4A4A4A !important; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div, div[data-testid="stWidgetLabel"] > label p { color: #ffffff !important; }
    g[class*="role-axis"] text { font-weight: bold !important; font-size: 11px !important; }
    .eshap-subhead-text { color: #FF0000 !important; }
    </style>
    """)

st.header("ESHAP Cross Screen Attention Index (ECSAI)")

st.markdown(
    "<p class='eshap-subhead-text' style='font-size: 0.9rem; font-weight: bold; margin-top: -1rem; margin-bottom: 0.5rem; font-style: normal;'>"
    "The Definitive Zero-Sum Scale For Total Attention From Media's Official Cartographer"
    "</p>", 
    unsafe_allow_html=True
)

st.markdown("For full analysis: **[ESHAP MEDIA WAR & PEACE: REPORTING ON THE WAR FOR ATTENTION](https://eshap.substack.com)**")
st.html("<style>div[data-testid='stSidebarNav'] + div, div[data-testid='stRadio'] > div { gap: 0.25rem !important; padding: 0 !important; } div[data-testid='stRadio'] label p { font-size: 0.88rem !important; margin: 0 !important; }</style>")
def handle_market_switch_callback():
    st.session_state.reset_id = st.session_state.get('reset_id', 0) + 1

market_choice = st.sidebar.radio(
    "Territory", 
    ["Global Index Overview", "United States", "Brazil", "Mexico", "Germany", "United Kingdom", "France", "Italy", "Spain"], 
    key="market_choice_sync",
    on_change=handle_market_switch_callback
)

cols = ["Platform/Publisher", "P13+", "55+ GenX+", "13-54 Majority", "13-44 NextGen", "13-34 Youth", "13-24 GenA/Z"]

# Direct Data Router Matrix
if market_choice == "Global Index Overview": df_matrix = None
elif market_choice == "United States": df_matrix = pd.DataFrame(US_BASE, columns=cols)
elif market_choice == "France": df_matrix = pd.DataFrame(FR_BASE, columns=cols)
elif market_choice == "United Kingdom": df_matrix = pd.DataFrame(UK_BASE, columns=cols)
elif market_choice == "Italy": df_matrix = pd.DataFrame(IT_BASE, columns=cols)
elif market_choice == "Germany": df_matrix = pd.DataFrame(DE_BASE, columns=cols)
elif market_choice == "Spain": df_matrix = pd.DataFrame(ES_BASE, columns=cols)
elif market_choice == "Brazil": df_matrix = pd.DataFrame(BR_BASE, columns=cols)
else: df_matrix = pd.DataFrame(MX_BASE, columns=cols)
if df_matrix is not None:
    if merge_meta:
        meta_rows = df_matrix[df_matrix["Platform/Publisher"].isin(["INSTAGRAM", "FACEBOOK"])]
        non_meta_df = df_matrix[~df_matrix["Platform/Publisher"].isin(["INSTAGRAM", "FACEBOOK"])]
        if not meta_rows.empty:
            summed_vals = meta_rows[cols[1:]].sum().tolist()
            df_matrix = pd.concat([non_meta_df, pd.DataFrame([["META"] + summed_vals], columns=cols)], ignore_index=True).sort_values(by="P13+", ascending=False).reset_index(drop=True)

    df_matrix[cols[1:]] = df_matrix[cols[1:]].astype(float)
    df_matrix["Platform/Publisher"] = df_matrix["Platform/Publisher"].replace({
        "TELEVISAUNIVISION": "TVSA/UNI", "SBT (SISTEMA BRASILEIRO DE TELEVISAO)": "SBT (BRAZIL)",
        "MEDIASET ESPANA": "MEDIASET ES", "MFE (MEDIASET)": "MFE", "GROUPO RECORD": "GROUPO RECORD"
    })
    df_static_base = df_matrix.copy()

    st.sidebar.markdown("### Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated")
    st.sidebar.markdown("<h2 style='color: #FF0000; margin-top: -0.5rem; margin-bottom: 0.5rem;'>MILLIONS OF HOURS</h2>", unsafe_allow_html=True)
if df_matrix is not None:
    user_shifts = {}
    for entity in df_matrix["Platform/Publisher"].unique():
        user_shifts[entity] = st.sidebar.slider(f"{entity} Shift Impact", -200.0, 200.0, 0.0, 5.0, key=f"{entity}_{st.session_state.get('reset_id', 0)}")

    if st.sidebar.button("Reset Defaults"):
        st.session_state.reset_id = st.session_state.get('reset_id', 0) + 1
        st.rerun()

    st.sidebar.markdown("<p style='font-size: 0.8rem; font-style: italic; color: #dddddd; margin-top: 1.5rem; line-height: 1.45;'>Time is not infinite. In a snapshot -- this index -- where population and time are constants, when attention shifts to one platform, it must come from somewhere else. These sliders adjust the whole based on adjustments made to any one.</p>", unsafe_allow_html=True)
else:
    st.sidebar.info("💡 *Global Index Overview mode active. Reallocation sliders are hidden for high-level macro baseline analysis.*")
    user_shifts = {}
if df_matrix is not None:
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
                for c in ["13-44 NextGen", "13-34 Youth", "13-24 GenA/Z"]: df_matrix.loc[idx, c] = df_static_base.loc[idx, c].values * ratio

    total_shifted_hours = sum(active_shifts.values())
    if abs(total_shifted_hours) > 0.01:
        non_shifted_mask = ~df_matrix["Platform/Publisher"].isin(active_shifts.keys())
        total_non_shifted_pool = float(df_static_base[non_shifted_mask]["P13+"].sum())
        if total_non_shifted_pool > 0.0:
            for entity in df_static_base[non_shifted_mask]["Platform/Publisher"].unique():
                idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
                p13_orig_val = float(df_static_base.loc[idx, "P13+"].values)
                ratio = max(0.0, p13_orig_val + (-total_shifted_hours * (p13_orig_val / total_non_shifted_pool))) / p13_orig_val if p13_orig_val > 0.0 else 1.0
                df_matrix.loc[idx, "P13+"] = p13_orig_val * ratio
                df_matrix.loc[idx, "13-54 Majority"] = max(0.0, (p13_orig_val * ratio) - float(df_static_base.loc[idx, "55+ GenX+"].values))
                for c in ["13-44 NextGen", "13-34 Youth", "13-24 GenA/Z"]: df_matrix.loc[idx, c] = float(df_static_base.loc[idx, c].values) * ratio

    df_matrix[cols[1:]] = df_matrix[cols[1:]].round(1)
    if abs(df_matrix["P13+"].sum() - df_static_base["P13+"].sum()) > 0.1: st.sidebar.warning("Simulated Shift Imbalance Detected")
    else: st.sidebar.success("Zero-Sum Balance Maintained")

f_map = {"Global Index Overview": "🌐", "United States": "🇺🇸", "Germany": "🇩🇪", "United Kingdom": "🇬🇧", "France": "🇫🇷", "Italy": "🇮🇹", "Spain": "🇪🇸", "Brazil": "🇧🇷", "Mexico": "🇲🇽"}
active_flag = f_map.get(market_choice, "🇺🇸")

tab1, tab2, tab3, tab4 = st.tabs(["CSAI Interactive Index Matrix", "Why ECSAI?", "ECSAI FAQs", "Index Architecture & Methodology"])
with tab1:
    if market_choice == "Global Index Overview":
        # ----------------================================================================----------------
        # HIGH-LEVEL GLOBAL INDEX CANVAS MODE: Renders Brief Document Layout Elements (Splits text strictly)
        # ----------------================================================================----------------
        st.subheader("THE GLOBAL INDEX")
        st.markdown(
            "What happens when we drop the pretense that TV is premium and social video is not? "
            "What becomes of the mainstream mindset when we take down the silo walls and measure Media "
            "consumption not BY device, but rather ACROSS devices? Turns out, a lot. Which is why we "
            "embarked on this mission to measure it all, side-by-side."
        )
        
        if os.path.exists("global_index_13+.png"):
            st.image("global_index_13+.png", caption="CROSS-SCREEN ATTENTION INDEX - GLOBAL SHARE OF ATTENTION: P13+ (DEC 2025 - MAY 2026)", use_container_width=True)
        else:
            st.warning("⚠️ `global_index_13+.png` asset missing from repository folder. Verify file location boundaries.")
        st.markdown("Look at this chart.")
        st.markdown(
            "You can see the share of consumer attention, spread across all eight regions in The Index, for all "
            "people 13+. Note that the Local Legacy Media index is ALL local traditional Media from these "
            "eight regions, combined, and compared to the rest of the global players on the chart. Note also "
            "that for total attention, for all fourteen of the legacy media platforms across all eight regions, lose "
            "the battle for cross-screen attention to the global attention champ, YouTube."
        )
        st.markdown(
            "More importantly, this is total attention paid (not total people watching), for all people 13+ in "
            "these regions. When we ZOOM IN and look at how the majority of humans on earth, consumer media..."
        )
        
        if os.path.exists("global_index_13-54.png"):
            st.image("global_index_13-54.png", caption="CROSS-SCREEN ATTENTION INDEX - GLOBAL SHARE OF ATTENTION: P13-54 (DEC 2025 - MAY 2026)", use_container_width=True)
        else:
            st.warning("⚠️ `global_index_13-54.png` asset missing from repository folder. Verify file location boundaries.")
        st.markdown(
            "##### **Of all the data in this report, the most crucial datapoint is this: 82% of the world population — 73% of the people in these eight regions — are now under 54.**"
        )
        st.markdown(
            "This new index reveals that Legacy TV relies, almost entirely, on the shrinking minority of our "
            "most senior citizens watching the same stuff, over and over and over, throwing off the balance of "
            "measured video consumption. When you remove that dying demographic (of which I am, myself, "
            "solidly a member), the combined fourteen Legacy outlets in this index are surpassed — handily — "
            "by YouTube, Netflix, and TikTok."
        )
        st.markdown(
            "##### **Even more eye-opening: Across these countries, YouTube garners more attention among people 13-54 than Disney, Disco Bros, Paramount, NBCU, and FOX — combined.**"
        )
        st.markdown(
            "##### **TikTok beats all other platforms except YouTube for attention paid, including Netflix, and Local Legacy Media.**"
        )
        st.markdown(
            "But this zoomed-out global view is not truly actionable, nor the point of this new index. Rather, "
            "our intent with this new, free, interactive, user-driven index, is to provide a strategic fiscal and "
            "investment planning compass for *each* of these regions."
        )
        st.markdown("---")
        st.subheader("US REGIONAL DEMOGRAPHIC PROFILE FOCUS")
# Removed line break and heading to let the text flow continuously across columns
        st.markdown(
            "The ESHAP Cross-Screen Attention Index is hard-wired with data for total cross-device "
            "attention, for France, Brazil, Mexico, UK, France, Italy, Spain, and the US, from December 2025 "
            "through May 2026."
        )
        st.markdown("**The ECSAI is the first zero-sum, wholly deduplicated map of human attention in history.**")
        st.markdown(
            "It shows the total hours of attention paid to each platform, side-by-side, accounting for daily "
            "human attention as a finite resource, which cannot be divided between screens. If someone is "
            "looking at TV, even if they have a phone in their hand, the time is allocated to the television. If "
            "someone is scrolling TikTok, even if the TV is on in the room, that attention is apportioned to the "
            "phone, while the TV not being watched is discounted."
        )
        
        if os.path.exists("us_index_13-54.png"):
            st.image("us_index_13-54.png", caption="CROSS-SCREEN ATTENTION INDEX - US MONTHLY TIME: P13-54 (SOURCE: NIELSEN, COMSCORE, GWI, FCC)", use_container_width=True)
        else:
            st.warning("⚠️ `us_index_13-54.png` asset missing from repository folder. Verify file location boundaries.")

        st.markdown(
            "While Trad Media continues to cling to an aging audience, **in ALL EIGHT MAJOR REGIONS**, even "
            "where Legacy Media is deeply entrenched in the free Media culture, and protected by local "
            "regulations, among the 13-54 majority YouTube is the most used platform, by a sizable margin. "
            "Netflix plays well across all eight regions, but among 13-54 and all the younger demos, especially "
            "with Millennials, Gen Z, and Gen A, in most of these areas, TikTok outpaces Netflix, and all other comers."
        )
        st.markdown(
            "##### **In fact, as this new data shows for the first time, in many regions — particularly in the US — while YouTube is tops in total attention, TikTok actually beats YouTube among Gen Z and Gen A (consumers 13-34).**"
        )
        
        # Stacked Final Comparative Age Frames
        c1, c2 = st.columns(2)
        with c1:
            if os.path.exists("us_index_13-34.png"):
                st.image("us_index_13-34.png", caption="US TOTAL ATTENTION: P13-34", use_container_width=True)
            else:
                st.warning("⚠️ `us_index_13-34.png` missing.")
        with c2:
            if os.path.exists("us_index_13-24.png"):
                st.image("us_index_13-24.png", caption="US TOTAL ATTENTION: P13-24", use_container_width=True)
            else:
                st.warning("⚠️ `us_index_13-24.png` missing.")
    else:
        # ----------------================================================================================
        # STANDARD LOCAL TERRITORY ENGINE INTERFACE: Renders charts and slider grids natively
        # ----------------================================================================================
        st.subheader(f"Cross-Screen Attention Tracker: {active_flag} {market_choice}")
        st.markdown("#### Interactive Visual Share Map")
        st.markdown("<p style='font-size: 0.92rem; font-weight: bold; font-style: italic; color: #FF0000; margin-top: -0.5rem; margin-bottom: 0.75rem;'>MILLIONS OF HOURS</p>", unsafe_allow_html=True)
        
        st.html("<style>div[data-testid='stRadio'] > div { gap: 1.5rem !important; } div[data-testid='stRadio'] label p { font-size: 0.95rem !important; white-space: nowrap !important; }</style>")
        demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
        selected_demo = st.radio("Select Demographic Cohort to Isolate in Bar Chart:", options=demo_columns, horizontal=True)
        
        chart_df = df_matrix.copy()
        chart_df["Platform/Publisher"] = chart_df["Platform/Publisher"].replace({"GROUPO RECORD": "RECORD"})
        chart_df_fixed = chart_df.set_index("Platform/Publisher")
        st.bar_chart(chart_df_fixed[[selected_demo]], horizontal=True, height=380, use_container_width=True, color="#FF0000")
            
        st.write("---")
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
    st.markdown("<div style='text-align: center; line-height: 0.95; margin-bottom: 1.5rem;'><h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold;'>WHY THE ECSAI?</h2><h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold; color: #FF0000;'>BECAUSE HUMAN ATTENTION IS FINITE.</h2><h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold;'>WE REALLY NEED TO TRACK IT THAT WAY.</h2></div>", unsafe_allow_html=True)
    st.markdown("And this, right here, is precisely why we need a Cross-Screen Index. No one else is measuring all these platforms, side by side, on all devices. So, the industry get easily distracted by flaccid signposts that tells us \"YouTube is #1 on TV!\" (with P2+ and without counting phones, laptops, or tablets).")
    st.markdown("Traditional currencies track the device canvas; they do not track the human. They count a television playing to a room as an absolute hit, while treating a high-intensity mobile session that requires active thumb-and-eye engagement to exist as \"digital noise.\" This is a collective industry blindness. Legacy tracking systems want you to look at media through isolated reach silos — treating an open screen in an empty room as equal to an active, single-screen consumer focus.")
    st.markdown("So much of our Media measurement investment is spent measuring television viewing — even when that TV is not being watched. As a result, the Media Industrial complex spends a disproportionate amount of time, energy and resources fighting over control of a screen that **only captures 40% of video consumption**. That's not just bad business; it's a suicide mission.")
    st.markdown("The Index is designed to prevent that — designed to show, specifically, where the entirety of consumer attention is actually being paid, so that Media professionals can invest in content, advertising, overhead, and infrastructure, accordingly.")
    st.markdown("Each quarter, we will update the ECSAI (pronounced EE-say) with new data, on a rolling six months basis. Simultaneously, we will drop an Index Report, on **[Media War & Peace](https://substack.com)**, with deep analysis of the data and the trends, right here on Substack.", unsafe_allow_html=True)
    st.markdown("This is different from other measurement offerings, which provide small, irrelevant glimpses of data for free, then charge clients millions to fund it, while keeping the vast majority of us who work in Media in the dark. This incentivizes the measurement industrial complex to keep our data in silos, dividing and double-counting consumer attention.")
    st.markdown("### HERE ARE THE RED HOT TAKES FROM THE FIRST ESCAI REPORT:")
    st.markdown("* While Local & Global Traditional Media in all eight regions continues to draw attention from local consumers, their businesses have become senior living societies — disproportionately dependent on the minority of their populations over the age of 55.")
    st.markdown("* For the *majority* of audiences in all eight countries, people 54 and younger, YouTube now dominates our collective attention.")
    st.markdown("* *However, TikTok is coming on, fast.* In the US and many other regions, TikTok is now #2 with consumers under 55 for total attention paid each month, #1 with consumers under 35, and actively threatening YouTube's attention title with consumers under 45.")
    st.markdown("* Netflix is strong in many of these regions. Yet, they appear vulnerable to phone set around the world.")
    st.markdown("* Netflix loses to YouTube in every region. More urgently, they are now behind TikTok for total cross-screen attention with consumers 13-54 in the US, the UK, Brazil, Mexico, Germany, France, Italy, and Spain.")
    st.markdown("* For audiences 13-44 Netflix loses the battle for attention to Instagram in five of the eight regions: Brazil, Mexico, Spain, Italy, and the United States.")
    st.markdown("* When we collapse Facebook and Instagram into a de-duplicated META metric, Meta sweeps Netflix in all eight regions for users 54 and younger.")
    st.markdown("* YouTube still beats Meta in all these regions among consumers 13-54, but not by much.")
    st.markdown("* On the interactive Cross-Screen Index, we allow you to toggle the data to combine or separate Meta into IG and FB. However, we look at Instagram and Facebook separately in this report, as they have dramatically different user-bases. 53% of Facebook's user-base in these eight countries is over 55, whereas 90% of Instagram's audience is 54 or younger.")
    st.markdown("* Global Trad Media in The Index — Disney, Fox, Disco Bros, Paramount, NBCU — play differently in various regions, but their total lack of cross-screen strategy has them losing badly to Global Big Tech platforms in *all eight territories*. All the Trad US Media giants fail to secure even one #1 or #2 spot in among people 13-54 in any of the eight regions covered.")
    st.markdown("When we embark on projects like this, we start fresh. No preconceptions. No confirmation bias. We let the data give us the plot, then we tell the story. This is, by far, our most ambitious data endeavor yet. It's a mountain of data and it tells a remarkable story about the future of Media based on the actual needs of real consumers. We will keep following the data where it leads us.")
with tab3:
    st.subheader("ECSAI Frequently Asked Questions (FAQs)")
    st.markdown("#### Q: THE ZERO-SUM SQUEEZE AND DIARY DE-DUPLICATION")
    if os.path.exists("ecsai_flow.png"): st.image("ecsai_flow.png", caption="ESHAP Cross-Screen Attention Index Production Workflow Map", use_container_width=True)
    st.markdown("This zero-sum squeeze is where the smooth, cross-screen blending actually happens. If we simply added the television hours to the digital hours, the market sponge would explode past the census ceiling due to concurrent multi-screening — a consumer scrolling on TikTok while the television plays a broadcast in the background. Our index model applies localized duplication coefficients derived from GWI Consumer Diaries and verified attention panels. These diaries track the exact percentage of a cohort that multi-screens daily (e.g., 77% of Gen Z in France). The model uses this percentage to calculate a duplication discount factor. It treats human attention as a finite zero-sum resource: if the eye is looking at a smartphone screen, that fraction of time is physically subtracted from the traditional television glass volume. The digital hours (which require active, focused scrolling on a handheld device) are treated as hard, primary attention blocks. The background television glass hours are programmatically squeezed down until the entire multi-screen overlap is flattened and the duplication is erased. This prioritized single-screen eye focus is a primary reason background audio is not covered in this index.")
    st.write("---")
    st.markdown("<p style='font-size: 0.92rem; font-weight: bold; line-height: 1.5;'>Take The ECSAI for a test drive! Let us know what you think at <a href='mailto:info@eshap.tv' style='color: #007bff; text-decoration: underline; font-weight: bold;'>info@eshap.tv</a>.<br><br>And, please, don't forget to take some time to enjoy your day!<br><br>Cheers!<br><br>ESHAP</p>", unsafe_allow_html=True)

with tab4:
    sub_method, sub_source = st.tabs(["Methodology Blueprint", "Sourcing Matrix"])
    is_global_view = market_choice == "Global Index Overview"
    f_token = "us" if is_global_view else {"United States": "us", "France": "fr", "United Kingdom": "uk", "Italy": "it", "Germany": "de", "Spain": "sp", "Brazil": "br", "Mexico": "mx"}.get(market_choice, "us")
    
    with sub_method:
        st.markdown(f"### METHODOLOGY: CARTOGRAPHER'S BLUEPRINT ({active_flag} {market_choice.upper()})")
        if not is_global_view:
            w1, w2 = {"United States": ("64.2%", "35.8%"), "France": ("65.1%", "34.9%"), "United Kingdom": ("63.8%", "36.2%"), "Italy": ("59.8%", "40.2%"), "Germany": ("61.5%", "38.5%"), "Spain": ("62.0%", "38.0%"), "Brazil": ("68.5%", "31.5%"), "Mexico": ("71.0%", "29.0%")}.get(market_choice, ("64.2%", "35.8%"))
            st.markdown(f"**Territorial Demographic Weight:** {w1} is &le; 54 / {w2} is &ge; 55")
        
        # Method line-by-line file injector
        if os.path.exists(f"methodology_{f_token}.txt"):
            with open(f"methodology_{f_token}.txt", "r", encoding="utf-8") as m_f: st.write(m_f.read())
        else: st.info(f"{market_choice} methodology text loading...")
            
    with sub_source:
        st.markdown(f"### DATA SOURCES ({active_flag} {market_choice.upper()})")
        if os.path.exists(f"sources_{f_token}.txt"):
            with open(f"sources_{f_token}.txt", "r", encoding="utf-8") as s_f: st.write(s_f.read())
        else: st.info(f"{market_choice} sourcing data loading...")
