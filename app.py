import streamlit as st
import pandas as pd
import base64, os, io

CORE_TOKENS = ["us", "fr", "uk", "it", "de", "sp", "br", "mx", "ca", "in", "jp", "kr", "denmark", "se", "no", "fi", "sk", "si", "hr", "bg", "ro", "md", "cz"]

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
    ["YOUTUBE", 1285.0, 145.0, 1140.0, 825.0, 665.0, 395.0],
    ["OTHER", 880.0, 15.0, 865.0, 710.0, 580.0, 420.0],
    ["NETFLIX", 1008.0, 98.0, 910.0, 780.0, 515.0, 235.0],
    ["INSTAGRAM", 683.0, 38.0, 645.0, 515.0, 435.0, 210.0],
    ["CBC", 585.0, 245.0, 340.0, 210.0, 125.0, 48.0],
    ["ROGERS", 525.0, 215.0, 310.0, 195.0, 110.0, 42.0],
    ["BELL MEDIA", 480.0, 195.0, 285.0, 175.0, 98.0, 35.0],
    ["CRAVE", 217.0, 42.0, 175.0, 130.0, 82.0, 31.0],
    ["AMAZON", 550.0, 65.0, 485.0, 380.0, 240.0, 115.0],
    ["CORUS", 255.0, 115.0, 140.0, 95.0, 55.0, 18.0],
    ["DISNEY", 347.0, 32.0, 315.0, 245.0, 160.0, 72.0],
    ["WBD (MAX)", 263.0, 28.0, 235.0, 180.0, 115.0, 50.0],
    ["FACEBOOK", 185.0, 75.0, 110.0, 72.0, 24.0, 4.0],
    ["TIKTOK", 645.0, 25.0, 620.0, 485.0, 395.0, 265.0]
]

IN_BASE = [
    ["YOUTUBE", 4275.0, 65.0, 4210.0, 3680.0, 3120.0, 2150.0],
    ["OTHER", 3425.0, 5.0, 3420.0, 3040.0, 2650.0, 1910.0],
    ["JIOSTAR", 2810.0, 465.0, 2345.0, 1890.0, 1340.0, 615.0],
    ["INSTAGRAM", 2032.0, 52.0, 1980.0, 1670.0, 1410.0, 925.0],
    ["NETFLIX", 1033.0, 48.0, 985.0, 810.0, 595.0, 260.0],
    ["ZEE ENTERTAINMENT", 730.0, 315.0, 415.0, 235.0, 125.0, 45.0],
    ["SONY PICTURES NETWORKS", 575.0, 245.0, 330.0, 195.0, 105.0, 38.0],
    ["DOORDARSHAN", 550.0, 385.0, 165.0, 95.0, 48.0, 14.0],
    ["SUN TV NETWORK", 450.0, 210.0, 240.0, 145.0, 78.0, 24.0],
    ["AMAZON", 677.0, 32.0, 645.0, 525.0, 390.0, 175.0],
    ["FACEBOOK", 435.0, 125.0, 310.0, 190.0, 95.0, 22.0],
    ["TIKTOK", 120.0, 2.0, 118.0, 95.0, 78.0, 45.0]
]
JP_BASE = [
    ["YOUTUBE", 1605.0, 485.0, 1120.0, 745.0, 525.0, 295.0],
    ["NHK", 1100.0, 585.0, 515.0, 315.0, 165.0, 68.0],
    ["TVER", 790.0, 145.0, 645.0, 490.0, 365.0, 195.0],
    ["NETFLIX", 635.0, 115.0, 520.0, 385.0, 240.0, 110.0],
    ["TIKTOK", 510.0, 25.0, 485.0, 340.0, 275.0, 185.0],
    ["NIPPON TV", 760.0, 395.0, 365.0, 225.0, 115.0, 42.0],
    ["FUJI MEDIA", 675.0, 365.0, 310.0, 195.0, 102.0, 35.0],
    ["TBS HOLDINGS", 625.0, 340.0, 285.0, 170.0, 88.0, 28.0],
    ["TV ASAHI", 555.0, 310.0, 245.0, 140.0, 72.0, 22.0],
    ["ABEMA", 427.0, 42.0, 385.0, 295.0, 210.0, 115.0],
    ["U-NEXT", 267.0, 52.0, 215.0, 155.0, 105.0, 48.0],
    ["AMAZON", 540.0, 95.0, 445.0, 340.0, 220.0, 98.0],
    ["DISNEY", 197.0, 32.0, 165.0, 125.0, 82.0, 35.0],
    ["WBD", 160.0, 25.0, 135.0, 105.0, 68.0, 24.0],
    ["FACEBOOK", 200.0, 115.0, 85.0, 52.0, 18.0, 2.0],
    ["OTHER", 415.0, 185.0, 230.0, 165.0, 110.0, 48.0]
]

