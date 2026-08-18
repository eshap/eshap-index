import streamlit as st
import pandas as pd
import base64
import os
import io

# Explicit Master File List matching your physical repository assets exactly
EXPLICIT_METHODOLOGIES = [
    "methodology_us.txt", "methodology_fr.txt", "methodology_uk.txt",
    "methodology_it.txt", "methodology_de.txt", "methodology_sp.txt",
    "methodology_br.txt", "methodology_mx.txt", "Canada Methodology.txt",
    "India Methodology.txt", "methodology_jp.txt", "South Korea Methodology.txt",
    "DENMARK Methodology.txt", "SWEDEN Methodology.txt", "NORWAY Methodology.txt",
    "FINLAND Methodology.txt", "SLOVAKIA Methodology.txt", "SLOVENIA Methodology.txt",
    "CROATIA Methodology.txt", "BULGARIA Methodology.txt", "ROMANIA Methodology.txt",
    "MOLDOVA Methodology.txt", "CZECH REPUBLIC Methodology.txt"
]

EXPLICIT_SOURCES = [
    "sources_us.txt", "sources_fr.txt", "sources_uk.txt",
    "sources_it.txt", "sources_de.txt", "sources_sp.txt",
    "sources_br.txt", "sources_orig_mx.txt", "Canada Sources.txt",
    "India Sources.txt", "sources_jp.txt", "South Korea Sources.txt",
    "DENMARK Sources.txt", "SWEDEN Sources.txt", "NORWAY Sources.txt",
    "FINLAND Sources.txt", "SLOVAKIA Sources.txt", "SLOVENIA Sources.txt",
    "CROATIA Sources.txt", "BULGARIA Sources.txt", "ROMANIA Sources.txt",
    "MOLDOVA Sources.txt", "CZECH REPUBLIC Sources.txt"
]

# Memory Cache Bootstrapper: Pre-loads your exact filenames into server RAM once at startup
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
    return st.session_state.text_memory_cache.get(filename, default_text)

st.set_page_config(page_title="ESHAP CSAI Dashboard", layout="wide")

US_BASE = [
    ["YOUTUBE", 2110.0, 490.0, 1620.0, 1134.0, 884.5, 539.5],
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
    ["YOUTUBE", 128.5, 34.2, 94.3, 73.1, 56.4, 38.1],
    ["NETFLIX", 108.2, 28.5, 79.7, 52.4, 38.1, 22.4],
    ["TIKTOK", 92.4, 3.8, 88.6, 68.1, 54.2, 40.5],
    ["CBC", 88.4, 52.1, 36.3, 24.1, 16.5, 10.2],
    ["BELL MEDIA", 82.5, 46.4, 36.1, 23.4, 14.2, 8.5],
    ["ROGERS", 64.2, 38.5, 25.7, 16.2, 10.1, 5.4],
    ["INSTAGRAM", 62.4, 6.1, 56.3, 44.2, 36.1, 22.4],
    ["DISNEY", 54.1, 21.3, 32.8, 21.4, 15.2, 8.4],
    ["WBD (MAX)", 48.2, 22.4, 25.8, 16.1, 10.4, 5.2],
    ["FACEBOOK", 46.5, 24.2, 22.3, 12.1, 4.4, 1.1],
    ["AMAZON", 38.4, 12.1, 26.3, 19.2, 12.4, 5.2]
]
MX_BASE = [
    ["TELEVISAUNIVISION", 1640.0, 685.0, 955.0, 744.9, 558.7, 284.9],
    ["YOUTUBE", 1390.0, 115.0, 1275.0, 905.2, 733.2, 476.6],
    ["TIKTOK", 860.0, 12.0, 848.0, 695.3, 591.0, 461.0],
    ["INSTAGRAM", 695.0, 18.0, 677.0, 602.5, 518.1, 305.7],
    ["NETFLIX", 635.0, 54.0, 581.0, 447.4, 295.3, 156.4],
    ["TV AZTECA", 485.0, 245.0, 240.0, 180.0, 122.4, 52.8],
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
    ["AMAZON", 390.0, 65.0, 325.0, 266.5, 173.2, 77.9],
    ["DISNEY", 325.0, 48.0, 277.0, 213.3, 139.3, 64.0],
    ["WBD (MAX)", 290.0, 82.0, 208.0, 151.8, 95.6, 43.0],
    ["FACEBOOK", 285.0, 135.0, 150.0, 85.5, 32.4, 6.3],
    ["BAND (GRUPO)", 210.0, 122.0, 88.0, 61.6, 38.7, 15.4]
]
IN_BASE = [
    ["YOUTUBE", 1485.4, 110.2, 1375.2, 1142.1, 982.4, 645.2],
    ["JIOSTAR", 1124.5, 412.1, 712.4, 524.2, 382.1, 211.4],
    ["TIKTOK", 642.1, 8.4, 633.7, 512.4, 442.1, 318.5],
    ["INSTAGRAM", 588.2, 12.1, 576.1, 484.2, 392.1, 214.2],
    ["NETFLIX", 412.4, 54.2, 358.2, 264.1, 182.4, 94.2],
    ["ZEE ENTERTAINMENT", 385.2, 184.2, 201.0, 142.1, 94.2, 48.5],
    ["SONY PICTURES NETWORKS", 312.4, 148.5, 163.9, 112.4, 78.5, 38.2],
    ["DOORDARSHAN", 248.5, 142.1, 106.4, 74.2, 48.1, 22.4],
    ["AMAZON", 194.2, 38.2, 156.0, 118.2, 74.2, 31.4],
    ["FACEBOOK", 182.4, 68.2, 114.2, 64.1, 28.2, 5.1],
    ["DISNEY", 142.1, 28.4, 113.7, 82.4, 48.5, 21.2]
]

