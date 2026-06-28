import streamlit as st
import pandas as pd

# ==============================================================================
# 1. CORE DATA STRUCTURES & CONFIGURATION
# ==============================================================================
st.set_page_config(page_title="ESHAP CSAI Dashboard", layout="wide")

# Base Market Footprints (December 2025 - May 2026 Cycle)
# Structure: { Entity: (P13+ Baseline, 55+ Retirement Layer) }
US_RAW = {
    "YouTube": (2110.0, 490.0), "Disney": (1945.0, 1080.0), "Netflix": (1540.0, 380.0),
    "TikTok": (1480.0, 65.0), "Paramount": (1290.0, 810.0), "NBCU": (1265.0, 795.0),
    "Instagram": (1120.0, 110.0), "WBD": (1040.0, 685.0), "Facebook": (995.0, 520.0),
    "Amazon Prime": (635.0, 215.0), "Fox": (425.0, 315.0)
}

FR_RAW = {
    "France TV": (510.0, 385.0), "YouTube": (485.0, 95.0), "TF1 Group": (440.0, 270.0),
    "Netflix": (390.0, 85.0), "TikTok": (335.0, 12.0), "Groupe M6": (265.0, 145.0),
    "Instagram": (215.0, 20.0), "Canal+ Group": (195.0, 115.0), "Facebook": (165.0, 92.0),
    "Amazon Prime": (155.0, 48.0)
}

# Youth Fractional Decay Vectors (Derived from baseline curves)
DECAY = {"13-44": 0.78, "13-34": 0.54, "13-24": 0.32}

# Session State Tracker for Slider Resets
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
        
        # 13-54 Workforce direct subtraction derivation
        w13_54 = max(0.0, adj_p13 - p55)
        
        # Youth cohort calculation using fractional decay vectors
        w13_44 = w13_54 * DECAY["13-44"]
        w13_34 = w13_54 * DECAY["13-34"]
        w13_24 = w13_54 * DECAY["13-24"]
        
        # NESTED FUNNEL SAFETY GUARD (Monotonicity Check)
        w13_54 = min(w13_54, adj_p13)
        w13_44 = min(w13_44, w13_54)
        w13_34 = min(w13_34, w13_44)
        w13_24 = min(w13_24, w13_34)
        
        matrix.append({
            "Platform/Publisher": entity, "All P13+": adj_p13, "55+ Retirement": p55,
            "13-54 Workforce": w13_54, "13-44 Youth": w13_44, "13-34 NextGen": w13_34, "13-24 GenZ Core": w13_24
        })
    return pd.DataFrame(matrix)

# ==============================================================================
# 3. INTERFACE & SIDEBAR SIMULATION CONTROL
# ==============================================================================
st.title("ESHAP Cross-Screen Attention Index (CSAI)")
market_choice = st.sidebar.radio("Select Market Territory Component", ["United States", "France"])
raw_set = US_RAW if market_choice == "United States" else FR_RAW

st.sidebar.markdown("### Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated")
st.sidebar.markdown("## **MILLIONS OF HOURS**")

# Interactive Sliders with dynamic state key tracking to handle instant resets cleanly
user_shifts = {}
for entity in raw_set.keys():
    user_shifts[entity] = st.sidebar.slider(
        f"{entity} Shift Impact", min_value=-200.0, max_value=200.0, value=0.0, step=5.0,
        key=f"{entity}_slider_{st.session_state.reset_id}"
    )

if st.sidebar.button("Reset Defaults"):
    st.session_state.reset_id += 1
    st.rerun()

# Calculate active dataset matrix
df_matrix = build_demographic_matrix(raw_set, user_shifts)

# Net-zero balance verification monitor
net_balance = sum(user_shifts.values())
if abs(net_balance) > 0.001:
    st.sidebar.warning(f"Simulated Shift Imbalance: {net_balance:+.1f}M Hours (Ensure inputs cancel out for true Zero-Sum)")
else:
    st.sidebar.success("Zero-Sum Balance Maintained")

# ==============================================================================
# 4. PRIMARY DASHBOARD PRESENTATION TABS (WITH RESTORED VISUALIZATIONS)
# ==============================================================================
tab1, tab2 = st.tabs(["📊 CSAI Interactive Index Matrix", "📄 Index Architecture & Methodology"])

with tab1:
    st.subheader(f"Cross-Screen Attention Allocation Ledger — {market_choice}")
    
    # --- RESTORED VISUALIZATION LAYER ---
    # Isolating baseline viewing allocations in a horizontal layout bar chart
    chart_data = df_matrix.set_index("Platform/Publisher")[["All P13+", "13-54 Workforce", "55+ Retirement"]]
    st.bar_chart(chart_data, horizontal=True, height=380)
    # ------------------------------------

    # Render the main interactive database view
    st.dataframe(
        df_matrix.style.format({col: "{:,.1f}" for col in df_matrix.columns if col != "Platform/Publisher"}),
        use_container_width=True, hide_index=True
    )
    
    # Convert active dataframe matrix into a standard CSV download string
    csv_data = df_matrix.to_csv(index=False).encode('utf-8')
    
    # Responsive container layout for the download button tool
    col_dl, col_empty = st.columns()
    with col_dl:
        st.download_button(
            label="📥 Export Current Ledger to CSV",
            data=csv_data,
            file_name=f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv",
            mime="text/csv",
            use_container_width=True,
            help="Downloads a clean spreadsheet matching your active territory and simulated shift values."
        )

with tab2:
    sub_method, sub_source = st.tabs(["Methodology Framework", "Sourcing Matrix"])
    
    with sub_method:
        st.markdown("### 🔍 METHODOLOGY")
        if market_choice == "United States":
            st.markdown("**Territorial Demographic Weight:** 64.2% of Population is ≤ 54 Years Old (35.8% is ≥ 55)")
        else:
            st.markdown("**Territorial Demographic Weight:** 65.1% of Population is ≤ 54 Years Old (34.9% is ≥ 55)")
        st.write("Demographic buckets isolate high-earning workforce activity from retirement-heavy viewing patterns.")
        st.write("Youth segments apply mathematical fractional decay metrics capped tightly by nested parent ceilings.")
        
    with sub_source:
        st.markdown("### 🔍 DATA SOURCES")
        st.write("Data aggregated across custom local telemetry, publisher logs, internal panels, and consensus tracking.")
        st.write("Telemetry mapping captures overlapping multi-screen cross-device viewing distributions globally.")