KR_BASE = [
    ["YOUTUBE", 1395.0, 215.0, 1180.0, 815.0, 615.0, 385.0],
    ["NETFLIX", 710.0, 65.0, 645.0, 510.0, 340.0, 165.0],
    ["TIKTOK", 477.0, 12.0, 465.0, 340.0, 285.0, 195.0],
    ["KBS", 800.0, 385.0, 415.0, 245.0, 135.0, 52.0],
    ["MBC", 605.0, 295.0, 310.0, 185.0, 98.0, 35.0],
    ["SBS", 555.0, 260.0, 295.0, 170.0, 92.0, 31.0],
    ["CJENM", 430.0, 145.0, 285.0, 175.0, 110.0, 42.0],
    ["TVING", 387.0, 42.0, 345.0, 265.0, 195.0, 115.0],
    ["WAWVE", 325.0, 55.0, 270.0, 195.0, 130.0, 62.0],
    ["JTBC", 280.0, 115.0, 165.0, 105.0, 55.0, 18.0],
    ["AMAZON", 392.0, 32.0, 360.0, 280.0, 195.0, 85.0],
    ["DISNEY", 217.0, 22.0, 195.0, 150.0, 110.0, 48.0],
    ["WBD", 160.0, 15.0, 145.0, 115.0, 82.0, 32.0],
    ["FACEBOOK", 157.0, 92.0, 65.0, 40.0, 14.0, 1.0],
    ["OTHER", 310.0, 125.0, 185.0, 130.0, 95.0, 38.0]
]
DK_BASE = [
    ["YOUTUBE", 203.0, 38.0, 165.0, 115.0, 85.0, 52.0],
    ["DR", 220.0, 95.0, 125.0, 75.0, 42.0, 15.0],
    ["TV2 DANMARK", 150.0, 65.0, 85.0, 50.0, 28.0, 9.0],
    ["NETFLIX", 167.0, 22.0, 145.0, 115.0, 75.0, 35.0],
    ["TIKTOK", 129.0, 4.0, 125.0, 95.0, 78.0, 55.0],
    ["TV2 PLAY", 72.0, 12.0, 60.0, 45.0, 32.0, 14.0],
    ["VIAPLAY GROUP", 69.0, 15.0, 54.0, 40.0, 24.0, 10.0],
    ["AMAZON", 113.0, 18.0, 95.0, 75.0, 48.0, 18.0],
    ["DISNEY", 65.0, 10.0, 55.0, 40.0, 28.0, 12.0],
    ["WBD", 50.0, 8.0, 42.0, 32.0, 20.0, 8.0],
    ["FACEBOOK", 50.0, 28.0, 22.0, 14.0, 5.0, 0.5],
    ["OTHER", 88.0, 42.0, 46.0, 32.0, 22.0, 8.0]
]

SE_BASE = [
    ["YOUTUBE", 380.0, 65.0, 315.0, 225.0, 165.0, 98.0],
    ["SVT", 380.0, 165.0, 215.0, 135.0, 78.0, 28.0],
    ["TV4 MEDIA", 260.0, 115.0, 145.0, 90.0, 52.0, 18.0],
    ["NETFLIX", 323.0, 38.0, 285.0, 220.0, 145.0, 68.0],
    ["TIKTOK", 250.0, 5.0, 245.0, 185.0, 152.0, 110.0],
    ["VIAPLAY GROUP", 147.0, 22.0, 125.0, 95.0, 58.0, 22.0],
    ["AMAZON", 203.0, 28.0, 175.0, 135.0, 92.0, 38.0],
    ["DISNEY", 110.0, 15.0, 95.0, 75.0, 52.0, 22.0],
    ["WBD", 88.0, 12.0, 76.0, 58.0, 38.0, 15.0],
    ["FACEBOOK", 77.0, 42.0, 35.0, 22.0, 8.0, 1.0],
    ["OTHER", 145.0, 68.0, 77.0, 55.0, 38.0, 14.0]
]

