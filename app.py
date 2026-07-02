import streamlit as st
import pandas as pd
import base64, os, io

# Performance Cache Shield: Pre-loads regional txt assets permanently straight into memory
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
    cached_content = st.session_state.text_memory_cache.get(filename, "")
    return cached_content if cached_content else default_text

st.set_page_config(page_title="ESHAP CSAI Dashboard", layout="wide")

# Master Data Repository: Populated from your technical document specs (Millions of Hours/Month)
GLOBAL_DATA_REPOSITORY = {
    "US": {
        "YOUTUBE": {"P13+": 2110.0, "55+ GenX+": 490.0, "13-54 Majority": 1620.0, "13-44 NextGen": 1134.0, "13-34 Youth": 884.5, "13-24 GenA/Z": 539.5},
        "DISNEY": {"P13+": 1945.0, "55+ GenX+": 1080.0, "13-54 Majority": 865.0, "13-44 NextGen": 657.4, "13-34 Youth": 447.0, "13-24 GenA/Z": 228.0},
        "NETFLIX": {"P13+": 1540.0, "55+ GenX+": 380.0, "13-54 Majority": 1160.0, "13-44 NextGen": 846.8, "13-34 Youth": 533.5, "13-24 GenA/Z": 272.1},
        "TIKTOK": {"P13+": 1480.0, "55+ GenX+": 65.0, "13-54 Majority": 1415.0, "13-44 NextGen": 1103.7, "13-34 Youth": 905.0, "13-24 GenA/Z": 660.7},
        "PARAMOUNT": {"P13+": 1290.0, "55+ GenX+": 810.0, "13-54 Majority": 480.0, "13-44 NextGen": 331.2, "13-34 Youth": 195.4, "13-24 GenA/Z": 86.0},
        "NBCU": {"P13+": 1265.0, "55+ GenX+": 795.0, "13-54 Majority": 470.0, "13-44 NextGen": 319.6, "13-34 Youth": 185.4, "13-24 GenA/Z": 76.0}
    }
# Continuation of GLOBAL_DATA_REPOSITORY configuration for remaining core regions
GLOBAL_DATA_REPOSITORY["US"].update({
    "INSTAGRAM": {"P13+": 1120.0, "55+ GenX+": 110.0, "13-54 Majority": 1010.0, "13-44 NextGen": 878.7, "13-34 Youth": 711.7, "13-24 GenA/Z": 391.4},
    "WBD": {"P13+": 1040.0, "55+ GenX+": 685.0, "13-54 Majority": 355.0, "13-44 NextGen": 241.4, "13-34 Youth": 120.7, "13-24 GenA/Z": 50.7},
    "FACEBOOK": {"P13+": 995.0, "55+ GenX+": 520.0, "13-54 Majority": 475.0, "13-44 NextGen": 261.3, "13-34 Youth": 96.7, "13-24 GenA/Z": 18.4},
    "AMAZON": {"P13+": 635.0, "55+ GenX+": 215.0, "13-54 Majority": 420.0, "13-44 NextGen": 344.4, "13-34 Youth": 213.5, "13-24 GenA/Z": 89.7},
    "FOX": {"P13+": 425.0, "55+ GenX+": 315.0, "13-54 Majority": 110.0, "13-44 NextGen": 55.0, "13-34 Youth": 24.8, "13-24 GenA/Z": 5.0}
})

GLOBAL_DATA_REPOSITORY["BR"] = {
    "GRUPO GLOBO": {"P13+": 2210.0, "55+ GenX+": 1015.0, "13-54 Majority": 1195.0, "13-44 NextGen": 920.2, "13-34 Youth": 680.9, "13-24 GenA/Z": 354.1},
    "YOUTUBE": {"P13+": 1980.0, "55+ GenX+": 260.0, "13-54 Majority": 1720.0, "13-44 NextGen": 1221.2, "13-34 Youth": 976.9, "13-24 GenA/Z": 625.2},
    "TIKTOK": {"P13+": 1150.0, "55+ GenX+": 28.0, "13-54 Majority": 1122.0, "13-44 NextGen": 908.8, "13-34 Youth": 763.4, "13-24 GenA/Z": 587.8},
    "INSTAGRAM": {"P13+": 1040.0, "55+ GenX+": 52.0, "13-54 Majority": 988.0, "13-44 NextGen": 879.3, "13-34 Youth": 747.4, "13-24 GenA/Z": 433.5},
    "NETFLIX": {"P13+": 915.0, "55+ GenX+": 120.0, "13-54 Majority": 795.0, "13-44 NextGen": 604.2, "13-34 Youth": 398.7, "13-24 GenA/Z": 211.3},
    "GROUPO RECORD": {"P13+": 620.0, "55+ GenX+": 365.0, "13-54 Majority": 255.0, "13-44 NextGen": 186.1, "13-34 Youth": 122.8, "13-24 GenA/Z": 54.8},
    "SBT": {"P13+": 515.0, "55+ GenX+": 290.0, "13-54 Majority": 225.0, "13-44 NextGen": 168.7, "13-34 Youth": 115.8, "13-24 GenA/Z": 53.2},
    "AMAZON": {"P13+": 390.0, "55+ GenX+": 65.0, "13-54 Majority": 325.0, "13-44 NextGen": 266.5, "13-34 Youth": 173.2, "13-24 GenA/Z": 77.9},
    "DISNEY": {"P13+": 325.0, "55+ GenX+": 48.0, "13-54 Majority": 277.0, "13-44 NextGen": 213.3, "13-34 Youth": 139.3, "13-24 GenA/Z": 64.0},
    "WBD": {"P13+": 290.0, "55+ GenX+": 82.0, "13-54 Majority": 208.0, "13-44 NextGen": 151.8, "13-34 Youth": 95.6, "13-24 GenA/Z": 43.0},
    "FACEBOOK": {"P13+": 285.0, "55+ GenX+": 135.0, "13-54 Majority": 150.0, "13-44 NextGen": 85.5, "13-34 Youth": 32.4, "13-24 GenA/Z": 6.3},
    "BAND": {"P13+": 210.0, "55+ GenX+": 122.0, "13-54 Majority": 88.0, "13-44 NextGen": 61.6, "13-34 Youth": 38.7, "13-24 GenA/Z": 15.4}
}
GLOBAL_DATA_REPOSITORY["MX"] = {
    "TELEVISAUNIVISION": {"P13+": 1640.0, "55+ GenX+": 685.0, "13-54 Majority": 955.0, "13-44 NextGen": 744.9, "13-34 Youth": 558.7, "13-24 GenA/Z": 284.9},
    "YOUTUBE": {"P13+": 1390.0, "55+ GenX+": 115.0, "13-54 Majority": 1275.0, "13-44 NextGen": 905.2, "13-34 Youth": 733.2, "13-24 GenA/Z": 476.6},
    "TIKTOK": {"P13+": 860.0, "55+ GenX+": 12.0, "13-54 Majority": 848.0, "13-44 NextGen": 695.3, "13-34 Youth": 591.0, "13-24 GenA/Z": 461.0},
    "INSTAGRAM": {"P13+": 695.0, "55+ GenX+": 18.0, "13-54 Majority": 677.0, "13-44 NextGen": 602.5, "13-34 Youth": 518.1, "13-24 GenA/Z": 305.7},
    "NETFLIX": {"P13+": 635.0, "55+ GenX+": 54.0, "13-54 Majority": 581.0, "13-44 NextGen": 447.4, "13-34 Youth": 295.3, "13-24 GenA/Z": 156.4},
    "TV AZTECA": {"P13+": 485.0, "55+ GenX+": 245.0, "13-54 Majority": 240.0, "13-44 NextGen": 180.0, "13-34 Youth": 122.4, "13-24 GenA/Z": 52.8},
    "AMAZON": {"P13+": 245.0, "55+ GenX+": 32.0, "13-54 Majority": 213.0, "13-44 NextGen": 176.8, "13-34 Youth": 116.7, "13-24 GenA/Z": 52.5},
    "DISNEY": {"P13+": 220.0, "55+ GenX+": 25.0, "13-54 Majority": 195.0, "13-44 NextGen": 152.1, "13-34 Youth": 100.4, "13-24 GenA/Z": 46.2},
    "WBD": {"P13+": 195.0, "55+ GenX+": 42.0, "13-54 Majority": 153.0, "13-44 NextGen": 113.2, "13-34 Youth": 72.4, "13-24 GenA/Z": 33.3},
    "FACEBOOK": {"P13+": 180.0, "55+ GenX+": 78.0, "13-54 Majority": 102.0, "13-44 NextGen": 59.2, "13-34 Youth": 23.1, "13-24 GenA/Z": 4.6}
}

GLOBAL_DATA_REPOSITORY["DE"] = {
    "ARD": {"P13+": 710.0, "55+ GenX+": 560.0, "13-54 Majority": 150.0, "13-44 NextGen": 115.5, "13-34 Youth": 90.1, "13-24 GenA/Z": 57.6},
    "YOUTUBE": {"P13+": 625.0, "55+ GenX+": 135.0, "13-54 Majority": 490.0, "13-44 NextGen": 343.0, "13-34 Youth": 267.5, "13-24 GenA/Z": 163.2},
    "ZDF": {"P13+": 615.0, "55+ GenX+": 505.0, "13-54 Majority": 110.0, "13-44 NextGen": 84.7, "13-34 Youth": 66.1, "13-24 GenA/Z": 42.2},
    "RTL GROUP": {"P13+": 510.0, "55+ GenX+": 310.0, "13-54 Majority": 200.0, "13-44 NextGen": 150.0, "13-34 Youth": 108.0, "13-24 GenA/Z": 49.0},
    "NETFLIX": {"P13+": 445.0, "55+ GenX+": 95.0, "13-54 Majority": 350.0, "13-44 NextGen": 255.5, "13-34 Youth": 160.9, "13-24 GenA/Z": 82.1},
    "TIKTOK": {"P13+": 385.0, "55+ GenX+": 14.0, "13-54 Majority": 371.0, "13-44 NextGen": 289.4, "13-34 Youth": 237.3, "13-24 GenA/Z": 173.2},
    "PROSIEBENSAT.1": {"P13+": 340.0, "55+ GenX+": 195.0, "13-54 Majority": 145.0, "13-44 NextGen": 107.3, "13-34 Youth": 73.0, "13-24 GenA/Z": 31.2},
    "INSTAGRAM": {"P13+": 295.0, "55+ GenX+": 28.0, "13-54 Majority": 267.0, "13-44 NextGen": 232.3, "13-34 Youth": 188.2, "13-24 GenA/Z": 103.5},
    "AMAZON": {"P13+": 230.0, "55+ GenX+": 68.0, "13-54 Majority": 162.0, "13-44 NextGen": 132.8, "13-34 Youth": 82.3, "13-24 GenA/Z": 34.6},
    "DISNEY": {"P13+": 195.0, "55+ GenX+": 42.0, "13-54 Majority": 153.0, "13-44 NextGen": 116.3, "13-34 Youth": 73.3, "13-24 GenA/Z": 30.3},
    "WBD": {"P13+": 145.0, "55+ GenX+": 78.0, "13-54 Majority": 67.0, "13-44 NextGen": 48.9, "13-34 Youth": 30.8, "13-24 GenA/Z": 12.7},
    "FACEBOOK": {"P13+": 140.0, "55+ GenX+": 82.0, "13-54 Majority": 58.0, "13-44 NextGen": 31.9, "13-34 Youth": 11.8, "13-24 GenA/Z": 2.2}
}
GLOBAL_DATA_REPOSITORY["UK"] = {
    "BBC": {"P13+": 640.0, "55+ GenX+": 460.0, "13-54 Majority": 180.0, "13-44 NextGen": 122.4, "13-34 Youth": 85.7, "13-24 GenA/Z": 45.4},
    "YOUTUBE": {"P13+": 590.0, "55+ GenX+": 110.0, "13-54 Majority": 480.0, "13-44 NextGen": 336.0, "13-34 Youth": 262.1, "13-24 GenA/Z": 159.9},
    "ITV PLC": {"P13+": 510.0, "55+ GenX+": 335.0, "13-54 Majority": 175.0, "13-44 NextGen": 113.8, "13-34 Youth": 75.1, "13-24 GenA/Z": 36.8},
    "NETFLIX": {"P13+": 495.0, "55+ GenX+": 105.0, "13-54 Majority": 390.0, "13-44 NextGen": 284.7, "13-34 Youth": 179.4, "13-24 GenA/Z": 91.5},
    "TIKTOK": {"P13+": 410.0, "55+ GenX+": 18.0, "13-54 Majority": 392.0, "13-44 NextGen": 305.8, "13-34 Youth": 250.7, "13-24 GenA/Z": 183.0},
    "SKY GROUP": {"P13+": 385.0, "55+ GenX+": 210.0, "13-54 Majority": 175.0, "13-44 NextGen": 119.0, "13-34 Youth": 70.2, "13-24 GenA/Z": 28.8},
    "INSTAGRAM": {"P13+": 275.0, "55+ GenX+": 28.0, "13-54 Majority": 247.0, "13-44 NextGen": 214.9, "13-34 Youth": 174.1, "13-24 GenA/Z": 95.8},
    "PARAMOUNT": {"P13+": 245.0, "55+ GenX+": 155.0, "13-54 Majority": 90.0, "13-44 NextGen": 61.2, "13-34 Youth": 36.1, "13-24 GenA/Z": 14.8},
    "WBD": {"P13+": 220.0, "55+ GenX+": 128.0, "13-54 Majority": 92.0, "13-44 NextGen": 62.6, "13-34 Youth": 31.3, "13-24 GenA/Z": 13.1},
    "CHANNEL 4": {"P13+": 290.0, "55+ GenX+": 165.0, "13-54 Majority": 125.0, "13-44 NextGen": 85.0, "13-34 Youth": 50.2, "13-24 GenA/Z": 20.6},
    "FACEBOOK": {"P13+": 210.0, "55+ GenX+": 115.0, "13-54 Majority": 95.0, "13-44 NextGen": 52.3, "13-34 Youth": 19.3, "13-24 GenA/Z": 3.7},
    "AMAZON": {"P13+": 195.0, "55+ GenX+": 62.0, "13-54 Majority": 133.0, "13-44 NextGen": 109.1, "13-34 Youth": 67.6, "13-24 GenA/Z": 28.4}
}

GLOBAL_DATA_REPOSITORY["FR"] = {
    "YOUTUBE": {"P13+": 485.0, "55+ GenX+": 95.0, "13-54 Majority": 390.0, "13-44 NextGen": 273.0, "13-34 Youth": 212.9, "13-24 GenA/Z": 129.9},
    "TIKTOK": {"P13+": 335.0, "55+ GenX+": 12.0, "13-54 Majority": 323.0, "13-44 NextGen": 251.9, "13-34 Youth": 206.6, "13-24 GenA/Z": 150.8},
    "NETFLIX": {"P13+": 390.0, "55+ GenX+": 85.0, "13-54 Majority": 305.0, "13-44 NextGen": 222.7, "13-34 Youth": 140.3, "13-24 GenA/Z": 71.6},
    "INSTAGRAM": {"P13+": 215.0, "55+ GenX+": 20.0, "13-54 Majority": 195.0, "13-44 NextGen": 169.7, "13-34 Youth": 137.5, "13-24 GenA/Z": 75.6},
    "TF1": {"P13+": 440.0, "55+ GenX+": 270.0, "13-54 Majority": 170.0, "13-44 NextGen": 136.0, "13-34 Youth": 102.0, "13-24 GenA/Z": 51.8},
    "DISNEY": {"P13+": 180.0, "55+ GenX+": 42.0, "13-54 Majority": 138.0, "13-44 NextGen": 104.9, "13-34 Youth": 66.1, "13-24 GenA/Z": 27.3},
    "FRANCE TV": {"P13+": 510.0, "55+ GenX+": 385.0, "13-54 Majority": 125.0, "13-44 NextGen": 102.5, "13-34 Youth": 82.0, "13-24 GenA/Z": 54.2},
    "ARTE": {"P13+": 120.0, "55+ GenX+": 57.6, "13-54 Majority": 62.4, "13-44 NextGen": 48.0, "13-34 Youth": 33.6, "13-24 GenA/Z": 10.1},
    "GROUP M6": {"P13+": 265.0, "55+ GenX+": 145.0, "13-54 Majority": 120.0, "13-44 NextGen": 93.6, "13-34 Youth": 65.5, "13-24 GenA/Z": 29.5},
    "AMAZON": {"P13+": 155.0, "55+ GenX+": 48.0, "13-54 Majority": 107.0, "13-44 NextGen": 87.7, "13-34 Youth": 54.4, "13-24 GenA/Z": 22.8},
    "WBD": {"P13+": 170.0, "55+ GenX+": 95.0, "13-54 Majority": 75.0, "13-44 NextGen": 54.8, "13-34 Youth": 34.5, "13-24 GenA/Z": 14.3},
    "L'ÉQUIPE": {"P13+": 65.0, "55+ GenX+": 19.5, "13-54 Majority": 45.5, "13-44 NextGen": 33.7, "13-34 Youth": 21.6, "13-24 GenA/Z": 8.9},
    "CANAL+ GROUP": {"P13+": 195.0, "55+ GenX+": 115.0, "13-54 Majority": 80.0, "13-44 NextGen": 58.4, "13-34 Youth": 40.9, "13-24 GenA/Z": 13.9},
    "FACEBOOK": {"P13+": 165.0, "55+ GenX+": 92.0, "13-54 Majority": 73.0, "13-44 NextGen": 40.2, "13-34 Youth": 14.9, "13-24 GenA/Z": 2.8},
    "DAZN": {"P13+": 20.0, "55+ GenX+": 2.0, "13-54 Majority": 18.0, "13-44 NextGen": 16.2, "13-34 Youth": 12.8, "13-24 GenA/Z": 7.7}
}

GLOBAL_DATA_REPOSITORY["ES"] = {
    "RTVE": {"P13+": 395.0, "55+ GenX+": 295.0, "13-54 Majority": 100.0, "13-44 NextGen": 77.0, "13-34 Youth": 55.4, "13-24 GenA/Z": 35.5},
    "ATRESMEDIA": {"P13+": 380.0, "55+ GenX+": 235.0, "13-54 Majority": 145.0, "13-44 NextGen": 108.8, "13-34 Youth": 78.3, "13-24 GenA/Z": 39.5},
    "YOUTUBE": {"P13+": 365.0, "55+ GenX+": 85.0, "13-54 Majority": 280.0, "13-44 NextGen": 196.0, "13-34 Youth": 152.9, "13-24 GenA/Z": 93.3},
    "MEDIASET ESPANA": {"P13+": 320.0, "55+ GenX+": 198.0, "13-54 Majority": 122.0, "13-44 NextGen": 91.5, "13-34 Youth": 65.9, "13-24 GenA/Z": 33.3},
    "TIKTOK": {"P13+": 255.0, "55+ GenX+": 10.0, "13-54 Majority": 245.0, "13-44 NextGen": 191.1, "13-34 Youth": 156.7, "13-24 GenA/Z": 114.4},
    "NETFLIX": {"P13+": 240.0, "55+ GenX+": 52.0, "13-54 Majority": 188.0, "13-44 NextGen": 137.2, "13-34 Youth": 86.5, "13-24 GenA/Z": 44.1},
    "INSTAGRAM": {"P13+": 215.0, "55+ GenX+": 20.0, "13-54 Majority": 195.0, "13-44 NextGen": 169.7, "13-34 Youth": 137.5, "13-24 GenA/Z": 75.6},
    "MOVISTAR+": {"P13+": 145.0, "55+ GenX+": 82.0, "13-54 Majority": 63.0, "13-44 NextGen": 44.1, "13-34 Youth": 26.5, "13-24 GenA/Z": 11.1},
    "DISNEY": {"P13+": 115.0, "55+ GenX+": 24.0, "13-54 Majority": 91.0, "13-44 NextGen": 69.2, "13-34 Youth": 43.6, "13-24 GenA/Z": 18.0},
    "WBD (MAX)": {"P13+": 105.0, "55+ GenX+": 55.0, "13-54 Majority": 50.0, "13-44 NextGen": 36.5, "13-34 Youth": 23.0, "13-24 GenA/Z": 9.6},
    "AMAZON": {"P13+": 95.0, "55+ GenX+": 28.0, "13-54 Majority": 67.0, "13-44 NextGen": 54.9, "13-34 Youth": 34.0, "13-24 GenA/Z": 14.3},
    "FACEBOOK": {"P13+": 90.0, "55+ GenX+": 55.0, "13-54 Majority": 35.0, "13-44 NextGen": 19.3, "13-34 Youth": 7.1, "13-24 GenA/Z": 1.3}
}
GLOBAL_DATA_REPOSITORY["IT"] = {
    "RAI": {"P13+": 520.0, "55+ GenX+": 415.0, "13-54 Majority": 105.0, "13-44 NextGen": 80.9, "13-34 Youth": 58.2, "13-24 GenA/Z": 37.2},
    "YOUTUBE": {"P13+": 440.0, "55+ GenX+": 110.0, "13-54 Majority": 330.0, "13-44 NextGen": 231.0, "13-34 Youth": 180.2, "13-24 GenA/Z": 109.9},
    "MFE (MEDIASET)": {"P13+": 415.0, "55+ GenX+": 265.0, "13-54 Majority": 150.0, "13-44 NextGen": 112.5, "13-34 Youth": 81.0, "13-24 GenA/Z": 40.8},
    "TIKTOK": {"P13+": 295.0, "55+ GenX+": 12.0, "13-54 Majority": 283.0, "13-44 NextGen": 220.7, "13-34 Youth": 181.0, "13-24 GenA/Z": 132.1},
    "NETFLIX": {"P13+": 310.0, "55+ GenX+": 70.0, "13-54 Majority": 240.0, "13-44 NextGen": 175.2, "13-34 Youth": 110.4, "13-24 GenA/Z": 56.3},
    "INSTAGRAM": {"P13+": 250.0, "55+ GenX+": 25.0, "13-54 Majority": 225.0, "13-44 NextGen": 195.8, "13-34 Youth": 158.6, "13-24 GenA/Z": 87.2},
    "SKY ITALIA": {"P13+": 175.0, "55+ GenX+": 102.0, "13-54 Majority": 73.0, "13-44 NextGen": 50.4, "13-34 Youth": 29.7, "13-24 GenA/Z": 12.2},
    "DISNEY": {"P13+": 170.0, "55+ GenX+": 38.0, "13-54 Majority": 132.0, "13-44 NextGen": 100.3, "13-34 Youth": 63.2, "13-24 GenA/Z": 26.1},
    "WBD": {"P13+": 165.0, "55+ GenX+": 92.0, "13-54 Majority": 73.0, "13-44 NextGen": 51.1, "13-34 Youth": 31.7, "13-24 GenA/Z": 12.9},
    "FACEBOOK": {"P13+": 160.0, "55+ GenX+": 101.0, "13-54 Majority": 59.0, "13-44 NextGen": 32.5, "13-34 Youth": 12.0, "13-24 GenA/Z": 2.3},
    "AMAZON": {"P13+": 140.0, "55+ GenX+": 42.0, "13-54 Majority": 98.0, "13-44 NextGen": 80.4, "13-34 Youth": 49.8, "13-24 GenA/Z": 20.9}
}

# Master Dynamic Relational UI Presentation Tag Invariant Map
REGIONAL_UI_LABELS = {
    "US": {"YOUTUBE": "YOUTUBE", "DISNEY": "DISNEY", "NETFLIX": "NETFLIX", "TIKTOK": "TIKTOK", "PARAMOUNT": "PARAMOUNT", "NBCU": "NBCU", "INSTAGRAM": "INSTAGRAM", "WBD": "WBD", "FACEBOOK": "FACEBOOK", "AMAZON": "AMAZON", "FOX": "FOX"},
    "UK": {"BBC": "BBC", "YOUTUBE": "YOUTUBE", "ITV PLC": "ITV PLC", "NETFLIX": "NETFLIX", "TIKTOK": "TIKTOK", "SKY GROUP": "SKY GROUP", "INSTAGRAM": "INSTAGRAM", "PARAMOUNT": "PARAMOUNT (Channel 5)", "WBD": "WBD", "CHANNEL 4": "CHANNEL 4", "FACEBOOK": "FACEBOOK", "AMAZON": "AMAZON"},
    "FR": {"YOUTUBE": "YOUTUBE", "TIKTOK": "TIKTOK", "NETFLIX": "NETFLIX", "INSTAGRAM": "INSTAGRAM", "TF1": "TF1", "DISNEY": "DISNEY", "FRANCE TV": "FRANCE TV", "ARTE": "ARTE", "M6": "GROUP M6", "AMAZON": "AMAZON", "WBD": "WBD (MAX / Eurosport)", "LEQUIPE": "L'ÉQUIPE", "CANAL+ GROUP": "CANAL+ GROUP", "FACEBOOK": "FACEBOOK", "DAZN": "DAZN"},
    "DE": {"ARD": "ARD", "YOUTUBE": "YOUTUBE", "ZDF": "ZDF", "RTL GROUP": "RTL GROUP", "NETFLIX": "NETFLIX", "TIKTOK": "TIKTOK", "PROSIEBENSAT.1": "PROSIEBENSAT.1", "INSTAGRAM": "INSTAGRAM", "AMAZON": "AMAZON", "DISNEY": "DISNEY", "WBD": "WBD (MAX / Discovery)", "FACEBOOK": "FACEBOOK"},
    "ES": {"RTVE": "RTVE", "ATRESMEDIA": "ATRESMEDIA", "YOUTUBE": "YOUTUBE", "MEDIASET ESPANA": "MEDIASET ESPAÑA", "TIKTOK": "TIKTOK", "NETFLIX": "NETFLIX", "INSTAGRAM": "INSTAGRAM", "MOVISTAR+": "MOVISTAR+", "DISNEY": "DISNEY", "WBD (MAX)": "WBD (MAX)", "AMAZON": "AMAZON", "FACEBOOK": "FACEBOOK"},
    "BR": {"GLOBO": "GRUPO GLOBO", "YOUTUBE": "YOUTUBE", "TIKTOK": "TIKTOK", "INSTAGRAM": "INSTAGRAM", "NETFLIX": "NETFLIX", "RECORD": "GROUPO RECORD", "SBT": "SBT", "AMAZON": "AMAZON", "DISNEY": "DISNEY", "WBD": "WBD (MAX)", "FACEBOOK": "FACEBOOK", "BAND": "BAND"},
    "MX": {"TELEVISAUNIVISION": "TELEVISAUNIVISION", "YOUTUBE": "YOUTUBE", "TIKTOK": "TIKTOK", "INSTAGRAM": "INSTAGRAM", "NETFLIX": "NETFLIX", "TV_AZTECA": "TV AZTECA", "AMAZON": "AMAZON", "DISNEY": "DISNEY", "WBD": "WBD (MAX)", "FACEBOOK": "FACEBOOK"}
}
# =====================================================================================
# CORE STRUCTURAL MATHEMATICAL ENGINES
# =====================================================================================

def apply_closed_system_normalization(df_raw, capacity_ceiling, protection_multipliers):
    """
    Overrolls intermedia volume addition with structural territory constraints (alpha)
    compressing totals back down to the target market's fixed Awake Time Budget.
    """
    df_normalized = df_raw.copy()
    df_normalized['Intermediate_Weight'] = df_normalized.apply(
        lambda r: r['Value'] * protection_multipliers.get(r['Platform/Publisher'], 1.000), axis=1
    )
    total_intermediate_weight = df_normalized['Intermediate_Weight'].sum()
    if total_intermediate_weight > 0:
        df_normalized['Value'] = (df_normalized['Intermediate_Weight'] / total_intermediate_weight) * capacity_ceiling
    else:
        df_normalized['Value'] = 0.0
    return df_normalized.drop(columns=['Intermediate_Weight'])


def execute_meta_parent_consolidation(dataframe_current):
    """
    Executes cross-app sliding-scale de-duplication vectors penalizing multi-switching
    among narrower young cohorts while honoring linear legacy baseline habits.
    """
    DUPLICATION_VECTOR = {
        "P13+": 0.18, "55+ GenX+": 0.04, "13-54 Majority": 0.15,
        "13-44 NextGen": 0.20, "13-34 Youth": 0.24, "13-24 GenA/Z": 0.32
    }
    df_output = dataframe_current.copy()
    if "INSTAGRAM" in df_output["Platform/Publisher"].values and "FACEBOOK" in df_output["Platform/Publisher"].values:
        meta_row = {"Platform/Publisher": "META"}
        for col in df_output.columns:
            if col != "Platform/Publisher":
                v_ig = float(df_output[df_output["Platform/Publisher"] == "INSTAGRAM"][col].values[0])
                v_fb = float(df_output[df_output["Platform/Publisher"] == "FACEBOOK"][col].values[0])
                delta = DUPLICATION_VECTOR.get(col, 0.15)
                meta_row[col] = (v_ig + v_fb) * (1.000 - delta)
        df_output = df_output[~df_output["Platform/Publisher"].isin(["INSTAGRAM", "FACEBOOK"])]
        df_output = pd.concat([df_output, pd.DataFrame([meta_row])], ignore_index=True)
    return df_output
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

st.sidebar.markdown("### Test Market Share Shifts - Add/Subtract Attention And See Where It Would Be Reallocated\n## **MILLIONS OF HOURS**")
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
            
            # Extract the raw float scalar value out of the array to prevent type conversion errors
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

# Programmatic Tab 4-Interface Engine Initialization Split
tab1, tab2, tab3, tab4 = st.tabs(["CSAI Interactive Index Matrix", "Why ECSAI?", "ECSAI FAQs", "Index Architecture & Methodology"])
with tab1:
    st.subheader(f"Cross-Screen Attention Allocation Ledger: {active_flag} {market_choice}")
    st.markdown("<p style='font-size: 0.92rem; font-weight: bold; font-style: italic; color: var(--text-color, inherit); margin-top: -0.75rem; margin-bottom: 0.75rem;'>MILLIONS OF HOURS</p>", unsafe_allow_html=True)
    
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
    st.write("")
    
    st.markdown("#### Interactive Visual Share Map")
    st.markdown("<p style='font-size: 0.92rem; font-weight: bold; font-style: italic; color: var(--text-color, inherit); margin-top: -0.5rem; margin-bottom: 0.75rem;'>MILLIONS OF HOURS</p>", unsafe_allow_html=True)
    
    st.html("<style>div[data-testid='stRadio'] > div { gap: 1.5rem !important; } div[data-testid='stRadio'] label p { font-size: 0.95rem !important; white-space: nowrap !important; }</style>")
    demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
    selected_demo = st.radio("Select Demographic Cohort to Isolate in Bar Chart:", options=["Cohorts Overlaid"] + demo_columns, horizontal=True)
    
    chart_df = df_matrix.copy()
    chart_df["Platform/Publisher"] = chart_df["Platform/Publisher"].replace({"GROUPO RECORD": "RECORD"})
    chart_df = chart_df.set_index("Platform/Publisher")
    chart_metrics = ["P13+", "13-54 Majority", "55+ GenX+"] if selected_demo == "Cohorts Overlaid" else [selected_demo]
    st.bar_chart(chart_df[chart_metrics], horizontal=True, height=380, use_container_width=True)
    
    if market_choice == "Brazil":
        st.markdown("<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross-Screen Attention Allocation Ledger: BRAZIL</strong><br>Platform totals represent unified corporate parent structures. Grupo Globo incorporates all Globoplay streaming telemetry. WBD fully encapsulates Max sessions and TNT Sports premium footprints. Concurrent multi-screening duplication and passive device use discounted.</p>", unsafe_allow_html=True)
    elif market_choice == "Mexico":
        st.markdown("<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross-Screen Attention Allocation Ledger: MEXICO</strong><br>Platform totals represent unified corporate parent structures. TelevisaUnivision incorporates all ViX streaming telemetry. YouTube and mobile digital baselines natively absorb all open-distribution and telco-bundled attention siphons, including consolidated cross-screen volumes for Claro Sports and Uno TV. Concurrent multi-screening duplication and passive device use discounted.</p>", unsafe_allow_html=True)
    elif market_choice in ["France", "Germany", "United Kingdom", "Italy", "Spain"]:
        st.markdown(f"<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross-Screen Attention Allocation Ledger: {market_choice.upper()}</strong><br>Platform totals represent unified holding corporate structures. Traditional TV volumes are scaled using audited single-screen panel metrics from regional state-backed systems (including BARB, Médiamétrie, and Agf/Gfk) and balanced against hardware-level handset logs. Multi-screening and background device noise programmatically flattened through duplication discounts to retain zero-sum integrity.</p>", unsafe_allow_html=True)
        
    st.download_button(label="Export Current Ledger to CSV", data=df_matrix.to_csv(index=False).encode('utf-8'), file_name=f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv", mime="text/csv", use_container_width=True)
with tab2:
    st.subheader("Why ECSAI? Understanding the Cross-Screen Attention Index")
    st.markdown("In the commercial Media industry, measurement has always been divided by screens. No major auditing bureau or currency panel has ever forced television meters, handset timestamps, and browser logs into a singular, logic-enforced, zero-sum attention budget. **This is collective malpractice.** If you still treat social video and television as separate silos, to twist the age-old Wanamaker adage: *You are wasting half your money.*")
    st.markdown("In the next three years, one trillion dollars will be spent on advertising in the US alone. More than three quarters of that will be spent on digital platforms. Another \$180 billion will be spent on television advertising. No one is measuring the reach, frequency, or effectiveness of this massive cashflow across these platforms.")
    
    if os.path.exists("eshap_us_devices.png"): 
        st.image("eshap_us_devices.png", caption="Video Consumption Share By Device Ecosystem (US Baseline)", use_container_width=True)
    else: 
        st.info("💡 *[Placeholder for eshap_us_devices.png: In a recent survey of 3,000 US consumers, 59% watch video primarily on phones vs 28% on traditional TV glass]*")
    
    st.markdown("Publishers and advertisers look at their TV ratings, digital buyers and social media experts look at mobile handset logs, and everybody claims they are winning the war for reach. Meanwhile the measurement industry locks agencies into long-term contracts, then charges sellers through the nose to use their 'currency.' Or, they will track attention across all the platforms, but only by campaign - not as a map nor trajectory of total cross-screen attention. This leaves our collective data on real attention siloed to the point of pointlessness.")
    st.markdown("The industry is totally blind to how real people actually behave. Today's consumer is a singular, fluid entity moving seamlessly across a multi-screen day, allocating a single, finite commodity: attention.")
    st.markdown("The Media industry is lost specifically because they are charting their course based on the failed logic of vanity metrics, rather than following the actual data; the voice of the audience.")
    
    if os.path.exists("eshap_devicesgen.png"): 
        st.image("eshap_devicesgen.png", caption="Video Device Preference Layout Broken Down Across Generational Cohorts", use_container_width=True)
    else: 
        st.info("💡 *[Placeholder for eshap_devicesgen.png: Media Generation Gap breakdown charting step-down linear curves from 18-24 up to Boomer demographics]*")
    
    st.markdown("Only Baby Boomers watch more video on televisions than on phones. Every other generation of Americans watches video on their phones two to three times more than their TVs.")
    st.markdown("We have conducted the same study across the Big 5 in Europe. The results are not identical - but they are quite similar. You can see all this survey data on Media War & Peace.")
    st.markdown("This is the Media Generation Gap.")
    st.markdown("We have been studying this trend. We have become obsessed with the idea of measuring total attention among competing platforms across all screens.")
    st.markdown("As far as I can tell, the ESHAP Cross-Screen Attention Index (ECSAI) represents something never achieved in media analytics: a singular, logic-enforced, zero-sum attention budget that tracks the whole consumer across all attention endpoints simultaneously.")
    st.markdown("By treating human focus as a tangible physical property constrained by a fixed 24-hour clock, we built a model that removes corporate bias, complacency, and corruption from measurement.")
    st.markdown("Please check out our Methodology Blueprint and Sourcing Matrix pages for more details on how we created this index across all these regions.")
    st.markdown("The results in this index show, for the first time, a more accurate media hierarchy across every format and screen — from vertical social feeds and letterboxed streaming to smartphones, laptops, and Connected TVs. Is this Index a 110% perfect read of all Media usage? No. Does it provide a clearer, more accurate account of actual, total Media attention in these regions than the industry has ever had? Hells to the yeah.")
    st.markdown("Here's the craziest part of this (and the point of this exercise for us):")
    st.markdown("The underlying raw inputs we used to construct this index — regulatory agency white papers, investor relations slide decks, quarterly financial reporting statements, public commission audits from accredited data providers, government agencies, public utilities, and published research — are all 100% publicly available, out in the open for anyone to access. Our methodology does not rely on secretly passed corporate logs or restricted database leaks, or paywalled data dashboards. Instead, we took fragmented fragments of data that sit in the open public domain and applied a proprietary mathematical synthesis that no one else has bothered to execute, until now.")
    st.markdown("Why? Because our industry is kept in eat-what-you-kill silos. So we don't ask.")
    st.markdown("Our data construct is sound. But the framework for this index is not built solely on quantitative analysis. Each year, we interview hundreds of experts, practitioners, vendors, buyers, managers, executives, interns, academics, data scientists, platforms, publishers, producers, and members of our community. On nearly every one of our working days.")
    st.markdown("The numbers in this index are from companies we all know. So is the point of view. We ask the right questions - in this case, where is the attention of the whole consumer actually going — because everyone asked us.")
    st.markdown("That fear of finding out is the systemic blindness now pushing our industry off a cliff. Thus, the ECSAI - the ESHAP Cross-Screen Attention Index. It's our new compass toward today's audience: The Whole Consumer.")
    st.write("---")
    st.markdown(
        "<p style='font-size: 0.92rem; font-weight: bold; line-height: 1.5; color: var(--text-color, inherit); font-style: normal;'>"
        "There is more to come &ndash; more regions, more detailed data cuts, more!<br><br>"
        "We would love to know what you think. Please send your feedback and questions to "
        "<a href='https://substack.com' target='_blank' style='color: #007bff; text-decoration: underline; font-weight: bold;'>info@eshap.tv</a>.<br><br>"
        "Cheers!<br><br>"
        "ESHAP"
        "</p>", 
        unsafe_allow_html=True
    )
with tab3:
    st.subheader("ECSAI Frequently Asked Questions (FAQs)")
    st.markdown("#### HOW DID WE CHOOSE THE VARIOUS COMBINATION OF SOURCES FOR THE INDEX ACROSS THE REGIONS?")
    st.markdown("To establish an unassailable cross-border baseline, data sources for each country were selected based on three criteria: sovereign regulatory authority, parent corporate transparency, and audited single-screen telemetry. The index ingests data from official state census registries (such as INSEE, Destatis, and the ONS) for macro population controls, alongside published annual disclosures from public service broadcasters and quarterly investor relations filings from publicly traded platforms. To bridge the traditional glass and mobile screen gap, these baselines are matched against the hardware-level device telemetry of globally recognized digital tracking firms and local regulatory media white papers. This ensures that every source component sits legitimately in the open public domain, provides absolute consistency in tracking parent corporate holding structures, and natively supports the normalization of disparate metrics into absolute hours of focused human attention.")
    st.markdown("#### HOW DO YOU BLEND THE VARIOUS INPUTS - GLASS DATA, CENSUS, DIARIES - INTO ONE SMOOTH INDEX FOR EACH COUNTRY, CUTTING ACROSS DEMOS BASED ONLY ON PUBLICLY AVAILABLE DATA?")
    st.markdown("To blend these completely disparate public inputs into a single, seamless cross-screen index for each territory, our model runs a three-step mathematical normalization loop that forces apples-and-oranges data into a strict, logic-enforced daily time budget. Because we use free, un-siloed data scattered across corporate and government reports, our system treats each country as a closed market sponge where total population and total available hours are hard constants.")
    st.markdown("Here is the exact step-by-step math mechanics of how the index blends glass data, census records, and consumer diaries into a single smooth number for each demographic cohort:")
    st.markdown("**Census Denominator Lock (The Total Volume Ceiling)**<br>The entire model is anchored on the local state census registry (such as INSEE, Destatis, ISTAT, or the U.S. Census Bureau). The index takes the total population headcount for the territory, filters for the P13+ universe. It then establishes a Total Available Awake Hours Budget per month (assuming a standardized 16-hour active day). This number is our absolute ceiling. It represents the total size of the market sponge. No matter how many apps or TV channels claim massive usage, the combined monthly hours in our index can never exceed this hard, census-backed population budget.", unsafe_allow_html=True)
    st.markdown("**Normalizing Metrics into 'Absolute Attention Hours'**<br>Next, our model takes the fragmented public data points and converts them into a singular currency: Millions of Attention Hours per Month. *Blending the Glass and Feed Data:* Traditional linear TV currencies (like Médiamétrie or BARB) publish reach and 'Time Spent Viewing' (TSV) per day. The model takes the average daily TSV for a specific cohort, multiplies it by the demographic population weight from the census, and scales it to 30 days to find total linear hours. Big Tech investor filings and regulatory white papers present usage in 'Daily Active Users' (DAUs) or 'Monthly Active Users' (MAUs) paired with global or regional average session lengths. The model intercepts these ratios, applies the local territory footprint weight, and multiplies active users by daily active minutes to extract total digital hours. We take the stated number of users per digital platforms, apportion them by region/populations, then using diaries, surveys, public reports, and other regional research data, the model assigns pro rata usage hours per day in those regions.", unsafe_allow_html=True)
    st.markdown("**The Zero-Sum Squeeze and Diary De-Duplication**<br>This is where the smooth, cross-screen blending actually happens. If we simply added the television hours to the digital hours, the market sponge would explode past the census ceiling. This over-allocation happens because of concurrent multi-screening -- a consumer scrolling on TikTok while the television plays a telenovela or news broadcast in the background. *The Diary Filter:* Our index model applies localized duplication coefficients derived from GWI Consumer Diaries and Dentsu/Lumen attention panels. These diaries track the percentage of a cohort that multi-screens daily (e.g., 77% of Gen Z in France). *The Squeeze:* The model uses this percentage to calculate a duplication discount factor. It treats human attention as a finite zero-sum resource: if the eye is looking at a smartphone screen, that fraction of time is physically subtracted from the traditional television glass volume. Digital hours (which require active, focused scrolling on a handheld device) are treated as hard, primary attention blocks. Glass hours are programmatically squeezed until the multi-screen overlap is flattened and duplication is erased.", unsafe_allow_html=True)
    st.markdown("**The Generational Decay Calibration**<br>This is a crucial step to understanding how populations in different regions adapt to different media differently.", unsafe_allow_html=True)
    st.markdown("To cut smoothly across the narrower demographic tiers (13-44, 13-34, 13-24) based only on public data, the model processes the numbers through localized fractional decay curves. Instead of assuming identical generational behavioral migration everywhere, the curves are adjusted using the baseline ratios found in the regulatory white papers (like Ofcom's Media Nations or Arcom's reports). The system applies a *Nested Funnel Safety Guard:* A strict structural logic barrier hardcoded into the model to ensure horizontal and vertical cohort integrity; this mathematically prevents narrower, younger generational slices of the population from ever showing a higher attention volume than the broader demographics that encapsulate them. This forces a mathematical step-down multiplier from left to right. This ensures that as the age bracket narrows, the legacy broadcaster values decay smoothly according to local policy protections, while the digital platform volumes scale up without causing a data inflation spill -- more attention data than the population of any region could fill in any one day.", unsafe_allow_html=True)
    
    st.markdown("#### IF YOUR MODEL RELIES ON PUBLIC DATA, HOW QUICKLY CAN IT ADAPT WHEN A BRAND-NEW PLATFORM LAUNCHES AND STARTS STEALING ATTENTION?")
    st.markdown("Because the index is built as a strict closed time budget, focused on the consumer, it adapts with consumer attention. If a new platform experiences a sudden user growth explosion, its daily active user metrics and time-spent parameters will show up in public regulatory papers and quarterly financial investor filings. Is there a lag? Yes. Welcome to measurement. When that new platform line-item is introduced to the index, the pro-rata redistribution algorithm automatically squeezes the existing rows down to make room for it. The zero-sum daily clock allows for new platform gains by subtracting from the rest of the market budget, based on the combination of corporate earnings, public records, and ongoing panel diaries.")
    
    st.markdown("#### HOW DID YOU CHOOSE THESE REGIONS TO INCLUDE FIRST?")
    st.markdown("The selection of these eight territories for the initial rollout was driven by a two-part economic framework: macro-advertising scale and demographic diversity. Rather than picking markets at random, we prioritized the absolute largest media-buying engines on earth alongside the core European and Latin American bellwethers that dictate global distribution strategies. The index natively anchors itself in the highest-monetized ad economies in the Western hemisphere. The United States stands as the undisputed global capital of ad-supported media volume, the United Kingdom represents the most digitally advanced, frictionless English-speaking market in Europe, while Germany commands the absolute largest total advertising and consumer economy on the European continent.")
    st.markdown("The index must be stress-tested against markets that actively resist international digital migration through aggressive state intervention and distinct cultural infrastructure, such as Italy, France, and Spain. By forcing the zero-sum model to process these three protectionist territories, by engineering specialized local policy friction curves to honor their defensive cushions, the index can be a flexible global tool, not just a cookie-cutter American proxy. To balance the inverted, aging demographic pyramids of Europe, the index integrates the two heavyweights of Latin America. Brazil and Mexico represent massive, youth-heavy populations that boast some of the highest daily smartphone video consumption lengths on earth. Including these territories allows us to visualize the absolute opposite end of the media lifecycle: markets where traditional pay-TV infrastructures are entirely bypassable, mobile-velocity acceleration is absolute, and tech utilities operate at an unprecedented 97% to 98% workforce density.")
    st.markdown("We did not include Asia or a wider Latin American footprint in this initial launch for one reason: data maturity and local currency standardization. To deliver a logic-enforced zero-sum matrix, the index requires every country baseline to sit completely transparently in the public domain. The foundational data layers - specifically, open regulatory white papers, audited public broadcaster disclosures, and standardized local device telemetry panels - must possess structural transparency. Markets like Japan, South Korea, India, and smaller Latin American territories currently operate on highly fragmented, proprietary, or state-cloaked measurement silos. Trying to force those opaque systems into a strict human daily clock, right now, requires speculative modeling that compromises the index's standard of data integrity.")
    
    st.markdown("#### DOESN'T BLENDING 'SOFT' SURVEY RECALL WITH 'HARD' DEVICE TELEMETRY CORRUPT THE DATA FOUNDATION?")
    st.markdown("The index operates on a strict Separation of Powers. We use a Sovereign Boundary Model where the hard quantitative ceilings are locked down entirely by currency-grade, hard telemetry logs (Nielsen, BARB, Médiamétrie, Comscore). The index does not ask consumers how many hours they watched; it uses hard regulatory telemetry to establish total volume. Behavioral surveys (GWI) are introduced strictly as a coefficient matrix to calculate the mathematical overlap when two devices are running in the same room. We use behavioral data solely to map the friction points where those macro volumes intersect. Legacy currencies rely on passive boxes in empty rooms, counting a television playing to an empty sofa as a hit. We use behavioral data to verify human presence and device co-activity, injecting human reality back into blind hardware metrics.")
    
    st.markdown("#### ISN'T IT AN 'EQUIVALENCY FALLACY' TO TREAT A SMALL MOBILE SCREEN THE SAME AS A 75-INCH LIVING ROOM TV?")
    st.markdown("The fallacy is in the concept of 'premium attention.' It is a self-serving myth designed to protect high television CPMs. Screen size does not equal cognitive impact. A living room television screen frequently functions as ambient, household background noise. Conversely, a smartphone screen requires active physical interaction - holding, scrolling, unmuting - to maintain the media stream. This index does not flatten attention; it democratizes conscious eye-hours. Our Attention Index (ECSAI, pronounced EE-say) strips away the unearned premium of the living room glass when it isn't actually being watched, exposing how mobile feeds capture high-intensity, active physical engagement - even in front of a playing TV set. If the eye is looking at a smartphone screen, that fraction of time is physically subtracted from the traditional television volume, regardless of how large the TV glass is. That is the real premium.")
    
    st.markdown("#### IF A MEDIA BUYER CANNOT USE THIS HIGH-LEVEL DASHBOARD TO EXECUTE AN AD PLACEMENT ON A DSP, ISN'T THE DATA TOO COARSE FOR REAL-WORLD BUYING?")
    st.markdown("This app is a macroeconomic strategy engine, not a trading desk. It is built specifically for members of the Media community to audit structural asset mismatches. If your enterprise allocates 60% of its budget to a legacy channel that commands only 15% of your target workforce demographic's finite daily time budget, that is an enterprise failure. This scale is built to align multi-million-dollar corporate capital allocations with human reality, not to execute a local programmatic trade.")
    
    st.write("---")
    st.markdown(
        "<p style='font-size: 0.92rem; font-weight: bold; line-height: 1.5; color: var(--text-color, inherit); font-style: normal;'>"
        "There is more to come &ndash; more regions, more detailed data cuts, more!<br><br>"
        "We would love to know what you think. Please send your feedback and questions to "
        "<a href='mailto:info@eshap.tv' style='color: #007bff; text-decoration: underline; font-weight: bold;'>info@eshap.tv</a>.<br><br>"
        "Cheers!<br><br>"
        "ESHAP"
        "</p>", 
        unsafe_allow_html=True
    )

with tab4:
    # Restored Original Tab Styling Architecture: Syncs layout, fonts, and active design icons perfectly
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