JP_BASE = [
    ["YOUTUBE", 524.2, 182.4, 341.8, 238.5, 184.2, 112.4],
    ["NHK", 412.5, 264.2, 148.3, 102.4, 74.1, 42.5],
    ["NIPPON TV", 318.4, 184.5, 133.9, 88.5, 58.2, 31.4],
    ["FUJI TV", 284.2, 162.1, 122.1, 74.2, 48.5, 22.4],
    ["TBS", 264.1, 154.2, 109.9, 68.1, 42.4, 18.5],
    ["TV ASAHI", 242.5, 142.1, 100.4, 61.2, 38.1, 14.2],
    ["NETFLIX", 188.2, 42.1, 146.1, 98.4, 64.2, 31.5],
    ["INSTAGRAM", 142.4, 18.2, 124.2, 102.5, 78.4, 42.1],
    ["TIKTOK", 124.5, 5.4, 119.1, 92.4, 74.2, 52.4],
    ["AMAZON", 112.4, 28.2, 84.2, 62.1, 38.4, 15.2],
    ["FACEBOOK", 68.2, 42.1, 26.1, 14.2, 5.1, 0.8]
]
KR_BASE = [
    ["YOUTUBE", 284.5, 74.2, 210.3, 162.4, 124.5, 82.4],
    ["KBS", 194.2, 112.4, 81.8, 54.2, 38.1, 18.5],
    ["MBC", 142.5, 78.4, 64.1, 42.1, 28.4, 12.1],
    ["SBS", 138.4, 74.2, 64.2, 40.5, 26.3, 10.4],
    ["NETFLIX", 112.4, 24.1, 88.3, 62.4, 42.1, 21.4],
    ["CJ ENM", 94.2, 42.1, 52.1, 36.4, 22.1, 10.5],
    ["TIKTOK", 78.5, 3.1, 75.4, 58.2, 48.1, 34.2],
    ["INSTAGRAM", 68.4, 5.4, 63.0, 52.1, 42.4, 22.1],
    ["NAVER", 54.2, 21.2, 33.0, 22.4, 14.2, 6.1],
    ["FACEBOOK", 38.2, 20.4, 17.8, 10.2, 4.1, 0.8]
]

FR_BASE = [
    ["FRANCE TV", 510.0, 385.0, 125.0, 102.5, 82.0, 54.2],
    ["YOUTUBE", 485.0, 95.0, 390.0, 273.0, 212.9, 129.9],
    ["TF1", 440.0, 270.0, 170.0, 136.0, 102.0, 51.8],
    ["NETFLIX", 390.0, 85.0, 305.0, 222.7, 140.3, 71.6],
    ["TIKTOK", 335.0, 12.0, 323.0, 251.9, 206.6, 150.8],
    ["GROUP M6", 265.0, 145.0, 120.0, 93.6, 65.5, 29.5],
    ["INSTAGRAM", 215.0, 20.0, 195.0, 169.7, 137.5, 75.6],
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
    ["INSTAGRAM", 295.0, 28.0, 267.0, 232.3, 188.2, 103.5],
    ["AMAZON", 230.0, 68.0, 162.0, 132.8, 82.3, 34.6],
    ["DISNEY", 195.0, 42.0, 153.0, 116.3, 73.3, 30.3],
    ["WBD", 145.0, 78.0, 67.0, 48.9, 30.8, 12.7],
    ["FACEBOOK", 140.0, 82.0, 58.0, 31.9, 11.8, 2.2]
]

UK_BASE = [
    ["BBC", 640.0, 460.0, 180.0, 122.4, 85.7, 45.4],
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
    ["INSTAGRAM", 215.0, 20.0, 195.0, 169.7, 137.5, 75.6],
    ["MOVISTAR+", 145.0, 82.0, 63.0, 44.1, 26.5, 11.1],
    ["DISNEY", 115.0, 24.0, 91.0, 69.2, 43.6, 18.0],
    ["WBD (MAX)", 105.0, 55.0, 50.0, 36.5, 23.0, 9.6],
    ["AMAZON", 95.0, 28.0, 67.0, 54.9, 34.0, 14.3],
    ["FACEBOOK", 90.0, 55.0, 35.0, 19.3, 7.1, 1.3]
]

DENMARK_BASE = [
    ["DR", 54.2, 32.1, 22.1, 15.4, 10.2, 5.1],
    ["YOUTUBE", 48.5, 11.2, 37.3, 26.1, 20.2, 12.4],
    ["TV2", 42.1, 25.4, 16.7, 11.2, 8.4, 4.1],
    ["NETFLIX", 38.4, 8.5, 29.9, 21.4, 14.2, 7.5],
    ["TIKTOK", 32.1, 1.1, 31.0, 24.2, 20.1, 14.5],
    ["INSTAGRAM", 24.5, 2.4, 22.1, 18.5, 14.2, 8.1],
    ["VIAPLAY", 18.4, 9.2, 9.2, 6.1, 4.2, 2.1],
    ["AMAZON", 14.2, 3.1, 11.1, 8.4, 5.1, 2.1],
    ["DISNEY", 12.1, 2.4, 9.7, 6.5, 4.2, 1.8],
    ["FACEBOOK", 11.5, 6.2, 5.3, 3.1, 1.1, 0.2]
]
SE_BASE = [
    ["SVT", 98.4, 58.2, 40.2, 28.1, 18.4, 9.2],
    ["YOUTUBE", 88.5, 20.4, 68.1, 48.2, 38.1, 24.2],
    ["TV4", 74.2, 44.1, 30.1, 20.4, 14.2, 7.1],
    ["NETFLIX", 68.4, 15.2, 53.2, 38.1, 26.2, 14.1],
    ["TIKTOK", 58.2, 2.1, 56.1, 44.1, 36.4, 26.2],
    ["INSTAGRAM", 44.1, 4.5, 39.6, 32.1, 26.1, 15.2],
    ["VIAPLAY", 32.4, 16.2, 16.2, 11.1, 7.4, 3.5],
    ["AMAZON", 24.5, 5.4, 19.1, 14.2, 9.1, 4.1],
    ["DISNEY", 22.1, 4.2, 17.9, 12.1, 8.2, 3.4],
    ["FACEBOOK", 21.4, 12.1, 9.3, 5.2, 1.8, 0.3]
]

NO_BASE = [
    ["NRK", 48.5, 28.4, 20.1, 14.2, 9.1, 4.5],
    ["YOUTUBE", 44.1, 10.2, 33.9, 24.1, 19.2, 12.1],
    ["TV2 NORWAY", 36.4, 21.2, 15.2, 10.4, 7.1, 3.4],
    ["NETFLIX", 34.2, 7.8, 26.4, 18.5, 13.1, 7.1],
    ["TIKTOK", 28.4, 0.9, 27.5, 21.4, 18.1, 13.2],
    ["INSTAGRAM", 22.1, 2.1, 20.0, 16.2, 13.1, 7.8],
    ["VIAPLAY", 16.2, 8.1, 8.1, 5.4, 3.5, 1.5],
    ["AMAZON", 12.1, 2.8, 9.3, 7.1, 4.5, 1.8],
    ["DISNEY", 11.4, 2.1, 9.3, 6.2, 4.1, 1.5],
    ["FACEBOOK", 10.8, 6.1, 4.7, 2.6, 0.8, 0.1]
]

FI_BASE = [
    ["YLE", 54.2, 32.4, 21.8, 15.2, 10.1, 5.1],
    ["YOUTUBE", 46.1, 10.5, 35.6, 25.1, 19.8, 12.4],
    ["MTV3", 38.4, 23.1, 15.3, 10.4, 7.1, 3.2],
    ["NETFLIX", 34.5, 7.8, 26.7, 18.9, 13.2, 6.8],
    ["TIKTOK", 28.2, 1.0, 27.2, 21.4, 17.9, 13.1],
    ["INSTAGRAM", 22.4, 2.4, 20.0, 16.4, 13.2, 7.5],
    ["SANOMA", 18.5, 11.2, 7.3, 4.8, 3.1, 1.2],
    ["VIAPLAY", 14.2, 7.1, 7.1, 4.8, 3.1, 1.2],
    ["AMAZON", 11.8, 2.5, 9.3, 7.1, 4.5, 1.8],
    ["FACEBOOK", 11.2, 6.4, 4.8, 2.8, 0.9, 0.1]
]
SK_BASE = [
    ["STVR (RTVS)", 52.4, 31.5, 20.9, 14.5, 9.8, 4.8],
    ["MARKÍZA", 46.2, 26.4, 19.8, 13.2, 9.1, 4.2],
    ["YOUTUBE", 42.1, 9.5, 32.6, 23.1, 18.2, 11.4],
    ["JOJ GROUP", 38.4, 22.1, 16.3, 11.2, 7.8, 3.5],
    ["NETFLIX", 28.5, 6.4, 22.1, 15.4, 10.8, 5.4],
    ["TIKTOK", 24.2, 0.8, 23.4, 18.4, 15.2, 11.1],
    ["INSTAGRAM", 18.4, 1.9, 16.5, 13.5, 10.8, 6.2],
    ["AMAZON", 11.2, 2.4, 8.8, 6.5, 4.1, 1.5],
    ["FACEBOOK", 10.5, 6.1, 4.4, 2.5, 0.8, 0.1]
]

SI_BASE = [
    ["RTV SLOVENIJA", 21.4, 12.8, 8.6, 6.0, 4.1, 2.0],
    ["PRO PLUS (POP TV)", 18.5, 10.5, 8.0, 5.4, 3.8, 1.8],
    ["YOUTUBE", 16.2, 3.8, 12.4, 8.8, 7.1, 4.5],
    ["NETFLIX", 12.4, 2.8, 9.6, 6.8, 4.8, 2.4],
    ["TIKTOK", 11.2, 0.4, 10.8, 8.5, 7.1, 5.2],
    ["INSTAGRAM", 8.4, 0.9, 7.5, 6.2, 5.1, 2.8],
    ["PLANET TV", 7.5, 4.2, 3.3, 2.1, 1.4, 0.6],
    ["AMAZON", 4.8, 1.0, 3.8, 2.8, 1.8, 0.6],
    ["FACEBOOK", 4.5, 2.6, 1.9, 1.1, 0.3, 0.0]
]

HR_BASE = [
    ["HRT", 41.2, 24.8, 16.4, 11.4, 7.8, 3.8],
    ["NOVA TV", 36.4, 21.1, 15.3, 10.5, 7.1, 3.2],
    ["YOUTUBE", 32.1, 7.4, 24.7, 17.5, 13.8, 8.8],
    ["RTL CROATIA", 28.5, 16.4, 12.1, 8.4, 5.4, 2.5],
    ["NETFLIX", 22.4, 5.1, 17.3, 12.1, 8.5, 4.2],
    ["TIKTOK", 19.8, 0.6, 19.2, 15.1, 12.8, 9.4],
    ["INSTAGRAM", 14.5, 1.5, 13.0, 10.8, 8.8, 5.1],
    ["AMAZON", 8.4, 1.8, 6.6, 4.8, 3.1, 1.1],
    ["FACEBOOK", 8.1, 4.8, 3.3, 1.9, 0.6, 0.1]
]
bg_BASE = [
    ["BMG (bTV)", 64.2, 38.5, 25.7, 17.8, 12.1, 5.8],
    ["NOVA BROADCASTING", 58.4, 34.8, 23.6, 16.5, 11.2, 5.2],
    ["YOUTUBE", 44.1, 10.2, 33.9, 24.1, 19.1, 12.1],
    ["BNT", 32.5, 21.4, 11.1, 7.8, 5.1, 2.2],
    ["NETFLIX", 24.2, 5.5, 18.7, 13.1, 9.2, 4.5],
    ["TIKTOK", 22.1, 0.7, 21.4, 16.8, 14.2, 10.4],
    ["INSTAGRAM", 16.4, 1.8, 14.6, 12.1, 9.8, 5.4],
    ["AMAZON", 8.8, 1.9, 6.9, 5.1, 3.1, 1.1],
    ["FACEBOOK", 8.5, 5.1, 3.4, 1.9, 0.6, 0.1]
]

