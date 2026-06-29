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

# Narrow text layouts strictly bounded to eliminate horizontal screen spillage
US_DATA = "YOUTUBE 2110.0 490.0 1620.0 1134.0 884.5 539.5\n" \
          "DISNEY 1945.0 1080.0 865.0 657.4 447.0 228.0\n" \
          "NETFLIX 1540.0 380.0 1160.0 846.8 533.5 272.1\n" \
          "TIKTOK 1480.0 65.0 1415.0 1103.7 905.0 660.7\n" \
          "PARAMOUNT 1290.0 810.0 480.0 331.2 195.4 86.0\n" \
          "NBCU 1265.0 795.0 470.0 319.6 185.4 76.0\n" \
          "INSTAGRAM 1120.0 110.0 1010.0 878.7 711.7 391.4\n" \
          "WBD 1040.0 685.0 355.0 241.4 120.7 50.7\n" \
          "FACEBOOK 995.0 520.0 475.0 261.3 96.7 18.4\n" \
          "AMAZON 635.0 215.0 420.0 344.4 213.5 89.7\n" \
          "FOX 425.0 315.0 110.0 55.0 24.8 5.0"

FR_DATA = "YOUTUBE 485.0 95.0 390.0 273.0 212.9 129.9\n" \
          "TIKTOK 335.0 12.0 323.0 251.9 206.6 150.8\n" \
          "NETFLIX 390.0 85.0 305.0 222.7 140.3 71.6\n" \
          "INSTAGRAM 215.0 20.0 195.0 169.7 137.5 75.6\n" \
          "TF1 440.0 270.0 170.0 136.0 102.0 51.8\n" \
          "DISNEY 180.0 42.0 138.0 104.9 66.1 27.3\n" \
          "FRANCE TV 510.0 385.0 125.0 102.5 82.0 54.2\n" \
          "ARTE 120.0 57.6 62.4 48.0 33.6 10.1\n" \
          "GROUP M6 265.0 145.0 120.0 93.6 65.5 29.5\n" \
          "AMAZON 155.0 48.0 107.0 87.7 54.4 22.8\n" \
          "WBD 170.0 95.0 75.0 54.8 34.5 14.3\n" \
          "L'ÉQUIPE 65.0 19.5 45.5 33.7 21.6 8.9\n" \
          "CANAL+ GROUP 195.0 115.0 80.0 58.4 40.9 13.9\n" \
          "FACEBOOK 165.0 92.0 73.0 40.2 14.9 2.8\n" \
          "DAZN 20.0 2.0 18.0 16.2 12.8 7.7"

UK_DATA = "BBC 640.0 460.0 180.0 122.4 85.7 45.4\n" \
          "YOUTUBE 590.0 110.0 480.0 336.0 262.1 159.9\n" \
          "ITV 510.0 335.0 175.0 113.8 75.1 36.8\n" \
          "NETFLIX 495.0 105.0 390.0 284.7 179.4 91.5\n" \
          "TIKTOK 410.0 18.0 392.0 305.8 250.7 183.0\n" \
          "SKY GROUP 385.0 210.0 175.0 119.0 70.2 28.8\n" \
          "INSTAGRAM 275.0 28.0 247.0 214.9 174.1 95.8\n" \
          "PARAMOUNT 245.0 155.0 90.0 61.2 36.1 14.8\n" \
          "DISNEY 235.0 52.0 183.0 139.1 87.6 36.2\n" \
          "WBD 220.0 128.0 92.0 62.6 31.3 13.1\n" \
          "FACEBOOK 210.0 115.0 95.0 52.3 19.3 3.7\n" \
          "AMAZON 195.0 62.0 133.0 109.1 67.6 28.4"

