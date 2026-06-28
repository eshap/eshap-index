import streamlit as st
import pandas as pd
import base64
import os

# ==============================================================================
# 0. GLOBAL EMBEDDED METHODOLOGY AND DATA SOURCE COPY TEXTS
# ==============================================================================
METHODOLOGY_US = "Figures represent an exclusive Cross-Screen Attention Index generated via ESHAP analysis that models independent, platform-specific measurement panels into a singular, logic-enforced zero-sum market budget across televisions, smartphones, and computers. The baseline establishes total available time allocation parameters using U.S. Census Bureau headcounts and GWI daily consumer diaries, applying a duplication coefficient to filter out simultaneous multi-screening sessions so that concurrent device use is not double-counted. Television glass viewing shares from Nielsen’s Media Distributor Gauge and application session tracking from Comscore Mobile Metrix are collapsed back into their unified parent corporate holding structures (including all linear networks, direct-to-consumer streaming apps, and social feeds), with the final matrix subjected to a python-enforced mathematical filter that caps high-intensity platforms by age cohort size and guarantees strict downward monotonicity and exact demographic balance across all sub-tables. This data is from December 2025 through May 2026, and tracks all attention, including time spent watching video and consuming other social media."

METHODOLOGY_FR = "Figures represent an exclusive Cross-Screen Attention Index generated via ESHAP analysis that models independent, platform-specific measurement panels into a singular, logic-enforced zero-sum market budget across televisions, smartphones, and computers. The baseline establishes total available time allocation parameters using territorial population data from the Institut National de la Statistique et des Études Économiques (INSEE) and GWI daily consumer diaries, applying an empirical duplication coefficient to filter out simultaneous multi-screening sessions so that concurrent device use is not double-counted. Television glass viewing shares from Médiamétrie’s Médiamat and application session tracking from Sensor Tower France and data.ai Europe telemetry are collapsed back into their unified parent corporate holding structures (including all linear networks, direct-to-consumer streaming apps, and social feeds). To isolate the commercially vital workforce pool and eliminate legacy reach distortions, the index applies an unyielding zero-sum filter that strips the heavy 55+ demographic retirement layer directly out of the gen-pop baseline. The narrower, nested generational cohorts (13–44, 13–34, and 13–24) are then programmatically processed through a proprietary mathematical curve. This curve uses established transitional benchmarks to calculate historical territory lag and local market friction—such as state cultural subsidies and local content quotas—while automatically enforcing a nested safety guard that guarantees strict downward monotonicity across all sub-tables. This data covers the December 2025 through May 2026 cycle, tracking absolute volume of attention across both total video and active social media usage."

METHODOLOGY_UK = "Figures represent an exclusive Cross-Screen Attention Index generated via ESHAP analysis that models independent, platform-specific measurement panels into a singular, logic-enforced zero-sum market budget across televisions, smartphones, and computers. The baseline establishes total available time allocation parameters using Office for National Statistics (ONS) resident headcounts and GWI daily consumer diaries, applying an empirical duplication coefficient to filter out simultaneous multi-screening sessions so that concurrent device use is not double-counted. Television glass viewing shares from BARB (Broadcasters' Audience Research Board) monthly metrics and application session tracking from Sensor Tower UK and data.ai Europe telemetry are collapsed back into their unified parent corporate holding structures (including all linear networks, direct-to-consumer streaming apps, and social feeds). To isolate the commercially vital workforce pool and eliminate legacy reach distortions, the index applies an unyielding zero-sum filter that strips the heavy 55+ demographic retirement layer directly out of the gen-pop baseline. This data covers the December 2025 through May 2026 cycle, tracking absolute volume of attention across both total video and active social media usage."