RO_BASE = [
    ["PRO TV", 188.4, 112.4, 76.0, 52.4, 36.1, 18.2],
    ["ANTENA GROUP", 164.2, 98.5, 65.7, 45.1, 31.2, 15.4],
    ["YOUTUBE", 134.5, 31.2, 103.3, 73.4, 58.2, 36.5],
    ["TVR", 84.2, 56.1, 28.1, 19.4, 12.5, 5.8],
    ["NETFLIX", 74.2, 16.8, 57.4, 40.2, 28.1, 14.1],
    ["TIKTOK", 68.4, 2.2, 66.2, 52.1, 44.1, 32.4],
    ["INSTAGRAM", 51.2, 5.4, 45.8, 38.1, 31.2, 18.1],
    ["AMAZON", 28.4, 6.1, 22.3, 16.5, 10.1, 3.8],
    ["FACEBOOK", 27.5, 16.4, 11.1, 6.4, 2.1, 0.3]
]
MD_BASE = [
    ["PUBLIC TELEVISION (TRM)", 24.5, 15.2, 9.3, 6.5, 4.2, 1.9],
    ["PRIME TV", 18.4, 11.1, 7.3, 5.1, 3.2, 1.4],
    ["YOUTUBE", 16.2, 3.8, 12.4, 8.8, 7.1, 4.4],
    ["JURNAL TV", 14.2, 8.5, 5.7, 4.1, 2.5, 1.1],
    ["NETFLIX", 9.4, 2.1, 7.3, 5.1, 3.5, 1.7],
    ["TIKTOK", 8.8, 0.3, 8.5, 6.8, 5.8, 4.2],
    ["INSTAGRAM", 6.4, 0.7, 5.7, 4.8, 3.8, 2.1],
    ["AMAZON", 3.2, 0.7, 2.5, 1.8, 1.1, 0.4],
    ["FACEBOOK", 3.1, 1.8, 1.3, 0.8, 0.2, 0.0]
]

CZ_BASE = [
    ["ČESKÁ TELEVIZE", 98.4, 59.1, 39.3, 27.2, 18.5, 9.1],
    ["TV NOVA", 88.5, 51.4, 37.1, 25.4, 17.1, 8.2],
    ["YOUTUBE", 74.2, 16.8, 57.4, 40.5, 32.1, 20.4],
    ["PRIMA GROUP", 71.4, 42.1, 29.3, 20.1, 13.5, 6.4],
    ["NETFLIX", 52.4, 12.1, 40.3, 28.2, 19.5, 9.8],
    ["TIKTOK", 46.1, 1.4, 44.7, 35.1, 29.8, 21.5],
    ["INSTAGRAM", 34.2, 3.8, 30.4, 25.1, 20.4, 11.2],
    ["AMAZON", 18.5, 4.1, 14.4, 10.5, 6.4, 2.4],
    ["FACEBOOK", 18.1, 10.5, 7.6, 4.2, 1.4, 0.2]
]

bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    with open("planet_bullet.png", "rb") as b_f: 
        bullet_base64 = base64.b64encode(b_f.read()).decode()
eshap_logo_base64 = ""
if os.path.exists("eshap_map.png"):
    with open("eshap_map.png", "rb") as f_logo:
        eshap_logo_base64 = base64.b64encode(f_logo.read()).decode()

logo_html = ""
if eshap_logo_base64:
    logo_html = f'<div style="text-align: center; margin-bottom: 1.5rem;"><a href="https://substack.com" target="_blank"><img src="data:image/png;base64,{eshap_logo_base64}" style="width: 140px; height: auto; transition: transform 0.2s;" onmouseover="this.style.transform=\'scale(1.05)\'" onmouseout="this.style.transform=\'scale(1)\'"></a></div>'

custom_bullet_style = ""
if bullet_base64:
    custom_bullet_style = f"""
    div[data-testid="stMarkdownContainer"] ul li::marker,
    div[data-testid="stTab"] button p::before {{
        content: url("data:image/png;base64,{bullet_base64}") !important;
    }}
    """

css_shield = f"""
<style>
div[data-testid="stSidebarUserContent"] {{
    background-color: #4A4A4A !important;
    padding: 1.5rem 1rem !important;
}}
div[data-testid="stSidebarUserContent"] h2,
div[data-testid="stSidebarUserContent"] p,
div[data-testid="stSidebarUserContent"] label p {{
    color: #ffffff !important;
}}
div[data-testid="stSidebarUserContent"] div[data-testid="stMarkdownContainer"] p {{
    font-size: 0.85rem !important;
    line-height: 1.45 !important;
}}
div[data-testid="stSidebarUserContent"] button[data-testid="baseButton-secondary"] {{
    background-color: #ffffff !important;
    border: 1px solid #ffffff !important;
    border-radius: 4px !important;
    width: 100% !important;
}}
div[data-testid="stSidebarUserContent"] button[data-testid="baseButton-secondary"] p {{
    color: #111111 !important;
    font-weight: bold !important;
}}
{custom_bullet_style}
</style>
"""
st.html(css_shield)
st.sidebar.html(logo_html)

# Strip whitespace lookup traps from the visual tracker universally
market_options = [
    "Global Overview", "United States", "Germany", "United Kingdom", "France", 
    "Italy", "Spain", "Brazil", "Mexico", "Canada", "India", "Japan", 
    "South Korea", "Denmark", "Sweden", "Norway", "Finland", "Slovakia", 
    "Slovenia", "Croatia", "Bulgaria", "Romania", "Moldova", "Czech Republic"
]
market_choice = st.sidebar.radio("Select Territory View:", options=market_options)
market_choice = str(market_choice).strip()

