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

# Master Absolute Baseline Matrices Hardcoded From Corrected eshap_index_data.pdf
# Format: { Platform: (All P13+, 55+ Layer, 13-54 Workfc, 13-44 Youth, 13-34 Core, 13-24 Gen Z) }
US_BASE = {
    "YOUTUBE": (2110.0, 490.0, 1620.0, 1134.0, 884.5, 539.5),
    "DISNEY": (1945.0, 1080.0, 865.0, 657.4, 447.0, 228.0),
    "NETFLIX": (1540.0, 380.0, 1160.0, 846.8, 533.5, 272.1),
    "TIKTOK": (1480.0, 65.0, 1415.0, 1103.7, 905.0, 660.7),
    "PARAMOUNT": (1290.0, 810.0, 480.0, 331.2, 195.4, 86.0),
    "NBCU": (1265.0, 795.0, 470.0, 319.6, 185.4, 76.0),
    "INSTAGRAM": (1120.0, 110.0, 1010.0, 878.7, 711.7, 391.4),
    "WBD": (1040.0, 685.0, 355.0, 241.4, 120.7, 50.7),
    "FACEBOOK": (995.0, 520.0, 475.0, 261.3, 96.7, 18.4),
    "AMAZON": (635.0, 215.0, 420.0, 344.4, 213.5, 89.7),
    "FOX": (425.0, 315.0, 110.0, 55.0, 24.8, 5.0)
}

FR_BASE = {
    "YOUTUBE": (485.0, 95.0, 390.0, 273.0, 212.9, 129.9),
    "TIKTOK": (335.0, 12.0, 323.0, 251.9, 206.6, 150.8),
    "NETFLIX": (390.0, 85.0, 305.0, 222.7, 140.3, 71.6),
    "INSTAGRAM": (215.0, 20.0, 195.0, 169.7, 137.5, 75.6),
    "TF1": (440.0, 270.0, 170.0, 136.0, 102.0, 51.8),
    "DISNEY": (180.0, 42.0, 138.0, 104.9, 66.1, 27.3),
    "FRANCE TV": (510.0, 385.0, 125.0, 102.5, 82.0, 54.2),
    "ARTE": (120.0, 57.6, 62.4, 48.0, 33.6, 10.1),
    "GROUP M6": (265.0, 145.0, 120.0, 93.6, 65.5, 29.5),
    "AMAZON": (155.0, 48.0, 107.0, 87.7, 54.4, 22.8),
    "WBD": (170.0, 95.0, 75.0, 54.8, 34.5, 14.3),
    "L'ÉQUIPE": (65.0, 19.5, 45.5, 33.7, 21.6, 8.9),
    "CANAL+ GROUP": (195.0, 115.0, 80.0, 58.4, 40.9, 13.9),
    "FACEBOOK": (165.0, 92.0, 73.0, 40.2, 14.9, 2.8),
    "DAZN": (20.0, 2.0, 18.0, 16.2, 12.8, 7.7)
}

UK_BASE = {
    "BBC": (640.0, 460.0, 180.0, 122.4, 85.7, 45.4),
    "YOUTUBE": (590.0, 110.0, 480.0, 336.0, 262.1, 159.9),
    "ITV": (510.0, 335.0, 175.0, 113.8, 75.1, 36.8),
    "NETFLIX": (495.0, 105.0, 390.0, 284.7, 179.4, 91.5),
    "TIKTOK": (410.0, 18.0, 392.0, 305.8, 250.7, 183.0),
    "SKY GROUP": (385.0, 210.0, 175.0, 119.0, 70.2, 28.8),
    "INSTAGRAM": (275.0, 28.0, 247.0, 214.9, 174.1, 95.8),
    "PARAMOUNT": (245.0, 155.0, 90.0, 61.2, 36.1, 14.8),
    "DISNEY": (235.0, 52.0, 183.0, 139.1, 87.6, 36.2),
    "WBD": (220.0, 128.0, 92.0, 62.6, 31.3, 13.1),
    "FACEBOOK": (210.0, 115.0, 95.0, 52.3, 19.3, 3.7),
    "AMAZON": (195.0, 62.0, 133.0, 109.1, 67.6, 28.4)
}

IT_BASE = {
    "Rai": (520.0, 415.0, 105.0, 80.9, 58.2, 37.2),
    "YOUTUBE": (440.0, 110.0, 330.0, 231.0, 180.2, 109.9),
    "MFE (Mediaset)": (415.0, 265.0, 150.0, 112.5, 81.0, 40.8),
    "TIKTOK": (295.0, 12.0, 283.0, 220.7, 181.0, 132.1),
    "NETFLIX": (310.0, 70.0, 240.0, 175.2, 110.4, 56.3),
    "INSTAGRAM": (250.0, 25.0, 225.0, 195.8, 158.6, 87.2),
    "SKY ITALIA": (175.0, 102.0, 73.0, 50.4, 29.7, 12.2),
    "DISNEY": (170.0, 38.0, 132.0, 100.3, 63.2, 26.1),
    "WBD": (165.0, 92.0, 73.0, 51.1, 31.7, 12.9),
    "FACEBOOK": (160.0, 101.0, 59.0, 32.5, 12.0, 2.3),
    "AMAZON": (140.0, 42.0, 98.0, 80.4, 49.8, 20.9)
}

