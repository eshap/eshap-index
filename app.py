import streamlit as st
import pandas as pd
import base64
import os

# Helper function to safely read external copy files if they exist
def load_text_asset(filename, default_text=""):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
    return default_text

# ==============================================================================
# 1. PLATFORM INTERFACE & CONFIGURATION
# ==============================================================================
st.set_page_config(page_title="ESHAP CSAI Dashboard", layout="wide")

# Base Market Footprints (December 2025 - May 2026 Cycle)
# UPDATED: Revised United States parameter dictionary tracking curves
US_RAW = {
    "YOUTUBE": (2110.0, 490.0), 
    "DISNEY": (1945.0, 1080.0), 
    "NETFLIX": (1540.0, 380.0),
    "TIKTOK": (1480.0, 65.0), 
    "PARAMOUNT": (1290.0, 810.0), 
    "NBCU": (1265.0, 795.0),
    "INSTAGRAM": (1120.0, 110.0), 
    "WBD": (1040.0, 685.0), 
    "FACEBOOK": (995.0, 520.0),
    "AMAZON": (635.0, 215.0), 
    "FOX": (425.0, 315.0)
}

# France Core Market Ecosystem Standardized Parameters
FR_RAW = {
    "YOUTUBE": (485.0, 95.0),
    "TIKTOK": (335.0, 12.0),
    "NETFLIX": (390.0, 85.0),
    "INSTAGRAM": (215.0, 20.0),
    "TF1": (440.0, 270.0),
    "DISNEY": (180.0, 42.0),
    "FRANCE TV": (510.0, 385.0),
    "ARTE": (120.0, 57.6),
    "GROUP M6": (265.0, 145.0),
    "AMAZON": (155.0, 48.0),
    "WBD": (170.0, 95.0),
    "L'ÉQUIPE": (65.0, 19.5),
    "CANAL+ GROUP": (195.0, 115.0),
    "FACEBOOK": (165.0, 92.0),
    "DAZN": (20.0, 2.0)
}

# United Kingdom Core Market Ecosystem Standardized Parameters
UK_RAW = {
    "BBC": (640.0, 460.0),
    "YOUTUBE": (590.0, 110.0),
    "ITV": (510.0, 335.0),
    "NETFLIX": (495.0, 105.0),
    "TIKTOK": (410.0, 18.0),
    "SKY GROUP": (385.0, 210.0),
    "INSTAGRAM": (275.0, 28.0),
    "PARAMOUNT": (245.0, 155.0),
    "DISNEY": (235.0, 52.0),
    "WBD": (220.0, 128.0),
    "FACEBOOK": (210.0, 115.0),
    "AMAZON": (195.0, 62.0)
}

# Italy Core Market Ecosystem Standardized Parameters
IT_RAW = {
    "Rai": (520.0, 415.0),
    "YOUTUBE": (440.0, 110.0),
    "MFE (Mediaset)": (415.0, 265.0),
    "TIKTOK": (295.0, 12.0),
    "NETFLIX": (310.0, 70.0),
    "INSTAGRAM": (250.0, 25.0),
    "SKY ITALIA": (175.0, 102.0),
    "DISNEY": (170.0, 38.0),
    "WBD": (165.0, 92.0),
    "FACEBOOK": (160.0, 101.0),
    "AMAZON": (140.0, 42.0)
}

# Youth Fractional Decay Vectors
DECAY = {"13-44": 0.78, "13-34": 0.54, "13-24": 0.32}

if "reset_id" not in st.session_state:
    st.session_state.reset_id = 0

# ==============================================================================
# 2. COMPUTATION ENGINE (WITH FUNNEL SAFETY GUARDS)
# ==============================================================================
def build_demographic_matrix(raw_data, shifts=None):
    matrix = []
    for entity, (p13, p55) in raw_data.items():
        # Apply Zero-Sum Shift modifications from sidebar sliders if active
        shift_val = shifts.get(entity, 0.0) if shifts else 0.0
        adj_p13 = max(0.0, p13 + shift_val)
        w13_54 = max(0.0, adj_p13 - p55)
        
        w13_44 = w13_54 * DECAY["13-44"]
        w13_34 = w13_54 * DECAY["13-34"]
        w13_24 = w13_54 * DECAY["13-24"]
        
        w13_54 = min(w13_54, adj_p13)
        w13_44 = min(w13_44, w13_54)
        w13_34 = min(w13_34, w13_44)
        w13_24 = min(w13_24, w13_34)
        
        matrix.append({
            "Platform/Publisher": entity, 
            "All P13+": adj_p13, 
            "55+ GenX+": p55,
            "13-54 Workforce": w13_54, 
            "13-44 Youth": w13_44, 
            "13-34 NextGen": w13_34, 
            "13-24 Gen A/Z": w13_24
        })
    return pd.DataFrame(matrix)

# ==============================================================================
# 3. GLOBAL CUSTOM BULLET AND BRAND LOGO STYLES SHEET
# ==============================================================================
logo_base64 = ""
if os.path.exists("eshap_map.png"):
    with open("eshap_map.png", "rb") as img_f:
        logo_base64 = base64.b64encode(img_f.read()).decode()

bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    with open("planet_bullet.png", "rb") as b_f:
        bullet_base64 = base64.b64encode(b_f.read()).decode()

if bullet_base64:
    css_injection = """
    <style>
    span[data-testid="stWidgetLabel"] p, button[data-testid="stBaseButton-secondary"] p, [data-baseweb="tab"] p {
        position: relative;
        padding-left: 1.5rem !important;
    }
    span[data-testid="stWidgetLabel"] p::before, button[data-testid="stBaseButton-secondary"] p::before, [data-baseweb="tab"] p::before {
        content: "";
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 16px;
        height: 16px;
        background-image: url("data:image/png;base64,""" + bullet_base64 + """") !important;
        background-size: contain;
        background-repeat: no-repeat;
    }
    </style>
    """
    st.html(css_injection)

# Render vertically centered interface header map next to your index title
if logo_base64:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem; width: 100%;">
            <h1 style="margin: 0; padding: 0;">ESHAP Cross-Screen Attention Index (CSAI)</h1>
            <img src="data:image/png;base64,{logo_base64}" style="max-width: 15%; height: auto; object-fit: contain;" />
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.title("ESHAP Cross-Screen Attention Index (CSAI)")

st.write("") 

# ==============================================================================
# 4. INTERFACE & SIDEBAR SIMULATION CONTROL
# ==============================================================================
market_choice = st.sidebar.radio("Select Market Territory Component", ["United States", "France", "United Kingdom", "Italy"])

if market_choice == "United States":
    raw_set = US_RAW
elif market_choice == "France":
    raw_set = FR_RAW
elif market_choice == "United Kingdom":
    raw_set = UK_RAW
else:
    raw_set = IT_RAW

st.sidebar.markdown("### Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated")
st.sidebar.markdown("## **MILLIONS OF HOURS**")

user_shifts = {}
for entity in raw_set.keys():
    user_shifts[entity] = st.sidebar.slider(
        f"{entity} Shift Impact", min_value=-200.0, max_value=200.0, value=0.0, step=5.0,
        key=f"{entity}_slider_{st.session_state.reset_id}"
    )

if st.sidebar.button("Reset Defaults"):
    st.session_state.reset_id += 1
    st.rerun()

df_matrix = build_demographic_matrix(raw_set, user_shifts)

net_balance = sum(user_shifts.values())
if abs(net_balance) > 0.001:
    st.sidebar.warning(f"Simulated Shift Imbalance: {net_balance:+.1f}M Hours")
else:
    st.sidebar.success("Zero-Sum Balance Maintained")

# ==============================================================================
# 5. PRIMARY DASHBOARD PRESENTATION TABS
# ==============================================================================
tab1, tab2 = st.tabs(["CSAI Interactive Index Matrix", "Index Architecture & Methodology"])

with tab1:
    st.subheader(f"Cross-Screen Attention Allocation Ledger — {market_choice}")
    st.markdown("<p style='font-size: 0.85rem; font-weight: bold; margin-top: -0.75rem; margin-bottom: 1rem; color: #555555;'>Click Header To Reorder By Column</p>", unsafe_allow_html=True)
    
    st.dataframe(
        df_matrix.style.format({col: "{:,.1f}" for col in df_matrix.columns if col != "Platform/Publisher"}),
        use_container_width=True, hide_index=True
    )
    
    csv_data = df_matrix.to_csv(index=False).encode('utf-8')
    col_dl, col_empty = st.columns(2)
    with col_dl:
        st.download_button(
            label="Export Current Ledger to CSV",
            data=csv_data,
            file_name=f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    st.write("") 
    st.write("") 
    
    st.markdown("#### Interactive Visual Share Map")
    demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
    selected_demo = st.radio(
        "Select Demographic Cohort to Isolate in Bar Chart:",
        options=["Show All Cohorts Overlaid"] + demo_columns,
        horizontal=True
    )
    
    chart_df = df_matrix.set_index("Platform/Publisher")
    chart_metrics = ["All P13+", "13-54 Workforce", "55+ GenX+"] if selected_demo == "Show All Cohorts Overlaid" else [selected_demo]
    st.bar_chart(chart_df[chart_metrics], horizontal=True, height=380)

# ==============================================================================
# 6. ARCHITECTURE, SOURCING & METHODOLOGY DOCUMENTATION BLOCKS
# ==============================================================================
with tab2:
    sub_method, sub_source = st.tabs(["Methodology Framework", "Sourcing Matrix"])
    
    with sub_method:
        st.markdown("### METHODOLOGY")
        if market_choice == "United States":
            st.markdown("**Territorial Demographic Weight:** 64.2% of Population is ≤ 54 Years Old (35.8% is ≥ 55)")
            st.write(load_text_asset("methodology_us.txt", "United States architecture documentation placeholder."))
        elif market_choice == "France":
            st.markdown("**Territorial Demographic Weight:** 65.1% of Population is ≤ 54 Years Old (34.9% is ≥ 55)")
            st.write(load_text_asset("methodology_fr.txt", "France architecture documentation placeholder."))
        elif market_choice == "United Kingdom":
            st.markdown("**Territorial Demographic Weight:** 63.8% of Population is ≤ 54 Years Old (36.2% is ≥ 55)")