df_matrix = None
df_static_base = None
cols = ["Platform/Publisher", "P13+", "55+ GenX+", "13-54 Majority", "13-44 NextGen", "13-34 Youth", "13-24 GenA/Z"]

if market_choice == "United States": df_matrix = pd.DataFrame(US_BASE, columns=cols)
elif market_choice == "Germany": df_matrix = pd.DataFrame(DE_BASE, columns=cols)
elif market_choice == "United Kingdom": df_matrix = pd.DataFrame(UK_BASE, columns=cols)
elif market_choice == "France": df_matrix = pd.DataFrame(FR_BASE, columns=cols)
elif market_choice == "Italy": df_matrix = pd.DataFrame(IT_BASE, columns=cols)
elif market_choice == "Spain": df_matrix = pd.DataFrame(ES_BASE, columns=cols)
elif market_choice == "Brazil": df_matrix = pd.DataFrame(BR_BASE, columns=cols)
elif market_choice == "Mexico": df_matrix = pd.DataFrame(MX_BASE, columns=cols)
elif market_choice == "Canada": df_matrix = pd.DataFrame(CA_BASE, columns=cols)
elif market_choice == "India": df_matrix = pd.DataFrame(IN_BASE, columns=cols)
elif market_choice == "Japan": df_matrix = pd.DataFrame(JP_BASE, columns=cols)
elif market_choice == "South Korea": df_matrix = pd.DataFrame(KR_BASE, columns=cols)
elif market_choice == "Denmark": df_matrix = pd.DataFrame(DENMARK_BASE, columns=cols)
elif market_choice == "Sweden": df_matrix = pd.DataFrame(SE_BASE, columns=cols)
elif market_choice == "Norway": df_matrix = pd.DataFrame(NO_BASE, columns=cols)
elif market_choice == "Finland": df_matrix = pd.DataFrame(FI_BASE, columns=cols)
elif market_choice == "Slovakia": df_matrix = pd.DataFrame(SK_BASE, columns=cols)
elif market_choice == "Slovenia": df_matrix = pd.DataFrame(SI_BASE, columns=cols)
elif market_choice == "Croatia": df_matrix = pd.DataFrame(HR_BASE, columns=cols)
elif market_choice == "Bulgaria": df_matrix = pd.DataFrame(bg_BASE, columns=cols)
elif market_choice == "Romania": df_matrix = pd.DataFrame(RO_BASE, columns=cols)
elif market_choice == "Moldova": df_matrix = pd.DataFrame(MD_BASE, columns=cols)
elif market_choice == "Czech Republic": df_matrix = pd.DataFrame(CZ_BASE, columns=cols)

if df_matrix is not None:
    df_static_base = df_matrix.copy()
user_shifts = {}

if df_matrix is not None and market_choice != "Global Overview":
    st.sidebar.write("---")
    st.sidebar.markdown("#### Adjust Platform Attention Weights")
    
    for entity in df_matrix["Platform/Publisher"].unique():
        orig_val = float(df_matrix[df_matrix["Platform/Publisher"] == entity]["P13+"].iloc[0])
        max_down = -float(orig_val)
        
        slider_min = max(max_down, -500.0)
        slider_max = 500.0
        
        val = st.sidebar.slider(
            label=f"Shift {entity} (Hours)",
            min_value=float(slider_min),
            max_value=float(slider_max),
            value=0.0,
            step=5.0,
            key=f"slide_{entity}_v1"
        )
        if val != 0.0:
            user_shifts[entity] = val
if df_matrix is not None:
    active_shifts = {k: float(v) for k, v in user_shifts.items() if v != 0.0}
    if active_shifts:
        for entity, shift_val in active_shifts.items():
            idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
            if len(idx) > 0:
                p13_orig = float(df_static_base.loc[idx, "P13+"])
                if p13_orig > 0:
                    adj_p13 = max(0.0, p13_orig + shift_val)
                    ratio = adj_p13 / p13_orig
                    df_matrix.loc[idx, "P13+"] = adj_p13
                    df_matrix.loc[idx, "13-54 Majority"] = max(0.0, adj_p13 - float(df_static_base.loc[idx, "55+ GenX+"]))
                    for c in ["13-44 NextGen", "13-34 Youth", "13-24 GenA/Z"]:
                        df_matrix.loc[idx, c] = float(df_static_base.loc[idx, c]) * ratio

    total_shifted_hours = sum(active_shifts.values())
    if abs(total_shifted_hours) > 0.01:
        non_shifted_mask = ~df_matrix["Platform/Publisher"].isin(active_shifts.keys())
        total_non_shifted_pool = float(df_static_base[non_shifted_mask]["P13+"].sum())
        if total_non_shifted_pool > 0.0:
            for entity in df_static_base[non_shifted_mask]["Platform/Publisher"].unique():
                idx = df_matrix[df_matrix["Platform/Publisher"] == entity].index
                if len(idx) > 0:
                    p13_orig_val = float(df_static_base.loc[idx, "P13+"])
                    ratio = max(0.0, p13_orig_val + (-total_shifted_hours * (p13_orig_val / total_non_shifted_pool))) / p13_orig_val if p13_orig_val > 0.0 else 1.0
                    df_matrix.loc[idx, "P13+"] = p13_orig_val * ratio
                    df_matrix.loc[idx, "13-54 Majority"] = max(0.0, (p13_orig_val * ratio) - float(df_static_base.loc[idx, "55+ GenX+"]))
                    for c in ["13-44 NextGen", "13-34 Youth", "13-24 GenA/Z"]:
                        df_matrix.loc[idx, c] = float(df_static_base.loc[idx, c]) * ratio

    df_matrix[cols[1:]] = df_matrix[cols[1:]].round(1)