IT_DATA = "Rai 520.0 415.0 105.0 80.9 58.2 37.2\n" \
          "YOUTUBE 440.0 110.0 330.0 231.0 180.2 109.9\n" \
          "MFE (Mediaset) 415.0 265.0 150.0 112.5 81.0 40.8\n" \
          "TIKTOK 295.0 12.0 283.0 220.7 181.0 132.1\n" \
          "NETFLIX 310.0 70.0 240.0 175.2 110.4 56.3\n" \
          "INSTAGRAM 250.0 25.0 225.0 195.8 158.6 87.2\n" \
          "SKY ITALIA 175.0 102.0 73.0 50.4 29.7 12.2\n" \
          "DISNEY 170.0 38.0 132.0 100.3 63.2 26.1\n" \
          "WBD 165.0 92.0 73.0 51.1 31.7 12.9\n" \
          "FACEBOOK 160.0 101.0 59.0 32.5 12.0 2.3\n" \
          "AMAZON 140.0 42.0 98.0 80.4 49.8 20.9"

bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    with open("planet_bullet.png", "rb") as b_f:
        bullet_base64 = base64.b64encode(b_f.read()).decode()

if bullet_base64:
    st.html(f"""
        <style>
        span[data-testid='stWidgetLabel'] p, 
        button[data-testid='stBaseButton-secondary'] p, 
        [data-baseweb='tab'] p {{
            position: relative;
            padding-left: 1.5rem !important;
        }}
        span[data-testid='stWidgetLabel'] p::before, 
        button[data-testid='stBaseButton-secondary'] p::before, 
        [data-baseweb='tab'] p::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 16px;
            height: 16px;
            background-size: contain;
            background-repeat: no-repeat;
            background-image: url('data:image/png;base64,{bullet_base64}') !important;
        }}
        </style>
        """)

logo_base64 = ""
if os.path.exists("eshap_map.png"):
    with open("eshap_map.png", "rb") as img_f:
        logo_base64 = base64.b64encode(img_f.read()).decode()

if logo_base64:
    st.sidebar.html(f"""
        <style>
        div[data-testid="stSidebarUserContent"] {{
            padding-top: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }}
        div.sidebar-logo-container {{
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 0 !important;
        }}
        div.sidebar-logo-container img {{
            width: 100% !important;
            height: auto !important;
            display: block !important;
        }}
        div[data-testid="stSidebarUserContent"] > div:not(.sidebar-logo-container) {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
        </style>
        <div class="sidebar-logo-container">
            <img src="data:image/png;base64,{logo_base64}">
        </div>
        """)

# New, verified title element and styled gray pronunciation subtext layout
st.title("ESHAP Cross-Screen Attention Index (ESCAI)")
st.markdown("<p style='font-size: 0.85rem; font-weight: bold; margin-top: -1rem; margin-bottom: 1.5rem; color: #555555;'>(pronounced: EE-say - the C is silent)</p>", unsafe_allow_html=True)

market_choice = st.sidebar.radio("Select Market Territory Component", ["United States", "France", "United Kingdom", "Italy"])
cols = ["Platform/Publisher", "All P13+", "55+ Layer", "13-54 Workfc", "13-44 Youth", "13-34 NextGen", "13-24 Gen Z"]

raw_txt = {"United States": US_DATA, "France": FR_DATA, "United Kingdom": UK_DATA, "Italy": IT_DATA}.get(market_choice, US_DATA)

parsed_rows = []
for line in raw_txt.strip().split("\n"):
    parts = line.split()
    if len(parts) >= 7:
        p_name = parts[0] if len(parts) == 7 else " ".join(parts[:-6])
        nums = [float(x) for x in parts[-6:]]
        parsed_rows.append([p_name] + nums)

