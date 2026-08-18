import streamlit as st
import pandas as pd
import base64
import os
import io

# ------------------------------------------------------------------------------------------------
# COMPREHENSIVE REPOSITORY REGIONAL FILE MAPPING (ALL 23 EXPANDED TERRITORIES)
# ------------------------------------------------------------------------------------------------
EXPLICIT_METHODOLOGIES = [
    "methodology_us.txt", "methodology_fr.txt", "methodology_uk.txt",
    "methodology_it.txt", "methodology_de.txt", "methodology_sp.txt",
    "methodology_br.txt", "methodology_mx.txt", "methodology_can.txt",
    "methodology_in.txt", "methodology_jp.txt", "methodology_sk.txt",
    "methodology_den.txt", "methodology_swe.txt", "methodology_nor.txt",
    "methodology_fin.txt", "methodology_sv.txt", "methodology_sle.txt",
    "methodology_cro.txt", "methodology_bg.txt", "methodology_ro.txt",
    "methodology_mol.txt", "methodology_cr.txt"
]

EXPLICIT_SOURCES = [
    "sources_us.txt", "sources_fr.txt", "sources_uk.txt",
    "sources_it.txt", "sources_de.txt", "sources_sp.txt",
    "sources_br.txt", "sources_orig_mx.txt", "sources_can.txt",
    "sources_in.txt", "sources_jp.txt", "sources_kr.txt",
    "sources_den.txt", "sources_swe.txt", "sources_nor.txt",
    "sources_fin.txt", "sources_sv.txt", "sources_sle.txt",
    "sources_cro.txt", "sources_bg.txt", "sources_ro.txt",
    "sources_mol.txt", "sources_cr.txt"
]

# ------------------------------------------------------------------------------------------------
# INITIAL MEMORY BOOTSTRAPPER (READS ONCE TO RAM CACHE PERMANENTLY)
# ------------------------------------------------------------------------------------------------
if "text_memory_cache" not in st.session_state:
    st.session_state.text_memory_cache = {}
    all_target_files = EXPLICIT_METHODOLOGIES + EXPLICIT_SOURCES
    for filename in all_target_files:
        content = ""
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    content = str(f.read().strip())
            except Exception:
                content = ""
        st.session_state.text_memory_cache[filename] = content

def load_text_asset(filename, default_text=""):
    """Safely extracts decoupled plaintext methodology and sources data from RAM cache arrays."""
    if "text_memory_cache" in st.session_state:
        return st.session_state.text_memory_cache.get(filename, default_text)
    return default_text

st.set_page_config(page_title="ESHAP CSAI Dashboard", layout="wide")
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

CA_BASE = [
    ["YOUTUBE", 220.0, 32.0, 188.0, 142.0, 112.0, 74.0],
    ["NETFLIX", 185.0, 28.0, 157.0, 108.0, 78.0, 38.0],
    ["TIKTOK", 124.0, 2.5, 121.5, 98.0, 82.0, 62.0],
    ["CBC", 98.0, 54.0, 44.0, 28.0, 16.0, 7.0],
    ["BELL MEDIA", 88.0, 46.0, 42.0, 24.0, 14.0, 5.5],
    ["ROGERS", 74.0, 38.0, 36.0, 20.0, 11.5, 4.0],
    ["INSTAGRAM", 68.0, 6.0, 62.0, 51.0, 42.0, 24.0],
    ["AMAZON", 62.0, 16.0, 46.0, 32.0, 18.0, 8.0],
    ["WBD (MAX)", 54.0, 22.0, 32.0, 20.0, 12.0, 5.0],
    ["FACEBOOK", 42.0, 19.5, 22.5, 11.0, 4.0, 0.8]
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

IN_BASE = [
    ["YOUTUBE", 850.0, 85.0, 765.0, 620.0, 510.0, 390.0],
    ["JIO CINEMA", 410.0, 115.0, 295.0, 210.0, 145.0, 85.0],
    ["DISNEY+ HOTSTAR", 380.0, 95.0, 285.0, 195.0, 130.0, 74.0],
    ["ZEE ENTERTAINMENT", 290.0, 140.0, 150.0, 98.0, 62.0, 32.0],
    ["SONY LIV", 210.0, 98.0, 112.0, 74.0, 45.0, 21.0],
    ["NETFLIX", 185.0, 22.0, 163.0, 124.0, 88.0, 48.0],
    ["AMAZON PRIME", 160.0, 25.0, 135.0, 102.0, 70.0, 35.0],
    ["INSTAGRAM", 540.0, 20.0, 520.0, 460.0, 395.0, 240.0],
    ["OTHER LOCAL", 310.0, 135.0, 175.0, 110.0, 65.0, 24.0],
    ["FACEBOOK", 220.0, 110.0, 110.0, 62.0, 22.0, 4.5]
]
JP_BASE = [
    ["NHK", 610.0, 495.0, 115.0, 74.0, 42.0, 18.0],
    ["NIPPON TV", 420.0, 290.0, 130.0, 88.0, 54.0, 26.0],
    ["FUJI TV", 380.0, 255.0, 125.0, 82.0, 48.0, 22.0],
    ["TBS", 365.0, 248.0, 117.0, 76.0, 44.0, 19.5],
    ["TV ASAHI", 340.0, 238.0, 102.0, 64.0, 36.0, 14.0],
    ["YOUTUBE", 580.0, 112.0, 468.0, 340.0, 268.0, 154.0],
    ["LINE VIEW", 240.0, 65.0, 175.0, 134.0, 102.0, 58.0],
    ["NETFLIX", 195.0, 34.0, 161.0, 118.0, 74.0, 36.0],
    ["AMAZON PRIME", 185.0, 42.0, 143.0, 104.0, 62.0, 28.0],
    ["X (TWITTER LOGS)", 210.0, 22.0, 188.0, 154.0, 122.0, 74.0],
    ["OTHER LOCAL", 190.0, 115.0, 75.0, 42.0, 20.0, 6.5],
    ["TIKTOK", 165.0, 5.5, 159.5, 128.0, 104.0, 78.0],
    ["INSTAGRAM", 150.0, 12.0, 138.0, 114.0, 92.0, 48.0]
]

SK_BASE = [
    ["KBS", 290.0, 232.0, 58.0, 34.0, 18.0, 7.5],
    ["MBC", 210.0, 154.0, 56.0, 36.0, 20.0, 8.8],
    ["SBS", 205.0, 148.0, 57.0, 38.0, 21.5, 9.2],
    ["YOUTUBE", 390.0, 64.0, 326.0, 245.0, 198.0, 122.0],
    ["NAVER TV", 165.0, 48.0, 117.0, 88.0, 64.0, 32.0],
    ["KAKAO TOONS/VIDEO", 140.0, 32.0, 108.0, 84.0, 66.0, 38.0],
    ["NETFLIX", 135.0, 18.0, 117.0, 88.0, 58.0, 26.0],
    ["TIKTOK", 98.0, 2.2, 95.8, 76.0, 64.0, 49.5],
    ["INSTAGRAM", 88.0, 6.5, 81.5, 70.0, 58.0, 31.0],
    ["OTHER LOCAL", 95.0, 54.0, 41.0, 23.0, 11.0, 3.5]
]
DEN_BASE = [
    ["DR (DANMARKS RADIO)", 48.0, 38.0, 10.0, 7.2, 4.4, 1.8],
    ["TV2 DENMARK", 44.0, 32.0, 12.0, 8.5, 5.2, 2.1],
    ["YOUTUBE", 39.5, 6.2, 33.3, 24.1, 18.8, 11.4],
    ["NETFLIX", 28.0, 4.5, 23.5, 17.2, 11.4, 5.8],
    ["TIKTOK", 22.0, 0.4, 21.6, 17.0, 14.2, 10.5],
    ["VIAPLAY", 16.5, 8.2, 8.3, 5.8, 3.6, 1.4],
    ["INSTAGRAM", 15.0, 1.1, 13.9, 12.1, 9.8, 5.4],
    ["AMAZON PRIME", 11.5, 2.4, 9.1, 7.2, 4.5, 1.8],
    ["DISNEY+", 10.5, 1.8, 8.7, 6.5, 4.1, 1.6],
    ["FACEBOOK", 9.5, 5.2, 4.3, 2.1, 0.6, 0.1]
]

SWE_BASE = [
    ["SVT (SVERIGES TELEVISION)", 82.0, 65.0, 17.0, 11.8, 7.1, 2.9],
    ["TV4 NETWORK", 74.0, 52.0, 22.0, 15.4, 9.5, 3.8],
    ["YOUTUBE", 69.0, 11.5, 57.5, 41.2, 32.0, 19.5],
    ["NETFLIX", 49.0, 8.0, 41.0, 30.1, 19.8, 10.1],
    ["TIKTOK", 39.5, 0.8, 38.7, 30.5, 25.4, 18.8],
    ["VIAPLAY", 31.0, 15.0, 16.0, 11.2, 7.0, 2.7],
    ["INSTAGRAM", 27.5, 2.2, 25.3, 22.0, 17.8, 9.8],
    ["DISNEY+", 19.5, 3.2, 16.3, 12.1, 7.6, 3.1],
    ["AMAZON PRIME", 18.0, 4.0, 14.0, 11.1, 6.8, 2.6],
    ["FACEBOOK", 16.5, 9.2, 7.3, 3.6, 1.1, 0.1]
]
NOR_BASE = [
    ["NRK", 44.0, 35.0, 9.0, 6.2, 3.7, 1.5],
    ["TV2 NORWAY", 36.0, 25.0, 11.0, 7.6, 4.6, 1.8],
    ["YOUTUBE", 34.5, 5.8, 28.7, 20.6, 16.0, 9.7],
    ["NETFLIX", 24.5, 4.1, 20.4, 15.0, 9.9, 5.0],
    ["TIKTOK", 19.8, 0.4, 19.4, 15.3, 12.7, 9.4],
    ["VIAPLAY", 15.0, 7.4, 7.6, 5.3, 3.3, 1.3],
    ["INSTAGRAM", 13.8, 1.1, 12.7, 11.0, 8.9, 4.9],
    ["DISNEY+", 10.0, 1.6, 8.4, 6.2, 3.9, 1.6],
    ["AMAZON PRIME", 9.2, 2.0, 7.2, 5.7, 3.5, 1.4],
    ["FACEBOOK", 8.4, 4.7, 3.7, 1.8, 0.5, 0.1]
]

FIN_BASE = [
    ["YLE", 46.0, 37.5, 8.5, 5.8, 3.4, 1.3],
    ["MTV3 FINLAND", 32.5, 23.5, 9.0, 6.2, 3.7, 1.4],
    ["YOUTUBE", 31.0, 5.2, 25.8, 18.5, 14.4, 8.7],
    ["NETFLIX", 21.0, 3.5, 17.5, 12.8, 8.4, 4.2],
    ["TIKTOK", 17.5, 0.3, 17.2, 13.5, 11.2, 8.3],
    ["SANOMA MEDIA", 16.0, 9.5, 6.5, 4.4, 2.5, 0.9],
    ["INSTAGRAM", 12.2, 0.9, 11.3, 9.8, 7.9, 4.3],
    ["DISNEY+", 9.0, 1.4, 7.6, 5.6, 3.5, 1.4],
    ["AMAZON PRIME", 8.0, 1.7, 6.3, 5.0, 3.1, 1.2],
    ["FACEBOOK", 7.8, 4.4, 3.4, 1.6, 0.4, 0.05]
]
SV_BASE = [
    ["RTVS", 38.0, 30.5, 7.5, 5.2, 3.1, 1.2],
    ["MARKIZA GROUP", 34.0, 23.0, 11.0, 7.6, 4.6, 1.8],
    ["JOJ GROUP", 29.5, 20.5, 9.0, 6.1, 3.6, 1.4],
    ["YOUTUBE", 32.0, 5.4, 26.6, 19.1, 14.8, 9.0],
    ["NETFLIX", 18.5, 2.8, 15.7, 11.5, 7.5, 3.7],
    ["TIKTOK", 16.0, 0.3, 15.7, 12.4, 10.3, 7.6],
    ["INSTAGRAM", 13.5, 1.0, 12.5, 10.8, 8.8, 4.8],
    ["OTHER REGIONAL", 14.0, 8.2, 5.8, 3.8, 2.1, 0.7],
    ["WBD (MAX)", 8.5, 1.4, 7.1, 5.2, 3.2, 1.3],
    ["FACEBOOK", 9.0, 5.1, 3.9, 1.8, 0.5, 0.05]
]

SLE_BASE = [
    ["RTVSLO", 16.5, 13.2, 3.3, 2.3, 1.3, 0.5],
    ["PRO PLUS (POP TV)", 15.0, 10.2, 4.8, 3.3, 2.0, 0.8],
    ["YOUTUBE", 13.2, 2.2, 11.0, 7.9, 6.1, 3.7],
    ["NETFLIX", 8.2, 1.2, 7.0, 5.1, 3.3, 1.6],
    ["TIKTOK", 7.4, 0.1, 7.3, 5.7, 4.8, 3.5],
    ["INSTAGRAM", 6.2, 0.5, 5.7, 4.9, 4.0, 2.2],
    ["OTHER LOCAL", 5.5, 3.2, 2.3, 1.5, 0.8, 0.2],
    ["WBD (MAX)", 3.8, 0.6, 3.2, 2.3, 1.4, 0.6],
    ["FACEBOOK", 3.6, 2.0, 1.6, 0.7, 0.2, 0.02]
]
CRO_BASE = [
    ["HRT", 31.0, 25.2, 5.8, 4.0, 2.4, 0.9],
    ["RTL CROATIA", 24.5, 16.4, 8.1, 5.6, 3.4, 1.3],
    ["NOVA TV", 26.0, 17.8, 8.2, 5.7, 3.4, 1.4],
    ["YOUTUBE", 25.0, 4.2, 20.8, 14.9, 11.6, 7.0],
    ["NETFLIX", 14.5, 2.2, 12.3, 9.0, 5.9, 2.9],
    ["TIKTOK", 12.8, 0.2, 12.6, 9.9, 8.2, 6.1],
    ["INSTAGRAM", 10.5, 0.8, 9.7, 8.4, 6.8, 3.7],
    ["OTHER LOCAL", 11.0, 6.4, 4.6, 3.0, 1.6, 0.5],
    ["WBD (MAX)", 6.8, 1.1, 5.7, 4.1, 2.5, 1.0],
    ["FACEBOOK", 7.2, 4.1, 3.1, 1.4, 0.4, 0.04]
]

BG_BASE = [
    ["BNT", 54.0, 44.5, 9.5, 6.5, 3.8, 1.5],
    ["BTV MEDIA GROUP", 49.0, 33.5, 15.5, 10.7, 6.4, 2.5],
    ["NOVA BROADCASTING", 46.5, 31.2, 15.3, 10.5, 6.3, 2.4],
    ["YOUTUBE", 42.0, 7.1, 34.9, 25.1, 19.5, 11.8],
    ["NETFLIX", 22.0, 3.3, 18.7, 13.7, 8.9, 4.4],
    ["TIKTOK", 19.5, 0.3, 19.2, 15.1, 12.5, 9.2],
    ["INSTAGRAM", 16.5, 1.2, 15.3, 13.2, 10.7, 5.9],
    ["OTHER LOCAL", 18.0, 10.5, 7.5, 4.9, 2.6, 0.8],
    ["WBD (MAX)", 10.5, 1.7, 8.8, 6.4, 3.9, 1.6],
    ["FACEBOOK", 11.4, 6.5, 4.9, 2.2, 0.6, 0.06]
]
RO_BASE = [
    ["TVR", 148.0, 122.0, 26.0, 17.8, 10.5, 4.2],
    ["PRO TV", 134.0, 91.0, 43.0, 29.8, 17.8, 7.1],
    ["ANTENA GROUP", 121.0, 82.5, 38.5, 26.5, 15.9, 6.4],
    ["YOUTUBE", 114.0, 19.4, 94.6, 68.1, 52.9, 32.1],
    ["NETFLIX", 62.0, 9.2, 52.8, 38.6, 25.2, 12.4],
    ["TIKTOK", 54.0, 0.9, 53.1, 41.8, 34.6, 25.5],
    ["INSTAGRAM", 45.0, 3.4, 41.6, 36.0, 29.2, 16.0],
    ["OTHER LOCAL", 49.0, 28.5, 20.5, 13.5, 7.2, 2.2],
    ["WBD (MAX)", 28.5, 4.6, 23.9, 17.4, 10.7, 4.4],
    ["FACEBOOK", 31.0, 17.8, 13.2, 5.9, 1.7, 0.16]
]

MOL_BASE = [
    ["TRM (MOLDOVA 1)", 21.0, 17.4, 3.6, 2.5, 1.4, 0.5],
    ["PRIME REGIONAL", 17.5, 12.0, 5.5, 3.8, 2.3, 0.9],
    ["YOUTUBE", 16.2, 2.7, 13.5, 9.7, 7.5, 4.5],
    ["NETFLIX", 7.8, 1.1, 6.7, 4.9, 3.2, 1.6],
    ["TIKTOK", 7.2, 0.1, 7.1, 5.6, 4.6, 3.4],
    ["INSTAGRAM", 5.8, 0.4, 5.4, 4.6, 3.7, 2.0],
    ["OTHER RE-BROADCAST", 8.2, 4.9, 3.3, 2.1, 1.1, 0.3],
    ["WBD (MAX)", 3.2, 0.5, 2.7, 2.0, 1.2, 0.5],
    ["FACEBOOK", 4.1, 2.3, 1.8, 0.8, 0.2, 0.02]
]
CR_BASE = [
    ["CESKA TELEVIZE", 88.0, 72.5, 15.5, 10.6, 6.2, 2.5],
    ["TV NOVA", 76.0, 51.5, 24.5, 17.0, 10.2, 4.1],
    ["PRIMA GROUP", 69.0, 47.0, 22.0, 15.2, 9.1, 3.6],
    ["YOUTUBE", 66.0, 11.2, 54.8, 39.4, 30.6, 18.6],
    ["NETFLIX", 38.0, 5.6, 32.4, 23.7, 15.5, 7.6],
    ["TIKTOK", 32.5, 0.5, 32.0, 25.1, 20.8, 15.3],
    ["INSTAGRAM", 27.0, 2.0, 25.0, 21.6, 17.5, 9.6],
    ["OTHER LOCAL", 29.0, 16.8, 12.2, 8.0, 4.2, 1.3],
    ["WBD (MAX)", 17.5, 2.8, 14.7, 10.7, 6.6, 2.7],
    ["FACEBOOK", 18.5, 10.6, 7.9, 3.5, 1.0, 0.1]
]

# ------------------------------------------------------------------------------------------------
# REPOSITORY GRAPHICS VECTORIZATION (BASE64 SHIELD GUARDS)
# ------------------------------------------------------------------------------------------------
bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    try:
        with open("planet_bullet.png", "rb") as b_f:
            bullet_base64 = base64.b64encode(b_f.read()).decode()
    except Exception:
        pass

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
    try:
        with open("eshap_map.png", "rb") as img_f:
            logo_base64 = base64.b64encode(img_f.read()).decode()
    except Exception:
        pass

if logo_base64:
    st.sidebar.html("""
        <style>
        div.sidebar-logo-container { width: 100% !important; margin: 0 0 0.5rem 0 !important; padding: 0 !important; text-align: center !important; }
        div.sidebar-logo-container img { max-width: 100% !important; height: auto !important; }
        </style>
        <div class="sidebar-logo-container"><a href="https://substack.com" target="_blank"><img src="data:image/png;base64,""" + logo_base64 + """"></a></div>
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
    
    button[data-testid="stBaseButton-secondary"] {
        color: #111111 !important;
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
        font-weight: bold !important;
    }
    button[data-testid="stBaseButton-secondary"] p {
        color: #111111 !important;
        font-weight: bold !important;
    }
    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #eeeeee !important;
        border-color: #999999 !important;
    }
    </style>
    """)

# Permanent Header Positioning Flush Top
st.header("ESHAP Cross Screen Attention Index (ECSAI)")

st.markdown(
    "<p class='eshap-subhead-text' style='font-size: 0.9rem; font-weight: bold; margin-top: -1rem; margin-bottom: 0.5rem; font-style: normal;'>"
    "The Definitive Zero-Sum Scale For Total Attention From Media's Official Cartographer"
    "</p>", 
    unsafe_allow_html=True
)

st.markdown("For full analysis: **[Media War & Peace](https://substack.com)**")
st.html("<style>div[data-testid='stSidebarNav'] + div, div[data-testid='stRadio'] > div { gap: 0.25rem !important; padding: 0 !important; } div[data-testid='stRadio'] label p { font-size: 0.88rem !important; margin: 0 !important; }</style>")
def handle_market_switch_callback():
    st.session_state.reset_id = st.session_state.get('reset_id', 0) + 1

market_choice = st.sidebar.radio(
    "Territory", 
    [
        "Global Overview", "United States", "Brazil", "Mexico", "Germany", 
        "United Kingdom", "France", "Italy", "Spain", "Canada", "India", 
        "Japan", "South Korea", "Denmark", "Sweden", "Norway", "Finland", 
        "Slovakia", "Slovenia", "Croatia", "Bulgaria", "Romania", "Moldova", 
        "Czech Republic"
    ], 
    key="market_choice_sync",
    on_change=handle_market_switch_callback
)

cols = ["Platform/Publisher", "P13+", "55+ GenX+", "13-54 Majority", "13-44 NextGen", "13-34 Youth", "13-24 GenA/Z"]

if market_choice == "Global Overview": df_matrix = None
elif market_choice == "United States": df_matrix = pd.DataFrame(US_BASE, columns=cols)
elif market_choice == "France": df_matrix = pd.DataFrame(FR_BASE, columns=cols)
elif market_choice == "United Kingdom": df_matrix = pd.DataFrame(UK_BASE, columns=cols)
elif market_choice == "Italy": df_matrix = pd.DataFrame(IT_BASE, columns=cols)
elif market_choice == "Germany": df_matrix = pd.DataFrame(DE_BASE, columns=cols)
elif market_choice == "Spain": df_matrix = pd.DataFrame(ES_BASE, columns=cols)
elif market_choice == "Brazil": df_matrix = pd.DataFrame(BR_BASE, columns=cols)
elif market_choice == "Mexico": df_matrix = pd.DataFrame(MX_BASE, columns=cols)
elif market_choice == "Canada": df_matrix = pd.DataFrame(CA_BASE, columns=cols)
elif market_choice == "India": df_matrix = pd.DataFrame(IN_BASE, columns=cols)
elif market_choice == "Japan": df_matrix = pd.DataFrame(JP_BASE, columns=cols)
elif market_choice == "South Korea": df_matrix = pd.DataFrame(SK_BASE, columns=cols)
elif market_choice == "Denmark": df_matrix = pd.DataFrame(DEN_BASE, columns=cols)
elif market_choice == "Sweden": df_matrix = pd.DataFrame(SWE_BASE, columns=cols)
elif market_choice == "Norway": df_matrix = pd.DataFrame(NOR_BASE, columns=cols)
elif market_choice == "Finland": df_matrix = pd.DataFrame(FIN_BASE, columns=cols)
elif market_choice == "Slovakia": df_matrix = pd.DataFrame(SV_BASE, columns=cols)
elif market_choice == "Slovenia": df_matrix = pd.DataFrame(SLE_BASE, columns=cols)
elif market_choice == "Croatia": df_matrix = pd.DataFrame(CRO_BASE, columns=cols)
elif market_choice == "Bulgaria": df_matrix = pd.DataFrame(BG_BASE, columns=cols)
elif market_choice == "Romania": df_matrix = pd.DataFrame(RO_BASE, columns=cols)
elif market_choice == "Moldova": df_matrix = pd.DataFrame(MOL_BASE, columns=cols)
else: df_matrix = pd.DataFrame(CR_BASE, columns=cols)
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
        "MEDIASET ESPANA": "MEDIASET ES", "MFE (MEDIASET)": "MFE", "GROUPO RECORD": "RECORD"
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
    user_shifts = {}
if df_matrix is not None:
    active_shifts = {k: float(v) for k, v in user_shifts.items() if v != 0.0}
    if active_shifts:
        for entity, shift_val in active_shifts.items():
            idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
            if len(idx) > 0:
                p13_orig = float(df_static_base.loc[idx, "P13+"].iloc[0])
                adj_p13 = max(0.0, p13_orig + shift_val)
                ratio = adj_p13 / p13_orig if p13_orig > 0 else 1.0
                df_matrix.loc[idx, "P13+"] = adj_p13
                df_matrix.loc[idx, "13-54 Majority"] = max(0.0, adj_p13 - float(df_static_base.loc[idx, "55+ GenX+"].iloc[0]))
                for c in ["13-44 NextGen", "13-34 Youth", "13-24 GenA/Z"]:
                    df_matrix.loc[idx, c] = float(df_static_base.loc[idx, c].iloc[0]) * ratio

    total_shifted_hours = sum(active_shifts.values())
    if abs(total_shifted_hours) > 0.01:
        non_shifted_mask = ~df_matrix["Platform/Publisher"].isin(active_shifts.keys())
        total_non_shifted_pool = float(df_static_base[non_shifted_mask]["P13+"].sum())
        if total_non_shifted_pool > 0.0:
            for entity in df_static_base[non_shifted_mask]["Platform/Publisher"].unique():
                idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
                if len(idx) > 0:
                    p13_orig_val = float(df_static_base.loc[idx, "P13+"].iloc[0])
                    ratio = max(0.0, p13_orig_val + (-total_shifted_hours * (p13_orig_val / total_non_shifted_pool))) / p13_orig_val if p13_orig_val > 0.0 else 1.0
                    df_matrix.loc[idx, "P13+"] = p13_orig_val * ratio
                    df_matrix.loc[idx, "13-54 Majority"] = max(0.0, (p13_orig_val * ratio) - float(df_static_base.loc[idx, "55+ GenX+"].iloc[0]))
                    for c in ["13-44 NextGen", "13-34 Youth", "13-24 GenA/Z"]:
                        df_matrix.loc[idx, c] = float(df_static_base.loc[idx, c].iloc[0]) * ratio

    df_matrix[cols[1:]] = df_matrix[cols[1:]].round(1)
flag_icon = {
    "Global Overview": "🌐", "United States": "🇺🇸", "Brazil": "🇧🇷", 
    "Mexico": "🇲🇽", "Germany": "🇩🇪", "United Kingdom": "🇬🇧", 
    "France": "🇫🇷", "Italy": "🇮🇹", "Spain": "🇪🇸", "Canada": "🇨🇦", 
    "India": "🇮🇳", "Japan": "🇯🇵", "South Korea": "🇰🇷", "Denmark": "🇩🇰", 
    "Sweden": "🇸🇪", "Norway": "🇳🇴", "Finland": "🇫🇮", "Slovakia": "🇸🇰", 
    "Slovenia": "🇸🇮", "Croatia": "🇭🇷", "Bulgaria": "🇧🇬", "Romania": "🇷🇴", 
    "Moldova": "🇲🇩", "Czech Republic": "🇨🇿"
}.get(market_choice, "🇺🇸")

# ------------------------------------------------------------------------------------------------
# COMPONENT ROUTING MAPS & VARIABLE ENFORCEMENT
# ------------------------------------------------------------------------------------------------
flag_icon = {
    "Global Overview": "🌐", "United States": "🇺🇸", "Germany": "🇩🇪", 
    "United Kingdom": "🇬🇧", "France": "🇫🇷", "Italy": "🇮🇹", 
    "Spain": "🇪🇸", "Brazil": "🇧🇷", "Mexico": "🇲🇽"
}.get(market_choice, "🇺🇸")

# Flat Single-Line Initializer: Declared globally at indent level 0 to un-nest tabs
tab_labels = ["CSAI Interactive Index Matrix", "Why ECSAI?", "ECSAI FAQs", "Index Architecture & Methodology"]
tab1, tab2, tab3, tab4 = st.tabs(tab_labels)
# ================================================================================================
# TAB 1: THE ACTIVE MATRIX / CANVAS RENDERING SECTION
# ================================================================================================
with tab1:
    if market_choice == "Global Overview":
        st.subheader("THE GLOBAL INDEX")
        st.markdown(
            "What happens when we measure Media consumption not BY device, but ACROSS devices? "
            "Turns out, a lot. We embarked on this mission to measure it all, side-by-side. "
            "Full analysis: [Media War & Peace](https://substack.com)"
        )
        
        if os.path.exists("global_index_13+.png"):
            st.image("global_index_13+.png", caption="GLOBAL ATTENTION INDEX: P13+", use_container_width=True)
        else:
            st.warning("⚠️ `global_index_13+.png` asset missing from repository folder.")
            
        st.markdown("This reveals the share of consumer attention spread across all eight regions in The Index.")
        
        if os.path.exists("global_index_13-54.png"):
            st.image("global_index_13-54.png", caption="GLOBAL ATTENTION INDEX: P13-54", use_container_width=True)
        else:
            st.warning("⚠️ `global_index_13-54.png` asset missing from repository folder.")
        st.markdown("##### **Crucial datapoint: 82% of the world population — 73% of the people in these eight regions — are now under 54.**")
        st.markdown("Legacy TV relies almost entirely on the shrinking minority of senior citizens watching the same stuff. When you remove that demographic, combined legacy outlets are handily surpassed by YouTube, Netflix, and TikTok.")
        st.markdown("##### **YouTube garners more attention among people 13-54 than Disney, Disco Bros, Paramount, NBCU, and FOX — combined.**")
        st.markdown("The ECSAI is the first zero-sum, wholly deduplicated map of human attention in history.")
        
        if os.path.exists("us_index_13-54.png"):
            st.image("us_index_13-54.png", caption="US ATTENTION DATA PROFILE", use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if os.path.exists("us_index_13-34.png"): st.image("us_index_13-34.png", caption="US: P13-34", use_container_width=True)
        with c2:
            if os.path.exists("us_index_13-24.png"): st.image("us_index_13-24.png", caption="US: P13-24", use_container_width=True)
            
        st.markdown("Traditional currencies track the device canvas; they do not track the human. They count a television playing to an empty room as a hit, while treating active mobile engagement as noise. Each quarter, we will update the ECSAI on a rolling six months basis.")
    else:
        st.subheader(f"Cross-Screen Attention Tracker: {flag_icon} {market_choice}")
        st.markdown("#### Interactive Visual Share Map")
        st.html("<style>div[data-testid='stRadio'] > div { gap: 1.5rem !important; } div[data-testid='stRadio'] label p { font-size: 0.95rem !important; white-space: nowrap !important; }</style>")
        demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
        selected_demo = st.radio("Select Demographic Cohort to Isolate in Bar Chart:", options=demo_columns, horizontal=True)
        
        chart_df = df_matrix.copy()
        chart_df["Platform/Publisher"] = chart_df["Platform/Publisher"].replace({"GROUPO RECORD": "RECORD"})
        chart_df_fixed = chart_df.set_index("Platform/Publisher")
        st.bar_chart(chart_df_fixed[[selected_demo]], horizontal=True, height=380, use_container_width=True, color="#FF0000")
            
        st.write("---")
        st.markdown("#### Cross Screen Attention Ledger")
        st.dataframe(df_matrix, use_container_width=True, hide_index=True)
        
        if market_choice == "Brazil":
            st.markdown("<p style='font-size: 0.82rem; font-style: italic; color: #444444;'>Corporate structures incorporate streaming telemetry.</p>", unsafe_allow_html=True)
        elif market_choice == "Mexico":
            st.markdown("<p style='font-size: 0.82rem; font-style: italic; color: #444444;'>TelevisaUnivision incorporates ViX telemetry.</p>", unsafe_allow_html=True)
            
        # FIXED: Broken down into independent short variables to completely protect text window width restrictions
        csv_payload = df_matrix.to_csv(index=False).encode('utf-8')
        target_filename = f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv"
        st.download_button(label="Export Current Ledger to CSV", data=csv_payload, file_name=target_filename, mime="text/csv", use_container_width=True)
# ================================================================================================
# TAB 2: WHY THE ECSAI CRITERIA BLOCK (DECLARED CLEANLY AT INDENT 0)
# ================================================================================================
with tab2:
    st.markdown("<div style='text-align: center; line-height: 0.95;'><h2 style='margin: 0;'>WHY THE ECSAI?</h2><h2 style='color: #FF0000; margin: 0;'>BECAUSE HUMAN ATTENTION IS FINITE.</h2></div>", unsafe_allow_html=True)
    st.markdown("Our multi-billion-dollar industry is navigating by a map that does not match the earth. Traditional currencies track the device canvas; they do not track the human. They count a television playing to an empty room as an absolute hit, while treating a high-intensity mobile session that requires active thumb-and-eye engagement to exist as digital noise.")
    st.markdown("##### **TO BE CLEAR: THIS IS NOT A MEDIA BUYING MECHANISM. IT'S A STRATEGIC AND FISCAL PLANNING COMPASS.**")
    st.markdown("Since COVID and the arrival of TikTok, the phone has replaced the television as the center of video gravity. 60% of the world's video attention is now on mobile phones. If you are a media company investing 100% of your budget on TV sets, you are mapping a course to irrelevancy.")
    
    if os.path.exists("eshap_us_devices.png"): 
        st.image("eshap_us_devices.png", caption="Video Consumption Share By Device Ecosystem", use_container_width=True)
        
    st.markdown("ESCAI enforces the absolute laws of human physics. Human time is a non-elastic, zero-sum commodity—a closed market sponge. Every single hour gained by an algorithm is an hour permanently destroyed for a broadcast tower. The model uses duplication discounts derived from consumer diaries to calculate the mathematical overlap when two devices are running in the same room. We didn't invent new numbers, and we didn't hide our math inside a proprietary black box. Every data point sits out in the open public domain.")
# ================================================================================================
# TAB 3: FREQUENTLY ASKED QUESTIONS (FAQs) (DECLARED CLEANLY AT INDENT 0)
# ================================================================================================
with tab3:
    st.subheader("ECSAI Frequently Asked Questions (FAQs)")
    st.markdown("#### Q: HOW DID WE CHOOSE THE VARIOUS COMBINATION OF SOURCES FOR THE INDEX ACROSS THE REGIONS?")
    st.markdown("Data sources for each country were selected based on strict criteria: sovereign regulatory authority, parent corporate transparency, and audited single-screen telemetry. We ingest data from official state census registries for macro population controls, alongside published annual disclosures from public service broadcasters and tech titans.")
    st.markdown("#### Q: HOW DO YOU BLEND THE VARIOUS INPUTS INTO ONE SMOOTH INDEX?")
    st.markdown("Our model runs a three-step mathematical normalization loop that forces data into a strict, logic-enforced daily time budget. The index takes the total population headcount, filters for the P13+ universe, and establishes a Total Available Awake Hours Budget per month. This represents our absolute volume ceiling.")
    
    if os.path.exists("ecsai_flow.png"): 
        st.image("ecsai_flow.png", caption="ESHAP Cross-Screen Attention Index Production Workflow Map", use_container_width=True)
        
    st.markdown("#### Q: DOESN'T BLENDING SURVEY RECALL WITH TELEMETRY CORRUPT THE DATA?")
    st.markdown("The index operates on a strict Separation of Powers. We use a Sovereign Boundary Model where hard quantitative ceilings are locked down entirely by currency-grade, hard telemetry logs. Behavioral data from GWI Consumer Diaries is introduced strictly as a coefficient matrix to calculate the mathematical overlap when two devices are running in the same room.")
# ================================================================================================
# TAB 4: BLUEPRINTS & CACHED TEXT LOOKUPS (DECLARED CLEANLY AT INDENT 0)
# ================================================================================================
with tab4:
    sub_method, sub_source = st.tabs(["Methodology Blueprint", "Sourcing Matrix"])
    is_global_view = (market_choice == "Global Overview")
    
    token_dict = {
        "United States": "us", "France": "fr", "United Kingdom": "uk", 
        "Italy": "it", "Germany": "de", "Spain": "sp", "Brazil": "br", "Mexico": "mx"
    }
    f_token = "us" if is_global_view else token_dict.get(market_choice, "us")
    
    with sub_method:
        st.markdown(f"### METHODOLOGY BLUEPRINT ({flag_icon} {market_choice.upper()})")
        if not is_global_view:
            w_dict = {
                "United States": ("64.2%", "35.8%"), "France": ("65.1%", "34.9%"), "United Kingdom": ("63.8%", "36.2%"), 
                "Italy": ("59.8%", "40.2%"), "Germany": ("61.5%", "38.5%"), "Spain": ("62.0%", "38.0%"), 
                "Brazil": ("68.5%", "31.5%"), "Mexico": ("71.0%", "29.0%")
            }
            w1, w2 = w_dict.get(market_choice, ("64.2%", "35.8%"))
            st.markdown(f"**Territorial Demographic Weight:** {w1} is &le; 54 / {w2} is &ge; 55")
        
        f_method = f"methodology_{f_token}.txt"
        methodology_text = load_text_asset(f_method, "Methodology assets loading safely from cache...")
        st.text_area(label="Active Regulatory Methodology Statement Data Logs", value=methodology_text, height=450, disabled=True)
            
    with sub_source:
        st.markdown(f"### DATA SOURCES ({flag_icon} {market_choice.upper()})")
        f_source = f"sources_{f_token}.txt"
        if f_token == "mx": f_source = "sources_orig_mx.txt"
            
        sources_text = load_text_asset(f_source, "Sourcing footprint parameters extracting from cache...")
        st.text_area(label="Verified Enterprise Metric Ingestion Registries", value=sources_text, height=450, disabled=True)
