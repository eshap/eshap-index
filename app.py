import streamlit as st
import pandas as pd
import base64
import os

# Helper function to safely read external methodology text copies if they exist
def load_text_asset(filename, default_text=""):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
    return default_text

# ==============================================================================
# 1. PLATFORM INTERFACE & EXCEL DATA PIPELINE CONFIGURATION
# ==============================================================================
st.set_page_config(page_title="ESHAP CSAI Dashboard", layout="wide")

@st.cache_data
def fetch_complete_matrix_from_excel(file_path, sheet_name):
    """Safely extracts all 6 hardcoded demographic columns from your repository spreadsheet tab."""
    fallback_df = pd.DataFrame(columns=[
        "Platform/Publisher", "All P13+", "55+ GenX+", 
        "13-54 Workforce", "13-44 Youth", "13-34 NextGen", "13-24 Gen A/Z"
    ])
    if not os.path.exists(file_path):
        return fallback_df
        
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df.columns = df.columns.str.strip()
        
        # Standardize spreadsheet column header variants to match user-facing labels perfectly
        rename_map = {
            "55+ Layer": "55+ GenX+",
            "13-34 Core": "13-34 NextGen",
            "13-24 Gen Z": "13-24 Gen A/Z"
        }
        df = df.rename(columns=rename_map)
        return df
    except Exception:
        return fallback_df

# Reference token mapped exactly to your file name in the root repository folder
EXCEL_FILE_NAME = "eshap_index_data.xlsx"

if "reset_id" not in st.session_state:
    st.session_state.reset_id = 0

# ==============================================================================
# 2. GLOBAL NAVIGATION BULLET DESIGN STYLES
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
            position: relative; padding-left: 1.5rem !important;
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
# 3. INTERFACE & SIDEBAR SIMULATION CONTROL
# ==============================================================================
market_choice = st.sidebar.radio("Select Market Territory Component", ["United States", "France", "United Kingdom", "Italy"])

# Dynamically read the active country data matrix tab from the Excel spreadsheet file
base_df = fetch_complete_matrix_from_excel(EXCEL_FILE_NAME, market_choice)

st.sidebar.markdown("### Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated")
st.sidebar.markdown("## **MILLIONS OF HOURS**")

# Generate responsive simulation sliders using the platforms listed in the spreadsheet
user_shifts = {}
if not base_df.empty and "Platform/Publisher" in base_df.columns:
    for entity in base_df["Platform/Publisher"].unique():
        user_shifts[entity] = st.sidebar.slider(
            f"{entity} Shift Impact", min_value=-200.0, max_value=200.0, value=0.0, step=5.0,
            key=f"{entity}_slider_{st.session_state.reset_id}"
        )

if st.sidebar.button("Reset Defaults"):
    st.session_state.reset_id += 1
    st.rerun()

# Proportional shift computation loop working off your exact spreadsheet baselines
df_matrix = base_df.copy()
if not df_matrix.empty and user_shifts:
    for entity, shift_val in user_shifts.items():
        if shift_val != 0.0:
            idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
            if len(idx) > 0:
                p13_orig = df_matrix.loc[idx, "All P13+"].values[0]
                adj_p13 = max(0.0, p13_orig + shift_val)
                ratio = (adj_p13 / p13_orig) if p13_orig > 0 else 1.0
                
                # Mutate cells proportionally while applying safety guards
                df_matrix.loc[idx, "All P13+"] = adj_p13
                df_matrix.loc[idx, "13-54 Workforce"] = max(0.0, adj_p13 - df_matrix.loc[idx, "55+ GenX+"].values[0])
                df_matrix.loc[idx, "13-44 Youth"] = max(0.0, df_matrix.loc[idx, "13-44 Youth"].values[0] * ratio)
                df_matrix.loc[idx, "13-34 NextGen"] = max(0.0, df_matrix.loc[idx, "13-34 NextGen"].values[0] * ratio)
                df_matrix.loc[idx, "13-24 Gen A/Z"] = max(0.0, df_matrix.loc[idx, "13-24 Gen A/Z"].values[0] * ratio)

net_balance = sum(user_shifts.values()) if user_shifts else 0.0
if abs(net_balance) > 0.001:
    st.sidebar.warning(f"Simulated Shift Imbalance: {net_balance:+.1f}M Hours")
else:
    st.sidebar.success("Zero-Sum Balance Maintained")

# ==============================================================================
# 4. PRIMARY DASHBOARD PRESENTATION TABS
# ==============================================================================
tab1, tab2 = st.tabs(["CSAI Interactive Index Matrix", "Index Architecture & Methodology"])

with tab1:
    st.subheader(f"Cross-Screen Attention Allocation Ledger — {market_choice}")
    st.markdown("<p style='font-size: 0.85rem; font-weight: bold; margin-top: -0.75rem; margin-bottom: 1rem; color: #555555;'>Click Header To Reorder By Column</p>", unsafe_allow_html=True)
    st.dataframe(df_matrix.style.format({col: "{:,.1f}" for col in df_matrix.columns if col != "Platform/Publisher"}), use_container_width=True, hide_index=True)
    
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
    st.bar_chart(chart_df[chart_metrics], horizontal=True, height=380)

# ==============================================================================
# 5. ARCHITECTURE DOCUMENTATION BLOCKS
# ==============================================================================
with tab2:
    sub_method, sub_source = st.tabs(["Methodology Framework", "Sourcing Matrix"])
    
    with sub_method:
        st.markdown("### METHODOLOGY")
        if market_choice == "United States":
            st.markdown("**Territorial Demographic Weight:** 64.2% of Population is ≤ 54 Years Old (35.8% is ≥ 55)")
            st.write(load_text_asset("methodology_us.txt", "US methodology asset file missing."))
        elif market_choice == "France":
            st.markdown("**Territorial Demographic Weight:** 65.1% of Population is ≤ 54 Years Old (34.9% is ≥ 55)")
            st.write(load_text_asset("methodology_fr.txt", "France methodology asset file missing."))
        elif market_choice == "United Kingdom":
            st.markdown("**Territorial Demographic Weight:** 63.8% of Population is ≤ 54 Years Old (36.2% is ≥ 55)")
            st.write(load_text_asset("methodology_uk.txt", "UK methodology asset file missing."))
        else:
            st.markdown("**Territorial Demographic Weight:** 59.8% of Population is ≤ 54 Years Old (40.2% is ≥ 55)")
            st.write(load_text_asset("methodology_it.txt", "Italy methodology asset file missing."))
        
    with sub_source:
        st.markdown("### DATA SOURCES")
        if market_choice == "United States":
            st.write(load_text_asset("sources_us.txt", "US sources asset file missing."))
        elif market_choice == "France":
            st.write(load_text_asset("sources_fr.txt", "France sources asset file missing."))
        elif market_choice == "United Kingdom":
            st.write(load_text_asset("sources_uk.txt", "UK sources asset file missing."))
        else:
            st.write(load_text_asset("sources_it.txt", "Italy sources asset file missing."))