NO_BASE = [
    ["YOUTUBE", 187.0, 42.0, 145.0, 105.0, 78.0, 48.0],
    ["NRK", 260.0, 125.0, 135.0, 85.0, 48.0, 18.0],
    ["TV2 NORGE", 177.0, 82.0, 95.0, 60.0, 35.0, 12.0],
    ["NETFLIX", 165.0, 25.0, 140.0, 110.0, 72.0, 32.0],
    ["TIKTOK", 139.0, 4.0, 135.0, 105.0, 88.0, 62.0],
    ["TV2 PLAY", 91.0, 15.0, 76.0, 58.0, 38.0, 15.0],
    ["VIAPLAY GROUP", 58.0, 10.0, 48.0, 36.0, 22.0, 8.0],
    ["AMAZON", 108.0, 18.0, 90.0, 70.0, 48.0, 18.0],
    ["DISNEY", 62.0, 10.0, 52.0, 40.0, 28.0, 12.0],
    ["WBD", 48.0, 8.0, 40.0, 31.0, 20.0, 8.0],
    ["FACEBOOK", 43.0, 25.0, 18.0, 11.0, 4.0, 0.2],
    ["OTHER", 78.0, 35.0, 43.0, 28.0, 18.0, 6.0]
]
FI_BASE = [
    ["YOUTUBE", 175.0, 40.0, 135.0, 98.0, 72.0, 44.0],
    ["YLE", 240.0, 118.0, 122.0, 78.0, 42.0, 14.0],
    ["MTV3", 145.0, 72.0, 63.0, 40.0, 22.0, 8.0],
    ["SANOMA", 115.0, 55.0, 60.0, 38.0, 20.0, 6.0],
    ["NETFLIX", 152.0, 22.0, 130.0, 102.0, 68.0, 30.0],
    ["TIKTOK", 124.0, 4.0, 120.0, 92.0, 76.0, 54.0],
    ["AMAZON", 98.0, 15.0, 80.0, 62.0, 42.0, 15.0],
    ["DISNEY", 58.0, 8.0, 50.0, 38.0, 25.0, 10.0],
    ["WBD", 44.0, 6.0, 38.0, 28.0, 18.0, 6.0],
    ["FACEBOOK", 40.0, 24.0, 16.0, 10.0, 3.0, 0.1],
    ["OTHER", 72.0, 32.0, 40.0, 25.0, 15.0, 5.0]
]

SK_BASE = [
    ["MARKIZA GROUP", 325.0, 145.0, 180.0, 115.0, 68.0, 24.0],
    ["YOUTUBE", 245.0, 48.0, 197.0, 142.0, 110.0, 68.0],
    ["JOJ GROUP", 215.0, 110.0, 105.0, 65.0, 38.0, 12.0],
    ["STVR", 195.0, 105.0, 90.0, 55.0, 28.0, 8.0],
    ["NETFLIX", 175.0, 25.0, 150.0, 118.0, 78.0, 35.0],
    ["TIKTOK", 168.0, 3.0, 165.0, 128.0, 110.0, 78.0],
    ["VOYO", 98.0, 18.0, 80.0, 58.0, 42.0, 18.0],
    ["AMAZON", 124.0, 15.0, 109.0, 85.0, 58.0, 22.0],
    ["DISNEY", 68.0, 8.0, 60.0, 45.0, 32.0, 12.0],
    ["WBD", 52.0, 6.0, 46.0, 35.0, 24.0, 8.0],
    ["FACEBOOK", 48.0, 26.0, 22.0, 14.0, 4.0, 0.2],
    ["OTHER", 82.0, 38.0, 44.0, 28.0, 18.0, 6.0]
]

SI_BASE = [
    ["PRO PLUS", 165.0, 72.0, 93.0, 58.0, 34.0, 12.0],
    ["YOUTUBE", 124.0, 22.0, 102.0, 74.0, 58.0, 35.0],
    ["RTVSLO", 115.0, 64.0, 51.0, 32.0, 15.0, 4.0],
    ["NETFLIX", 88.0, 12.0, 76.0, 60.0, 40.0, 18.0],
    ["TIKTOK", 86.0, 1.0, 85.0, 65.0, 55.0, 38.0],
    ["VOYO", 48.0, 8.0, 40.0, 28.0, 20.0, 8.0],
    ["AMAZON", 62.0, 8.0, 54.0, 42.0, 28.0, 10.0],
    ["DISNEY", 34.0, 4.0, 30.0, 22.0, 15.0, 6.0],
    ["WBD", 26.0, 3.0, 23.0, 18.0, 12.0, 4.0],
    ["FACEBOOK", 24.0, 14.0, 10.0, 6.0, 2.0, 0.1],
    ["OTHER", 42.0, 18.0, 24.0, 15.0, 10.0, 3.0]
]
HR_BASE = [
    ["NOVA TV CROATIA", 245.0, 112.0, 133.0, 85.0, 48.0, 15.0],
    ["YOUTUBE", 198.0, 35.0, 163.0, 118.0, 92.0, 55.0],
    ["RTL HRVATSKA", 175.0, 88.0, 87.0, 54.0, 30.0, 10.0],
    ["HRT", 168.0, 92.0, 76.0, 46.0, 24.0, 6.0],
    ["NETFLIX", 138.0, 18.0, 120.0, 95.0, 62.0, 26.0],
    ["TIKTOK", 136.0, 3.0, 133.0, 102.0, 88.0, 62.0],
    ["VOYO", 68.0, 10.0, 58.0, 42.0, 28.0, 12.0],
    ["AMAZON", 98.0, 12.0, 86.0, 68.0, 45.0, 15.0],
    ["DISNEY", 54.0, 6.0, 48.0, 35.0, 24.0, 9.0],
    ["WBD", 42.0, 5.0, 37.0, 28.0, 18.0, 6.0],
    ["FACEBOOK", 38.0, 22.0, 16.0, 10.0, 3.0, 0.1],
    ["OTHER", 64.0, 28.0, 36.0, 22.0, 14.0, 5.0]
]

