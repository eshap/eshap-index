import streamlit as st
import pandas as pd
import base64
import os
import io

CORE_TOKENS = [
    "us", "fr", "uk", "it", "de", "sp", "br", "mx", "can", "in", 
    "jp", "sk", "den", "swe", "nor", "fin", "sv", "sle", "cro", "bg", 
    "ro", "mol", "cr"
]

# Instant Memory Cache Bootstrapper: Reads the filesystem once and retains data permanently in RAM
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
    return st.session_state.text_memory_cache.get(filename, default_text)

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
CA_BASE = [
    ["CBC (Radio-Canada)", 540.0, 395.0, 145.0, 118.9, 95.1, 42.4],
    ["YOUTUBE", 520.0, 105.0, 415.0, 290.5, 226.7, 138.2],
    ["BELL MEDIA (CTV)", 495.0, 315.0, 180.0, 135.0, 97.2, 44.1],
    ["NETFLIX", 435.0, 95.0, 340.0, 248.2, 156.4, 79.8],
    ["TIKTOK", 365.0, 15.0, 350.0, 273.0, 223.8, 163.4],
    ["ROGERS (Citytv)", 310.0, 195.0, 115.0, 86.2, 62.1, 27.9],
    ["INSTAGRAM", 245.0, 25.0, 220.0, 191.4, 155.1, 85.3],
    ["CORUS (Global TV)", 225.0, 155.0, 70.0, 52.5, 37.8, 16.8],
    ["DISNEY", 210.0, 48.0, 162.0, 123.1, 77.6, 32.1],
    ["WBD", 195.0, 110.0, 85.0, 57.9, 28.9, 12.1],
    ["FACEBOOK", 185.0, 102.0, 83.0, 45.6, 16.9, 3.2],
    ["AMAZON", 175.0, 55.0, 120.0, 98.4, 61.0, 25.6]
]
IN_BASE = [
    ["JIOSTAR (Corp Portfolio)", 3890.0, 810.0, 3080.0, 2464.0, 1878.8, 1016.4],
    ["YOUTUBE", 3640.0, 210.0, 3430.0, 2572.5, 2092.3, 1372.0],
    ["ZEE ENTERTAINMENT", 1945.0, 540.0, 1405.0, 1095.9, 814.9, 421.5],
    ["SONY (SPNI Holdings)", 1620.0, 435.0, 1185.0, 924.3, 687.3, 355.5],
    ["INSTAGRAM", 1480.0, 35.0, 1445.0, 1286.1, 1098.2, 635.8],
    ["TIKTOK", 1120.0, 12.0, 1108.0, 864.2, 731.3, 565.1],
    ["NETFLIX", 915.0, 85.0, 830.0, 647.4, 431.6, 215.8],
    ["AMAZON", 635.0, 92.0, 543.0, 445.3, 293.2, 128.6],
    ["DD (Doordarshan)", 515.0, 365.0, 150.0, 112.5, 76.5, 31.5],
    ["FACEBOOK", 495.0, 225.0, 270.0, 162.0, 64.8, 10.8]
]
JP_BASE = [
    ["NHK (Japan Broadcasting)", 1120.0, 845.0, 275.0, 211.8, 151.3, 77.0],
    ["FUJI MEDIA HOLDINGS", 780.0, 495.0, 285.0, 213.8, 153.9, 77.5],
    ["NIPPON TV (NTV)", 765.0, 480.0, 285.0, 213.8, 153.9, 77.5],
    ["YOUTUBE", 735.0, 185.0, 550.0, 385.0, 300.3, 183.4],
    ["TBS HOLDINGS", 710.0, 455.0, 255.0, 191.3, 137.7, 69.4],
    ["TV ASAHI HOLDINGS", 685.0, 440.0, 245.0, 183.8, 132.3, 66.6],
    ["NETFLIX", 390.0, 95.0, 295.0, 215.4, 138.7, 70.8],
    ["TIKTOK", 315.0, 18.0, 297.0, 231.7, 189.2, 136.6],
    ["AMAZON (Prime Video)", 295.0, 82.0, 213.0, 174.7, 108.6, 49.0],
    ["INSTAGRAM", 220.0, 22.0, 198.0, 172.3, 139.6, 76.8],
    ["CYBERAGENT (AbemaTV)", 185.0, 55.0, 130.0, 104.0, 78.0, 39.0],
    ["U-NEXT", 145.0, 38.0, 107.0, 85.6, 53.5, 23.5],
    ["FACEBOOK", 95.0, 62.0, 33.0, 18.2, 6.7, 1.2]
]
SK_BASE = [
    ["KBS (Korean Broad.)", 435.0, 295.0, 140.0, 107.8, 77.6, 39.5],
    ["YOUTUBE", 415.0, 68.0, 347.0, 242.9, 189.5, 115.7],
    ["CJ ENM (TvN/Tving)", 365.0, 145.0, 220.0, 165.0, 121.0, 61.6],
    ["NETFLIX", 310.0, 42.0, 268.0, 195.6, 126.0, 64.3],
    ["MBC", 290.0, 195.0, 95.0, 71.3, 51.3, 26.1],
    ["SBS", 285.0, 185.0, 100.0, 75.0, 54.0, 27.5],
    ["TIKTOK", 195.0, 6.0, 189.0, 147.4, 120.4, 87.0],
    ["WAVVE", 155.0, 65.0, 90.0, 67.5, 47.7, 22.5],
    ["INSTAGRAM", 140.0, 12.0, 128.0, 111.4, 90.4, 49.7],
    ["JTBC", 125.0, 78.0, 47.0, 35.3, 25.4, 12.9],
    ["AMAZON", 55.0, 12.0, 43.0, 35.2, 21.8, 9.2],
    ["FACEBOOK", 45.0, 28.0, 17.0, 9.4, 3.5, 0.6]
]
DEN_BASE = [
    ["DR (Danmarks Radio)", 295.0, 195.0, 100.0, 77.0, 55.4, 25.5],
    ["YOUTUBE", 265.0, 42.0, 223.0, 156.1, 121.5, 74.2],
    ["TV2 DANMARK", 245.0, 135.0, 110.0, 82.5, 59.4, 27.2],
    ["NETFLIX", 215.0, 28.0, 187.0, 136.5, 87.8, 44.7],
    ["TIKTOK", 165.0, 3.0, 162.0, 126.3, 103.6, 74.8],
    ["VIAPLAY GROUP", 115.0, 48.0, 67.0, 46.9, 28.1, 10.7],
    ["INSTAGRAM", 110.0, 8.0, 102.0, 88.7, 71.9, 39.5],
    ["AMAZON", 90.0, 18.0, 72.0, 59.0, 36.6, 15.4],
    ["DISNEY", 75.0, 12.0, 63.0, 47.9, 30.2, 12.7],
    ["WBD", 65.0, 15.0, 50.0, 36.5, 23.0, 9.7],
    ["FACEBOOK", 52.0, 28.0, 24.0, 13.2, 4.9, 0.9]
]
SWE_BASE = [
    ["YOUTUBE", 380.0, 65.0, 315.0, 225.0, 165.0, 85.0],
    ["SVT (Sveriges Tel.)", 380.0, 165.0, 215.0, 135.0, 85.0, 40.0],
    ["TV4 MEDIA", 260.0, 115.0, 145.0, 90.0, 55.0, 25.0],
    ["NETFLIX", 323.0, 38.0, 285.0, 220.0, 150.0, 75.0],
    ["TIKTOK", 250.0, 5.0, 245.0, 185.0, 145.0, 105.0],
    ["VIAPLAY GROUP", 147.0, 22.0, 125.0, 95.0, 65.0, 32.0],
    ["AMAZON", 203.0, 28.0, 175.0, 135.0, 95.0, 52.0],
    ["DISNEY", 110.0, 15.0, 95.0, 75.0, 50.0, 28.0],
    ["WBD", 88.0, 12.0, 76.0, 58.0, 40.0, 22.0],
    ["FACEBOOK", 77.0, 42.0, 35.0, 22.0, 12.0, 4.0]
]
NOR_BASE = [
    ["NRK (Norsk Rikskringkasting)", 285.0, 185.0, 100.0, 77.0, 55.4, 25.5],
    ["YOUTUBE", 255.0, 40.0, 215.0, 150.5, 117.1, 71.5],
    ["TV2 NORGE", 215.0, 115.0, 100.0, 75.0, 54.0, 24.8],
    ["NETFLIX", 210.0, 25.0, 185.0, 135.0, 86.9, 44.3],
    ["TIKTOK", 155.0, 2.0, 153.0, 119.3, 97.9, 70.7],
    ["VIAPLAY GROUP", 105.0, 42.0, 63.0, 44.1, 26.5, 10.1],
    ["INSTAGRAM", 102.0, 7.0, 95.0, 82.6, 67.0, 36.8],
    ["AMAZON", 85.0, 15.0, 70.0, 57.4, 35.6, 15.0],
    ["DISNEY", 72.0, 10.0, 62.0, 47.1, 29.7, 12.5],
    ["WBD", 58.0, 12.0, 46.0, 33.6, 21.2, 8.9],
    ["FACEBOOK", 48.0, 25.0, 23.0, 12.6, 4.7, 0.8]
]
FIN_BASE = [
    ["Yle (Yleisradio)", 245.0, 175.0, 70.0, 53.9, 38.8, 17.8],
    ["YOUTUBE", 225.0, 35.0, 190.0, 133.0, 103.5, 63.3],
    ["SANOMA MEDIA", 185.0, 95.0, 90.0, 67.5, 48.6, 22.3],
    ["NETFLIX", 175.0, 22.0, 153.0, 111.7, 71.9, 36.6],
    ["TIKTOK", 135.0, 2.0, 133.0, 103.7, 85.1, 61.4],
    ["MTV OY", 125.0, 68.0, 57.0, 42.7, 30.7, 14.1],
    ["INSTAGRAM", 95.0, 6.0, 89.0, 77.4, 62.7, 34.5],
    ["AMAZON", 75.0, 15.0, 60.0, 49.2, 30.5, 12.8],
    ["DISNEY", 65.0, 10.0, 55.0, 41.8, 26.4, 11.1],
    ["WBD", 52.0, 12.0, 40.0, 29.2, 18.4, 7.7],
    ["FACEBOOK", 42.0, 22.0, 20.0, 11.0, 4.1, 0.7]
]
SV_BASE = [
    ["MARKÍZA GROUP", 245.0, 135.0, 110.0, 82.5, 59.4, 27.2],
    ["JOJ GROUP", 215.0, 122.0, 93.0, 69.7, 50.2, 23.0],
    ["YOUTUBE", 195.0, 42.0, 153.0, 107.1, 83.5, 50.9],
    ["STVR (Slovak TV)", 165.0, 115.0, 50.0, 35.0, 20.0, 5.5],
    ["NETFLIX", 145.0, 25.0, 120.0, 87.6, 56.4, 28.8],
    ["TIKTOK", 115.0, 2.0, 113.0, 88.1, 72.3, 48.6],
    ["INSTAGRAM", 90.0, 5.0, 85.0, 73.9, 59.9, 32.9],
    ["WBD (MAX)", 45.0, 18.0, 27.0, 19.7, 12.4, 5.2],
    ["AMAZON", 38.0, 8.0, 30.0, 24.6, 15.2, 6.4],
    ["FACEBOOK", 32.0, 18.0, 14.0, 7.7, 2.8, 0.5]
]
SLE_BASE = [
    ["PRO PLUS (POP TV/A Kanal)", 95.0, 52.0, 43.0, 32.2, 23.2, 10.6],
    ["RTVSLO (Radiotelevizija)", 85.0, 58.0, 27.0, 18.9, 10.8, 2.9],
    ["YOUTUBE", 75.0, 15.0, 60.0, 42.0, 32.7, 19.9],
    ["TIKTOK", 52.0, 1.0, 51.0, 39.8, 32.6, 21.9],
    ["NETFLIX", 48.0, 8.0, 40.0, 29.2, 18.8, 9.6],
    ["INSTAGRAM", 38.0, 2.0, 36.0, 31.3, 25.4, 13.9],
    ["WBD", 20.0, 8.0, 12.0, 8.7, 5.5, 2.3],
    ["AMAZON", 18.0, 4.0, 14.0, 11.5, 7.1, 3.0],
    ["FACEBOOK", 15.0, 8.0, 7.0, 3.8, 1.4, 0.2]
]
CRO_BASE = [
    ["HTV (Hrvatska Radiotelevizija)", 195.0, 125.0, 70.0, 53.9, 38.8, 19.5],
    ["YOUTUBE", 185.0, 32.0, 153.0, 107.1, 83.5, 50.9],
    ["RTL HRVATSKA", 175.0, 95.0, 80.0, 60.0, 43.2, 21.8],
    ["NOVA TV CROATIA", 165.0, 88.0, 77.0, 57.7, 41.6, 21.0],
    ["TIKTOK", 125.0, 2.0, 123.0, 95.9, 78.7, 52.9],
    ["NETFLIX", 115.0, 18.0, 97.0, 70.8, 45.5, 23.2],
    ["INSTAGRAM", 85.0, 5.0, 80.0, 69.6, 56.4, 31.0],
    ["WBD", 45.0, 18.0, 27.0, 19.7, 12.4, 5.2],
    ["AMAZON", 35.0, 8.0, 27.0, 22.1, 13.7, 5.8],
    ["FACEBOOK", 32.0, 18.0, 14.0, 7.7, 2.8, 0.5]
]
BG_BASE = [
    ["bTV Media Group", 345.0, 215.0, 130.0, 97.5, 68.9, 31.2],
    ["Nova Broadcasting Group", 330.0, 195.0, 135.0, 101.2, 72.9, 33.5],
    ["YOUTUBE", 285.0, 52.0, 233.0, 163.1, 127.2, 77.6],
    ["TIKTOK", 195.0, 4.0, 191.0, 148.9, 122.2, 82.1],
    ["NETFLIX", 145.0, 22.0, 123.0, 89.8, 57.6, 29.4],
    ["BNT (Bulgarian Nat. TV)", 125.0, 88.0, 37.0, 25.9, 14.8, 4.2],
    ["INSTAGRAM", 115.0, 8.0, 107.0, 93.1, 75.4, 41.5],
    ["WBD (MAX)", 65.0, 28.0, 37.0, 27.0, 17.0, 7.1],
    ["AMAZON", 55.0, 12.0, 43.0, 35.2, 21.8, 9.2],
    ["FACEBOOK", 50.0, 28.0, 22.0, 12.1, 4.4, 0.8]
]
RO_BASE = [
    ["PRO TV", 685.0, 365.0, 320.0, 240.0, 163.2, 70.4],
    ["ANTENA TV GROUP", 585.0, 345.0, 240.0, 180.0, 122.4, 52.8],
    ["YOUTUBE", 525.0, 85.0, 440.0, 308.0, 240.2, 146.5],
    ["TIKTOK", 390.0, 8.0, 382.0, 297.9, 244.5, 165.7],
    ["NETFLIX", 295.0, 42.0, 253.0, 184.6, 118.9, 60.6],
    ["TVR (Romanian TV)", 195.0, 135.0, 60.0, 42.0, 24.0, 6.6],
    ["INSTAGRAM", 185.0, 10.0, 175.0, 152.2, 123.5, 67.9],
    ["WBD (MAX)", 95.0, 38.0, 57.0, 41.6, 26.2, 11.0],
    ["AMAZON", 85.0, 18.0, 67.0, 54.9, 34.0, 14.3],
    ["FACEBOOK", 72.0, 42.0, 30.0, 16.5, 6.1, 1.1]
]
MOL_BASE = [
    ["Moldova 1", 115.0, 78.0, 37.0, 25.9, 14.8, 4.2],
    ["YOUTUBE", 95.0, 15.0, 80.0, 56.0, 43.5, 26.5],
    ["JURNAL TV", 85.0, 48.0, 37.0, 25.9, 14.8, 4.2],
    ["TIKTOK", 65.0, 1.0, 64.0, 49.9, 41.0, 27.8],
    ["NETFLIX", 55.0, 8.0, 47.0, 34.3, 22.1, 11.2],
    ["PRIME TV MOLDOVA", 45.0, 28.0, 17.0, 11.9, 6.8, 1.9],
    ["INSTAGRAM", 38.0, 2.0, 36.0, 31.3, 25.4, 13.9],
    ["FACEBOOK", 22.0, 12.0, 10.0, 5.5, 2.0, 0.4]
]
CR_BASE = [
    ["ČT (Česká Televize)", 485.0, 335.0, 150.0, 115.5, 83.2, 42.4],
    ["TV NOVA", 455.0, 260.0, 195.0, 146.2, 105.3, 53.7],
    ["YOUTUBE", 425.0, 85.0, 340.0, 238.0, 185.6, 113.2],
    ["PRIMA GROUP", 390.0, 225.0, 165.0, 123.7, 89.1, 45.4],
    ["NETFLIX", 315.0, 52.0, 263.0, 192.0, 123.3, 62.9],
    ["TIKTOK", 255.0, 5.0, 250.0, 195.0, 160.0, 107.5],
    ["INSTAGRAM", 195.0, 12.0, 183.0, 159.2, 129.0, 71.0],
    ["WBD (MAX)", 95.0, 42.0, 53.0, 38.7, 24.4, 10.2],
    ["AMAZON", 85.0, 22.0, 63.0, 51.6, 32.0, 13.5],
    ["FACEBOOK", 75.0, 42.0, 33.0, 18.1, 6.7, 1.2]
]
bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    with open("planet_bullet.png", "rb") as b_f: 
        bullet_base64 = base64.b64encode(b_f.read()).decode()

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
    with open("eshap_map.png", "rb") as img_f: 
        logo_base64 = base64.b64encode(img_f.read()).decode()

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
        "Global Overview", "United States", "Brazil", "Mexico", "Germany", "United Kingdom", "France", "Italy", "Spain",
        "Canada", "India", "Japan", "South Korea", "Denmark", "Sweden", "Norway", "Finland", "Slovakia", "Slovenia",
        "Croatia", "Bulgaria", "Romania", "Moldova", "Czech Republic"
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
        "MEDIASET ESPANA": "MEDIASET ES", "MFE (MEDIASET)": "MFE", "GROUPO RECORD": "GROUPO RECORD"
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
    st.markdown(
        "**• Census Denominator Lock (The Total Volume Ceiling)**<br>"
        "The entire model is anchored on the local state census registry (such as INSEE, Destatis, ISTAT, or the "
        "U.S. Census Bureau). The index takes the total population headcount for the territory, filters for "
        "the P13+ universe. It then establishes a Total Available Awake Hours Budget per month (assuming a "
        "standardized 16-hour active day). This number is our absolute ceiling. It represents the total size "
        "of the market sponge. No matter how many apps or TV channels claim massive usage, the combined monthly "
        "hours in our index can never exceed this hard, census-backed population budget.", 
        unsafe_allow_html=True
    )
    st.markdown(
        "**• Normalizing Metrics into 'Absolute Attention Hours'**<br>"
        "Next, our model takes the fragmented public data points and converts them into a singular currency: "
        "Millions of Absolute Attention Hours per Month. Blending the Glass and Feed Data: Traditional linear "
        "TV currencies (like Médiamétrie or BARB) publish reach and 'Time Spent Viewing' (TSV) per day. "
        "The model takes the average daily TSV for a specific cohort, multiplies it by the demographic population "
        "weight from the census, and scales it to 30 days to find total linear hours.",
        unsafe_allow_html=True
    )
    st.markdown(
        "Big Tech investor filings and regulatory white papers present usage in 'Daily Active Users' (DAUs) "
        "or 'Monthly Active Users' (MAUs) paired with global or regional average session lengths. The model "
        "intercepts these ratios, applies the local territory footprint weight, and multiplies active users "
        "by daily active minutes to extract total digital hours. We take the stated number of users per digital "
        "platforms, apportion them by region/populations, then using diaries, surveys, public reports, and "
        "other regional research data, the model assigns pro rata usage hours per day in those regions.",
        unsafe_allow_html=True
    )
    st.markdown(
        "#### Q: THE ZERO-SUM SQUEEZE AND DIARY DE-DUPLICATION"
    )
    if os.path.exists("ecsai_flow.png"): 
        st.image("ecsai_flow.png", caption="ESHAP Cross-Screen Attention Index Production Workflow Map", use_container_width=True)
    else:
        st.info("💡 *[Placeholder for ecsai_flow.png: Baseline Ingestion, Squeeze Dynamics, and Closed Capacity Ceiling Workflow Layout]*")
        
    st.markdown(
        "This zero-sum squeeze is where the smooth, cross-screen blending actually happens. If we simply added "
        "the television hours to the digital hours, the market sponge would explode past the census ceiling "
        "due to concurrent multi-screening—a consumer scrolling on TikTok while the television plays a broadcast "
        "in the background. Our index model applies localized duplication coefficients derived from GWI "
        "Consumer Diaries and verified attention panels. These diaries track the exact percentage of a cohort "
        "that multi-screens daily (e.g., 77% of Gen Z in France)."
    )
    st.markdown(
        "The model uses this percentage to calculate a duplication discount factor. It treats human attention "
        "as a finite zero-sum resource: if the eye is looking at a smartphone screen, that fraction of time "
        "is physically subtracted from the traditional television glass volume. The digital hours (which require "
        "active, focused scrolling on a handheld device) are treated as hard, primary attention blocks. The "
        "background television glass hours are programmatically squeezed down until the entire multi-screen "
        "overlap is flattened and the duplication is erased. This prioritized single-screen eye focus is a primary "
        "reason background audio is not covered in this index."
    )
    st.markdown(
        "#### Q: DOESN'T BLENDING 'SOFT' SURVEY RECALL WITH 'HARD' DEVICE TELEMETRY CORRUPT THE DATA FOUNDATION?"
    )
    st.markdown(
        "The index operates on a strict Separation of Powers. We use a Sovereign Boundary Model where the hard "
        "quantitative ceilings are locked down entirely by currency-grade, hard telemetry logs (Nielsen, "
        "BARB, Médiamétrie, Comscore). The index does not ask consumers how many hours they watched; it uses "
        "hard regulatory telemetry to establish total volume. Behavioral data from GWI Consumer Diaries is "
        "introduced strictly as a coefficient matrix to calculate the mathematical overlap when two devices "
        "are running in the same room. We use behavioral data solely to map the friction points where those "
        "macro volumes intersect. Legacy currencies rely on passive boxes in empty rooms, counting a television "
        "playing to an empty sofa as a hit. We use behavioral data to verify human presence and device "
        "co-activity, injecting human reality back into blind hardware metrics."
    )
    st.markdown(
        "#### Q: ISN'T IT AN 'EQUIVALENCY FALLACY' TO TREAT A SMALL MOBILE SCREEN THE SAME AS A 75-INCH LIVING ROOM TV?"
    )
    st.markdown(
        "The legacy definition of \"premium attention\" is a self-serving myth designed to protect high television "
        "CPMs. Screen size does not equal cognitive impact. A living room television screen frequently functions "
        "as ambient, household background noise. Conversely, a smartphone screen requires active physical "
        "interaction-holding, scrolling, unmuting-to maintain the media stream. This index does not flatten "
        "attention; it democratizes conscious eye-hours. Our Attention Index (ECSAI, pronounced EE-say) strips "
        "away the unearned premium of the living room glass, exposing how mobile feeds capture high-intensity, "
        "active physical engagement while traditional TVs increasingly serve as expensive domestic wallpaper. "
        "If the eye is on the phone screen, that fraction of time is physically subtracted from the television "
        "volume, regardless of how large the TV glass is."
    )
    st.markdown(
        "#### Q: IF A MEDIA BUYER CANNOT USE THIS HIGH-LEVEL DASHBOARD TO EXECUTE AN AD PLACEMENT ON A DSP, ISN'T THE DATA TOO COARSE FOR REAL-WORLD BUYING?"
    )
    st.markdown(
        "To criticize ECSAI for not executing programmatic ad trades is to mistake a compass for a shovel. This "
        "app is a macroeconomic strategy engine, not a trading desk. It is built specifically for the C-suite "
        "and Chief Marketing Officers to audit structural enterprise asset risk. Media buyers measure individual "
        "twigs; CEOs use this index to see that their entire forest is on fire. If your enterprise allocates "
        "60% of its budget to a legacy channel that commands only 15% of your target workforce demographic's "
        "finite daily time budget, that is an enterprise failure. This scale is built to align "
        "multi-million-dollar corporate capital allocations with human reality, not to execute a local "
        "programmatic trade."
    )
    st.write("---")
    st.markdown(
        "<p style='font-size: 0.92rem; font-weight: bold; line-height: 1.5;'>Take The ECSAI for a test drive! "
        "Let us know what you think at <a href='mailto:info@eshap.tv' style='color: #007bff; text-decoration: underline; "
        "font-weight: bold;'>info@eshap.tv</a>.<br><br>And, please, don't forget to take some time to enjoy your day!"
        "<br><br>ESHAP</p>", 
        unsafe_allow_html=True
    )
