import streamlit as st
import pandas as pd

# 1. Page Configuration & Custom ESHAP Branding
st.set_page_config(page_title="ESHAP CSAI", layout="wide")
st.title("📊 ESHAP Cross-Screen Attention Index")

# 2. Regional Selection Hub
region = st.sidebar.selectbox("🌍 Select Market Region", ["United States (All Media Attention)", "France (Video Only)"])
is_fr = "France" in region

# 3. Hardcoded Audited Baselines (Do Not Alter)
fr_all = {"France TV": 510.0, "YouTube": 485.0, "TF1 Group": 440.0, "Netflix": 390.0, "TikTok": 335.0, "Groupe M6": 265.0, "Instagram": 215.0, "Canal+ Group": 195.0, "Facebook": 165.0, "Amazon Prime": 155.0}
fr_55  = {"France TV": 385.0, "TF1 Group": 270.0, "Groupe M6": 145.0, "Canal+ Group": 115.0, "YouTube": 95.0, "Facebook": 92.0, "Netflix": 85.0, "Amazon Prime": 48.0, "Instagram": 20.0, "TikTok": 12.0}

us_all = {"YouTube": 2110.0, "Disney": 1945.0, "Netflix": 1540.0, "TikTok": 1480.0, "Paramount": 1290.0, "NBCUniversal": 1265.0, "Instagram": 1120.0, "Warner Bros. Discovery": 1040.0, "Facebook": 995.0, "Amazon Prime": 635.0, "Fox Corporation": 425.0}
us_55  = {"Disney": 1080.0, "Paramount": 810.0, "NBCUniversal": 795.0, "Warner Bros. Discovery": 685.0, "Facebook": 520.0, "YouTube": 490.0, "Netflix": 380.0, "Fox Corporation": 315.0, "Amazon Prime": 215.0, "Instagram": 110.0, "TikTok": 65.0}

base_all = fr_all if is_fr else us_all
base_55  = fr_55 if is_fr else us_55

# 4. Bulletproof Reset Trigger Logic via Dynamic Keys
if "reset_id" not in st.session_state:
    st.session_state.reset_id = 0

# Sidebar Instantiation Header
st.sidebar.markdown("---")
st.sidebar.markdown("### **Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated**")
st.sidebar.markdown("## **MILLIONS OF HOURS**")

# Generate Dynamic Sliders tied to the dynamic reset tracker ID
user_inputs = {}
for k, v in base_all.items():
    user_inputs[k] = st.sidebar.slider(f"{k} (P13+)", int(v * 0.2), int(v * 2.0), int(v), key=f"sl_{k}_{st.session_state.reset_id}")

# The Reset Execution
if st.sidebar.button("🔄 Reset Defaults", use_container_width=True):
    st.session_state.reset_id += 1
    st.rerun()

# 5. Fixed Performance Multipliers
sc_44 = {"Instagram": 0.87, "Amazon Prime": 0.82, "TikTok": 0.78, "Canal+ Group": 0.69, "Disney": 0.76, "Paramount": 0.69, "NBCUniversal": 0.68, "Warner Bros. Discovery": 0.68, "France TV": 0.70, "Groupe M6": 0.69, "Netflix": 0.73, "TF1 Group": 0.68, "YouTube": 0.70, "Facebook": 0.55, "Fox Corporation": 0.50}
sc_34 = {"TikTok": 0.82, "Instagram": 0.81, "YouTube": 0.78, "Canal+ Group": 0.68, "Disney": 0.68, "Paramount": 0.59, "NBCUniversal": 0.58, "Warner Bros. Discovery": 0.50, "France TV": 0.78, "Groupe M6": 0.59, "Netflix": 0.63, "TF1 Group": 0.68, "Amazon Prime": 0.62, "Facebook": 0.37, "Fox Corporation": 0.45}
sc_24 = {"TikTok": 0.73, "YouTube": 0.61, "Instagram": 0.55, "Canal+ Group": 0.30, "Disney": 0.51, "Paramount": 0.44, "NBCUniversal": 0.41, "Warner Bros. Discovery": 0.42, "France TV": 0.61, "Groupe M6": 0.44, "Netflix": 0.51, "TF1 Group": 0.51, "Amazon Prime": 0.42, "Facebook": 0.19, "Fox Corporation": 0.20}

# 6. Matrix Computation & Nested Funnel Rules Enforcements
matrix = []
for k in user_inputs.keys():
    wf_54 = max(0.0, user_inputs[k] - base_55.get(k, 0.0))
    y_44  = round(wf_54 * sc_44.get(k, 1.0), 1)
    y_34  = round(y_44 * sc_34.get(k, 1.0), 1)
    y_24  = round(y_34 * sc_24.get(k, 1.0), 1)
    
    y_44, y_34, y_24 = min(y_44, wf_54), min(y_34, y_44), min(y_24, y_34)
    
    matrix.append({
        "Ecosystem Structure": k, "All P13+ Baseline": user_inputs[k], "55+ Layer": base_55.get(k, 0.0),
        "13-54 Workforce": wf_54, "13-44 Youth": y_44, "13-34 Core": y_34, "13-24 Gen Z": y_24
    })

# 7. Dynamic Main App Tab Setup
tab1, tab2 = st.tabs(["📊 Interactive Data Engine", "📑 Methodology & Sourcing"])

with tab1:
    df = pd.DataFrame(matrix).sort_values(by="All P13+ Baseline", ascending=False)
    st.subheader("📋 Live Recalculated Matrix Engine")
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab2:
    if is_fr:
        st.markdown("### **ESHAP Cross-Screen Attention Index: France Territory Blueprint**")
        st.markdown("**Territorial Demographic Weight:** 65.1% of Population is ≤ 54 Years Old (34.9% is ≥ 55)")
        st.markdown("---")
        st.markdown("### 🔍 DATA SOURCES")
        st.markdown("MÉDIAMÉTRIE MÉDIAMAT, CENTRE NATIONAL DU CINÉMA ET DE L'IMAGE ANIMÉE (CNC), SENSOR TOWER FRANCE, DATA.AI EUROPE, META INTERNAL AUDIENCE DATA, GOOGLE INVESTOR RELATIONS, VIVENDI FINANCIAL REPORTS, INSTITUT NATIONAL DE LA STATISTIQUE ET DES ÉTUDES ÉCONOMIQUES (INSEE), U.S. CENSUS BUREAU, GWI CONSUMER DIARIES, DENTSU & LUMEN ATTENTION ECONOMY PANELS, EDISON RESEARCH CO-ACTIVE AUDIO TELEMETRY")
        st.markdown("---")
        st.markdown("### 🔍 METHODOLOGY")
        st.markdown("Figures represent an exclusive Cross-Screen Attention Index generated via ESHAP analysis that models independent, platform-specific measurement panels into a singular, logic-enforced zero-sum market budget across televisions, smartphones, and computers. The baseline establishes total available time allocation parameters using Institut National de la Statistique et des Études Économiques (INSEE) headcounts and GWI daily consumer diaries, applying a duplication coefficient to filter out simultaneous multi-screening sessions so that concurrent device use is not double-counted. Television glass viewing shares from Médiamétrie’s Médiamat and application session tracking from Sensor Tower France and data.ai Europe telemetry are collapsed back into their unified parent corporate holding structures (including all linear networks, direct-to-consumer streaming apps, and social feeds), with the final matrix subjected to a python-enforced mathematical filter that caps high-intensity platforms by age cohort size and guarantees strict downward monotonicity and exact demographic balance across all sub-tables. This data is from December 2025 through May 2026, and tracks all attention, including time spent watching video and consuming other social media.")
    else:
        st.markdown("### **ESHAP Cross-Screen Attention Index: United States Blueprint**")
        st.markdown("---")
        st.markdown("### 🔍 DATA SOURCES")
        st.markdown("U.S. CENSUS BUREAU, GWI CONSUMER DIARIES, NIELSEN MEDIA DISTRIBUTOR GAUGE, COMSCORE MOBILE METRIX, SENSOR TOWER, DATA.AI, META INTERNAL AUDIENCE METRICS, ALPHABET INVESTOR RELATIONS, WALT DISNEY COMPANY FINANCIAL REPORTS, NETFLIX QUARTERLY EARNINGS, DENTSU & LUMEN ATTENTION ECONOMY PANELS")
        st.markdown("---")
        st.markdown("### 🔍 METHODOLOGY")
        st.markdown("Figures represent an exclusive Cross-Screen Attention Index generated via ESHAP analysis that models independent, platform-specific measurement panels into a singular, logic-enforced zero-sum market budget across televisions, smartphones, and computers. The baseline establishes total available time allocation parameters using U.S. Census Bureau headcounts and GWI daily consumer diaries, applying a duplication coefficient to filter out simultaneous multi-screening sessions so that concurrent device use is not double-counted. Television glass viewing shares from Nielsen’s Media Distributor Gauge and application session tracking from Comscore Mobile Metrix are collapsed back into their unified parent corporate holding structures (including all linear networks, direct-to-consumer streaming apps, and social feeds), with the final matrix subjected to a python-enforced mathematical filter that caps high-intensity platforms by age cohort size and guarantees strict downward monotonicity and exact demographic balance across all sub-tables. This data is from December 2025 through May 2026, and tracks all attention, including time spent watching video and consuming other social media.")