BG_BASE = [
    ["BTV MEDIA GROUP", 415.0, 210.0, 205.0, 128.0, 72.0, 24.0],
    ["NOVA BROADCASTING", 385.0, 195.0, 190.0, 118.0, 65.0, 20.0],
    ["YOUTUBE", 310.0, 62.0, 248.0, 182.0, 142.0, 88.0],
    ["BNT", 230.0, 135.0, 95.0, 58.0, 28.0, 8.0],
    ["NETFLIX", 215.0, 28.0, 187.0, 146.0, 98.0, 42.0],
    ["TIKTOK", 212.0, 4.0, 208.0, 162.0, 138.0, 98.0],
    ["VOYO", 112.0, 18.0, 94.0, 68.0, 46.0, 18.0],
    ["AMAZON", 154.0, 18.0, 136.0, 106.0, 72.0, 25.0],
    ["DISNEY", 84.0, 10.0, 74.0, 55.0, 38.0, 14.0],
    ["WBD", 65.0, 8.0, 57.0, 44.0, 30.0, 10.0],
    ["FACEBOOK", 60.0, 34.0, 26.0, 16.0, 5.0, 0.2],
    ["OTHER", 98.0, 45.0, 53.0, 34.0, 22.0, 7.0]
]

RO_BASE = [
    ["PROTV", 1150.0, 520.0, 630.0, 395.0, 224.0, 74.0],
    ["ANTENA TV GROUP", 980.0, 465.0, 515.0, 320.0, 182.0, 58.0],
    ["YOUTUBE", 865.0, 145.0, 720.0, 524.0, 412.0, 254.0],
    ["TVR", 480.0, 265.0, 215.0, 130.0, 64.0, 18.0],
    ["NETFLIX", 610.0, 75.0, 535.0, 418.0, 278.0, 118.0],
    ["TIKTOK", 595.0, 12.0, 583.0, 452.0, 385.0, 274.0],
    ["ANTENAPLAY", 310.0, 48.0, 262.0, 192.0, 134.0, 52.0],
    ["AMAZON", 435.0, 52.0, 383.0, 298.0, 204.0, 72.0],
    ["DISNEY", 240.0, 28.0, 212.0, 158.0, 110.0, 42.0],
    ["WBD", 185.0, 22.0, 163.0, 124.0, 84.0, 28.0],
    ["FACEBOOK", 170.0, 95.0, 75.0, 46.0, 14.0, 0.8],
    ["OTHER", 280.0, 124.0, 156.0, 98.0, 62.0, 20.0]
]
MD_BASE = [
    ["PRIME TV MOLDOVA", 145.0, 68.0, 77.0, 48.0, 26.0, 8.0],
    ["YOUTUBE", 112.0, 15.0, 97.0, 72.0, 58.0, 36.0],
    ["JURNAL TV", 98.0, 46.0, 52.0, 31.0, 16.0, 4.0],
    ["M1", 85.0, 48.0, 37.0, 22.0, 10.0, 2.0],
    ["NETFLIX", 78.0, 8.0, 70.0, 55.0, 36.0, 15.0],
    ["TIKTOK", 76.0, 1.0, 75.0, 58.0, 48.0, 34.0],
    ["VOYO", 40.0, 5.0, 35.0, 25.0, 18.0, 6.0],
    ["AMAZON", 56.0, 6.0, 50.0, 38.0, 26.0, 9.0],
    ["DISNEY", 31.0, 3.0, 28.0, 20.0, 14.0, 5.0],
    ["WBD", 24.0, 2.0, 22.0, 16.0, 10.0, 3.0],
    ["FACEBOOK", 22.0, 12.0, 10.0, 6.0, 1.0, 0.0],
    ["OTHER", 36.0, 16.0, 20.0, 12.0, 8.0, 2.0]
]