with tab4:
    sub_method, sub_source = st.tabs(["Methodology Blueprint", "Sourcing Matrix"])
    is_global_view = (market_choice == "Global Overview")
    
    # EXPANDED BIBLICAL NO-BLEED TOKEN RESOLUTION REGISTRY
    token_dict = {
        "United States": "us", "France": "fr", "United Kingdom": "uk", 
        "Italy": "it", "Germany": "de", "Spain": "sp", "Brazil": "br", "Mexico": "mx",
        "Canada": "can", "India": "in", "Japan": "jp", "South Korea": "sk",
        "Denmark": "den", "Sweden": "swe", "Norway": "nor", "Finland": "fin",
        "Slovakia": "sv", "Slovenia": "sle", "Croatia": "cro", "Bulgaria": "bg",
        "Romania": "ro", "Moldova": "mol", "Czech Republic": "cr"
    }
    f_token = "us" if is_global_view else token_dict.get(market_choice, "us")
    
    with sub_method:
        st.markdown(f"### METHODOLOGY: CARTOGRAPHER'S BLUEPRINT ({flag_icon} {market_choice.upper()})")
        if not is_global_view:
            # COMPREHENSIVE BIBLICAL CENSUS WEIGHT MATRIX
            w_dict = {
                "United States": ("64.2%", "35.8%"), "France": ("65.1%", "34.9%"), "United Kingdom": ("63.8%", "36.2%"), 
                "Italy": ("59.8%", "40.2%"), "Germany": ("61.5%", "38.5%"), "Spain": ("62.0%", "38.0%"), 
                "Brazil": ("68.5%", "31.5%"), "Mexico": ("71.0%", "29.0%"), "Canada": ("66.4%", "33.6%"),
                "India": ("74.1%", "25.9%"), "Japan": ("54.3%", "45.7%"), "South Korea": ("58.9%", "41.1%"),
                "Denmark": ("61.0%", "39.0%"), "Sweden": ("60.5%", "39.5%"), "Norway": ("61.2%", "38.8%"),
                "Finland": ("59.1%", "40.9%"), "Slovakia": ("63.4%", "36.6%"), "Slovenia": ("60.8%", "39.2%"),
                "Croatia": ("62.1%", "37.9%"), "Bulgaria": ("58.4%", "41.6%"), "Romania": ("61.7%", "38.3%"),
                "Moldova": ("64.0%", "36.0%"), "Czech Republic": ("62.5%", "37.5%")
            }
            w1, w2 = w_dict.get(market_choice, ("64.2%", "35.8%"))
            st.markdown(f"**Territorial Demographic Weight:** {w1} is &le; 54 / {w2} is &ge; 55")
        
        # Inversion Bypass: Query RAM storage memory cache natively
        f_method_name = f"methodology_{f_token}.txt"
        methodology_text = load_text_asset(f_method_name)
        if len(methodology_text.strip()) > 0:
            st.write(methodology_text)
        else: 
            st.info(f"{market_choice} methodology text loading...")
            
    with sub_source:
        st.markdown(f"### DATA SOURCES ({flag_icon} {market_choice.upper()})")
        
        # Fixed File Naming Invariant Resolution
        f_source_name = f"sources_{f_token}.txt"
        if f_token == "mx": 
            f_source_name = "sources_orig_mx.txt"
            
        sources_text = load_text_asset(f_source_name)
        if len(sources_text.strip()) > 0:
            st.write(sources_text)
        else: 
            st.info(f"{market_choice} sourcing data loading...")