if "reset_id" not in st.session_state:
    st.session_state.reset_id = 0

# ==============================================================================
# 2. PROPORTIONAL ENGINE BLOCK (DYNAMICS WITH FUNNEL GUARDS)
# ==============================================================================
def build_exact_demographic_matrix(base_data, shifts=None):
    matrix = []
    for entity, values in base_data.items():
        p13, p55, w54, y44, n34, z24 = values
        shift_val = shifts.get(entity, 0.0) if shifts else 0.0
        
        # Mutate the gen-pop baseline via slider input
        adj_p13 = max(0.0, p13 + shift_val)
        
        # Calculate dynamic scaling ratios to adjust cohorts proportionally
        ratio = (adj_p13 / p13) if p13 > 0 else 1.0
        
        # Mutate nested segments based on exact historical baseline curves
        adj_w54 = max(0.0, adj_p13 - p55)
        adj_y44 = max(0.0, y44 * ratio)
        adj_n34 = max(0.0, n34 * ratio)
        adj_z24 = max(0.0, z24 * ratio)
        
        # NESTED FUNNEL SAFETY GUARD (Monotonicity Enforcement Check)
        adj_w54 = min(adj_w54, adj_p13)
        adj_y44 = min(adj_y44, adj_w54)
        adj_n34 = min(adj_n34, adj_y44)
        adj_z24 = min(adj_z24, adj_n34)
        
        matrix.append({
            "Platform/Publisher": entity, 
            "All P13+": adj_p13, 
            "55+ GenX+": p55,
            "13-54 Workforce": adj_w54, 
            "13-44 Youth": adj_y44, 
            "13-34 NextGen": adj_n34, 
            "13-24 Gen A/Z": adj_z24
        })
    return pd.DataFrame(matrix)

# ==============================================================================
# 3. GLOBAL NAVIGATION BULLET DESIGN STYLES
# ==============================================================================
bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    with open("planet_bullet.png", "rb") as b_f:
        bullet_base64 = base64.b64encode(b_f.read()).decode()

if bullet_base64:
    st.html(
        """
        <style>
        span[data-testid="stWidgetLabel"] p, button[data-testid="stBaseButton-secondary"] p, [data-baseweb="tab"] p {
            position: relative;
            padding-left: 1.5rem !important;
        }
        span[data-testid="stWidgetLabel"] p::before, button[data-testid="stBaseButton-secondary"] p::before, [data-baseweb="tab"] p::before {
            content: ""; position: absolute; left: 0; top: 50%; transform: translateY(-50%);
            width: 16px; height: 16px; background-size: contain; background-repeat: no-repeat;
            background-image: url("data:image/png;base64,""" + bullet_base64 + """") !important;
        }
        </style>
        """
    )

logo_base64 = ""
if os.path.exists("eshap_map.png"):
    with open("eshap_map.png", "rb") as img_f:
        logo_base64 = base64.b64encode(img_f.read()).decode()

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
# 4. SIMULATION CONTROL & TERRITORY MANAGEMENT
# ==============================================================================
market_choice = st.sidebar.radio("Select Market Territory Component", ["United States", "France", "United Kingdom", "Italy"])

if market_choice == "United States":
    raw_set = US_BASE
elif market_choice == "France":
    raw_set = FR_BASE
elif market_choice == "United Kingdom":
    raw_set = UK_BASE
else:
    raw_set = IT_BASE

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

df_matrix = build_exact_demographic_matrix(raw_set, user_shifts)

net_balance = sum(user_shifts.values())
if abs(net_balance) > 0.001:
    st.sidebar.warning(f"Simulated Shift Imbalance: {net_balance:+.1f}M Hours")
else:
    st.sidebar.success("Zero-Sum Balance Maintained")

# ==============================================================================
# 5. PRIMARY INTERACTIVE PRESENTATION TABS
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
        st.download_button(label="Export Current Ledger to CSV", data=csv_data, file_name=f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv", mime="text/csv", use_container_width=True)
        
    st.write("")
    st.markdown("#### Interactive Visual Share Map")
    demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
    selected_demo = st.radio("Select Demographic Cohort to Isolate in Bar Chart:", options=["Show All Cohorts Overlaid"] + demo_columns, horizontal=True)
    
    chart_df = df_matrix.set_index("Platform/Publisher")
    chart_metrics = ["All P13+", "13-54 Workforce", "55+ GenX+"] if selected_demo == "Show All Cohorts Overlaid" else [selected_demo]
