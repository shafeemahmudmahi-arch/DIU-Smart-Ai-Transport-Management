#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║      DIU Smart Transport Management System v2.0              ║
║      Daffodil International University                        ║
║      Full-Featured Demo — All Panels Included                ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import random
import os
import math
from datetime import datetime, timedelta, date
import time as time_module

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG  (must be the very first Streamlit call)
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="DIU Smart Transport",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════
CAMPUS_LAT   = 23.8892
CAMPUS_LNG   = 90.2743
COMMON_PASS  = "diu2025"
ADMIN_CREDS  = {"ADMIN001": "admin123", "ADMIN002": "admin123"}
DRIVER_PASS  = "driver123"

ROUTES = {
    "Mirpur-1":        {"code":"M1",  "color":"#0A84FF","endpoint_lat":23.7937,"endpoint_lng":90.3529,"bus_count":10,"stops":["Mirpur-1 Circle","Mirpur-2","Sheorapara","Gabtoli","Aminbazar","Ashulia","DIU Campus"],"dist_km":22},
    "Mirpur-10":       {"code":"M10", "color":"#30D158","endpoint_lat":23.8088,"endpoint_lng":90.3657,"bus_count":10,"stops":["Mirpur-10 Square","Mirpur-12","Pallabi","Gabtoli","Aminbazar","DIU Campus"],"dist_km":18},
    "Mirpur-Soniasi":  {"code":"MS",  "color":"#FF9F0A","endpoint_lat":23.8325,"endpoint_lng":90.3580,"bus_count":8, "stops":["Soniasi","Baunia","Kafrul","Gabtoli","Aminbazar","DIU Campus"],"dist_km":15},
    "Dhanmondi":       {"code":"D",   "color":"#FF375F","endpoint_lat":23.7461,"endpoint_lng":90.3742,"bus_count":10,"stops":["Dhanmondi-27","Dhanmondi-15","Kalyanpur","Gabtoli","Aminbazar","Ashulia","DIU Campus"],"dist_km":28},
    "Uttara":          {"code":"U",   "color":"#BF5AF2","endpoint_lat":23.8759,"endpoint_lng":90.3795,"bus_count":10,"stops":["Uttara Sector-7","Uttara Sector-3","Airport Road","Ashulia","DIU Campus"],"dist_km":16},
    "Savar":           {"code":"SA",  "color":"#FF6961","endpoint_lat":23.8573,"endpoint_lng":90.2673,"bus_count":8, "stops":["Savar Bazar","Hemayetpur","DIU Campus"],"dist_km":8},
    "Narayanganj":     {"code":"N",   "color":"#64D2FF","endpoint_lat":23.6238,"endpoint_lng":90.4995,"bus_count":10,"stops":["Narayanganj City","Fatullah","Demra","Jatrabari","Sayedabad","Gabtoli","DIU Campus"],"dist_km":45},
    "Farmgate":        {"code":"F",   "color":"#FFD60A","endpoint_lat":23.7578,"endpoint_lng":90.3889,"bus_count":10,"stops":["Farmgate","Tejgaon","Rayer Bazar","Mirpur Road","Gabtoli","Ashulia","DIU Campus"],"dist_km":26},
    "Sonargaon":       {"code":"SG",  "color":"#5AC8FA","endpoint_lat":23.6539,"endpoint_lng":90.4277,"bus_count":10,"stops":["Sonargaon","Meghna Ghat","Demra","Jatrabari","Sayedabad","Gabtoli","DIU Campus"],"dist_km":38},
}

DEPARTMENTS = [
    "CSE","SWE","EEE","English","CIS","Pharmacy","Management",
    "Media & Journalism","Law","Public Health","Agriculture Science",
    "Biochemistry","NME","NFE","Civil Engineering","Textile Engineering",
    "Mechanical Engineering","BBA","Entrepreneurship & Innovation",
]
DEPT_CODES = {d: str(i+1).zfill(2) for i, d in enumerate(DEPARTMENTS)}

ROUTE_PATHS = {
    "Mirpur-1":       [(23.7937,90.3529),(23.7960,90.3510),(23.8010,90.3470),(23.8060,90.3420),(23.8110,90.3360),(23.8200,90.3260),(23.8360,90.3140),(23.8530,90.3010),(23.8690,90.2900),(23.8892,90.2743)],
    "Mirpur-10":      [(23.8088,90.3657),(23.8105,90.3600),(23.8135,90.3530),(23.8165,90.3450),(23.8210,90.3350),(23.8330,90.3200),(23.8490,90.3060),(23.8660,90.2930),(23.8892,90.2743)],
    "Mirpur-Soniasi": [(23.8325,90.3580),(23.8355,90.3500),(23.8385,90.3400),(23.8415,90.3280),(23.8455,90.3150),(23.8540,90.3030),(23.8690,90.2900),(23.8892,90.2743)],
    "Dhanmondi":      [(23.7461,90.3742),(23.7530,90.3700),(23.7640,90.3650),(23.7770,90.3580),(23.7910,90.3480),(23.8060,90.3370),(23.8230,90.3230),(23.8440,90.3080),(23.8660,90.2930),(23.8892,90.2743)],
    "Uttara":         [(23.8759,90.3795),(23.8785,90.3720),(23.8805,90.3630),(23.8815,90.3510),(23.8825,90.3380),(23.8845,90.3220),(23.8865,90.3070),(23.8885,90.2920),(23.8892,90.2743)],
    "Savar":          [(23.8573,90.2673),(23.8645,90.2690),(23.8738,90.2715),(23.8825,90.2732),(23.8892,90.2743)],
    "Narayanganj":    [(23.6238,90.4995),(23.6460,90.4830),(23.6710,90.4630),(23.6960,90.4400),(23.7210,90.4200),(23.7460,90.4000),(23.7690,90.3780),(23.7910,90.3580),(23.8130,90.3380),(23.8390,90.3150),(23.8630,90.2980),(23.8892,90.2743)],
    "Farmgate":       [(23.7578,90.3889),(23.7650,90.3830),(23.7740,90.3760),(23.7870,90.3670),(23.8010,90.3560),(23.8170,90.3430),(23.8370,90.3270),(23.8580,90.3080),(23.8790,90.2920),(23.8892,90.2743)],
    "Sonargaon":      [(23.6539,90.4277),(23.6740,90.4120),(23.6960,90.3950),(23.7210,90.3780),(23.7490,90.3590),(23.7760,90.3410),(23.8060,90.3220),(23.8340,90.3050),(23.8630,90.2900),(23.8892,90.2743)],
}

FIRST_NAMES = [
    "Md.","Fatima","Abdullah","Nusrat","Rakibul","Tania","Rifat","Sumaiya","Tanvir","Sadia",
    "Mahmudul","Ayesha","Farhan","Sharmin","Sohan","Lamia","Mehedi","Bristy","Khalid","Raisa",
    "Zahidul","Fariha","Sabbir","Champa","Asif","Halima","Rashed","Israt","Mostafizur","Ashrafun",
    "Golam","Meherun","Ariful","Rabeya","Nazmul","Kaniz","Ziaur","Roksana","Shafiqul","Mahmuda",
    "Anisur","Kulsum","Habibur","Masuma","Monirul","Layla","Abul","Rehana","Wahidur","Sabina",
    "Imran","Tahmina","Enamul","Nazma","Arafat","Rima","Sadman","Nasrin","Mahbubur","Shamima",
    "Aminul","Khadija","Tariqul","Moriam","Shahed","Parveen","Mizanur","Dilruba","Kamrul","Sonia",
    "Liton","Taslima","Moniruzzaman","Bilkis","Shahriar","Ferdousi","Nazmul","Razia","Shuvo","Priya",
    "Raj","Anjali","Biplab","Sumana","Ratan","Mita","Mukul","Reshma","Habib","Sadia",
    "Anik","Jhorna","Jahangir","Surovi","Limon","Mousumi","Pavel","Sumona","Robin","Laboni",
]
LAST_NAMES = [
    "Rahman","Khatun","Hossain","Akter","Islam","Sultana","Ahmed","Begum","Hasan","Jahan",
    "Karim","Alam","Ali","Khan","Siddiqui","Chowdhury","Miah","Uddin","Parveen","Bhuiyan",
    "Mondol","Sarker","Talukder","Sikder","Howlader","Mandal","Das","Roy","Sharma","Devi",
    "Nesa","Billah","Rashid","Reza","Aziz","Salam","Molla","Sheikh","Majumder","Paul",
    "Ghosh","Sen","Biswas","Barua","Chakraborty","Dey","Nath","Banik","Podder","Halder",
]

DRIVER_NAMES = [
    "Kamal Hossain","Rahim Miah","Jabbar Ali","Salam Sheikh","Manik Mia","Forkan Uddin",
    "Bashir Ahmed","Razzak Molla","Harun Mia","Ismail Sheikh","Kader Ali","Mobin Mia",
    "Nasir Uddin","Omar Faruk","Parvez Ahmed","Quamrul Islam","Rafiqul Islam","Salim Khan",
    "Taher Mia","Usman Goni","Vashkar Das","Wahab Mia","Xipu Mia","Yunus Ali","Zahed Mia",
    "Abdul Hannan","Belal Hossain","Chandan Mia","Dulal Mia","Ekram Hossain",
    "Farid Mia","Gias Uddin","Helal Uddin","Idris Ali","Jamal Mia",
    "Khaled Hossain","Liaquat Ali","Mamun Mia","Naser Mia","Omar Ali",
    "Palash Mia","Quasem Ali","Rofiq Mia","Sultan Mia","Tuhin Mia",
    "Ujjal Biswas","Viku Mia","Wahidur Rahman","Ximan Mia","Yasin Mia",
]

# ═══════════════════════════════════════════════════════════════
# CSS  – White / Sky-Blue Glassmorphism Design
# ═══════════════════════════════════════════════════════════════
def apply_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

:root{
  --p:#0A84FF; --pd:#0066CC; --ps:#34AADC;
  --g:#30D158; --r:#FF3B30; --o:#FF9F0A; --pu:#BF5AF2;
  --y:#FFD60A;
  --bg1:linear-gradient(135deg,#EAF4FF 0%,#F5FBFF 40%,#E0F0FF 100%);
  --glass:rgba(255,255,255,0.88);
  --glass2:rgba(255,255,255,0.60);
  --gb:rgba(10,132,255,0.18);
  --t1:#0D1117; --t2:#444C56; --t3:#8B949E;
  --sh:0 8px 32px rgba(10,132,255,0.12);
  --sh2:0 20px 60px rgba(10,132,255,0.18);
  --r8:12px; --r16:18px; --r24:24px;
}

*{font-family:'Outfit',sans-serif;box-sizing:border-box}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:0 1.2rem 2rem!important;max-width:100%!important}
.main{background:var(--bg1);min-height:100vh}

/* ── scrollbar ─────────────────────────────────── */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#CBD5E1;border-radius:3px}

/* ── Glass card ─────────────────────────────────── */
.gc{
  background:var(--glass);
  backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);
  border:1.5px solid var(--gb);
  border-radius:var(--r16);
  padding:22px 24px;
  box-shadow:var(--sh);
  margin-bottom:14px;
  transition:transform .2s,box-shadow .2s;
}
.gc:hover{transform:translateY(-2px);box-shadow:var(--sh2)}