CZ_BASE = [
    ["TV NOVA", 645.0, 295.0, 350.0, 222.0, 130.0, 46.0],
    ["YOUTUBE", 495.0, 98.0, 397.0, 286.0, 222.0, 138.0],
    ["PRIMA GROUP", 435.0, 220.0, 215.0, 134.0, 78.0, 24.0],
    ["CT", 395.0, 215.0, 180.0, 110.0, 56.0, 16.0],
    ["NETFLIX", 354.0, 52.0, 302.0, 238.0, 158.0, 72.0],
    ["TIKTOK", 340.0, 8.0, 332.0, 258.0, 222.0, 158.0],
    ["VOYO", 198.0, 35.0, 163.0, 118.0, 85.0, 36.0],
    ["AMAZON", 252.0, 32.0, 220.0, 172.0, 118.0, 45.0],
    ["DISNEY", 138.0, 15.0, 123.0, 92.0, 65.0, 24.0],
    ["WBD", 105.0, 12.0, 93.0, 70.0, 48.0, 16.0],
    ["FACEBOOK", 98.0, 54.0, 44.0, 28.0, 8.0, 0.4],
    ["OTHER", 165.0, 78.0, 87.0, 55.0, 36.0, 12.0]
]

bullet_base64 = ""
if os.path.exists("planet_bullet.png"):
    with open("planet_bullet.png", "rb") as b_f: bullet_base64 = base64.b64encode(b_f.read()).decode()
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
    with open("eshap_map.png", "rb") as img_f: logo_base64 = base64.b64encode(img_f.read()).decode()
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
    ["Global Overview", "United States", "Brazil", "Mexico", "Germany", "United Kingdom", "France", "Italy", "Spain", "Canada", "India", "Japan", "South Korea", "Denmark", "Sweden", "Norway", "Finland", "Slovakia", "Slovenia", "Croatia", "Bulgaria", "Romania", "Moldova", "Czech Republic"], 
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
elif market_choice == "South Korea": df_matrix = pd.DataFrame(KR_BASE, columns=cols)
elif market_choice == "Denmark": df_matrix = pd.DataFrame(DK_BASE, columns=cols)
elif market_choice == "Sweden": df_matrix = pd.DataFrame(SE_BASE, columns=cols)
elif market_choice == "Norway": df_matrix = pd.DataFrame(NO_BASE, columns=cols)
elif market_choice == "Finland": df_matrix = pd.DataFrame(FI_BASE, columns=cols)
elif market_choice == "Slovakia": df_matrix = pd.DataFrame(SK_BASE, columns=cols)
elif market_choice == "Slovenia": df_matrix = pd.DataFrame(SI_BASE, columns=cols)
elif market_choice == "Croatia": df_matrix = pd.DataFrame(HR_BASE, columns=cols)
elif market_choice == "Bulgaria": df_matrix = pd.DataFrame(BG_BASE, columns=cols)
elif market_choice == "Romania": df_matrix = pd.DataFrame(RO_BASE, columns=cols)
elif market_choice == "Moldova": df_matrix = pd.DataFrame(MD_BASE, columns=cols)
else: df_matrix = pd.DataFrame(CZ_BASE, columns=cols)
if df_matrix is not None:
    if merge_meta:
        meta_rows = df_matrix[df_matrix["Platform/Publisher"].isin(["INSTAGRAM", "FACEBOOK"])]
        non_meta_df = df_matrix[~df_matrix["Platform/Publisher"].isin(["INSTAGRAM", "FACEBOOK"])]
        if not meta_rows.empty:
            summed_vals = meta_rows[cols[1:]].sum().tolist()
            df_matrix
        st.markdown("Look at this chart.")
        st.markdown(
            "You can see the share of consumer attention, spread across all eight regions in The Index, for all "
            "people 13+. Note that the Local Legacy Media index is ALL local traditional Media from these "
            "eight regions, combined, and compared to the rest of the global players on the chart. Note also "
            "that for total attention, for all fourteen of the legacy media platforms across all eight regions, lose "
            "the battle for cross-screen attention to the global attention champ, YouTube."
        )
        st.markdown(
            "More importantly, this is total attention paid (not total people watching), for all people 13+ in "
            "these regions. When we ZOOM IN and look at how the majority of humans on earth, consumer media..."
        )
        
        if os.path.exists("global_index_13-54.png"):
            st.image("global_index_13-54.png", caption="CROSS-SCREEN ATTENTION INDEX - GLOBAL SHARE OF ATTENTION: P13-54 (DEC 2025 - MAY 2026)", use_container_width=True)
        else:
            st.warning("⚠️ `global_index_13-54.png` asset missing from repository folder.")
        st.markdown(
            "##### **Of all the data in this report, the most crucial datapoint is this: 82% of the world population — 73% of the people in these eight regions — are now under 54.**"
        )
        st.markdown(
            "This new index reveals that Legacy TV relies, almost entirely, on the shrinking minority of our "
            "most senior citizens watching the same stuff, over and over and over, throwing off the balance of "
            "measured video consumption. When you remove that dying demographic (of which I am, myself, "
            "solidly a member), the combined fourteen Legacy outlets in this index are surpassed — handily — "
            "by YouTube, Netflix, and TikTok."
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
            else: st.warning("⚠️ `us_index_13-34.png` missing from repository root.")
        with c2:
            if os.path.exists("us_index_13-24.png"): st.image("us_index_13-24.png", caption="US TOTAL ATTENTION: P13-24", use_container_width=True)
            else: st.warning("⚠️ `us_index_13-24.png` missing from repository root.")
        st.markdown(
            "And this, right here, is precisely why we need a Cross-Screen Index. No one else is measuring "
            "all these platforms, side by side, on all devices. So, the industry get easily distracted by flaccid "
            "signposts that tells us “YouTube is #1 on TV!” (with P2+ and without counting phones, laptops, "
            "or tablets)."
        )
        st.markdown(
            "Traditional currencies track the device canvas; they do not track the human. They count a "
            "television playing to a room as an absolute, while treating a high-intensity mobile session that "
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
        # Universal Global Flag Dictionary Map: Placed here to explicitly resolve any missing variable dropouts
        flag_icon = {
            "Global Overview": "🌐", "United States": "🇺🇸", "Germany": "🇩🇪", 
            "United Kingdom": "🇬🇧", "France": "🇫🇷", "Italy": "🇮🇹", 
            "Spain": "🇪🇸", "Brazil": "🇧🇷", "Mexico": "🇲🇽", "Canada": "🇨🇦",
            "India": "🇮🇳", "Japan": "🇯🇵", "South Korea": "🇰🇷", "Denmark": "🇩🇰",
            "Sweden": "🇸🇪", "Norway": "🇳🇴", "Finland": "🇫🇮", "Slovakia": "🇸🇰",
            "Slovenia": "🇸🇮", "Croatia": "🇭🇷", "Bulgaria": "🇧🇬", "Romania": "🇷🇴",
            "Moldova": "🇲🇩", "Czech Republic": "🇨🇿"
        }.get(market_choice, "🇺🇸")

        st.subheader(f"Cross-Screen Attention Tracker: {flag_icon} {market_choice}")
        st.markdown("#### Interactive Visual Share Map")
        st.markdown("<p style='font-size: 0.92rem; font-weight: bold; font-style: italic; color: #FF0000; margin-top: -0.5rem; margin-bottom: 0.75rem;'>MILLIONS OF HOURS</p>", unsafe_allow_html=True)
        
        st.html("<style>div[data-testid='stRadio'] > div { gap: 1.5rem !important; } div[data-testid='stRadio'] label p { font-size: 0.95rem !important; white-space: nowrap !important; }</style>")
        demo_columns = [col for col in df_matrix.columns if col != "Platform/Publisher"]
        selected_demo = st.radio("Select Demographic Cohort to Isolate in Bar Chart:", options=demo_columns, horizontal=True)
        
        chart_df = df_matrix.copy()
        chart_df["Platform/Publisher"] = chart_df["Platform/Publisher"].replace({"GROUPO RECORD": "RECORD"})
        chart_df_fixed = chart_df.set_index("Platform/Publisher")
        st.bar_chart(chart_df_fixed[[selected_demo]], horizontal=True, height=380, use_container_width=True, color="#FF0000")
            
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
            
        st.download_button(label="Export Current Ledger to CSV", data=df_matrix.to_csv(index=False).encode('utf-8'), file_name=f"ESHAP_CSAI_Ledger_{market_choice.replace(' ', '_')}_2026.csv", mime="text/csv", use_container_width=True)
# Flat Single-Line Initializer: Enforces zero leading spaces to make indentation crashes physically impossible
tab_labels = ["CSAI Interactive Index Matrix", "Why ECSAI?", "ECSAI FAQs", "Index Architecture & Methodology"]
tab1, tab2, tab3, tab4 = st.tabs(tab_labels)

with tab2:
    st.markdown("<div style='text-align: center; line-height: 0.95; margin-bottom: 1.5rem;'><h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold;'>WHY THE ECSAI?</h2><h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold; color: #FF0000;'>BECAUSE HUMAN ATTENTION IS FINITE.</h2><h2 style='margin: 0; padding: 0; font-size: 1.8rem; font-weight: bold;'>WE REALLY NEED TO TRACK IT THAT WAY.</h2></div>", unsafe_allow_html=True)
    st.markdown("Let's face the raw reality of modern media consumption: our entire multi-billion-dollar industry is navigating by a map that does not match the earth.")
    st.markdown("For years, the measurement establishment has relied on a self-serving mythology called \"premium attention quality\" to protect hyper-inflated television CPMs. They want you to believe that a 75-inch living room screen playing high-end drama possesses an inherent, elite cognitive impact. But look at what is actually happening under that roof. While the expensive television glass functions as background wallpaper to an empty sofa, the human being you are trying to reach is in the toilet, actively holding, scrolling, unmuting, and binging vertical video on a smartphone feed.")
    st.markdown("Traditional currencies track the device canvas; they do not track the human. They count a television playing to a room as an absolute hit, while treating a high-intensity mobile session that requires active thumb-and-eye engagement to exist as \"low-tier digital noise.\" This is a collective industry blindness. Legacy tracking systems want you to look at media through isolated reach silos—treating an open screen in an empty room as equal to an active, single-screen consumer focus.")
    st.markdown("When other industry signposts try to offer insight into this cross-screen crisis, they show up with a mallet rather than a magnifying glass. They aggregate soft consumer diaries, build clunky additive charts where the human daily clock magically stretches past 24 hours, or offer micro-level campaign widgets that count how many seconds an ad was technically \"on screen.\" They are handing you a shovel to look at individual twigs while your entire forest is burning to the ground.")
    st.markdown("<div style='text-align: center; line-height: 1.1; margin-top: 1rem; margin-bottom: 1.5rem;'><p style='color: #FF0000; font-weight: bold; margin: 0; font-size: 1.05rem;'>TO BE CLEAR:</p><p style='color: #FF0000; font-weight: bold; margin: 0; font-size: 1.05rem;'>THIS IS NOT A MEDIA BUYING MECHANISM.</p><p style='color: #FF0000; font-weight: bold; margin: 0; font-size: 1.05rem;'>IT'S A STRATEGIC AND FISCAL PLANNING COMPASS.</p></div>", unsafe_allow_html=True)
    st.markdown("The data is also clear: Since COVID and the arrival of TikTok, the phone has replaced the television as the center of video gravity. 60% of the world's video attention is now on mobile phones. If you are a media company and you are investing 100% of your budget on tv sets, you are mapping your course to irrelevancy and/or bankruptcy.")
    st.markdown("So much of our measurement investment is spent on measuring television viewing - even when the TV is not being watched! As a result, the Media Industrial complex spends a disproportionate amount of time, energy and resources fighting over control of a screen that ONLY captures 40% of video consumption. That's not just bad business; it's a suicide mission.")
    if os.path.exists("eshap_us_devices.png"): 
        st.image("eshap_us_devices.png", caption="Video Consumption Share By Device Ecosystem", use_container_width=True)
    else: 
        st.info("💡 *[Placeholder for eshap_us_devices.png: Video Consumption Share By Device Ecosystem]*")
        
    st.markdown("This real-world divergence isn't a theory; it is a measurable baseline. When tracking video share by device among US consumers, 59% of people point to their phone as the primary vehicle they use to watch video. Just 28% name the TV screen. When you pull back the demographic layers and look under the age of 55, this gap becomes a generational chasm. Two thirds of the video consumption by consumers under 55 is on smartphones, not TVs.")
    st.markdown("The ESHAP Cross-Screen Attention Index (ESCAI) introduces a completely new analytical paradigm to capture this shift. We didn't build a local programmatic tool to place an individual ad spot next Tuesday. To look at this index and ask how to execute a DSP trade is to confuse a compass with a shovel.")
    st.markdown("This scale is a macroeconomic strategy engine engineered for the C-suite to audit structural enterprise risk and investment. If your brand is allocating 60% of its capital to traditional glass viewing while our closed census time budget proves your active workforce demographic has permanently migrated its conscious time to a personal screen, that is an organizational asset failure.")
    st.markdown("ESCAI enforces the absolute laws of human physics. Human time is a non-elastic, zero-sum commodity—a closed market sponge. Every single hour gained by an algorithm is an hour permanently destroyed for a broadcast tower.")
    st.markdown("### THE ZERO-SUM SQUEEZE AND DIARY DE-DUPLICATION")
    st.markdown("This zero-sum squeeze is where the smooth, cross-screen blending actually happens. If we simply added the television hours to the digital hours, the market sponge would explode past the census ceiling due to concurrent multi-screening—a consumer scrolling on TikTok while the television plays a broadcast in the background. Our index model applies localized duplication coefficients derived from GWI Consumer Diaries and verified attention panels. These diaries track the exact percentage of a cohort that multi-screens daily (e.g., 77% of Gen Z in France).")
    st.markdown("The model uses this percentage to calculate a duplication discount factor. It treats human attention as a finite zero-sum resource: if the eye is looking at a smartphone screen, that fraction of time is physically subtracted from the traditional television glass volume. The digital hours (which require active, focused scrolling on a handheld device) are treated as hard, primary attention blocks. The background television glass hours are programmatically squeezed down until the entire multi-screen overlap is flattened and the duplication is erased. This prioritized single-screen eye focus is a primary reason background audio is not covered in this index.")
    st.markdown("### THE SEPARATION OF POWERS")
    st.markdown("To achieve this, the index operates on a strict Separation of Powers. We use a Sovereign Boundary Model where the hard quantitative ceilings are locked down entirely by currency-grade, hard telemetry logs (Nielsen, BARB, Médiamétrie, Comscore). The index does not ask consumers how many hours they watched; it uses codified telemetry to establish total volume.")
    st.markdown("Behavioral data from GWI Consumer Diaries is introduced strictly as a coefficient matrix to calculate the mathematical overlap when two devices are running in the same room. We use behavioral data solely to map the friction points where those macro volumes intersect. Legacy currencies rely on passive boxes in empty rooms, counting a television playing to an empty sofa as a hit. We use behavioral data to verify human presence and device co-activity, injecting human reality back into blind hardware metrics.")
    st.markdown("### PLEASE LOOK AT THE METHODOLOGY BLUEPRINTS AND SOURCE MATRICES FOR MORE DETAILS ON HOW WE BUILT THIS MODEL.")
    st.markdown("Perhaps the most important point for our industry: We didn't invent new numbers, and we didn't hide our math inside a proprietary black box. Every data point used to build this scale sits legitimately out in the open public domain, scattered across public broadcaster annual disclosures, investor relations filings, and sovereign regulatory white papers. Anyone could theoretically download these records and combine them to see the true division of human time for which they are competing. Until now, however, no one has.")
    st.markdown("Why? Because our industry incentivizes legacy silos. Because, among the most traditional of media and measurement experts, there is widespread fear of finding out how our consumers are actually spending their time and which half of their budgets are being wasted. The current system of content distribution and measurement is built by and for those who profit directly from it, whether or not it actually works.")
    st.markdown("We have built what we believe is the ultimate \"Attention Model,\" the first index to track the actual behavior of humans across all the screens they use and account for their attention in a way that helps us all map a course for the future of media.")
    st.markdown("We will update this index monthly, on a rolling six months basis. Simultaneously, we will drop analysis of the latest data on **[Media War & Peace](https://substack.com)**.")
    st.markdown("This is a FREE platform. This is a public project. We are VERY open to your feedback and critique and will continually strive to adapt and improve this product to meet the actual needs of the media community.")
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
    
    # 15-Market Token Registry Dictionary 
    token_dict = {
        "United States": "us", "France": "fr", "United Kingdom": "uk", "Italy": "it", "Germany": "de", 
        "Spain": "sp", "Brazil": "br", "Mexico": "mx", "Canada": "ca", "India": "in", "Japan": "jp", 
        "South Korea": "kr", "Denmark": "denmark", "Sweden": "se", "Norway": "no", "Finland": "fi", 
        "Slovakia": "sk", "Slovenia": "si", "Croatia": "hr", "Bulgaria": "bg", "Romania": "ro", 
        "Moldova": "md", "Czech Republic": "cz"
    }
    f_token = "us" if is_global_view else token_dict.get(market_choice, "us")
    # Dynamic Map Override: Instantiates a fallback mapping list flush-left to resolve variable exceptions
    local_flag_map = {
        "Global Overview": "🌐", "United States": "🇺🇸", "Germany": "🇩🇪", 
        "United Kingdom": "🇬🇧", "France": "🇫🇷", "Italy": "🇮🇹", 
        "Spain": "🇪🇸", "Brazil": "🇧🇷", "Mexico": "🇲🇽", "Canada": "🇨🇦",
        "India": "🇮🇳", "Japan": "🇯🇵", "South Korea": "🇰🇷", "Denmark": "🇩🇰",
        "Sweden": "🇸🇪", "Norway": "🇳🇴", "Finland": "🇫🇮", "Slovakia": "🇸🇰",
        "Slovenia": "🇸🇮", "Croatia": "🇭🇷", "Bulgaria": "🇧🇬", "Romania": "🇷🇴",
        "Moldova": "🇲🇩", "Czech Republic": "🇨🇿"
    }
    current_flag = local_flag_map.get(market_choice, "🇺🇸")

    with sub_method:
        st.markdown(f"### METHODOLOGY: CARTOGRAPHER'S BLUEPRINT ({current_flag} {market_choice.upper()})")
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
        if os.path.exists(f"methodology_{f_token}.txt"):
            with open(f"methodology_{f_token}.txt", "r", encoding="utf-8") as m_f: 
                st.write(m_f.read())
        else: 
            st.info(f"{market_choice} methodology blueprint text loading natively...")
            
    with sub_source:
        st.markdown(f"### DATA SOURCES ({current_flag} {market_choice.upper()})")
        if os.path.exists(f"sources_{f_token}.txt"):
            with open(f"sources_{f_token}.txt", "r", encoding="utf-8") as s_f: 
                st.write(s_f.read())
        else: 
            st.info(f"{market_choice} data sourcing index loading natively...")