METHODOLOGY_IT = "Figures represent an exclusive Cross-Screen Attention Index generated via ESHAP analysis that models independent, platform-specific measurement panels into a singular, logic-enforced zero-sum market budget across televisions, smartphones, and computers. The baseline establishes total available time allocation parameters using local demographic parameters and consumer telemetry diaries, applying an empirical duplication coefficient to filter out simultaneous multi-screening sessions so that concurrent device use is not double-counted. National network glass viewing shares and application telemetry session parameters are collapsed back into their unified parent holding structures, with the final matrix subjected to an unyielding zero-sum filter that strips the heavy 55+ demographic retirement layer directly out of the gen-pop baseline to isolate the high-intensity workforce pool."

SOURCES_US = "U.S. CENSUS BUREAU, GWI CONSUMER DIARIES, NIELSEN MEDIA DISTRIBUTOR GAUGE, COMSCORE MOBILE METRIX, SENSOR TOWER, DATA.AI, META INTERNAL AUDIENCE METRICS, ALPHABET INVESTOR RELATIONS, WALT DISNEY COMPANY FINANCIAL REPORTS, NETFLIX QUARTERLY EARNINGS, DENTSU & LUMEN ATTENTION ECONOMY PANELS"

SOURCES_FR = "MÉDIAMÉTRIE MÉDIAMAT, CENTRE NATIONAL DU CINÉMA ET DE L'IMAGE ANIMÉE (CNC), SENSOR TOWER FRANCE, DATA.AI EUROPE, META INTERNAL AUDIENCE DATA, GOOGLE INVESTOR RELATIONS, VIVENDI FINANCIAL REPORTS, INSTITUT NATIONAL DE LA STATISTIQUE ET DES ÉTUDES ÉCONOMIQUES (INSEE), U.S. CENSUS BUREAU, GWI CONSUMER DIARIES, DENTSU & LUMEN ATTENTION ECONOMY PANELS, EDISON RESEARCH CO-ACTIVE AUDIO TELEMETRY"

SOURCES_UK = "OFFICE FOR NATIONAL STATISTICS (ONS), GWI CONSUMER DIARIES, BARB (BROADCASTERS' AUDIENCE RESEARCH BOARD), SENSOR TOWER UK, DATA.AI EUROPE, COM_SCORE UK, META INTERNAL AUDIENCE DATA, ALPHABET INVESTOR RELATIONS, BBC ANNUAL REPORTS & ACCOUNTS, ITV PLC FINANCIAL RESULTS, DENTSU & LUMEN ATTENTION ECONOMY PANELS"

SOURCES_IT = "ISTITUTO NAZIONALE DI STATISTICA (ISTAT), GWI CONSUMER DIARIES, AUDITEL TELEMETRY DATA, SENSOR TOWER ITALY, DATA.AI EUROPE, META INTERNAL AUDIENCE METRICS, RAI ANNUAL REPORTS, MFE FINANCIAL STATEMENTS, WBD INVESTOR RELATIONS"

# ==============================================================================
# 1. PLATFORM INTERFACE & CONFIGURATION
# ==============================================================================
st.set_page_config(page_title="ESHAP CSAI Dashboard", layout="wide")

# Master Baseline Arrays mapping exactly to eshap_index_data.pdf
US_BASE = {
    "YOUTUBE": (2110.0, 490.0, 1620.0, 1134.0, 884.5, 539.5),
    "DISNEY": (1945.0, 1080.0, 865.0, 657.4, 447.0, 228.0),
    "NETFLIX": (1540.0, 380.0, 1160.0, 846.8, 533.5, 272.1),
    "TIKTOK": (1480.0, 65.0, 1415.0, 1103.7, 905.0, 660.7),
    "PARAMOUNT": (1290.0, 810.0, 480.0, 331.2, 195.4, 86.0),
    "NBCU": (1265.0, 795.0, 470.0, 319.6, 185.4, 76.0),
    "INSTAGRAM": (1120.0, 110.0, 1010.0, 878.7, 711.7, 391.4),
    "WBD": (1040.0, 685.0, 355.0, 241.4, 120.7, 50.7),
    "FACEBOOK": (995.0, 520.0, 475.0, 261.3, 96.7, 18.4),
    "AMAZON": (635.0, 215.0, 420.0, 344.4, 213.5, 89.7),
    "FOX": (425.0, 315.0, 110.0, 55.0, 24.8, 5.0)
}