/* ── Metric card ─────────────────────────────────── */
.mc{
  background:var(--glass);
  border:1.5px solid var(--gb);
  border-radius:var(--r16);
  padding:18px 20px;
  display:flex;flex-direction:column;gap:6px;
  box-shadow:var(--sh);
  transition:all .2s;
  overflow:hidden;position:relative;
}
.mc::before{
  content:'';position:absolute;top:-30px;right:-30px;
  width:80px;height:80px;border-radius:50%;
  background:linear-gradient(135deg,rgba(10,132,255,.12),rgba(52,170,220,.08));
}
.mc:hover{transform:translateY(-3px);box-shadow:var(--sh2)}
.mc .label{font-size:11px;font-weight:600;color:var(--t3);letter-spacing:.8px;text-transform:uppercase}
.mc .value{font-size:28px;font-weight:800;color:var(--t1);line-height:1.1}
.mc .sub{font-size:12px;color:var(--t3)}
.mc .icon{font-size:28px;margin-bottom:6px}

/* ── Top header ─────────────────────────────────── */
.top-header{
  display:flex;align-items:center;justify-content:space-between;
  background:var(--glass);
  border:1.5px solid var(--gb);
  border-radius:var(--r24);
  padding:14px 28px;
  box-shadow:var(--sh);
  margin-bottom:18px;
  backdrop-filter:blur(24px);
}
.diu-brand{display:flex;align-items:center;gap:14px}
.diu-logo-box{
  background:linear-gradient(135deg,#0A84FF,#34AADC);
  border-radius:12px;width:48px;height:48px;
  display:flex;align-items:center;justify-content:center;
  font-size:22px;font-weight:900;color:#fff;
  box-shadow:0 4px 14px rgba(10,132,255,.4);
  flex-shrink:0;
}
.diu-title{font-size:15px;font-weight:700;color:var(--t1);line-height:1.2}
.diu-sub{font-size:11px;color:var(--t3);font-weight:500}
.hdr-right{display:flex;align-items:center;gap:12px}

/* ── Buttons ─────────────────────────────────── */
.btn-primary{
  background:linear-gradient(135deg,#0A84FF,#34AADC);
  color:#fff;border:none;border-radius:10px;
  padding:10px 22px;font-weight:600;font-size:13px;
  cursor:pointer;box-shadow:0 4px 14px rgba(10,132,255,.35);
  transition:all .2s;white-space:nowrap;
}
.btn-primary:hover{box-shadow:0 6px 20px rgba(10,132,255,.5);transform:translateY(-1px)}
.btn-danger{background:linear-gradient(135deg,#FF3B30,#FF6B6B);color:#fff;border:none;border-radius:10px;padding:10px 22px;font-weight:600;font-size:13px;cursor:pointer;box-shadow:0 4px 14px rgba(255,59,48,.35);transition:all .2s}
.btn-success{background:linear-gradient(135deg,#30D158,#34C759);color:#fff;border:none;border-radius:10px;padding:10px 22px;font-weight:600;font-size:13px;cursor:pointer;box-shadow:0 4px 14px rgba(48,209,88,.35)}
.btn-warning{background:linear-gradient(135deg,#FF9F0A,#FFB340);color:#fff;border:none;border-radius:10px;padding:10px 22px;font-weight:600;font-size:13px;cursor:pointer}

/* ── Badge ─────────────────────────────────── */
.badge{display:inline-block;border-radius:20px;padding:3px 10px;font-size:11px;font-weight:700;letter-spacing:.4px}
.badge-blue{background:rgba(10,132,255,.15);color:#0A84FF}
.badge-green{background:rgba(48,209,88,.15);color:#28A745}
.badge-red{background:rgba(255,59,48,.15);color:#FF3B30}
.badge-orange{background:rgba(255,159,10,.15);color:#CC7A00}
.badge-purple{background:rgba(191,90,242,.15);color:#BF5AF2}
.badge-gray{background:rgba(100,100,100,.12);color:#666}

/* ── Notification pill ─────────────────────────────────── */
.notif{
  background:rgba(10,132,255,.08);
  border:1px solid rgba(10,132,255,.2);
  border-radius:10px;padding:10px 14px;
  display:flex;align-items:flex-start;gap:10px;
  margin-bottom:8px;font-size:13px;
}
.notif.warn{background:rgba(255,159,10,.08);border-color:rgba(255,159,10,.25)}
.notif.danger{background:rgba(255,59,48,.08);border-color:rgba(255,59,48,.25)}
.notif.success{background:rgba(48,209,88,.08);border-color:rgba(48,209,88,.25)}

/* ── Bus card ─────────────────────────────────── */
.bus-card{
  background:var(--glass);border:1.5px solid var(--gb);
  border-radius:var(--r16);padding:14px 16px;
  margin-bottom:10px;
  display:flex;flex-direction:column;gap:6px;
  box-shadow:0 4px 16px rgba(10,132,255,.08);
  transition:all .2s;cursor:pointer;
}
.bus-card:hover{border-color:rgba(10,132,255,.5);box-shadow:0 8px 24px rgba(10,132,255,.18);transform:translateX(3px)}
.bus-number{font-size:16px;font-weight:800;color:var(--p)}
.bus-route{font-size:11px;color:var(--t3);font-weight:500}
.seat-bar-bg{background:#e9ecef;border-radius:6px;height:6px;overflow:hidden}
.seat-bar-fill{height:6px;border-radius:6px;transition:width .3s}

/* ── Section title ─────────────────────────────────── */
.sec-title{font-size:16px;font-weight:700;color:var(--t1);margin-bottom:12px;display:flex;align-items:center;gap:8px}

/* ── Login page ─────────────────────────────────── */
.login-wrapper{
  min-height:100vh;
  background:linear-gradient(135deg,#E0F0FF 0%,#F5FBFF 50%,#EAF4FF 100%);
  display:flex;align-items:center;justify-content:center;
}
.login-card{
  background:var(--glass);
  backdrop-filter:blur(32px);
  border:2px solid rgba(10,132,255,.2);
  border-radius:28px;
  padding:44px 40px;
  width:420px;
  box-shadow:0 32px 80px rgba(10,132,255,.20);
}

/* ── Progress bar ─────────────────────────────────── */
.prog-track{background:#e0e7ef;border-radius:8px;height:8px;overflow:hidden;margin:4px 0}
.prog-fill{height:8px;border-radius:8px}

/* ── Stat row in bus card ─────────────────────────────────── */
.bus-stats{display:flex;gap:10px;flex-wrap:wrap}
.bstat{display:flex;flex-direction:column;align-items:center;background:rgba(10,132,255,.06);border-radius:8px;padding:6px 10px;min-width:60px}
.bstat .bv{font-size:15px;font-weight:700;color:var(--t1)}
.bstat .bl{font-size:9px;color:var(--t3);font-weight:600;text-transform:uppercase;letter-spacing:.5px}

/* ── SOS button ─────────────────────────────────── */
.sos-btn{
  background:linear-gradient(135deg,#FF3B30,#FF6B6B);
  color:#fff;border-radius:20px;padding:22px;
  text-align:center;font-size:22px;font-weight:800;
  cursor:pointer;box-shadow:0 8px 28px rgba(255,59,48,.45);
  border:3px solid rgba(255,255,255,.4);
  transition:all .2s;letter-spacing:1px;
}
.sos-btn:hover{box-shadow:0 12px 36px rgba(255,59,48,.6);transform:scale(1.02)}

/* ── Access signal ─────────────────────────────────── */
.access-granted{background:rgba(48,209,88,.12);border:2px solid #30D158;border-radius:14px;padding:16px;text-align:center}
.access-denied{background:rgba(255,59,48,.12);border:2px solid #FF3B30;border-radius:14px;padding:16px;text-align:center}

/* ── Chatbot ─────────────────────────────────── */
.chat-bubble-user{background:linear-gradient(135deg,#0A84FF,#34AADC);color:#fff;border-radius:16px 16px 4px 16px;padding:10px 14px;font-size:13px;margin:4px 0;max-width:80%;margin-left:auto}
.chat-bubble-bot{background:#fff;border:1.5px solid var(--gb);color:var(--t1);border-radius:16px 16px 16px 4px;padding:10px 14px;font-size:13px;margin:4px 0;max-width:85%;box-shadow:0 2px 8px rgba(10,132,255,.08)}

/* ── streamlit overrides ─────────────────────────────────── */
.stSelectbox label,.stTextInput label,.stTextArea label{font-weight:600;color:var(--t2)!important;font-size:13px!important}
div[data-testid="stMetric"]{background:var(--glass);border:1.5px solid var(--gb);border-radius:14px;padding:16px!important;box-shadow:var(--sh)}
div[data-testid="stMetricValue"]>div{font-weight:800!important}
.stAlert{border-radius:12px!important}
div.stButton>button{background:linear-gradient(135deg,#0A84FF,#34AADC);color:#fff;border:none;border-radius:10px;font-weight:600;font-size:13px;padding:8px 20px;box-shadow:0 4px 14px rgba(10,132,255,.3);transition:all .2s}
div.stButton>button:hover{box-shadow:0 6px 20px rgba(10,132,255,.5);transform:translateY(-1px)}
.stTabs [data-baseweb="tab"]{font-weight:600;font-size:13px}
.stTabs [aria-selected="true"]{color:#0A84FF!important}
.stDataFrame{border-radius:12px!important;overflow:hidden}

/* ── Map container ─────────────────────────────────── */
.map-wrap{border-radius:var(--r16);overflow:hidden;border:1.5px solid var(--gb);box-shadow:var(--sh)}

/* ── Floating chatbot ─────────────────────────────────── */
.chat-fab{
  position:fixed;bottom:28px;right:28px;z-index:9999;
  background:linear-gradient(135deg,#0A84FF,#34AADC);
  border-radius:50%;width:56px;height:56px;
  display:flex;align-items:center;justify-content:center;
  font-size:24px;cursor:pointer;
  box-shadow:0 8px 24px rgba(10,132,255,.45);
  border:3px solid rgba(255,255,255,.5);
  transition:all .2s;
}

/* ── Admin grid ─────────────────────────────────── */
.admin-stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin-bottom:18px}
.astat{background:var(--glass);border:1.5px solid var(--gb);border-radius:var(--r16);padding:18px;box-shadow:var(--sh);text-align:center}
.astat .av{font-size:30px;font-weight:800;color:var(--p)}
.astat .al{font-size:11px;font-weight:600;color:var(--t3);letter-spacing:.6px;text-transform:uppercase}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# DATA GENERATION
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def generate_students():
    rng = random.Random(42)
    intakes = [("221","2022","Spring"),("222","2022","Fall"),("231","2023","Spring"),
               ("232","2023","Fall"),("241","2024","Spring"),("242","2024","Fall"),
               ("251","2025","Spring"),("252","2025","Fall")]
    route_list = list(ROUTES.keys())
    records, id_set = [], set()
    for i in range(500):
        intake = rng.choice(intakes)
        dept   = rng.choice(DEPARTMENTS)
        dc     = DEPT_CODES[dept]
        while True:
            serial = str(rng.randint(1,999)).zfill(3)
            fid    = f"{intake[0]}{dc}{serial}"
            if fid not in id_set:
                id_set.add(fid); break
        display_id = f"{intake[0]}-{dc}-{serial}"
        name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
        yr   = int(intake[1])
        sem  = min(12, (2025 - yr)*2 + rng.randint(1,2))
        route = rng.choice(route_list)
        gpa   = round(rng.uniform(2.4, 4.0), 2)
        records.append({
            "id": fid, "display_id": display_id, "name": name,
            "department": dept, "semester": sem,
            "intake": intake[1], "intake_season": intake[2],
            "route": route,
            "email": f"{fid}@diu.edu.bd",
            "phone": "01" + "".join([str(rng.randint(0,9)) for _ in range(9)]),
            "gpa": gpa, "status": "Active",
            "transport_pass": rng.random() > 0.05,
        })
    return pd.DataFrame(records)

@st.cache_data
def generate_buses():
    rng = random.Random(7)
    now   = datetime.now()
    buses = []
    bid   = 1
    for rname, rinfo in ROUTES.items():
        for i in range(rinfo["bus_count"]):
            bnum  = f"{rinfo['code']}/{str(i+1).zfill(2)}"
            seats = rng.choice([40,42,44,46,48,50])
            # Distribute statuses realistically
            roll  = rng.random()
            if roll < 0.60:
                status = "Running"
            elif roll < 0.75:
                status = "At Campus"
            elif roll < 0.88:
                status = "At Terminal"
            else:
                status = "Maintenance"

            progress = (rng.uniform(0.05,0.95) if status=="Running"
                        else (1.0 if status=="At Campus" else 0.0))
            occ      = (int(seats * rng.uniform(0.3,1.0)) if status=="Running"
                        else (rng.randint(0,5) if status=="At Campus" else 0))
            path     = ROUTE_PATHS[rname]
            lat, lng = interp(path, progress)
            speed    = (rng.randint(20,65) if status=="Running" else 0)
            dist_rem = (1 - progress) * rinfo["dist_km"]
            eta      = (int(dist_rem / max(speed,1) * 60) if status=="Running" else
                        (0 if status=="At Campus" else None))
            drv_num  = (bid - 1) % len(DRIVER_NAMES)
            drv_name = DRIVER_NAMES[drv_num]
            drv_id   = f"DRV{str(bid).zfill(3)}"
            dep_time = now - timedelta(minutes=int(progress * 70))
            buses.append({
                "bus_id":bid,"bus_number":bnum,"route":rname,"route_code":rinfo["code"],
                "color":rinfo["color"],"total_seats":seats,"occupied_seats":occ,
                "available_seats":max(0,seats-occ),"status":status,
                "progress":progress,"lat":lat,"lng":lng,"speed":speed,
                "eta_minutes":eta,"driver_id":drv_id,"driver_name":drv_name,
                "distance_km":rinfo["dist_km"],
                "departure_time":dep_time.strftime("%H:%M"),
            })
            bid += 1
    return pd.DataFrame(buses)

@st.cache_data
def generate_drivers():
    buses_df = generate_buses()
    driver_rows = []
    for _, b in buses_df.iterrows():
        trips_month = random.Random(hash(b["driver_id"])).randint(18,28)
        overspeed   = random.Random(hash(b["driver_id"])+"ov").randint(0,5)
        on_time_pct = round(random.Random(hash(b["driver_id"])+"ot").uniform(75,99),1)
        driver_rows.append({
            "driver_id":b["driver_id"],"name":b["driver_name"],
            "bus_number":b["bus_number"],"route":b["route"],
            "trips_this_month":trips_month,"overspeed_incidents":overspeed,
            "on_time_pct":on_time_pct,"status":b["status"],
            "license_no":f"DHA-{random.Random(hash(b['driver_id'])).randint(100000,999999)}",
            "experience_yrs":random.Random(hash(b["driver_id"])+"exp").randint(2,20),
        })
    return pd.DataFrame(driver_rows)

@st.cache_data
def generate_ride_history():
    """30-day history for 500 students × ~2 trips/day sample."""
    rng       = random.Random(99)
    students  = generate_students()
    buses_df  = generate_buses()
    records   = []
    today     = date.today()
    sample_s  = students.sample(200, random_state=99)
    for _, s in sample_s.iterrows():
        for d in range(30):
            ride_date = today - timedelta(days=d)
            for _ in range(rng.randint(0,2)):
                bus = buses_df.sample(1).iloc[0]
                records.append({
                    "student_id":s["id"],"student_name":s["name"],"route":s["route"],
                    "bus_number":bus["bus_number"],"driver":bus["driver_name"],
                    "date":ride_date.isoformat(),"time":f"{rng.randint(7,20):02d}:{rng.choice(['00','15','30','45'])}",
                    "direction":rng.choice(["To Campus","From Campus"]),
                    "fare":15,
                })
    return pd.DataFrame(records)

@st.cache_data
def generate_complaints():
    rng = random.Random(55)
    cats = ["AC Not Working","Overcrowding","Driver Behaviour","Late Arrival",
            "Bus Breakdown","Route Deviation","Cleanliness","Other"]
    students = generate_students()
    rows = []
    for i in range(60):
        s = students.sample(1, random_state=i).iloc[0]
        dt = datetime.now() - timedelta(days=rng.randint(0,29), hours=rng.randint(0,23))
        rows.append({
            "id":f"CMP{str(i+1).zfill(4)}","student_id":s["id"],"student_name":s["name"],
            "route":s["route"],"category":rng.choice(cats),
            "description":f"Issue reported regarding {rng.choice(cats).lower()} on bus.",
            "datetime":dt.strftime("%Y-%m-%d %H:%M"),
            "status":rng.choice(["Open","In Progress","Resolved","Resolved","Resolved"]),
            "priority":rng.choice(["High","Medium","Low","Low"]),
        })
    return pd.DataFrame(rows)

@st.cache_data
def generate_lost_found():
    rng   = random.Random(66)
    items = ["Water Bottle","Umbrella","Bag","Phone Charger","Books","Wallet","Headphones",
             "ID Card","Jacket","Laptop","Keys","Glasses","Lunch Box"]
    students = generate_students()
    rows = []
    for i in range(40):
        s  = students.sample(1, random_state=i+10).iloc[0]
        dt = datetime.now() - timedelta(days=rng.randint(0,30))
        rows.append({
            "id":f"LF{str(i+1).zfill(3)}","student_id":s["id"],"student_name":s["name"],
            "item":rng.choice(items),"route":s["route"],
            "date":dt.strftime("%Y-%m-%d"),"status":rng.choice(["Reported","Found","Claimed"]),
            "description":f"{rng.choice(items)} left on bus.",
        })
    return pd.DataFrame(rows)

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def interp(path, t):
    if len(path) == 1: return path[0]
    n  = len(path) - 1
    sp = t * n
    i  = min(int(sp), n-1)
    f  = sp - i
    la = path[i][0] + (path[i+1][0]-path[i][0])*f
    lo = path[i][1] + (path[i+1][1]-path[i][1])*f
    return la, lo

def get_occ_color(pct):
    if pct >= 0.9: return "#FF3B30"
    if pct >= 0.6: return "#FF9F0A"
    return "#30D158"

def fmt_eta(mins):
    if mins is None: return "—"
    if mins == 0:    return "At Campus"
    if mins < 60:    return f"{mins} min"
    return f"{mins//60}h {mins%60}m"

def seat_pct(row):
    return row["occupied_seats"]/row["total_seats"] if row["total_seats"]>0 else 0

def update_bus_positions(buses_df):
    """Simulate buses moving — shift progress slightly each call."""
    df = buses_df.copy()
    now_sec = int(time_module.time())
    for idx, row in df.iterrows():
        if row["status"] == "Running":
            delta = (now_sec % 600) / 600 * 0.15
            new_p = min(1.0, row["progress"] + delta * 0.01)
            la, lo = interp(ROUTE_PATHS[row["route"]], new_p)
            df.at[idx,"progress"] = new_p
            df.at[idx,"lat"]      = la
            df.at[idx,"lng"]      = lo
            dist_rem = (1 - new_p) * row["distance_km"]
            spd = max(row["speed"], 1)
            df.at[idx,"eta_minutes"] = int(dist_rem / spd * 60)
    return df

# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "page":"login","logged_in":False,"user_type":None,
        "user_id":None,"user_data":None,
        "chat_history":[],"booked_seats":{},
        "sos_alerts":[],"deploy_queue":[],
        "id_check_result":None,"id_check_input":"",
        "selected_route_student":None,"selected_route_admin":"All Routes",
        "admin_tab":0,"student_tab":0,
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k]=v

# ═══════════════════════════════════════════════════════════════
# MAP BUILDER
# ═══════════════════════════════════════════════════════════════
def build_map(buses_df, route_filter="All Routes", student_stop=None, height=420):
    center_lat, center_lng = 23.820, 90.330
    m = folium.Map(location=[center_lat, center_lng], zoom_start=11,
                   tiles="CartoDB positron", prefer_canvas=True)

    # Campus marker
    folium.Marker(
        [CAMPUS_LAT, CAMPUS_LNG],
        tooltip="🏫 DIU Campus",
        popup=folium.Popup("<b>Daffodil International University</b><br>Ashulia, Savar", max_width=200),
        icon=folium.Icon(color="red", icon="university", prefix="fa"),
    ).add_to(m)

    # Route path
    if route_filter != "All Routes" and route_filter in ROUTE_PATHS:
        path = ROUTE_PATHS[route_filter]
        color = ROUTES[route_filter]["color"]
        folium.PolyLine(path, color=color, weight=3.5, opacity=0.7, dash_array="6 4").add_to(m)
        # Terminal marker
        folium.Marker(
            path[0],
            tooltip=f"📍 {route_filter} Terminal",
            icon=folium.Icon(color="blue", icon="flag", prefix="fa"),
        ).add_to(m)

    # Student stop
    if student_stop:
        folium.CircleMarker(
            student_stop, radius=9, color="#0A84FF", fill=True,
            fill_color="#0A84FF", fill_opacity=0.85,
            tooltip="📍 Your Stop",
        ).add_to(m)

    # Bus markers
    subset = buses_df if route_filter=="All Routes" else buses_df[buses_df["route"]==route_filter]
    for _, b in subset.iterrows():
        if b["status"] not in ("Running","At Campus"): continue
        occ_pct = seat_pct(b)
        dot_col = get_occ_color(occ_pct)
        popup_html = f"""
        <div style="font-family:Outfit,sans-serif;min-width:170px;font-size:13px">
          <b style="color:#0A84FF;font-size:15px">🚌 {b['bus_number']}</b><br>
          <b>Route:</b> {b['route']}<br>
          <b>Seats:</b> {b['available_seats']}/{b['total_seats']} free<br>
          <b>Speed:</b> {b['speed']} km/h<br>
          <b>ETA Campus:</b> {fmt_eta(b['eta_minutes'])}<br>
          <b>Driver:</b> {b['driver_name']}<br>
          <b>Status:</b> {b['status']}
        </div>"""
        icon_html = f"""
        <div style="
          background:{b['color']};color:#fff;border-radius:8px;
          padding:3px 7px;font-size:10px;font-weight:800;
          white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,0.3);
          border:2px solid rgba(255,255,255,0.8);
          display:inline-flex;align-items:center;gap:3px;">
          🚌 {b['bus_number']}
        </div>"""
        folium.Marker(
            [b["lat"], b["lng"]],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"🚌 {b['bus_number']} | {b['available_seats']} seats | {fmt_eta(b['eta_minutes'])}",
            icon=folium.DivIcon(html=icon_html, icon_size=(90,26), icon_anchor=(45,13)),
        ).add_to(m)

    return m

# ═══════════════════════════════════════════════════════════════
# AI CHATBOT
# ═══════════════════════════════════════════════════════════════
def get_ai_response(user_msg, buses_df, student_route=None):
    """Try Anthropic API; fall back to rule-based replies."""
    api_key = os.environ.get("ANTHROPIC_API_KEY","")
    try:
        api_key = api_key or st.secrets.get("ANTHROPIC_API_KEY","")
    except Exception:
        pass

    if api_key:
        try:
            import anthropic
            running = buses_df[buses_df["status"]=="Running"]
            ctx = (
                f"DIU Smart Transport System. "
                f"Total buses: {len(buses_df)}. Running: {len(running)}. "
                f"Routes: {', '.join(ROUTES.keys())}. "
                f"Student route: {student_route or 'unknown'}. "
                f"Today: {datetime.now().strftime('%A, %d %B %Y %H:%M')}."
            )
            history = [{"role":m["role"],"content":m["content"]}
                       for m in st.session_state.chat_history[-6:]]
            history.append({"role":"user","content":user_msg})
            client = anthropic.Anthropic(api_key=api_key)
            resp = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=400,
                system=(f"You are the friendly DIU Smart Transport Assistant. "
                        f"Context: {ctx} "
                        f"Answer concisely in the same language the user writes (Bangla or English). "
                        f"Keep answers short and practical."),
                messages=history,
            )
            return resp.content[0].text
        except Exception:
            pass

    # ── Rule-based fallback ──────────────────────────────────
    ml = user_msg.lower()
    running = buses_df[buses_df["status"]=="Running"]
    if student_route:
        route_buses = buses_df[buses_df["route"]==student_route]
        route_run   = route_buses[route_buses["status"]=="Running"]
    else:
        route_buses = buses_df; route_run = running

    if any(w in ml for w in ["hello","hi","হ্যালো","আস্সালামু","salam"]):
        return "🚌 **Welcome to DIU Smart Transport!**\nI can help with bus locations, seat availability, schedules, routes, weather, lost & found, and more. What would you like to know?"
    if any(w in ml for w in ["bus","বাস","কয়টা","কতটি"]):
        avail = route_run["available_seats"].sum()
        return (f"**{student_route or 'All routes'} — Live status:**\n"
                f"• Running: **{len(route_run)}** buses\n"
                f"• Total available seats: **{avail}**\n"
                f"• Next arrival: ~{int(route_run['eta_minutes'].dropna().min()) if len(route_run)>0 else '—'} min")
    if any(w in ml for w in ["seat","সিট","খালি","available"]):
        top = route_run.nsmallest(3,"eta_minutes")[["bus_number","available_seats","eta_minutes"]]
        lines = "\n".join([f"• Bus **{r.bus_number}**: {r.available_seats} seats, ETA {fmt_eta(r.eta_minutes)}" for _,r in top.iterrows()])
        return f"**Available seats on your route:**\n{lines or 'No running buses right now.'}"
    if any(w in ml for w in ["eta","time","সময়","কত মিনিট","কখন"]):
        if len(route_run)>0:
            nxt = route_run.nsmallest(1,"eta_minutes").iloc[0]
            return f"⏱️ Next bus **{nxt['bus_number']}** arrives in approximately **{fmt_eta(nxt['eta_minutes'])}**."
        return "No buses currently running on your route. Check back shortly."
    if any(w in ml for w in ["route","রুট","রাস্তা"]):
        return ("**Available routes:**\n" +
                "\n".join([f"• **{rn}** ({ri['code']}) — {ri['bus_count']} buses, {ri['dist_km']} km" for rn,ri in ROUTES.items()]))
    if any(w in ml for w in ["weather","আবহাওয়া","rain","বৃষ্টি","গরম"]):
        opts = ["☀️ Sunny — great day to travel! All buses on schedule.",
                "🌤️ Partly cloudy — normal conditions. No delays expected.",
                "🌧️ Light rain — carry an umbrella. Minor delays possible."]
        return f"**Today's weather:** {random.choice(opts)}"
    if any(w in ml for w in ["jam","জ্যাম","traffic","ট্র্যাফিক","congestion"]):
        return ("🚦 **Traffic update:**\n"
                "• Gabtoli area: Moderate congestion (+10 min)\n"
                "• Mirpur-10 circle: Light traffic\n"
                "• Ashulia Road: Clear ✅\n"
                "AI recommends buses use alternative via Bypass Road.")
    if any(w in ml for w in ["sos","emergency","জরুরি","help","বিপদ"]):
        return "🚨 **Emergency:** Use the red SOS button in the Driver Panel. Transport Office: **01700-000000**. Campus Security: **01800-000000**."
    if any(w in ml for w in ["schedule","সময়সূচি","class","ক্লাস","routine"]):
        return ("📋 **Bus Schedule (Departure from terminals):**\n"
                "• Morning: 7:00 AM, 8:30 AM, 10:00 AM\n"
                "• Afternoon: 12:00 PM, 1:00 PM, 2:30 PM\n"
                "• Evening: 4:00 PM, 6:00 PM\n"
                "Buses depart campus 30 min after class end.")
    if any(w in ml for w in ["lost","হারানো","found","পাওয়া","item"]):
        return "🔍 **Lost & Found:** Use the **Lost & Found** tab in your dashboard to report a lost item. Include bus number, date, and description for faster recovery."
    if any(w in ml for w in ["book","বুকিং","reserve","সিট বুক","lock"]):
        return ("💺 **Seat Booking:** Go to the **Seat Booking** section.\n"
                "Select your route → choose bus → confirm booking. Your seat is held for 15 minutes.")
    if any(w in ml for w in ["fare","ভাড়া","cost","টাকা","price"]):
        return "💳 Transport fare: **৳15 per trip** (all routes). Paid via university transport card / student ID."
    if any(w in ml for w in ["driver","ড্রাইভার","চালক"]):
        return "👨‍✈️ All DIU bus drivers are licensed professionals. Rate your driver after your trip. Report issues via the Complaint section."
    if any(w in ml for w in ["contact","যোগাযোগ","number","নম্বর","phone"]):
        return ("📞 **Contacts:**\n• Transport Office: 01700-000000\n• Admin: 02-222264190\n• Emergency: 01800-000000\n• Email: transport@diu.edu.bd")
    return ("🤖 I can help with:\n"
            "• **Bus status & ETA** — \"next bus\"\n"
            "• **Seat availability** — \"seats on my route\"\n"
            "• **Traffic/weather** — \"any jams today\"\n"
            "• **Schedule** — \"bus schedule\"\n"
            "• **Lost & Found** — \"I lost my bag\"\n"
            "• **Fare & contacts** — \"how much is the fare\"\n\n"
            "Type your question anytime! 😊")

# ═══════════════════════════════════════════════════════════════
# LOGO COMPONENT
# ═══════════════════════════════════════════════════════════════
def diu_logo_html(size="normal"):
    fs = "16px" if size=="normal" else "12px"
    lb = "48px" if size=="normal" else "36px"
    return f"""
<div class="diu-brand">
  <div class="diu-logo-box" style="width:{lb};height:{lb};font-size:{'20px' if size=='normal' else '14px'}">🌼</div>
  <div>
    <div class="diu-title" style="font-size:{fs}">Daffodil International University</div>
    <div class="diu-sub">DIU Smart Transport Management System</div>
  </div>
</div>"""

# ═══════════════════════════════════════════════════════════════
# ████  LOGIN PAGE
# ═══════════════════════════════════════════════════════════════
def show_login():
    st.markdown("""
<div style="text-align:center;padding:32px 0 8px">
  <div style="display:inline-flex;align-items:center;gap:16px;justify-content:center;margin-bottom:8px">
    <div style="background:linear-gradient(135deg,#0A84FF,#34AADC);border-radius:18px;width:64px;height:64px;display:flex;align-items:center;justify-content:center;font-size:32px;box-shadow:0 8px 28px rgba(10,132,255,0.4)">🌼</div>
    <div style="text-align:left">
      <div style="font-size:22px;font-weight:800;color:#0D1117;line-height:1.1">Daffodil International University</div>
      <div style="font-size:13px;color:#0A84FF;font-weight:600;letter-spacing:.5px">DIU SMART TRANSPORT MANAGEMENT SYSTEM</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    c1,c2,c3 = st.columns([1,1.4,1])
    with c2:
        with st.container():
            st.markdown('<div class="gc">', unsafe_allow_html=True)
            user_type = st.selectbox("🔐 Login as", ["Student", "Admin / Management", "Bus Driver"],
                                     label_visibility="visible")
            user_id   = st.text_input("🪪 User ID", placeholder="Enter your ID...")
            password  = st.text_input("🔑 Password", type="password",
                                      placeholder="Enter password...")

            if st.button("Sign In →", use_container_width=True):
                students_df = generate_students()
                drivers_df  = generate_drivers()
                ok = False

                if user_type == "Student":
                    # Strip dashes for matching
                    clean_id = user_id.replace("-","")
                    match = students_df[students_df["id"]==clean_id]
                    if not match.empty and password == COMMON_PASS:
                        st.session_state.update({
                            "logged_in":True,"user_type":"student",
                            "user_id":clean_id,"user_data":match.iloc[0].to_dict(),
                            "page":"student","selected_route_student":match.iloc[0]["route"],
                        }); ok=True

                elif user_type == "Admin / Management":
                    if user_id in ADMIN_CREDS and password == ADMIN_CREDS[user_id]:
                        st.session_state.update({"logged_in":True,"user_type":"admin",
                            "user_id":user_id,"user_data":{"name":"Transport Admin","id":user_id},
                            "page":"admin"}); ok=True

                elif user_type == "Bus Driver":
                    match = drivers_df[drivers_df["driver_id"]==user_id]
                    if not match.empty and password == DRIVER_PASS:
                        st.session_state.update({"logged_in":True,"user_type":"driver",
                            "user_id":user_id,"user_data":match.iloc[0].to_dict(),
                            "page":"driver"}); ok=True

                if ok:
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")

            st.markdown("</div>", unsafe_allow_html=True)

        # Demo credentials
        with st.expander("📋 Demo Credentials"):
            buses_df = generate_buses()
            students_df = generate_students()
            s1 = students_df.iloc[0]
            d1 = buses_df.iloc[0]
            st.markdown(f"""
**Student:** ID `{s1['display_id']}` · Password `{COMMON_PASS}`

**Admin:** ID `ADMIN001` · Password `admin123`

**Driver:** ID `{d1['driver_id']}` · Password `{DRIVER_PASS}`
""")


# ═══════════════════════════════════════════════════════════════
# ████  STUDENT DASHBOARD
# ═══════════════════════════════════════════════════════════════
def show_student():
    apply_css()
    ud = st.session_state.user_data
    buses_df = update_bus_positions(generate_buses())
    students_df = generate_students()

    # ── Header ─────────────────────────────────────────────
    hc1, hc2, hc3 = st.columns([3,2,1])
    with hc1:
        st.markdown(diu_logo_html(), unsafe_allow_html=True)
    with hc2:
        st.markdown(f"""
<div style="text-align:center;padding:6px 0">
  <div style="font-size:13px;font-weight:700;color:#0A84FF">🎓 {ud['name']}</div>
  <div style="font-size:11px;color:#8B949E">{ud['display_id']} · {ud['department']} · Sem {ud['semester']}</div>
</div>""", unsafe_allow_html=True)
    with hc3:
        if st.button("🚪 Logout"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

    st.markdown("---")

    # ── Route selector ──────────────────────────────────────
    route_list = ["My Route: "+ud["route"]] + [r for r in ROUTES if r!=ud["route"]]
    sel_label  = st.selectbox("🗺️ Select Route to View", route_list, index=0)
    sel_route  = ud["route"] if sel_label.startswith("My Route") else sel_label
    st.session_state["selected_route_student"] = sel_route

    route_buses = buses_df[buses_df["route"]==sel_route]
    running_b   = route_buses[route_buses["status"]=="Running"]
    at_campus   = route_buses[route_buses["status"]=="At Campus"]
    at_terminal = route_buses[route_buses["status"].isin(["At Terminal","Maintenance"])]
    total_avail = running_b["available_seats"].sum()
    next_eta    = int(running_b["eta_minutes"].dropna().min()) if len(running_b)>0 else None

    # ── KPI Cards ──────────────────────────────────────────
    k1,k2,k3,k4,k5 = st.columns(5)
    with k1:
        st.markdown(f"""<div class="mc"><div class="icon">🚌</div><div class="label">Total Buses</div>
        <div class="value">{len(route_buses)}</div><div class="sub">{sel_route} route</div></div>""",
        unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="mc"><div class="icon">▶️</div><div class="label">In Transit</div>
        <div class="value" style="color:#30D158">{len(running_b)}</div><div class="sub">Currently running</div></div>""",
        unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="mc"><div class="icon">🏫</div><div class="label">At Campus</div>
        <div class="value" style="color:#0A84FF">{len(at_campus)}</div><div class="sub">Arrived</div></div>""",
        unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="mc"><div class="icon">💺</div><div class="label">Free Seats</div>
        <div class="value" style="color:#FF9F0A">{total_avail}</div><div class="sub">Across running buses</div></div>""",
        unsafe_allow_html=True)
    with k5:
        eta_str = f"{next_eta} min" if next_eta is not None else "—"
        st.markdown(f"""<div class="mc"><div class="icon">⏱️</div><div class="label">Next Arrival</div>
        <div class="value" style="color:#BF5AF2">{eta_str}</div><div class="sub">Estimated ETA</div></div>""",
        unsafe_allow_html=True)

    # ── Notifications ──────────────────────────────────────
    notifs = []
    if next_eta is not None and next_eta <= 5:
        notifs.append(("🔔","danger",f"Bus {running_b.nsmallest(1,'eta_minutes').iloc[0]['bus_number']} arriving in <b>{next_eta} min</b>! Be at your stop."))
    if total_avail < 10 and len(running_b)>0:
        notifs.append(("⚠️","warn","Seats filling up fast! Only <b>{}</b> seats left. Consider booking now.".format(total_avail)))
    notifs.append(("🌤️","","Weather: Partly cloudy. Normal travel conditions today."))
    notifs.append(("📢","","Next class schedule buses depart campus at 2:30 PM and 4:00 PM."))
    with st.expander(f"🔔 Notifications ({len(notifs)})", expanded=True):
        for em,tp,msg in notifs:
            st.markdown(f'<div class="notif {tp}">{em} <span>{msg}</span></div>', unsafe_allow_html=True)

    # ── Map + Bus List ──────────────────────────────────────
    map_col, list_col = st.columns([1.6, 1])

    with map_col:
        st.markdown('<div class="sec-title">🗺️ Live Bus Map</div>', unsafe_allow_html=True)
        stop_idx = ROUTES[sel_route]["stops"].index(ROUTES[sel_route]["stops"][1]) if len(ROUTES[sel_route]["stops"])>1 else 0
        student_stop_pos = ROUTE_PATHS[sel_route][1] if len(ROUTE_PATHS[sel_route])>1 else None
        m = build_map(buses_df, route_filter=sel_route, student_stop=student_stop_pos)
        st_folium(m, width=None, height=430, returned_objects=[])

    with list_col:
        st.markdown('<div class="sec-title">🚌 Buses on This Route</div>', unsafe_allow_html=True)
        for _, b in route_buses.sort_values("eta_minutes", na_position="last").iterrows():
            occ_pct = seat_pct(b)
            bar_w   = int(occ_pct*100)
            bar_c   = get_occ_color(occ_pct)
            st_badge = {"Running":"badge-green","At Campus":"badge-blue","At Terminal":"badge-orange","Maintenance":"badge-red"}.get(b["status"],"badge-gray")
            st.markdown(f"""
<div class="bus-card">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div>
      <div class="bus-number">{b['bus_number']}</div>
      <div class="bus-route">{b['route']} · {b['driver_name']}</div>
    </div>
    <span class="badge {st_badge}">{b['status']}</span>
  </div>
  <div class="bus-stats">
    <div class="bstat"><div class="bv">{b['available_seats']}</div><div class="bl">Free</div></div>
    <div class="bstat"><div class="bv">{b['total_seats']}</div><div class="bl">Total</div></div>
    <div class="bstat"><div class="bv">{fmt_eta(b['eta_minutes'])}</div><div class="bl">ETA</div></div>
    <div class="bstat"><div class="bv">{b['speed']}</div><div class="bl">km/h</div></div>
  </div>
  <div>
    <div style="font-size:10px;color:#8B949E;margin-bottom:3px">Occupancy: {int(occ_pct*100)}%</div>
    <div class="seat-bar-bg"><div class="seat-bar-fill" style="width:{bar_w}%;background:{bar_c}"></div></div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Tabs: Booking | Chatbot | History | Lost+Found | Complaints ──
    st.markdown("---")
    tabs = st.tabs(["💺 Seat Booking","🤖 AI Assistant","📋 Ride History","🔍 Lost & Found","📢 Complaints"])

    # ─ Tab 0: Seat Booking ──────────────────────────────────
    with tabs[0]:
        st.markdown("### 💺 Virtual Seat Booking (Mid-Route)")
        b1,b2 = st.columns(2)
        with b1:
            avail_buses = running_b[running_b["available_seats"]>0]
            if len(avail_buses)==0:
                st.warning("No buses with available seats on this route right now.")
            else:
                sel_bus = st.selectbox("Choose Bus",
                    avail_buses["bus_number"].tolist())
                sel_bus_row = avail_buses[avail_buses["bus_number"]==sel_bus].iloc[0]
                st.markdown(f"""
<div class="gc">
  <div class="sec-title">🚌 {sel_bus_row['bus_number']}</div>
  <div style="display:flex;gap:12px;flex-wrap:wrap">
    <div class="bstat"><div class="bv">{sel_bus_row['available_seats']}</div><div class="bl">Free Seats</div></div>
    <div class="bstat"><div class="bv">{fmt_eta(sel_bus_row['eta_minutes'])}</div><div class="bl">ETA to Campus</div></div>
    <div class="bstat"><div class="bv">{sel_bus_row['speed']}</div><div class="bl">km/h</div></div>
  </div>
  <div style="margin-top:12px;font-size:12px;color:#8B949E">Driver: {sel_bus_row['driver_name']}</div>
</div>""", unsafe_allow_html=True)
                num_seats = st.number_input("Seats to Book", 1, min(5, int(sel_bus_row["available_seats"])), 1)
                stop_pick = st.selectbox("Your Boarding Stop", ROUTES[sel_route]["stops"][:-1])
                if st.button("🔒 Lock My Seat(s)", use_container_width=True):
                    bid = int(sel_bus_row["bus_id"])
                    if bid not in st.session_state.booked_seats:
                        st.session_state.booked_seats[bid]=[]
                    st.session_state.booked_seats[bid].append({
                        "student_id":ud["id"],"student_name":ud["name"],
                        "seats":int(num_seats),"stop":stop_pick,
                        "time":datetime.now().strftime("%H:%M"),
                    })
                    st.success(f"✅ {num_seats} seat(s) booked on bus {sel_bus}! "
                               f"Driver notified. Your seat is held for 15 minutes.")
        with b2:
            st.markdown("#### Your Active Bookings")
            found_any=False
            for bid,blist in st.session_state.booked_seats.items():
                for bk in blist:
                    if bk["student_id"]==ud["id"]:
                        found_any=True
                        bus_row = buses_df[buses_df["bus_id"]==bid]
                        bnum = bus_row.iloc[0]["bus_number"] if len(bus_row)>0 else f"Bus {bid}"
                        st.markdown(f"""
<div class="gc">
  <div style="font-weight:700;color:#0A84FF">🚌 {bnum}</div>
  <div style="font-size:12px;color:#444">Seats: {bk['seats']} · Stop: {bk['stop']} · Booked: {bk['time']}</div>
  <span class="badge badge-green">✅ Confirmed</span>
</div>""", unsafe_allow_html=True)
            if not found_any:
                st.info("No active bookings. Book a seat from the left panel.")

    # ─ Tab 1: AI Chatbot ───────────────────────────────────
    with tabs[1]:
        st.markdown("### 🤖 DIU Smart Transport Assistant")
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"]=="user":
                    st.markdown(f'<div style="display:flex;justify-content:flex-end;margin:6px 0"><div class="chat-bubble-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="display:flex;justify-content:flex-start;margin:6px 0"><span style="margin-right:6px">🤖</span><div class="chat-bubble-bot">{msg["content"]}</div></div>', unsafe_allow_html=True)

        prompt = st.chat_input("Ask anything about buses, routes, seats, schedule...")
        if prompt:
            st.session_state.chat_history.append({"role":"user","content":prompt})
            with st.spinner("Thinking..."):
                reply = get_ai_response(prompt, buses_df, ud["route"])
            st.session_state.chat_history.append({"role":"assistant","content":reply})
            st.rerun()

        # Quick queries
        st.markdown("**Quick queries:**")
        qcols = st.columns(4)
        quick_qs = ["Next bus ETA?","Seat availability","Today's schedule","Any traffic jams?"]
        for i, (qc, qq) in enumerate(zip(qcols, quick_qs)):
            with qc:
                if st.button(qq, key=f"qq_{i}"):
                    st.session_state.chat_history.append({"role":"user","content":qq})
                    reply = get_ai_response(qq, buses_df, ud["route"])
                    st.session_state.chat_history.append({"role":"assistant","content":reply})
                    st.rerun()

    # ─ Tab 2: Ride History ─────────────────────────────────
    with tabs[2]:
        st.markdown("### 📋 My Ride History (Last 30 Days)")
        history_df = generate_ride_history()
        my_hist = history_df[history_df["student_id"]==ud["id"]].sort_values("date", ascending=False)
        if len(my_hist)>0:
            st.dataframe(my_hist[["date","time","direction","route","bus_number","driver","fare"]].rename(columns={
                "date":"Date","time":"Time","direction":"Direction",
                "route":"Route","bus_number":"Bus","driver":"Driver","fare":"Fare (৳)"}),
                use_container_width=True, hide_index=True)
            total_fare = my_hist["fare"].sum()
            total_trips = len(my_hist)
            h1,h2 = st.columns(2)
            h1.metric("Total Trips (30 days)", total_trips)
            h2.metric("Total Fare", f"৳{total_fare}")
        else:
            st.info("No ride history yet. Your trips will appear here after your first journey.")

    # ─ Tab 3: Lost & Found ────────────────────────────────
    with tabs[3]:
        lf_col1, lf_col2 = st.columns(2)
        with lf_col1:
            st.markdown("### 🔍 Report Lost Item")
            with st.form("lf_form"):
                lf_item  = st.text_input("Item Name")
                lf_bus   = st.selectbox("Bus (if known)", ["Not Sure"] + buses_df["bus_number"].tolist())
                lf_route = st.selectbox("Route", list(ROUTES.keys()), index=list(ROUTES.keys()).index(ud["route"]))
                lf_date  = st.date_input("Date Lost", date.today())
                lf_desc  = st.text_area("Description", placeholder="Color, size, or any identifiable features...")
                if st.form_submit_button("📤 Submit Report", use_container_width=True):
                    st.success(f"✅ Lost item report submitted! Report ID: LF{random.randint(100,999)}. "
                               f"You'll be notified if found.")
        with lf_col2:
            st.markdown("### 📋 Current Lost & Found Items")
            lf_df = generate_lost_found()
            for _, lf in lf_df.head(8).iterrows():
                color = {"Reported":"#FF9F0A","Found":"#30D158","Claimed":"#0A84FF"}.get(lf["status"],"gray")
                st.markdown(f"""
<div class="gc" style="padding:12px 16px">
  <div style="display:flex;justify-content:space-between">
    <b>{lf['item']}</b>
    <span class="badge" style="background:{color}22;color:{color}">{lf['status']}</span>
  </div>
  <div style="font-size:11px;color:#8B949E">Route: {lf['route']} · Date: {lf['date']}</div>
</div>""", unsafe_allow_html=True)

    # ─ Tab 4: Complaints ──────────────────────────────────
    with tabs[4]:
        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown("### 📢 Submit a Complaint")
            with st.form("complaint_form"):
                cmp_cat  = st.selectbox("Category", ["AC Not Working","Overcrowding","Driver Behaviour",
                                                       "Late Arrival","Bus Breakdown","Route Deviation",
                                                       "Cleanliness","Other"])
                cmp_bus  = st.selectbox("Bus (if applicable)", ["Not Sure"]+buses_df["bus_number"].tolist())
                cmp_desc = st.text_area("Describe the issue", placeholder="Please provide details...")
                cmp_prio = st.radio("Priority", ["Low","Medium","High"], horizontal=True)
                if st.form_submit_button("📤 Submit Complaint", use_container_width=True):
                    cid = f"CMP{random.randint(1000,9999)}"
                    st.success(f"✅ Complaint submitted! Ticket ID: **{cid}**. Admin will respond within 24 hours.")
        with cc2:
            st.markdown("### 📋 My Previous Complaints")
            comp_df = generate_complaints()
            my_comp = comp_df[comp_df["student_id"]==ud["id"]]
            if len(my_comp)>0:
                for _,c in my_comp.iterrows():
                    sc = {"Open":"badge-red","In Progress":"badge-orange","Resolved":"badge-green"}.get(c["status"],"badge-gray")
                    st.markdown(f"""
<div class="gc" style="padding:12px 16px">
  <div style="display:flex;justify-content:space-between">
    <b>{c['category']}</b><span class="badge {sc}">{c['status']}</span>
  </div>
  <div style="font-size:11px;color:#8B949E">{c['datetime']} · Priority: {c['priority']}</div>
</div>""", unsafe_allow_html=True)
            else:
                st.info("No complaints submitted. We hope your experience has been smooth! 😊")


# ═══════════════════════════════════════════════════════════════
# ████  ADMIN DASHBOARD
# ═══════════════════════════════════════════════════════════════
def show_admin():
    apply_css()
    buses_df    = update_bus_positions(generate_buses())
    students_df = generate_students()
    drivers_df  = generate_drivers()
    comp_df     = generate_complaints()
    lf_df       = generate_lost_found()

    # ── Header ──────────────────────────────────────────────
    hc1,hc2,hc3 = st.columns([3,2,1])
    with hc1: st.markdown(diu_logo_html(), unsafe_allow_html=True)
    with hc2:
        st.markdown('<div style="text-align:center;padding:6px 0"><div style="font-size:14px;font-weight:700;color:#FF375F">⚙️ Admin Control Centre</div><div style="font-size:11px;color:#8B949E">Transport Management Dashboard</div></div>', unsafe_allow_html=True)
    with hc3:
        if st.button("🚪 Logout"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

    st.markdown("---")

    # ── KPI Row ─────────────────────────────────────────────
    total_buses   = len(buses_df)
    running_buses = len(buses_df[buses_df["status"]=="Running"])
    total_stu     = len(students_df)
    sos_count     = len(st.session_state.sos_alerts)
    open_comp     = len(comp_df[comp_df["status"]=="Open"])
    active_routes = buses_df[buses_df["status"]=="Running"]["route"].nunique()

    a1,a2,a3,a4,a5,a6 = st.columns(6)
    for col,icon,label,val,c in [
        (a1,"🚌","Total Fleet",total_buses,"#0A84FF"),
        (a2,"▶️","Running Now",running_buses,"#30D158"),
        (a3,"🎓","Students",total_stu,"#BF5AF2"),
        (a4,"🗺️","Active Routes",active_routes,"#FF9F0A"),
        (a5,"📢","Open Tickets",open_comp,"#FF3B30"),
        (a6,"🚨","SOS Alerts",sos_count,"#FF3B30"),
    ]:
        with col:
            st.markdown(f"""<div class="mc"><div class="icon">{icon}</div>
            <div class="label">{label}</div><div class="value" style="color:{c}">{val}</div></div>""",
            unsafe_allow_html=True)

    # ── SOS Alert Banner ────────────────────────────────────
    if st.session_state.sos_alerts:
        for alert in st.session_state.sos_alerts:
            st.error(f"🚨 **SOS ALERT** — Bus {alert['bus']}, Route {alert['route']}: {alert['msg']} | {alert['time']}")

    # ── Main Tabs ───────────────────────────────────────────
    tabs = st.tabs(["🗺️ Fleet Monitor","📊 AI Analytics","🚀 Deploy Control",
                    "👨‍✈️ Drivers","📢 Tickets","💳 Access & Revenue","📋 Reports"])

    # ─ Tab 0: Fleet Monitor ─────────────────────────────────
    with tabs[0]:
        fc1, fc2 = st.columns([1.8,1])
        with fc1:
            st.markdown("### 🗺️ Live Fleet Map — All Buses")
            route_filter_admin = st.selectbox("Filter by Route", ["All Routes"]+list(ROUTES.keys()))
            m = build_map(buses_df, route_filter=route_filter_admin)
            st_folium(m, width=None, height=500, returned_objects=[])
        with fc2:
            st.markdown("### 📋 Fleet Status")
            for rname in ROUTES:
                rb = buses_df[buses_df["route"]==rname]
                run_n = len(rb[rb["status"]=="Running"])
                avail = rb[rb["status"]=="Running"]["available_seats"].sum()
                load  = int((rb[rb["status"]=="Running"]["occupied_seats"].sum() /
                             max(rb[rb["status"]=="Running"]["total_seats"].sum(),1))*100)
                bar_c = get_occ_color(load/100)
                st.markdown(f"""
<div class="gc" style="padding:12px 16px;margin-bottom:8px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
    <div><b style="color:{ROUTES[rname]['color']}">{ROUTES[rname]['code']}</b> <span style="font-size:12px">{rname}</span></div>
    <div style="font-size:11px;color:#8B949E">{run_n}/{len(rb)} running · {avail} seats free</div>
  </div>
  <div class="prog-track"><div class="prog-fill" style="width:{load}%;background:{bar_c}"></div></div>
  <div style="font-size:10px;color:#8B949E;margin-top:2px">Load: {load}%</div>
</div>""", unsafe_allow_html=True)

    # ─ Tab 1: AI Analytics ──────────────────────────────────
    with tabs[1]:
        st.markdown("### 📊 AI-Powered Transport Analytics")
        an1, an2 = st.columns(2)

        with an1:
            # Buses per route chart
            route_data = []
            for rname, rinfo in ROUTES.items():
                rb = buses_df[buses_df["route"]==rname]
                run_n = len(rb[rb["status"]=="Running"])
                route_data.append({"Route":rinfo["code"],"Running":run_n,
                                   "Total":rinfo["bus_count"],"Idle":rinfo["bus_count"]-run_n})
            rdf = pd.DataFrame(route_data)
            fig = go.Figure()
            fig.add_bar(x=rdf["Route"],y=rdf["Running"],name="Running",marker_color="#30D158")
            fig.add_bar(x=rdf["Route"],y=rdf["Idle"],name="Idle",marker_color="#E0E7EF")
            fig.update_layout(barmode="stack",title="Buses per Route",
                              plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                              legend=dict(orientation="h"),height=300,
                              margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig, use_container_width=True)

        with an2:
            # Occupancy donut
            run_b = buses_df[buses_df["status"]=="Running"]
            total_occ = run_b["occupied_seats"].sum()
            total_free= run_b["available_seats"].sum()
            fig2 = go.Figure(go.Pie(
                labels=["Occupied","Available"],values=[total_occ,total_free],
                hole=0.6,marker=dict(colors=["#0A84FF","#E0F0FF"]),
                textinfo="percent",showlegend=True,
            ))
            fig2.update_layout(title="Overall Seat Utilization",height=300,
                               paper_bgcolor="rgba(0,0,0,0)",
                               margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig2, use_container_width=True)

        an3, an4 = st.columns(2)
        with an3:
            # Hourly demand prediction
            hours = list(range(7,21))
            demand = [40,90,70,60,80,95,75,60,85,90,70,55,40,30]
            fig3 = go.Figure()
            fig3.add_scatter(x=hours,y=demand,fill="tozeroy",
                             line=dict(color="#0A84FF",width=2.5),
                             fillcolor="rgba(10,132,255,0.12)",name="Demand")
            fig3.update_layout(title="AI Hourly Demand Prediction (Today)",
                               xaxis_title="Hour",yaxis_title="Student Count",
                               plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                               height=280,margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig3, use_container_width=True)

        with an4:
            # Satisfaction by route
            rts  = list(ROUTES.keys())
            sats = [round(random.uniform(72,97),1) for _ in rts]
            fig4 = go.Figure(go.Bar(
                x=[ROUTES[r]["code"] for r in rts], y=sats,
                marker=dict(color=sats, colorscale="Blues",showscale=False),
                text=[f"{s}%" for s in sats], textposition="auto",
            ))
            fig4.update_layout(title="Student Satisfaction by Route (%)",
                               plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                               height=280,margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig4, use_container_width=True)

        # AI text suggestions
        st.markdown("### 🤖 AI Recommendations for Today")
        ai_recs = [
            ("🟡","High","Dhanmondi route needs 2 backup buses for the 4:00 PM rush. Current load: 89%."),
            ("🟢","Normal","Savar route is well-covered. 8 buses, 42% average load."),
            ("🔴","Urgent","Narayanganj route — Bus N/07 reported slow speed. Check engine status."),
            ("🟡","High","Uttara route students increasing. Recommend adding 1 bus for morning 8:30 AM slot."),
            ("🟢","Normal","Farmgate route on-time performance: 94%. No changes needed."),
        ]
        for icon,prio,msg in ai_recs:
            c = {"Urgent":"danger","High":"warn","Normal":"success"}.get(prio,"")
            st.markdown(f'<div class="notif {c}">{icon} <b>[{prio}]</b> {msg}</div>', unsafe_allow_html=True)

    # ─ Tab 2: Deploy Control ────────────────────────────────
    with tabs[2]:
        st.markdown("### 🚀 Bus Deployment Control")
        st.info("ℹ️ AI suggests deployments below. Review and click **Deploy** to confirm. Nothing is automatic.")

        deploy_suggestions = [
            {"route":"Dhanmondi","suggestion":"Add 2 buses (D/11, D/12 from backup)","reason":"89% load, 4PM rush","priority":"High"},
            {"route":"Uttara","suggestion":"Add 1 bus (U/11 from backup)","reason":"Morning 8:30 AM demand spike","priority":"Medium"},
            {"route":"Narayanganj","suggestion":"Replace N/07 — engine alert","reason":"Driver SOS pre-warning","priority":"Urgent"},
            {"route":"Mirpur-1","suggestion":"Redeploy M1/08 to Mirpur-10 route","reason":"Mirpur-10 overloaded","priority":"Medium"},
        ]

        for ds in deploy_suggestions:
            pc  = {"Urgent":"#FF3B30","High":"#FF9F0A","Medium":"#0A84FF"}.get(ds["priority"],"gray")
            dc1,dc2,dc3 = st.columns([3,1.5,1])
            with dc1:
                st.markdown(f"""
<div class="gc" style="padding:14px 18px">
  <div style="display:flex;align-items:center;gap:10px">
    <span class="badge" style="background:{pc}22;color:{pc}">{ds['priority']}</span>
    <b>{ds['route']}</b>
  </div>
  <div style="font-size:13px;margin-top:6px;color:#444">{ds['suggestion']}</div>
  <div style="font-size:11px;color:#8B949E;margin-top:3px">Reason: {ds['reason']}</div>
</div>""", unsafe_allow_html=True)
            with dc2: st.write("")
            with dc3:
                if st.button(f"✅ Deploy", key=f"dep_{ds['route']}"):
                    st.session_state.deploy_queue.append({
                        "route":ds["route"],"action":ds["suggestion"],"time":datetime.now().strftime("%H:%M")})
                    st.success(f"Deployed for {ds['route']}!")

        if st.session_state.deploy_queue:
            st.markdown("#### ✅ Recent Deployments")
            for d in st.session_state.deploy_queue[-5:]:
                st.markdown(f'<div class="notif success">✅ [{d["time"]}] <b>{d["route"]}</b>: {d["action"]}</div>', unsafe_allow_html=True)

        # Manual deploy
        st.markdown("#### 🔧 Manual Deployment")
        mc1,mc2,mc3 = st.columns(3)
        with mc1:
            m_route = st.selectbox("Route",list(ROUTES.keys()),key="manual_route")
        with mc2:
            m_action = st.selectbox("Action",["Add Bus","Remove Bus","Reroute Bus","Emergency Replace"])
        with mc3:
            st.write("")
            if st.button("⚡ Execute Deployment", use_container_width=True):
                st.session_state.deploy_queue.append({
                    "route":m_route,"action":m_action,"time":datetime.now().strftime("%H:%M")})
                st.success(f"Manual deployment executed for {m_route}!")

    # ─ Tab 3: Drivers ────────────────────────────────────────
    with tabs[3]:
        st.markdown("### 👨‍✈️ Driver Performance Dashboard")
        dr1, dr2 = st.columns([1.5,1])
        with dr1:
            sel_route_drv = st.selectbox("Filter Route", ["All"]+list(ROUTES.keys()), key="drv_route")
            show_drv = drivers_df if sel_route_drv=="All" else drivers_df[drivers_df["route"]==sel_route_drv]
            sel_bus_drv   = st.selectbox("Select Bus", show_drv["bus_number"].tolist())
            drv_row = show_drv[show_drv["bus_number"]==sel_bus_drv].iloc[0]
            on_time_c = "#30D158" if drv_row["on_time_pct"]>=90 else ("#FF9F0A" if drv_row["on_time_pct"]>=75 else "#FF3B30")
            st.markdown(f"""
<div class="gc">
  <div style="font-size:18px;font-weight:800;color:#0A84FF;margin-bottom:10px">👨‍✈️ {drv_row['name']}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
    <div class="bstat"><div class="bv">{drv_row['driver_id']}</div><div class="bl">Driver ID</div></div>
    <div class="bstat"><div class="bv">{drv_row['bus_number']}</div><div class="bl">Bus</div></div>
    <div class="bstat"><div class="bv">{drv_row['trips_this_month']}</div><div class="bl">Trips (Month)</div></div>
    <div class="bstat"><div class="bv" style="color:{on_time_c}">{drv_row['on_time_pct']}%</div><div class="bl">On-Time</div></div>
    <div class="bstat"><div class="bv" style="color:{'#FF3B30' if drv_row['overspeed_incidents']>2 else '#30D158'}">{drv_row['overspeed_incidents']}</div><div class="bl">Overspeed</div></div>
    <div class="bstat"><div class="bv">{drv_row['experience_yrs']}yr</div><div class="bl">Experience</div></div>
  </div>
  <div style="margin-top:10px">
    <div style="font-size:11px;color:#8B949E;margin-bottom:3px">On-Time Rate</div>
    <div class="prog-track"><div class="prog-fill" style="width:{drv_row['on_time_pct']}%;background:{on_time_c}"></div></div>
  </div>
  <div style="margin-top:10px;font-size:12px;color:#8B949E">
    Route: {drv_row['route']} · License: {drv_row['license_no']} · Status: {drv_row['status']}
  </div>
</div>""", unsafe_allow_html=True)
        with dr2:
            st.markdown("#### Performance Overview — All Drivers")
            on_time_dist = pd.cut(drivers_df["on_time_pct"],
                bins=[0,70,80,90,101], labels=["<70%","70-80%","80-90%",">90%"])
            ot_counts = on_time_dist.value_counts().reset_index()
            ot_counts.columns = ["Range","Count"]
            fig_d = px.bar(ot_counts, x="Range", y="Count",
                color_discrete_sequence=["#0A84FF"],
                title="On-Time Performance Distribution")
            fig_d.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",height=260,margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig_d, use_container_width=True)

            top_drivers = drivers_df.nlargest(5,"on_time_pct")[["name","bus_number","on_time_pct","trips_this_month"]]
            st.markdown("#### 🏆 Top 5 Drivers")
            st.dataframe(top_drivers.rename(columns={"name":"Driver","bus_number":"Bus",
                "on_time_pct":"On-Time%","trips_this_month":"Trips"}),
                use_container_width=True, hide_index=True)

    # ─ Tab 4: Tickets (Complaints) ───────────────────────────
    with tabs[4]:
        st.markdown("### 📢 Student Complaints & Tickets")
        tc1,tc2 = st.columns([2,1])
        with tc1:
            status_filter = st.multiselect("Filter by Status",["Open","In Progress","Resolved"],default=["Open","In Progress"])
            show_comp = comp_df[comp_df["status"].isin(status_filter)] if status_filter else comp_df
            for _,c in show_comp.head(15).iterrows():
                sc = {"Open":"badge-red","In Progress":"badge-orange","Resolved":"badge-green"}.get(c["status"],"badge-gray")
                pc = {"High":"#FF3B30","Medium":"#FF9F0A","Low":"#30D158"}.get(c["priority"],"gray")
                st.markdown(f"""
<div class="gc" style="padding:12px 16px;margin-bottom:8px">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div><b>{c['category']}</b> <span style="color:#8B949E;font-size:11px">· {c['id']}</span></div>
    <div style="display:flex;gap:6px"><span class="badge" style="background:{pc}22;color:{pc}">{c['priority']}</span><span class="badge {sc}">{c['status']}</span></div>
  </div>
  <div style="font-size:12px;color:#444;margin-top:4px">{c['description']}</div>
  <div style="font-size:11px;color:#8B949E;margin-top:3px">Student: {c['student_name']} · Route: {c['route']} · {c['datetime']}</div>
</div>""", unsafe_allow_html=True)
        with tc2:
            st.markdown("#### Ticket Statistics")
            stat_counts = comp_df["status"].value_counts().reset_index()
            stat_counts.columns = ["Status","Count"]
            fig_t = px.pie(stat_counts, values="Count", names="Status",
                color_discrete_map={"Open":"#FF3B30","In Progress":"#FF9F0A","Resolved":"#30D158"},
                title="Complaint Status")
            fig_t.update_layout(paper_bgcolor="rgba(0,0,0,0)",height=250,margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig_t, use_container_width=True)

            cat_counts = comp_df["category"].value_counts().reset_index()
            cat_counts.columns = ["Category","Count"]
            fig_cat = px.bar(cat_counts, x="Count", y="Category", orientation="h",
                color_discrete_sequence=["#0A84FF"],title="By Category")
            fig_cat.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                height=250,margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig_cat, use_container_width=True)

    # ─ Tab 5: Access & Revenue ───────────────────────────────
    with tabs[5]:
        st.markdown("### 💳 Smart Access & Revenue Audit")
        rev1,rev2 = st.columns(2)
        with rev1:
            total_pass     = int(students_df["transport_pass"].sum())
            no_pass        = len(students_df) - total_pass
            today_trips    = len(generate_ride_history()[generate_ride_history()["date"]==date.today().isoformat()])
            revenue_today  = today_trips * 15
            st.metric("Students with Transport Pass", total_pass)
            st.metric("Unauthorized / No Pass", no_pass)
            st.metric("Today's Trips (Est.)", today_trips)
            st.metric("Today's Revenue", f"৳{revenue_today}")

            # Route usage
            route_usage = students_df["route"].value_counts().reset_index()
            route_usage.columns = ["Route","Students"]
            fig_ru = px.bar(route_usage, x="Students", y="Route", orientation="h",
                color_discrete_sequence=["#0A84FF"],title="Students per Route")
            fig_ru.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                height=320,margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig_ru, use_container_width=True)
        with rev2:
            fig_pass = go.Figure(go.Pie(
                labels=["Transport Pass","No Pass"],
                values=[total_pass,no_pass],
                hole=0.55,
                marker=dict(colors=["#30D158","#FF3B30"]),
                textinfo="percent+label",
            ))
            fig_pass.update_layout(title="Transport Pass Coverage",
                paper_bgcolor="rgba(0,0,0,0)",height=280,margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig_pass, use_container_width=True)

            dept_usage = students_df["department"].value_counts().head(10).reset_index()
            dept_usage.columns = ["Dept","Count"]
            fig_dept = px.bar(dept_usage,x="Count",y="Dept",orientation="h",
                color_discrete_sequence=["#BF5AF2"],title="Top Departments Using Transport")
            fig_dept.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                height=300,margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig_dept, use_container_width=True)

    # ─ Tab 6: Reports ────────────────────────────────────────
    with tabs[6]:
        st.markdown("### 📋 System Reports")
        rr1,rr2 = st.columns(2)
        with rr1:
            # Daily trend (last 7 days)
            days  = [(date.today()-timedelta(days=i)).strftime("%a %d") for i in range(6,-1,-1)]
            trips = [random.randint(380,520) for _ in days]
            fig_tr = go.Figure()
            fig_tr.add_scatter(x=days,y=trips,mode="lines+markers",
                line=dict(color="#0A84FF",width=2.5),
                marker=dict(size=7,color="#0A84FF"),
                fill="tozeroy",fillcolor="rgba(10,132,255,0.08)",
                name="Daily Trips")
            fig_tr.update_layout(title="Daily Trip Volume (Last 7 Days)",
                plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                height=280,margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig_tr, use_container_width=True)

            # On-time performance
            on_time_pct_overall = round(drivers_df["on_time_pct"].mean(), 1)
            avg_speed = round(buses_df[buses_df["status"]=="Running"]["speed"].mean(), 1)
            r1,r2,r3 = st.columns(3)
            r1.metric("Avg On-Time Rate", f"{on_time_pct_overall}%")
            r2.metric("Avg Speed", f"{avg_speed} km/h")
            r3.metric("Fleet Availability", f"{int(running_buses/total_buses*100)}%")

        with rr2:
            # Lost & found trend
            lf_status = lf_df["status"].value_counts().reset_index()
            lf_status.columns = ["Status","Count"]
            fig_lf = px.pie(lf_status, values="Count", names="Status",
                color_discrete_map={"Reported":"#FF9F0A","Found":"#30D158","Claimed":"#0A84FF"},
                title="Lost & Found Status")
            fig_lf.update_layout(paper_bgcolor="rgba(0,0,0,0)",height=260,margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig_lf, use_container_width=True)

            # Semester distribution
            sem_dist = students_df["semester"].value_counts().sort_index().reset_index()
            sem_dist.columns = ["Semester","Count"]
            fig_sem = px.bar(sem_dist, x="Semester", y="Count",
                color_discrete_sequence=["#34AADC"],title="Students by Semester")
            fig_sem.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                height=260,margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig_sem, use_container_width=True)

        # Full driver table
        st.markdown("#### 📊 Full Driver Report")
        st.dataframe(drivers_df[["driver_id","name","route","bus_number","trips_this_month",
                                  "on_time_pct","overspeed_incidents","experience_yrs","status"]].rename(columns={
            "driver_id":"ID","name":"Name","route":"Route","bus_number":"Bus",
            "trips_this_month":"Trips/Mo","on_time_pct":"OnTime%",
            "overspeed_incidents":"Overspeed","experience_yrs":"Exp(yr)","status":"Status"}),
            use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# ████  DRIVER DASHBOARD
# ═══════════════════════════════════════════════════════════════
def show_driver():
    apply_css()
    ud       = st.session_state.user_data
    buses_df = update_bus_positions(generate_buses())
    my_bus   = buses_df[buses_df["driver_id"]==ud["driver_id"]]
    if len(my_bus)==0:
        st.error("Bus not found for this driver."); return
    mb = my_bus.iloc[0]

    # ── Header ──────────────────────────────────────────────
    hc1,hc2,hc3 = st.columns([3,2,1])
    with hc1: st.markdown(diu_logo_html(), unsafe_allow_html=True)
    with hc2:
        st.markdown(f"""
<div style="text-align:center;padding:6px 0">
  <div style="font-size:14px;font-weight:700;color:#FF9F0A">🚍 Driver Panel</div>
  <div style="font-size:11px;color:#8B949E">{ud['name']} · Bus {mb['bus_number']} · {mb['route']}</div>
</div>""", unsafe_allow_html=True)
    with hc3:
        if st.button("🚪 Logout"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

    st.markdown("---")

    # ── Status Bar ──────────────────────────────────────────
    occ_pct = seat_pct(mb)
    bar_c   = get_occ_color(occ_pct)
    ds1,ds2,ds3,ds4 = st.columns(4)
    ds1.metric("🚌 Bus Number", mb["bus_number"])
    ds2.metric("🗺️ Route", mb["route"])
    ds3.metric("💺 Occupancy", f"{mb['occupied_seats']}/{mb['total_seats']}")
    ds4.metric("⚡ Status", mb["status"])

    # ── Schedule Health Monitor ──────────────────────────────
    delay_min = random.randint(-5, 18)
    sched_color = "#30D158" if delay_min <= 0 else ("#FF9F0A" if delay_min <= 10 else "#FF3B30")
    sched_msg   = "On Time ✅" if delay_min <= 0 else f"{delay_min} min Late ⚠️"
    st.markdown(f"""
<div class="gc" style="padding:14px 20px;margin-bottom:14px">
  <div class="sec-title">📡 Schedule Health Monitor</div>
  <div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap">
    <div class="bstat"><div class="bv" style="color:{sched_color}">{sched_msg}</div><div class="bl">Schedule</div></div>
    <div class="bstat"><div class="bv">{fmt_eta(mb['eta_minutes'])}</div><div class="bl">ETA Campus</div></div>
    <div class="bstat"><div class="bv">{mb['speed']} km/h</div><div class="bl">Speed</div></div>
    <div class="bstat"><div class="bv">{mb['departure_time']}</div><div class="bl">Departed</div></div>
    <div class="bstat"><div class="bv">{int(mb['progress']*100)}%</div><div class="bl">Progress</div></div>
  </div>
  <div style="margin-top:10px">
    <div style="font-size:11px;color:#8B949E;margin-bottom:3px">Trip Progress</div>
    <div class="prog-track"><div class="prog-fill" style="width:{int(mb['progress']*100)}%;background:#0A84FF"></div></div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Main columns ─────────────────────────────────────────
    col_a, col_b, col_c = st.columns([1.2, 1.5, 1])

    # ─ Col A: ID Verification ────────────────────────────────
    with col_a:
        st.markdown('<div class="sec-title">🪪 Student ID Verification</div>', unsafe_allow_html=True)
        id_input = st.text_input("Scan / Enter Student ID", placeholder="e.g. 252-14-087",
                                  key="driver_id_input")
        check_btn = st.button("🔍 Verify ID", use_container_width=True)

        if check_btn and id_input:
            students_df = generate_students()
            clean = id_input.replace("-","")
            match = students_df[students_df["id"]==clean]
            if not match.empty:
                s = match.iloc[0]
                has_pass = s["transport_pass"]
                on_route = s["route"] == mb["route"]
                valid    = has_pass and on_route
                if valid:
                    st.markdown(f"""
<div class="access-granted">
  <div style="font-size:28px">✅</div>
  <div style="font-size:16px;font-weight:800;color:#30D158">ACCESS GRANTED</div>
  <div style="font-size:13px;margin-top:6px"><b>{s['name']}</b></div>
  <div style="font-size:11px;color:#555">{s['department']} · Sem {s['semester']}</div>
  <div style="font-size:11px;color:#555">Route: {s['route']} ✅</div>
</div>""", unsafe_allow_html=True)
                else:
                    reason = "No transport pass" if not has_pass else f"Wrong route (registered: {s['route']})"
                    st.markdown(f"""
<div class="access-denied">
  <div style="font-size:28px">❌</div>
  <div style="font-size:16px;font-weight:800;color:#FF3B30">ACCESS DENIED</div>
  <div style="font-size:13px;margin-top:6px"><b>{s['name']}</b></div>
  <div style="font-size:11px;color:#666">Reason: {reason}</div>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
<div class="access-denied">
  <div style="font-size:28px">❌</div>
  <div style="font-size:16px;font-weight:800;color:#FF3B30">ID NOT FOUND</div>
  <div style="font-size:12px;color:#666;margin-top:4px">This ID is not in the university database.</div>
</div>""", unsafe_allow_html=True)

        # Mid-route passenger counter
        booked_for_me = []
        for bid, bklist in st.session_state.booked_seats.items():
            if int(bid) == int(mb["bus_id"]):
                booked_for_me.extend(bklist)
        if booked_for_me:
            st.markdown(f"""
<div class="gc" style="padding:12px;margin-top:10px">
  <div class="sec-title" style="margin-bottom:6px">📲 Mid-Route Seat Requests</div>
  <div style="font-size:22px;font-weight:800;color:#0A84FF;text-align:center">{len(booked_for_me)}</div>
  <div style="font-size:11px;text-align:center;color:#8B949E">students waiting at stops</div>
  {"".join([f'<div style="font-size:11px;margin-top:4px;padding:4px 8px;background:rgba(10,132,255,.06);border-radius:6px">🧍 {bk["student_name"]} @ {bk["stop"]}</div>' for bk in booked_for_me])}
</div>""", unsafe_allow_html=True)

    # ─ Col B: Map + Smart Routing ────────────────────────────
    with col_b:
        st.markdown('<div class="sec-title">🗺️ Route Map & Smart Navigation</div>', unsafe_allow_html=True)
        m = build_map(buses_df, route_filter=mb["route"])
        st_folium(m, width=None, height=360, returned_objects=[])

        # AI smart route suggestion
        jam_routes = {"Dhanmondi":"Via Rayerbazar Bypass (saves ~12 min)",
                      "Mirpur-1":"Via Pallabi alternative (saves ~8 min)",
                      "Uttara":"Via Airport connector road (normal)",
                      "Farmgate":"Via Tejgaon Link Road (saves ~6 min)"}
        suggestion = jam_routes.get(mb["route"], "Current route is clear ✅")
        st.markdown(f"""
<div class="notif warn">
  🚦 <b>AI Smart Routing:</b> {suggestion}
</div>""", unsafe_allow_html=True)

        # Road & weather info
        st.markdown(f"""
<div class="gc" style="padding:12px 16px">
  <div style="display:flex;gap:14px;flex-wrap:wrap">
    <div><b>🌤️ Weather:</b> Partly cloudy, 31°C</div>
    <div><b>🚦 Traffic:</b> Moderate on main road</div>
    <div><b>🛣️ Road:</b> Good condition</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ─ Col C: SOS + Occupancy ────────────────────────────────
    with col_c:
        # SOS Button
        st.markdown('<div class="sec-title">🆘 Emergency SOS</div>', unsafe_allow_html=True)
        sos_pressed = st.button("🆘 PRESS SOS\nEMERGENCY", use_container_width=True, key="sos_btn")
        st.markdown('<style>div.stButton>button[kind="secondary"]{background:linear-gradient(135deg,#FF3B30,#FF6B6B)!important;color:#fff!important;border-radius:14px!important;font-size:16px!important;font-weight:800!important;padding:20px!important;box-shadow:0 8px 24px rgba(255,59,48,.45)!important}</style>', unsafe_allow_html=True)
        if sos_pressed:
            alert = {"bus":mb["bus_number"],"route":mb["route"],
                     "msg":"Driver triggered SOS! Location shared with Admin.",
                     "time":datetime.now().strftime("%H:%M")}
            st.session_state.sos_alerts.append(alert)
            st.error(f"🚨 SOS SENT! Admin notified. Location: {mb['lat']:.4f}°N, {mb['lng']:.4f}°E")

        # Live Occupancy
        st.markdown('<div class="sec-title" style="margin-top:14px">👥 Live Occupancy</div>', unsafe_allow_html=True)
        occ_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=int(occ_pct*100),
            delta={"reference":70,"increasing":{"color":"#FF3B30"},"decreasing":{"color":"#30D158"}},
            gauge={
                "axis":{"range":[0,100],"tickwidth":1},
                "bar":{"color":bar_c},
                "steps":[{"range":[0,60],"color":"#E0F8E9"},{"range":[60,85],"color":"#FFF3CD"},{"range":[85,100],"color":"#FFE0DE"}],
                "threshold":{"line":{"color":"#FF3B30","width":3},"thickness":0.75,"value":90},
            },
            number={"suffix":"%","font":{"size":22}},
            title={"text":f"{mb['occupied_seats']}/{mb['total_seats']} Seats"},
        ))
        occ_gauge.update_layout(height=220,margin=dict(l=10,r=10,t=10,b=10),
            paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(occ_gauge, use_container_width=True)

        if occ_pct >= 1.0:
            st.error("🔴 BUS FULL — Inform next stop passengers!")
        elif occ_pct >= 0.9:
            st.warning("🟡 Almost full — 1-2 seats left.")
        else:
            st.success(f"🟢 {mb['available_seats']} seats available.")

    # ── Complaint / Suggestion Box ───────────────────────────
    st.markdown("---")
    st.markdown("### 📝 Report / Suggestion to Admin")
    with st.form("driver_complaint"):
        dc1,dc2 = st.columns(2)
        with dc1:
            d_type = st.selectbox("Type",["Bus Issue","Road Condition","Passenger Complaint",
                                           "Route Suggestion","Other"])
        with dc2:
            d_prio = st.radio("Priority",["Low","Medium","High"], horizontal=True)
        d_msg = st.text_area("Details", placeholder="Describe the issue or suggestion...")
        if st.form_submit_button("📤 Send to Admin", use_container_width=True):
            st.success("✅ Report sent to admin successfully!")


# ═══════════════════════════════════════════════════════════════
# MAIN ROUTER
# ═══════════════════════════════════════════════════════════════
def main():
    init_state()
    apply_css()

    if not st.session_state.logged_in:
        show_login()
        return

    page = st.session_state.get("page","login")
    if page == "student":
        show_student()
    elif page == "admin":
        show_admin()
    elif page == "driver":
        show_driver()
    else:
        show_login()


if __name__ == "__main__":
    main()
