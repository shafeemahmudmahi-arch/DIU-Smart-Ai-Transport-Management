"""
DIU Smart Transport Management System MVP
A complete, error-free, multi-role transport solution with AI features.
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import hashlib
from datetime import datetime
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px
import time as time_module

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="DIU Smart Transport",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS (GLASSMORPHISM) ====================
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        * { font-family: 'Inter', sans-serif; }
        .stApp { background: linear-gradient(135deg, #0a1628 0%, #1a2332 50%, #0f1922 100%); background-attachment: fixed; }
        .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); padding: 1.5rem; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); }
        .login-container { background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(20px); border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.15); padding: 3rem; max-width: 450px; margin: 0 auto; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4); }
        h1, h2, h3 { color: #ffffff; font-weight: 700; }
        .main-title { background: linear-gradient(135deg, #39b54a 0%, #5dd9e8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem; }
        .subtitle { color: rgba(255, 255, 255, 0.7); text-align: center; font-size: 1.1rem; margin-bottom: 2rem; }
        .stButton > button { background: linear-gradient(135deg, #39b54a 0%, #2d9a3a 100%); color: white; border: none; border-radius: 12px; padding: 0.75rem; font-weight: 600; width: 100%; transition: all 0.3s ease; }
        .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(57, 181, 74, 0.5); }
        .dashboard-card { background: linear-gradient(135deg, rgba(57, 181, 74, 0.1) 0%, rgba(93, 217, 232, 0.1) 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 1rem; }
        .scanner-verified { background: linear-gradient(135deg, rgba(57, 181, 74, 0.3) 0%, rgba(57, 181, 74, 0.1) 100%); border: 3px solid #39b54a; border-radius: 20px; padding: 3rem; text-align: center; font-size: 2.5rem; font-weight: 800; color: #39b54a; margin: 2rem 0; animation: pulse 1.5s infinite; }
        .scanner-denied { background: linear-gradient(135deg, rgba(220, 53, 69, 0.3) 0%, rgba(220, 53, 69, 0.1) 100%); border: 3px solid #dc3545; border-radius: 20px; padding: 3rem; text-align: center; font-size: 2.5rem; font-weight: 800; color: #dc3545; margin: 2rem 0; }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); } }
        .chat-user { background: rgba(93, 217, 232, 0.15); border-radius: 12px 12px 0 12px; padding: 10px; margin-bottom: 10px; text-align: right; border-right: 3px solid #5dd9e8; color: white; }
        .chat-ai { background: rgba(57, 181, 74, 0.15); border-radius: 12px 12px 12px 0; padding: 10px; margin-bottom: 10px; text-align: left; border-left: 3px solid #39b54a; color: white; }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==================== DATA GENERATORS ====================

@st.cache_data
def generate_routes():
    return ["Dhanmondi", "Narayanganj", "Uttara", "Savar", "Mirpur-14", "Mirpur-12", "Mirpur-1", "Gabtoli"]

@st.cache_data
def generate_buses():
    routes = generate_routes()
    buses = []
    base_coords = {
        "Dhanmondi": (23.7461, 90.3742), "Narayanganj": (23.6238, 90.5000), "Uttara": (23.8759, 90.3795),
        "Savar": (23.8583, 90.2667), "Mirpur-14": (23.8103, 90.3667), "Mirpur-12": (23.8256, 90.3689),
        "Mirpur-1": (23.7956, 90.3537), "Gabtoli": (23.7783, 90.3494)
    }
    drivers = ["Karim", "Jabbar", "Rashed", "Habib", "Mizan", "Shafiq", "Jahangir", "Rafiq", "Monir", "Kamrul"]
    
    for route in routes:
        # Generate 10-12 buses per route (Total approx 80 buses)
        for i in range(random.randint(10, 12)):
            prefix = route[0] if not route.startswith("Mirpur") else f"M{route.split('-')[1]}"
            buses.append({
                "Bus_ID": f"{prefix}-{i+1:02d}", "Route": route, "Total_Capacity": 40,
                "Current_Occupancy": random.randint(10, 40), "Driver_Name": f"{random.choice(drivers)} Ali",
                "Latitude": base_coords[route][0] + random.uniform(-0.04, 0.04),
                "Longitude": base_coords[route][1] + random.uniform(-0.04, 0.04),
                "Speed": random.randint(20, 50), "Status": random.choice(["Active", "Active", "Maintenance"])
            })
    return pd.DataFrame(buses)

@st.cache_data
def generate_students():
    routes = generate_routes()
    depts = ["CSE", "CIS", "EEE", "BBA", "Pharmacy"]
    students = []
    for i in range(300):
        students.append({
            "Student_ID": f"DIU{random.randint(20, 23)}{random.randint(100, 999)}{random.randint(1000, 9999)}",
            "Password": hashlib.md5("diu123".encode()).hexdigest(),
            "Name": f"Student {i+1}", "Phone": f"+88017{random.randint(10000000, 99999999)}",
            "Department": random.choice(depts), "Route": random.choice(routes),
            "Seat_Locked": random.choice([True, False])
        })
    return pd.DataFrame(students)

@st.cache_data
def generate_routine():
    routine = []
    for dept in ["CSE", "CIS", "EEE", "BBA"]:
        for day in ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday"]:
            for _ in range(random.randint(3, 5)):
                routine.append({
                    "Department": dept, "Day": day, "Time": random.choice(["08:30", "10:00", "11:30", "13:00", "14:30"]),
                    "Expected_Students": random.randint(40, 150)
                })
    return pd.DataFrame(routine)

# ==================== SESSION & AUTH ====================

def init_session():
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False
    if 'buses_db' not in st.session_state: st.session_state.buses_db = generate_buses()
    if 'students_db' not in st.session_state: st.session_state.students_db = generate_students()
    if 'routine_db' not in st.session_state: st.session_state.routine_db = generate_routine()
    if 'chat_history' not in st.session_state: st.session_state.chat_history = []
    if 'lost_found_db' not in st.session_state:
        st.session_state.lost_found_db = pd.DataFrame(columns=['Date', 'Type', 'Item', 'Route', 'Status'])

def auth_user(user_id, password, role):
    if role == "Student":
        student = st.session_state.students_db[st.session_state.students_db['Student_ID'] == user_id]
        if not student.empty and student.iloc[0]['Password'] == hashlib.md5(password.encode()).hexdigest():
            return True, student.iloc[0].to_dict()
    elif role == "Admin" and user_id == "admin" and password == "admin":
        return True, {"Name": "Admin Controller", "Role": "Admin"}
    elif role == "Driver":
        driver = st.session_state.buses_db[st.session_state.buses_db['Driver_Name'].str.lower().str.replace(" ", "") == user_id.lower()]
        if not driver.empty and password == "driver123":
            return True, {"Name": driver.iloc[0]['Driver_Name'], "Bus_ID": driver.iloc[0]['Bus_ID'], "Route": driver.iloc[0]['Route']}
    return False, None

# ==================== LOGIN SCREEN ====================

def login_screen():
    st.markdown('<h1 class="main-title">🚌 DIU Smart Transport</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Transport Management System</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>🔐 Account Login</h3>", unsafe_allow_html=True)
        
        st.info("💡 Demo: Copy a Student ID below. Password is `diu123`")
        st.dataframe(st.session_state.students_db[['Student_ID', 'Name', 'Route']].head(3), hide_index=True)
        
        role = st.selectbox("Select Role", ["Student", "Admin", "Driver"])
        if role == "Admin": st.caption("Admin ID: `admin`, Pass: `admin`")
        elif role == "Driver": st.caption("Driver ID (e.g., `karimali`), Pass: `driver123`")
        
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        
        if st.button("🚀 Secure Login"):
            if user_id and password:
                success, user_data = auth_user(user_id, password, role)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_role = role
                    st.session_state.user_data = user_data
                    st.rerun()
                else:
                    st.error("❌ Invalid ID or Password.")
            else:
                st.warning("⚠️ Enter credentials.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== CHATBOT LOGIC ====================

def get_ai_response(query, u_data, route_buses):
    q = query.lower()
    if any(w in q for w in ["weather", "rain", "hot", "temp"]):
        return random.choice(["🌡️ It's 32°C and Sunny. Perfect day for campus!", "🌧️ 24°C with light rain. Traffic might be slow, plan ahead!"])
    elif any(w in q for w in ["next", "bus", "time", "eta"]):
        return f"🚌 The next bus on your {u_data['Route']} route will arrive in approx {random.randint(5, 15)} minutes."
    elif any(w in q for w in ["seat", "capacity", "empty"]):
        seats = int((route_buses['Total_Capacity'] - route_buses['Current_Occupancy']).sum())
        return f"💺 Currently {seats} empty seats available across all active buses on the {u_data['Route']} route."
    elif any(w in q for w in ["lost", "found", "report"]):
        return "📦 You can report or find lost items in the 'Lost & Found' tab on your dashboard!"
    elif any(w in q for w in ["hi", "hello", "hey"]):
        return f"Hello {u_data['Name']}! Ask me about the weather, next bus ETA, seat availability, or lost & found."
    else:
        return "I am still learning! Please ask me about 'weather', 'next bus', 'seats', or 'lost items'."

# ==================== STUDENT DASHBOARD ====================

def student_dashboard():
    u_data = st.session_state.user_data
    b_db = st.session_state.buses_db
    route_buses = b_db[b_db['Route'] == u_data['Route']].copy()
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<h2 style="color: #39b54a;">🎓 Welcome, {u_data["Name"]}</h2>', unsafe_allow_html=True)
        st.markdown(f"**Route:** {u_data['Route']} | **Dept:** {u_data['Department']}")
    with col2:
        if st.button("🚪 Logout"): st.session_state.clear(); st.rerun()
        
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🚌 Active Buses", len(route_buses[route_buses['Status'] == 'Active']))
    c2.metric("👥 Route Load", int(route_buses['Current_Occupancy'].mean() if not route_buses.empty else 0))
    c3.metric("💺 Available Seats", int((route_buses['Total_Capacity'] - route_buses['Current_Occupancy']).sum() if not route_buses.empty else 0))
    c4.metric("⏱️ Next ETA", f"{random.randint(5, 15)} min")

    tab1, tab2, tab3 = st.tabs(["🗺️ Live Tracking", "🔒 Book Seat", "📦 Lost & Found"])
    
    with tab1:
        st.markdown("### 🗺️ Real-Time Fleet Map")
        if not route_buses.empty:
            route_buses['Seats'] = route_buses['Total_Capacity'] - route_buses['Current_Occupancy']
            layer = pdk.Layer('ScatterplotLayer', data=route_buses, get_position='[Longitude, Latitude]', get_color='[57, 181, 74, 200]', get_radius=250, pickable=True)
            text = pdk.Layer('TextLayer', data=route_buses, get_position='[Longitude, Latitude]', get_text='Bus_ID', get_color='[255, 255, 255, 255]', get_size=16)
            view = pdk.ViewState(latitude=route_buses['Latitude'].mean(), longitude=route_buses['Longitude'].mean(), zoom=11)
            tt = {"html": "<b>{Bus_ID}</b><br/>Speed: {Speed}km/h<br/>Seats: {Seats}", "style": {"backgroundColor": "#0f172a", "color": "white"}}
            st.pydeck_chart(pdk.Deck(layers=[layer, text], initial_view_state=view, tooltip=tt, map_style=None))
            st.dataframe(route_buses[['Bus_ID', 'Driver_Name', 'Seats', 'Speed', 'Status']], hide_index=True, use_container_width=True)
        else:
            st.warning("No active buses on your route.")
            
    with tab2:
        st.markdown("### 🔒 Virtual Seat Lock")
        if not route_buses.empty:
            cc1, cc2 = st.columns(2)
            with cc1:
                sel_bus = st.selectbox("Select Bus", route_buses['Bus_ID'].tolist())
            with cc2:
                avail = route_buses[route_buses['Bus_ID'] == sel_bus].iloc[0]['Seats']
                st.metric("Available Seats on Selected Bus", int(avail))
            if st.button("🔐 Lock Seat Now"):
                if avail > 0: st.success(f"✅ Seat locked successfully on {sel_bus}!")
                else: st.error("❌ Bus is fully occupied.")
                
    with tab3:
        st.markdown("### 📦 Report Lost or Found Items")
        with st.form("lf_form", clear_on_submit=True):
            type_lf = st.radio("Report Type", ["Lost Something", "Found Something"], horizontal=True)
            item = st.text_input("Item Description (e.g., Black Wallet, ID Card)")
            if st.form_submit_button("Submit Report") and item:
                new_item = pd.DataFrame([{'Date': datetime.now().strftime("%Y-%m-%d"), 'Type': type_lf.split()[0], 'Item': item, 'Route': u_data['Route'], 'Status': 'Open'}])
                st.session_state.lost_found_db = pd.concat([st.session_state.lost_found_db, new_item], ignore_index=True)
                st.success("✅ Report recorded successfully!")
        st.markdown("#### Recent Reports")
        st.dataframe(st.session_state.lost_found_db, hide_index=True, use_container_width=True)

    # Floating AI Chatbot
    with st.popover("🤖 Smart AI Assistant"):
        st.markdown("💬 **DIU Transport Assistant**")
        for msg in st.session_state.chat_history:
            cls = "chat-user" if msg['role'] == "You" else "chat-ai"
            st.markdown(f'<div class="{cls}">{msg["text"]}</div>', unsafe_allow_html=True)
        with st.form("chat_form", clear_on_submit=True):
            query = st.text_input("Ask about weather, buses, or seats...")
            if st.form_submit_button("Send") and query:
                st.session_state.chat_history.append({"role": "You", "text": query})
                reply = get_ai_response(query, u_data, route_buses)
                st.session_state.chat_history.append({"role": "AI", "text": reply})
                st.rerun()

# ==================== ADMIN DASHBOARD ====================

def admin_dashboard():
    b_db = st.session_state.buses_db
    s_db = st.session_state.students_db
    
    col1, col2 = st.columns([4, 1])
    with col1: st.markdown('<h2 style="color: #5dd9e8;">🏢 Admin Command Center</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout"): st.session_state.clear(); st.rerun()
        
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Fleet", len(b_db))
    c2.metric("Registered Students", len(s_db))
    c3.metric("System Load", f"{(b_db['Current_Occupancy'].sum() / b_db['Total_Capacity'].sum() * 100):.1f}%")
    c4.metric("Surge Warnings", len(b_db[b_db['Current_Occupancy'] > 35]))
    
    t1, t2, t3 = st.tabs(["🌍 Global Fleet Map", "📈 AI Analytics", "📦 Lost & Found Registry"])
    
    with t1:
        b_db['Color'] = b_db['Current_Occupancy'].apply(lambda x: [57, 181, 74, 200] if x < 25 else [220, 53, 69, 200])
        l = pdk.Layer('ScatterplotLayer', data=b_db, get_position='[Longitude, Latitude]', get_fill_color='Color', get_radius=180, pickable=True)
        txt = pdk.Layer('TextLayer', data=b_db, get_position='[Longitude, Latitude]', get_text='Bus_ID', get_color='[255, 255, 255, 255]', get_size=12)
        v = pdk.ViewState(latitude=23.81, longitude=90.41, zoom=10)
        st.pydeck_chart(pdk.Deck(layers=[l, txt], initial_view_state=v, tooltip={"html": "<b>{Route}</b><br/>ID: {Bus_ID}<br/>Load: {Current_Occupancy}/40"}, map_style=None))
        
    with t2:
        st.markdown("### Demand vs Allocation (AI Prediction)")
        route_load = b_db.groupby('Route').agg({'Current_Occupancy': 'sum', 'Total_Capacity': 'sum'}).reset_index()
        fig = px.bar(route_load, x='Route', y=['Current_Occupancy', 'Total_Capacity'], barmode='group', title="Current Load vs Total Route Capacity")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
        
    with t3:
        st.markdown("### Global Lost & Found Registry")
        st.dataframe(st.session_state.lost_found_db, hide_index=True, use_container_width=True)

# ==================== DRIVER DASHBOARD ====================

def driver_dashboard():
    u_data = st.session_state.user_data
    s_db = st.session_state.students_db
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<h2 style="color: #39b54a;">🚍 Bus {u_data["Bus_ID"]} Driver Panel</h2>', unsafe_allow_html=True)
        st.markdown(f"**Route:** {u_data['Route']} | **Driver:** {u_data['Name']}")
    with col2:
        if st.button("🚪 Logout"): st.session_state.clear(); st.rerun()
        
    st.markdown("### 🔍 Student Boarding Scanner")
    st.info(f"Only students registered for the **{u_data['Route']}** route are allowed.")
    
    sid = st.text_input("Enter Student ID to Scan", placeholder="DIU2023XXXXXXX")
    if st.button("🔍 SCAN ID", type="primary"):
        if sid:
            student = s_db[s_db['Student_ID'] == sid]
            if not student.empty:
                s_data = student.iloc[0]
                if s_data['Route'] == u_data['Route']:
                    st.markdown('<div class="scanner-verified">✅ ACCESS GRANTED</div>', unsafe_allow_html=True)
                    st.success(f"Name: {s_data['Name']} | Dept: {s_data['Department']}")
                else:
                    st.markdown('<div class="scanner-denied">❌ ROUTE MISMATCH</div>', unsafe_allow_html=True)
                    st.error(f"Student belongs to {s_data['Route']} route.")
            else:
                st.markdown('<div class="scanner-denied">❌ INVALID ID</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter an ID to scan.")

# ==================== MAIN ====================

def main():
    init_session()
    inject_custom_css()
    if not st.session_state.logged_in:
        login_screen()
    else:
        role = st.session_state.user_role
        if role == "Student": student_dashboard()
        elif role == "Admin": admin_dashboard()
        elif role == "Driver": driver_dashboard()

if __name__ == "__main__":
    main()