df_matrix = pd.DataFrame(parsed_rows, columns=cols)
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
            p13_orig = df_static_base.loc[idx, "All P13+"].values
            adj_p13 = max(0.0, p13_orig + shift_val)
            ratio = adj_p13 / p13_orig if p13_orig > 0 else 1.0
            df_matrix.loc[idx, "All P13+"] = adj_p13
            df_matrix.loc[idx, "13-54 Workfc"] = max(0.0, adj_p13 - df_static_base.loc[idx, "55+ Layer"].values)
            df_matrix.loc[idx, "13-44 Youth"] = df_static_base.loc[idx, "13-44 Youth"].values * ratio
            df_matrix.loc[idx, "13-34 NextGen"] = df_static_base.loc[idx, "13-34 NextGen"].values * ratio
            df_matrix.loc[idx, "13-24 Gen Z"] = df_static_base.loc[idx, "13-24 Gen Z"].values * ratio

    total_shifted_hours = sum(active_shifts.values())
    non_shifted_df = df_static_base[~df_static_base["Platform/Publisher"].isin(active_shifts.keys())]
    total_non_shifted_pool = non_shifted_df["All P13+"].sum()

    if total_non_shifted_pool > 0 and abs(total_shifted_hours) > 0.01:
        for entity in non_shifted_df["Platform/Publisher"].unique():
            idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
            p13_orig = df_static_base.loc[idx, "All P13+"].values
            pro_rata_weight = p13_orig / total_non_shifted_pool
            absorbed_share = -total_shifted_hours * pro_rata_weight
            adj_p13 = max(0.0, p13_orig + absorbed_share)
            ratio = adj_p13 / p13_orig if p13_orig > 0 else 1.0
            df_matrix.loc[idx, "All P13+"] = adj_p13
            df_matrix.loc[idx, "13-54 Workfc"] = max(0.0, adj_p13 - df_static_base.loc[idx, "55+ Layer"].values)
            df_matrix.loc[idx, "13-44 Youth"] = df_static_base.loc[idx, "13-44 Youth"].values * ratio
            df_matrix.loc[idx, "13-34 NextGen"] = df_static_base.loc[idx, "13-34 NextGen"].values * ratio
            df_matrix.loc[idx, "13-24 Gen Z"] = df_static_base.loc[idx, "13-24 Gen Z"].values * ratio

df_matrix[cols[1:]] = df_matrix[cols[1:]].round(1)
net_balance = df_matrix["All P13+"].sum() - df_static_base["All P13+"].sum()
if abs(net_balance) > 0.1: st.sidebar.warning(f"Simulated Shift Imbalance: {net_balance:+.1f}M Hours")
else: st.sidebar.success("Zero-Sum Balance Maintained")

tab1, tab2 = st.tabs(["CSAI Interactive Index Matrix", "Index Architecture & Methodology"])
with tab1:
    st.subheader(f"Cross-Screen Attention Allocation Ledger — {market_choice}")
    st.markdown("<p style='font-size: 0.85rem; font-weight: bold; margin-top: -0.75rem; margin-bottom: 1rem; color: #555555;'>Click Header To Reorder By Column</p>", unsafe_allow_html=True)
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
    st.download_button(
        label="Export Current Ledger to CSV",
        data=df_matrix.to_csv(index=False).encode('utf-8'),
        file_name=f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.write("")
    st.markdown("#### Interactive Visual Share Map")
    demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
    selected_demo = st.radio(
        "Select Demographic Cohort to Isolate in Bar Chart:",
        options=["Show All Cohorts Overlaid"] + demo_columns,
        horizontal=True
    )
    chart_df = df_matrix.set_index("Platform/Publisher")
    chart_metrics = ["All P13+", "13-54 Workfc", "55+ Layer"] if selected_demo == "Show All Cohorts Overlaid" else [selected_demo]
    st.bar_chart(chart_df[chart_metrics], horizontal=True, height=380)

with tab2:
    sub_method, sub_source = st.tabs(["Methodology Framework", "Sourcing Matrix"])
    w_map = {
        "United States": ("64.2%", "35.8%", "us"),
        "France": ("65.1%", "34.9%", "fr"),
        "United Kingdom": ("63.8%", "36.2%", "uk"),
        "Italy": ("59.8%", "40.2%", "it")
    }
    weight_info = w_map.get(market_choice, ("64.2%", "35.8%", "us"))
    with sub_method:
        st.markdown("### METHODOLOGY")
        st.markdown(f"**Territorial Demographic Weight:** {weight_info[0]} of Population is ≤ 54 Years Old ({weight_info[1]} is ≥ 55)")
        st.write(load_text_asset(f"methodology_{weight_info[2]}.txt", f"{market_choice} methodology text loading..."))
    with sub_source:
        st.markdown("### DATA SOURCES")
        st.write(load_text_asset(f"sources_{weight_info[2]}.txt", f"{market_choice} sourcing data loading..."))