flag_icon = {
    "Global Overview": "🌐", "United States": "🇺🇸", "Germany": "🇩🇪", 
    "United Kingdom": "🇬🇧", "France": "🇫🇷", "Italy": "🇮🇹", 
    "Spain": "🇪🇸", "Brazil": "🇧🇷", "Mexico": "🇲🇽", "Canada": "🇨🇦",
    "India": "🇮🇳", "Japan": "🇯🇵", "South Korea": "🇰🇷", "Denmark": "🇩🇰",
    "Sweden": "🇸🇪", "Norway": "🇳🇴", "Finland": "🇫🇮", "Slovakia": "🇸🇰",
    "Slovenia": "🇸🇮", "Croatia": "🇭🇷", "Bulgaria": "🇧🇬", "Romania": "🇷🇴",
    "Moldova": "🇲🇩", "Czech Republic": "🇨🇿"
}.get(market_choice, "🇺🇸")

tab_labels = ["CSAI Interactive Index Matrix", "Why ECSAI?", "ECSAI FAQs", "Index Architecture & Methodology"]
tab1, tab2, tab3, tab4 = st.tabs(tab_labels)
with tab1:
    if market_choice == "Global Overview":
        # ----------------================================================================================
        # HIGH-LEVEL GLOBAL OVERVIEW CANVAS MODE: Continuous Narrative Sequence Architecture
        # --------------------------------================================================================
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
            st.warning("⚠️ `global_index_13+.png` asset missing from repository folder.")
        st.markdown(
            "##### **Of all the data in this report, the most crucial datapoint is this: 82% of the world population — 73% of the people in these eight regions — are now under 54.**"
        )
        st.markdown(
            "This new index reveals that Legacy TV relies, almost entirely, on the shrinking minority of our "
            "most senior citizens watching the same stuff, over and over and over, throwing off the balance of "
            "measured video consumption. When you remove that dying demographic, the combined fourteen Legacy outlets "
            "in this index are surpassed — handily — by YouTube, Netflix, and TikTok."
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
            st.warning("⚠️ `us_index_13-54.png` asset missing from repository folder.")

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
        
        # Dual Column Layout for Side-by-Side Generation Profiles
        c1, c2 = st.columns(2)
        with c1:
            if os.path.exists("us_index_13-34.png"): st.image("us_index_13-34.png", caption="US TOTAL ATTENTION: P13-34", use_container_width=True)
            else: st.warning("⚠️ `us_index_13-34.png` missing from repository.")
        with c2:
            if os.path.exists("us_index_13-24.png"): st.image("us_index_13-24.png", caption="US TOTAL ATTENTION: P13-24", use_container_width=True)
            else: st.warning("⚠️ `us_index_13-24.png` missing from repository.")

        st.markdown(
            "And this, right here, is precisely why we need a Cross-Screen Index. No one else is measuring "
            "all these platforms, side by side, on all devices. So, the industry get easily distracted by flaccid "
            "signposts that tells us “YouTube is #1 on TV!” (with P2+ and without counting phones, laptops, "
            "or tablets)."
        )
        st.markdown(
            "Traditional currencies track the device canvas; they do not track the human. They count a "
            "television playing to a room as an absolute hit, while treating a high-intensity mobile session that "
            "requires active thumb-and-eye engagement to exist as \"digital noise.\" This is a collective "
            "industry blindness. Legacy tracking systems want you to look at media through isolated reach "
            "silos — treating an open screen in an empty room as equal to an active, single-screen consumer "
            "focus."
        )
        st.markdown(
            "So much of our Media measurement investment is spent measuring television "
            "viewing — even when that TV is not being watched. As a result, the Media "
            "Industrial complex spends a disproportionate amount of time, energy and "
            "resources fighting over control of a screen that *only captures 40% of video "
            "consumption*. That's not just bad business; it's a suicide mission."
        )
        st.markdown(
            "The Index is designed to prevent that — designed to show, specifically, where the entirety of "
            "consumer attention is actually being paid, so that Media professionals can invest in content, "
            "advertising, overhead, and infrastructure, accordingly."
        )
        st.markdown(
            "Each quarter, we will update the ECSAI (pronounced EE-say) with new data, on a rolling six "
            "months basis. Simultaneously, we will drop an Index Report, on [Media War & Peace](https://substack.com), "
            "with deep analysis of the data and the trends, right here on Substack."
        )
        st.markdown(
            "This is different from other measurement offerings, which provide small, irrelevant glimpses of "
            "data for free, then charge clients millions to fund it, while keeping the vast majority of us who "
            "work in Media in the dark. This incentivizes the measurement industrial complex to keep our "
            "data in silos, dividing and double-counting consumer attention."
        )

        st.markdown(
            "When we embark on projects like this, we start fresh. No preconceptions. No confirmation bias. "
            "We let the data give us the plot, then we tell the story. This is, by far, our most ambitious data "
            "endeavor yet. It's a mountain of data and it tells a remarkable story about the future of Media "
            "based on the actual needs of real consumers. We will keep following the data where it leads us."
        )
        st.markdown(
            "<p style='font-size: 0.95rem; font-weight: bold; line-height: 1.5;'>Take The ECSAI for a test drive! "
            "Let us know what you think at <a href='mailto:info@eshap.tv' style='color: #007bff; text-decoration: underline; "
            "font-weight: bold;'>info@eshap.tv</a>.<br><br>And, please, don't forget to take some time to enjoy your day!"
            "<br><br>ESHAP</p>", 
            unsafe_allow_html=True
        )

    else:
        st.subheader(f"Cross-Screen Attention Tracker: {flag_icon} {market_choice}")
        st.markdown("#### Interactive Visual Share Map")
        st.markdown("<p style='font-size: 0.92rem; font-weight: bold; font-style: italic; color: #FF0000; margin-top: -0.5rem; margin-bottom: 0.75rem;'>MILLIONS OF HOURS</p>", unsafe_allow_html=True)
        
        st.html("<style>div[data-testid='stRadio'] > div { gap: 1.5rem !important; } div[data-testid='stRadio'] label p { font-size: 0.95rem !important; white-space: nowrap !important; }</style>")
        demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
        selected_demo = st.radio("Select Demographic Cohort to Isolate in Bar Chart:", options=demo_columns, horizontal=True)
        
        chart_df = df_matrix.copy()
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
            st.markdown("<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross Screen Attention Ledger: MEXICO</strong><br>Platform totals represent unified corporate parent structures. TelevisaUnivision incorporates all ViX streaming telemetry. YouTube and mobile digital baselines natively absorb all open-distribution and telco-bundled attention siphons. Concurrent multi-screening duplication and passive device use discounted.</p>", unsafe_allow_html=True)
        elif market_choice == "Canada":
            st.markdown("<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross Screen Attention Ledger: CANADA</strong><br>Platform totals represent unified corporate parent structures. CBC includes all CBC Gem digital consumption parameters. Bell Media consolidates Crave, CTV, and TSN properties. Rogers includes Sportsnet and Citytv cross-screen streaming configurations.</p>", unsafe_allow_html=True)

        elif market_choice in ["France", "Germany", "United Kingdom", "Italy", "Spain", "Denmark", "Sweden", "Norway", "Finland", "Slovakia", "Slovenia", "Croatia", "Bulgaria", "Romania", "Moldova", "Czech Republic"]:
            st.markdown(f"<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross Screen Attention Ledger: {market_choice.upper()}</strong><br>Platform totals represent unified holding corporate structures. Traditional TV volumes are scaled using audited single-screen panel metrics from regional state-backed systems (including BARB, Médiamétrie, and Agf/Gfk) and balanced against hardware-level handset logs. Multi-screening and background device noise programmatically flattened through duplication discounts to retain zero-sum integrity.</p>", unsafe_allow_html=True)
        elif market_choice == "India":
            st.markdown("<p style='font-size: 0.82rem; font-style: italic; color: #444444; margin-top: 0.5rem; line-height: 1.4;'><strong>Cross Screen Attention Ledger: INDIA</strong><br>Platform totals represent unified corporate parent holdings. JioStar integrates Star TV, Viacom18, and JioCinema streaming telemetry parameters. Doordarshan tracks all linear configurations managed under Prasar Bharati public distribution frameworks.</p>", unsafe_allow_html=True)
            
        export_filename = f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv"
        st.download_button(label="Export Current Ledger to CSV", data=df_matrix.to_csv(index=False).encode('utf-8'), file_name=export_filename, mime="text/csv", use_container_width=True)

with tab2:
    st.markdown("<div style='text-align: center; line-height: 0.95; margin-bottom: 1.5rem;'><h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold;'>WHY THE ECSAI?</h2><h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold; color: #FF0000;'>BECAUSE HUMAN ATTENTION IS FINITE.</h2><h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold;'>WE REALLY NEED TO TRACK IT THAT WAY.</h2></div>", unsafe_allow_html=True)
    st.markdown("Let's face the raw reality of modern media consumption: our entire multi-billion-dollar industry is navigating by a map that does not match the earth.")
    st.markdown("Traditional currencies track the device canvas; they do not track the human. They count a television playing to a room as an absolute hit, while treating a high-intensity mobile session that requires active thumb-and-eye engagement to exist as \"low-tier digital noise.\" This is a collective industry blindness. Legacy tracking systems want you to look at media through isolated reach silos—treating an open screen in an empty room as equal to an active, single-screen consumer focus.")
    st.markdown("The ESHAP Cross-Screen Attention Index (ESCAI) introduces a completely new analytical paradigm to capture this shift. We didn't build a local programmatic tool to place an individual ad spot next Tuesday. To look at this index and ask how to execute a DSP trade is to confuse a compass with a shovel.")
    st.markdown("ESCAI enforces the absolute laws of human physics. Human time is a non-elastic, zero-sum commodity—a closed market sponge. Every single hour gained by an algorithm is an hour permanently destroyed for a broadcast tower.")
    st.markdown("We have built what we believe is the ultimate \"Attention Model,\" the first index to track the actual behavior of humans across all the screens they use and account for their attention in a way that helps us all map a course for the future of media.")
    st.markdown("We will update this index monthly, on a rolling six months basis. Simultaneously, we will drop analysis of the latest data on **[Media War & Peace](https://substack.com)**.")
    st.markdown("Thanks for your attention!\n\n**ESHAP**")

with tab3:
    st.subheader("ECSAI Frequently Asked Questions (FAQs)")
    st.markdown("#### Q: THE ZERO-SUM SQUEEZE AND DIARY DE-DUPLICATION")
    if os.path.exists("ecsai_flow.png"): 
        st.image("ecsai_flow.png", caption="ESHAP Cross-Screen Attention Index Production Workflow Map", use_container_width=True)
    st.markdown("This zero-sum squeeze is where the smooth, cross-screen blending actually happens. If we simply added the television hours to the digital hours, the market sponge would explode past the census ceiling due to concurrent multi-screening — a consumer scrolling on TikTok reply window while the television plays a broadcast in the background. Our index model applies localized duplication coefficients derived from GWI Consumer Diaries and verified attention panels. These diaries track the exact percentage of a cohort that multi-screens daily (e.g., 77% of Gen Z in France). Our model uses this percentage to calculate a duplication discount factor. It treats human attention as a finite zero-sum resource: if the eye is looking at a smartphone screen, that fraction of time is physically subtracted from the traditional television glass volume. The digital hours (which require active, focused scrolling on a handheld device) are treated as hard, primary attention blocks. The background television glass hours are programmatically squeezed down until the entire multi-screen overlap is flattened and the duplication is erased. This prioritized single-screen eye focus is a primary reason background audio is not covered in this index.")
    st.write("---")
    st.markdown("<p style='font-size: 0.92rem; font-weight: bold; line-height: 1.5;'>Take The ECSAI for a test drive! Let us know what you think at <a href='mailto:info@eshap.tv' style='color: #007bff; text-decoration: underline; font-weight: bold;'>info@eshap.tv</a>.<br><br>And, please, don't forget to take some time to enjoy your day!<br><br>ESHAP</p>", unsafe_allow_html=True)

with tab4:
    sub_method, sub_source = st.tabs(["Methodology Blueprint", "Sourcing Matrix"])
    is_global_view = (market_choice == "Global Overview")
    
    # Explicit File Registry: Maps your exact uploaded filenames directly to the interface views
    method_file_map = {
        "United States": "methodology_us.txt", "France": "methodology_fr.txt", "United Kingdom": "methodology_uk.txt",
        "Italy": "methodology_it.txt", "Germany": "methodology_de.txt", "Spain": "methodology_sp.txt",
        "Brazil": "methodology_br.txt", "Mexico": "methodology_mx.txt", "Canada": "Canada Methodology.txt",
        "India": "India Methodology.txt", "Japan": "methodology_jp.txt", "South Korea": "South Korea Methodology.txt",
        "Denmark": "DENMARK Methodology.txt", "Sweden": "SWEDEN Methodology.txt", "Norway": "NORWAY Methodology.txt",
        "Finland": "FINLAND Methodology.txt", "Slovakia": "SLOVAKIA Methodology.txt", "Slovenia": "SLOVENIA Methodology.txt",
        "Croatia": "CROATIA Methodology.txt", "Bulgaria": "BULGARIA Methodology.txt", "Romania": "ROMANIA Methodology.txt",
        "Moldova": "MOLDOVA Methodology.txt", "Czech Republic": "CZECH REPUBLIC Methodology.txt"
    }
    
    sources_file_map = {
        "United States": "sources_us.txt", "France": "sources_fr.txt", "United Kingdom": "sources_uk.txt",
        "Italy": "sources_it.txt", "Germany": "sources_de.txt", "Spain": "sources_sp.txt",
        "Brazil": "sources_br.txt", "Mexico": "sources_orig_mx.txt", "Canada": "Canada Sources.txt",
        "India": "India Sources.txt", "Japan": "sources_jp.txt", "South Korea": "South Korea Sources.txt",
        "Denmark": "DENMARK Sources.txt", "Sweden": "SWEDEN Sources.txt", "Norway": "NORWAY Sources.txt",
        "Finland": "FINLAND Sources.txt", "Slovakia": "SLOVAKIA Sources.txt", "Slovenia": "SLOVENIA Sources.txt",
        "Croatia": "CROATIA Sources.txt", "Bulgaria": "BULGARIA Sources.txt", "Romania": "ROMANIA Sources.txt",
        "Moldova": "MOLDOVA Sources.txt", "Czech Republic": "CZECH REPUBLIC Sources.txt"
    }
    
    f_method = method_file_map.get(market_choice, "methodology_us.txt")
    f_source = sources_file_map.get(market_choice, "sources_us.txt")
    if is_global_view:
        f_method = "methodology_us.txt"
        f_source = "sources_us.txt"
    
    with sub_method:
        st.markdown(f"### METHODOLOGY: CARTOGRAPHER'S BLUEPRINT ({flag_icon} {market_choice.upper()})")
        if not is_global_view:
            w_dict = {
                "United States": ("64.2%", "35.8%"), "France": ("65.1%", "34.9%"), "United Kingdom": ("63.8%", "36.2%"), 
                "Italy": ("59.8%", "40.2%"), "Germany": ("61.5%", "38.5%"), "Spain": ("62.0%", "38.0%"), 
                "Brazil": ("68.5%", "31.5%"), "Mexico": ("71.0%", "29.0%"), "Canada": ("64.2%", "35.8%"), 
                "India": ("78.4%", "21.6%"), "Japan": ("51.2%", "48.8%"), "South Korea": ("61.0%", "39.0%"), 
                "Denmark": ("62.4%", "37.6%"), "Sweden": ("61.8%", "38.2%"), "Norway": ("63.0%", "37.0%"), 
                "Finland": ("60.5%", "39.5%"), "Slovakia": ("64.0%", "36.0%"), "Slovenia": ("61.2%", "38.8%"), 
                "Croatia": ("58.5%", "41.5%"), "Bulgaria": ("57.2%", "42.8%"), "Romania": ("59.1%", "40.9%"), 
                "Moldova": ("65.4%", "34.6%"), "Czech Republic": ("62.8%", "37.2%")
            }
            w1, w2 = w_dict.get(market_choice, ("64.2%", "35.8%"))
            st.markdown(f"**Territorial Demographic Weight:** {w1} is &le; 54 / {w2} is &ge; 55")
        
        # Pull text safely from the server RAM memory cache using the exact file names
        methodology_text = load_text_asset(f_method)
        if methodology_text:
            if "rtf1" in methodology_text or "ansicpg" in methodology_text:
                # Strip out rich text format headers if they contaminate your plain text window
                clean_lines = [line for line in methodology_text.split("\n") if "{" not in line and "}" not in line and "\\" not in line]
                st.write("\n".join(clean_lines).strip())
            else:
                st.write(methodology_text)
        else:
            st.info(f"Methodology text asset `{f_method}` not found in memory cache.")
            
    with sub_source:
        st.markdown(f"### DATA SOURCES ({flag_icon} {market_choice.upper()})")
        sources_text = load_text_asset(f_source)
        if sources_text:
            st.write(sources_text)
        else:
            st.info(f"Sources text asset `{f_source}` not found in memory cache.")