FR_BASE = {
    "YOUTUBE": (485.0, 95.0, 390.0, 273.0, 212.9, 129.9),
    "TIKTOK": (335.0, 12.0, 323.0, 251.9, 206.6, 150.8),
    "NETFLIX": (390.0, 85.0, 305.0, 222.7, 140.3, 71.6),
    "INSTAGRAM": (215.0, 20.0, 195.0, 169.7, 137.5, 75.6),
    "TF1": (440.0, 270.0, 170.0, 136.0, 102.0, 51.8),
    "DISNEY": (180.0, 42.0, 138.0, 104.9, 66.1, 27.3),
    "FRANCE TV": (510.0, 385.0, 125.0, 102.5, 82.0, 54.2),
    "ARTE": (120.0, 57.6, 62.4, 48.0, 33.6, 10.1),
    "GROUP M6": (265.0, 145.0, 120.0, 93.6, 65.5, 29.5),
    "AMAZON": (155.0, 48.0, 107.0, 87.7, 54.4, 22.8),
    "WBD": (170.0, 95.0, 75.0, 54.8, 34.5, 14.3),
    "L'ÉQUIPE": (65.0, 19.5, 45.5, 33.7, 21.6, 8.9),
    "CANAL+ GROUP": (195.0, 115.0, 80.0, 58.4, 40.9, 13.9),
    "FACEBOOK": (165.0, 92.0, 73.0, 40.2, 14.9, 2.8),
    "DAZN": (20.0, 2.0, 18.0, 16.2, 12.8, 7.7)
}

UK_BASE = {
    "BBC": (640.0, 460.0, 180.0, 122.4, 85.7, 45.4),
    "YOUTUBE": (590.0, 110.0, 480.0, 336.0, 262.1, 159.9),
    "ITV": (510.0, 335.0, 175.0, 113.8, 75.1, 36.8),
    "NETFLIX": (495.0, 105.0, 390.0, 284.7, 179.4, 91.5),
    "TIKTOK": (410.0, 18.0, 392.0, 305.8, 250.7, 183.0),
    "SKY GROUP": (385.0, 210.0, 175.0, 119.0, 70.2, 28.8),
    "INSTAGRAM": (275.0, 28.0, 247.0, 214.9, 174.1, 95.8),
    "PARAMOUNT": (245.0, 155.0, 90.0, 61.2, 36.1, 14.8),
    "DISNEY": (235.0, 52.0, 183.0, 139.1, 87.6, 36.2),
    "WBD": (220.0, 128.0, 92.0, 62.6, 31.3, 13.1),
    "FACEBOOK": (210.0, 115.0, 95.0, 52.3, 19.3, 3.7),
    "AMAZON": (195.0, 62.0, 133.0, 109.1, 67.6, 28.4)
}

IT_BASE = {
    "Rai": (520.0, 415.0, 105.0, 80.9, 58.2, 37.2),
    "YOUTUBE": (440.0, 110.0, 330.0, 231.0, 180.2, 109.9),
    "MFE (Mediaset)": (415.0, 265.0, 150.0, 112.5, 81.0, 40.8),
    "TIKTOK": (295.0, 12.0, 283.0, 220.7, 181.0, 132.1),
    "NETFLIX": (310.0, 70.0, 240.0, 175.2, 110.4, 56.3),
    "INSTAGRAM": (250.0, 25.0, 225.0, 195.8, 158.6, 87.2),
    "SKY ITALIA": (175.0, 102.0, 73.0, 50.4, 29.7, 12.2),
    "DISNEY": (170.0, 38.0, 132.0, 100.3, 63.2, 26.1),
    "WBD": (165.0, 92.0, 73.0, 51.1, 31.7, 12.9),
    "FACEBOOK": (160.0, 101.0, 59.0, 32.5, 12.0, 2.3),
    "AMAZON": (140.0, 42.0, 98.0, 80.4, 49.8, 20.9)
}

if "reset_id" not in st.session_state:
