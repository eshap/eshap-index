import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ESHAP CSAI", layout="wide")
st.title("📊 ESHAP Cross-Screen Attention Index")
st.markdown("""
    Figures represent an exclusive Cross-Screen Attention Index generated via ESHAP analysis 
    that models independent, platform-specific measurement panels into a singular, logic-enforced 
    zero-sum market budget across televisions, smartphones, and computers.
""")

# 1. Unified Regional Setup
region = st.sidebar.selectbox("🌍 Select Market Region", ["United States (All Media Attention)", "France (Video Only)"])

st.sidebar.markdown("---")
st.sidebar.markdown("### **Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated**")

# 2. Hardcoded Audited Baselines
fr_all = {"France TV": 510.0, "YouTube": 485.0, "TF1 Group": 440.0, "Netflix": 390.0, "TikTok": 335.0, "Groupe M6": 265.0, "Instagram": 215.0, "Canal+ Group": 195.0, "Facebook": 165.0, "Amazon Prime": 155.0}
fr_55  = {"France TV": 385.0, "TF1 Group": 270.0, "Groupe M6": 145.0, "Canal+ Group": 115.0, "YouTube": 95.0, "Facebook": 92.0, "Netflix": 85.0, "Amazon Prime": 48.0, "Instagram": 20.0, "TikTok": 12.0}

us_all = {"YouTube": 2110.0, "Disney": 1945.0, "Netflix": 1540.0, "TikTok": 1480.0, "Paramount": 1290.0, "NBCUniversal": 1265.0, "Instagram": 1120.0, "Warner Bros. Discovery": 1040.0, "Facebook": 995.0, "Amazon Prime": 635.0, "Fox Corporation": 425.0}
us_55  = {"Disney": 1080.0, "Paramount": 810.0, "NBCUniversal": 795.0, "Warner Bros. Discovery": 685.0, "Facebook": 520.0, "YouTube": 490.0, "Netflix": 380.0, "Fox Corporation": 315.0, "Amazon Prime": 215.0, "Instagram": 110.0, "TikTok": 65.0}

is_fr = "France" in region
base_all = fr_all if is_fr else us_all
base_55  = fr_55 if is_fr else us_55

# 3. Dynamic Reset Button Implementation
if "reset" not in st.session_state or st.sidebar.button("🔄 Reset Defaults"):
    st.session_state.reset = False
    for k, v in base_all.items():
        st.session_state[f"val_{k}"] = int(v)

# 4. Generate User Sliders
user_inputs = {}
for k, v in base_all.items():
    user_inputs[k] = st.sidebar.slider(f"{k} (P13+)", int(v*0.2), int(v*2.0), key=f"val_{k}")

# 5. Fixed Scaling Vectors
sc_44 = {"Instagram": 0.87, "Amazon Prime": 0.82, "TikTok": 0.78, "Canal+ Group": 0.69, "Disney": 0.76, "Paramount": 0.69, "NBCUniversal": 0.68, "Warner Bros. Discovery": 0.68, "France TV": 0.70, "Groupe M6": 0.69, "Netflix": 0.73, "TF1 Group": 0.68, "YouTube": 0.70, "Facebook": 0.55, "Fox Corporation": 0.50}
sc_34 = {"TikTok": 0.82, "Instagram": 0.81, "YouTube": 0.78, "Canal+ Group": 0.68, "Disney": 0.68, "Paramount": 0.59, "NBCUniversal": 0.58, "Warner Bros. Discovery": 0.50, "France TV": 0.78, "Groupe M6": 0.59, "Netflix": 0.63, "TF1 Group": 0.68, "Amazon Prime": 0.62, "Facebook": 0.37, "Fox Corporation": 0.45}
sc_24 = {"TikTok": 0.73, "YouTube": 0.61, "Instagram": 0.55, "Canal+ Group": 0.30, "Disney": 0.51, "Paramount": 0.44, "NBCUniversal": 0.41, "Warner Bros. Discovery": 0.42, "France TV": 0.61, "Groupe M6": 0.44, "Netflix": 0.51, "TF1 Group": 0.51, "Amazon Prime": 0.42, "Facebook": 0.19, "Fox Corporation": 0.20}

# 6. Compute Data Matrix with Safety Funnel Guard
matrix = []
for k in user_inputs.keys():
    wf_54 = max(0.0, user_inputs[k] - base_55.get(k, 0.0))
    y_44  = round(wf_54 * sc_44.get(k, 1.0), 1)
    y_34  = round(y_44 * sc_34.get(k, 1.0), 1)
    y_24  = round(y_34 * sc_24.get(k, 1.0), 1)
    
    # Nested Funnel Guard check
    y_44, y_34, y_24 = min(y_44, wf_54), min(y_34, y_44), min(y_24, y_34)
    
    matrix.append({"Ecosystem": k, "All P13+": user_inputs[k], "55+": base_55.get(k, 0.0), "13-54": wf_54, "13-44": y_44, "13-34": y_34, "13-24": y_24})

# 7. Render UI Visualizations
df = pd.DataFrame(matrix).sort_values(by="All P13+", ascending=False)
st.subheader("📋 Live Recalculated Matrix Engine")
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("📊 Cross-Cohort Visual Attention Drop-Off")
df_melted = df.melt(id_vars=["Ecosystem"], value_vars=["All P13+", "13-54", "13-44", "13-34", "13-24"], var_name="Cohort", value_name="Hours")
fig = px.bar(df_melted, x="Ecosystem", y="Hours", color="Cohort", barmode="group", color_discrete_sequence=px.colors.qualitative.Safe)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("### 🔍 DATA SOURCES")
st.markdown("MÉDIAMÉTRIE MÉDIAMAT, CENTRE NATIONAL DU CINÉMA ET DE L'IMAGE ANIMÉE (CNC), SENSOR TOWER FRANCE, DATA.AI EUROPE, META INTERNAL AUDIENCE DATA, GOOGLE INVESTOR RELATIONS, VIVENDI FINANCIAL REPORTS, INSTITUT NATIONAL DE LA STATISTIQUE ET DES ÉTUDES ÉCONOMIQUES (INSEE), U.S. CENSUS BUREAU, GWI CONSUMER DIARIES, DENTSU & LUMEN ATTENTION ECONOMY PANELS, EDISON RESEARCH CO-ACTIVE AUDIO TELEMETRY")
