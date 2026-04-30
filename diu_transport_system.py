"""
DIU Smart Transport Management System - Ultimate MVP
A complete, error-free, multi-role transport solution with advanced AI & Analytics features.
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import hashlib
from datetime import datetime, timedelta
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="DIU Smart Transport MVP",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS (GLASSMORPHISM & ANIMATIONS) ====================
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        * { font-family: 'Inter', sans-serif; }
        .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); background-attachment: fixed; }
        
        .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(12px); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); padding: 1.5rem; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); }
        .login-container { background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(20px); border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.15); padding: 3rem; max-width: 450px; margin: 0 auto; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4); }
        
        h1, h2, h3, h4 { color: #ffffff; font-weight: 700; }
        .main-title { background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem; }
        .subtitle { color: #94a3b8; text-align: center; font-size: 1.1rem; margin-bottom: 2rem; }
        
        .stButton > button { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; border-radius: 12px; padding: 0.75rem; font-weight: 600; width: 100%; transition: all 0.3s ease; }
        .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4); }
        
        .dashboard-card { background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 1rem; }
        .alert-card { background: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; color: #fca5a5; }
        .ai-notify { background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; color: #bfdbfe; }
        
        .scanner-verified { background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.05) 100%); border: 2px solid #10b981; border-radius: 16px; padding: 2rem; text-align: center; font-size: 2rem; font-weight: 800; color: #10b981; margin: 1rem 0; animation: pulse-green 1.5s infinite; }
        .scanner-denied { background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.05) 100%); border: 2px solid #ef4444; border-radius: 16px; padding: 2rem; text-align: center; font-size: 2rem; font-weight: 800; color: #ef4444; margin: 1rem 0; animation: pulse-red 1.5s infinite; }
        .sos-active { background: #ef4444; color: white; padding: 1rem; border-radius: 12px; text-align: center; font-weight: bold; animation: pulse-red 1s infinite; }
        
        @keyframes pulse-green { 0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); } 50% { box-shadow: 0 0 0 15px rgba(16, 185, 129, 0); } }
        @keyframes pulse-red { 0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); } 50% { box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); } }
        
        .chat-user { background: rgba(6, 182, 212, 0.15); border-radius: 12px 12px 0 12px; padding: 12px; margin-bottom: 10px; text-align: right; border-right: 3px solid #06b6d4; color: white; }
        .chat-ai { background: rgba(16, 185, 129, 0.15); border-radius: 12px 12px 12px 0; padding: 12px; margin-bottom: 10px; text-align: left; border-left: 3px solid #10b981; color: white; }
        
        #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==================== DATA GENERATORS ====================

@st.cache_data
def generate_routes():
    return ["Dhanmondi", "Narayanganj", "Uttara", "Savar", "Mirpur-14", "Mirpur-12", "Gabtoli"]

@st.cache_data
def generate_buses():
    routes = generate_routes()
    buses = []
    base_coords = {
        "Dhanmondi": (23.7461, 90.3742), "Narayanganj": (23.6238, 90.5000), "Uttara": (23.8759, 90.3795),
        "Savar": (23.8583, 90.2667), "Mirpur-14": (23.8103, 90.3667), "Mirpur-12": (23.8256, 90.3689), "Gabtoli": (23.7783, 90.3494)
    }
    drivers = ["Karim", "Jabbar", "Rashed", "Habib", "Mizan", "Shafiq", "Jahangir", "Rafiq", "Monir", "Kamrul"]
    
    for route in routes:
        for i in range(random.randint(10, 12)):
            buses.append({
                "Bus_ID": f"{route[:3].upper()}-{i+1:02d}", "Route": route, "Total_Capacity": 40,
                "Current_Occupancy": random.randint(10, 40), "Driver_Name": f"{random.choice(drivers)} Ali",
                "Latitude": base_coords[route][0] + random.uniform(-0.04, 0.04),
                "Longitude": base_coords[route][1] + random.uniform(-0.04, 0.04),
                "Speed": random.randint(20, 50), "Status": random.choice(["Active", "Active", "Active", "Maintenance"]),
                "Punctuality": random.randint(85, 100)
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
            "Password": hashlib.md5("diu123".encode()).hexdigest(), "Name": f"Student {i+1}",
            "Department": random.choice(depts), "Route": random.choice(routes), "Payment_Status": random.choice(["Paid", "Paid", "Due"])
        })
    return pd.DataFrame(students)

@st.cache_data
def generate_routine():
    routine = []
    for dept in ["CSE", "CIS", "EEE", "BBA"]:
        for day in ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday"]:
            for _ in range(random.randint(3, 5)):
                routine.append({"Department": dept, "Day": day, "Time": random.choice(["08:30", "10:00", "11:30", "13:00"]), "Expected_Students": random.randint(40, 150)})
    return pd.DataFrame(routine)

# ==================== SESSION & AUTH ====================

def init_session():
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False
    if 'buses_db' not in st.session_state: st.session_state.buses_db = generate_buses()
    if 'students_db' not in st.session_state: st.session_state.students_db = generate_students()
    if 'routine_db' not in st.session_state: st.session_state.routine_db = generate_routine()
    if 'chat_history' not in st.session_state: st.session_state.chat_history = []
    if 'issues_db' not in st.session_state: st.session_state.issues_db = pd.DataFrame(columns=['Date', 'Type', 'Item_Issue', 'Route', 'Status'])
    if 'sos_active' not in st.session_state: st.session_state.sos_active = False
    if 'sos_details' not in st.session_state: st.session_state.sos_details = {}

def auth_user(user_id, password, role):
    if role == "Student":
        student = st.session_state.students_db[st.session_state.students_db['Student_ID'] == user_id]
        if not student.empty and student.iloc[0]['Password'] == hashlib.md5(password.encode()).hexdigest():
            return True, student.iloc[0].to_dict()
    elif role == "Admin" and user_id == "admin" and password == "admin":
        return True, {"Name": "Authority", "Role": "Admin"}
    elif role == "Driver":
        driver = st.session_state.buses_db[st.session_state.buses_db['Driver_Name'].str.lower().str.replace(" ", "") == user_id.lower()]
        if not driver.empty and password == "driver123":
            return True, {"Name": driver.iloc[0]['Driver_Name'], "Bus_ID": driver.iloc[0]['Bus_ID'], "Route": driver.iloc[0]['Route']}
    return False, None

# ==================== LOGIN SCREEN ====================

def login_screen():
    st.markdown('<h1 class="main-title">🚌 DIU Smart Transport</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Ecosystem | Student • Admin • Driver</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🔐 System Access</h3>", unsafe_allow_html=True)
        
        st.info("💡 **Demo Accounts:**")
        st.caption("Student: Copy an ID below. Pass: `diu123`\nAdmin: ID: `admin`, Pass: `admin`\nDriver: ID: `karimali`, Pass: `driver123`")
        st.dataframe(st.session_state.students_db[['Student_ID', 'Name', 'Route']].head(3), hide_index=True)
        
        role = st.selectbox("Select Access Level", ["Student", "Admin", "Driver"])
        user_id = st.text_input("User ID / Badge No.")
        password = st.text_input("Security PIN / Password", type="password")
        
        if st.button("🚀 Authorize Access"):
            if user_id and password:
                success, user_data = auth_user(user_id, password, role)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_role = role
                    st.session_state.user_data = user_data
                    st.rerun()
                else:
                    st.error("❌ Authentication Failed.")
            else:
                st.warning("⚠️ Enter credentials.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== CHATBOT LOGIC ====================

def get_ai_response(query, route):
    q = query.lower()
    if any(w in q for w in ["weather", "rain"]): return "🌤️ **Smart Alert:** 32°C and clear. Traffic is flowing normally on your route."
    elif any(w in q for w in ["next", "eta", "time"]): return f"🚌 Next bus on the **{route}** route is approx {random.randint(3, 12)} mins away."
    elif any(w in q for w in ["seat", "capacity"]): return f"💺 Mid-route sensors detect {random.randint(15, 40)} empty seats approaching."
    else: return "🤖 I am your DIU Transport AI. Ask me about ETAs, weather delays, or seat availability!"

# ==================== STUDENT DASHBOARD ====================

def student_dashboard():
    u_data = st.session_state.user_data
    b_db = st.session_state.buses_db
    route_buses = b_db[(b_db['Route'] == u_data['Route']) & (b_db['Status'] == 'Active')].copy()
    
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f'<h2 style="color: #10b981;">🎓 Personalized Dashboard: {u_data["Name"]}</h2>', unsafe_allow_html=True)
        st.caption(f"📍 Route: {u_data['Route']} | 🏫 Dept: {u_data['Department']} | 💳 Payment: {u_data['Payment_Status']}")
    with col2:
        if st.button("🚪 Logout"): st.session_state.clear(); st.rerun()

    # AI Push Notification
    st.markdown('<div class="ai-notify">🤖 <b>AI Alert:</b> Traffic is light today. Your usual bus is 5 minutes away. Don\'t forget your umbrella, 10% chance of rain later!</div>', unsafe_allow_html=True)

    # Bus Count Tracker
    c1, c2, c3, c4 = st.columns(4)
    total_buses = len(b_db[b_db['Route'] == u_data['Route']])
    active = len(route_buses)
    c1.metric("🚌 Total Route Buses", total_buses)
    c2.metric("🟢 Currently Active", active)
    c3.metric("🏁 Departed/Depot", total_buses - active)
    c4.metric("⏱️ Nearest ETA", f"{random.randint(3, 10)} min")

    t1, t2, t3, t4 = st.tabs(["🗺️ Live ETA & Map", "🔒 Mid-Route Booking", "📜 Digital Ride Log", "🛠️ Report & AI"])
    
    with t1:
        st.markdown("### Location-Based Live Tracking")
        if not route_buses.empty:
            route_buses['Seats_Free'] = route_buses['Total_Capacity'] - route_buses['Current_Occupancy']
            l = pdk.Layer('ScatterplotLayer', data=route_buses, get_position='[Longitude, Latitude]', get_color='[16, 185, 129, 200]', get_radius=250, pickable=True)
            txt = pdk.Layer('TextLayer', data=route_buses, get_position='[Longitude, Latitude]', get_text='Bus_ID', get_color='[255, 255, 255, 255]', get_size=14)
            v = pdk.ViewState(latitude=route_buses['Latitude'].mean(), longitude=route_buses['Longitude'].mean(), zoom=11)
            st.pydeck_chart(pdk.Deck(layers=[l, txt], initial_view_state=v, tooltip={"html": "<b>{Bus_ID}</b><br/>Speed: {Speed}km/h<br/>Free Seats: {Seats_Free}<br/>Status: {Status}"}, map_style=None))
        else: st.warning("No buses active.")
        
    with t2:
        st.markdown("### Virtual Seat Booking (Mid-Route)")
        st.info("Standing at a mid-route stop (e.g., Savar/Gabtoli)? Request a seat reservation.")
        if not route_buses.empty:
            sel_bus = st.selectbox("Select Approaching Bus", route_buses['Bus_ID'].tolist())
            avail = route_buses[route_buses['Bus_ID'] == sel_bus].iloc[0]['Seats_Free']
            st.metric("Real-Time Seat Status", f"{avail} Empty Seats")
            if st.button("🙋‍♂️ Request Seat Hold"):
                if avail > 0: st.success("✅ Seat hold request sent to driver's Mid-Route Counter!")
                else: st.error("❌ Bus is fully loaded.")
                
    with t3:
        st.markdown("### Digital Ride Log & History")
        history = pd.DataFrame({
            "Date": [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 6)],
            "Bus_ID": [random.choice(b_db['Bus_ID'].tolist()) for _ in range(5)],
            "Driver": [random.choice(b_db['Driver_Name'].tolist()) for _ in range(5)],
            "Status": ["Completed"] * 5
        })
        st.dataframe(history, use_container_width=True, hide_index=True)
        
    with t4:
        colA, colB = st.columns(2)
        with colA:
            st.markdown("### 🛠️ Quick Issue / Lost & Found")
            with st.form("issue_form", clear_on_submit=True):
                i_type = st.selectbox("Issue Type", ["Lost Item", "Found Item", "AC Not Working", "Reckless Driving", "Cleanliness"])
                desc = st.text_input("Details")
                if st.form_submit_button("Submit to Admin") and desc:
                    new_i = pd.DataFrame([{'Date': datetime.now().strftime("%Y-%m-%d"), 'Type': i_type, 'Item_Issue': desc, 'Route': u_data['Route'], 'Status': 'Open/Ticketed'}])
                    st.session_state.issues_db = pd.concat([st.session_state.issues_db, new_i], ignore_index=True)
                    st.success("✅ Ticket generated & sent to ERP.")
        with colB:
            st.markdown("### 🤖 Transport AI Chatbot")
            for msg in st.session_state.chat_history:
                cls = "chat-user" if msg['role'] == "You" else "chat-ai"
                st.markdown(f'<div class="{cls}">{msg["text"]}</div>', unsafe_allow_html=True)
            with st.form("chat_form", clear_on_submit=True):
                q = st.text_input("Ask me anything...")
                if st.form_submit_button("Ask AI") and q:
                    st.session_state.chat_history.append({"role": "You", "text": q})
                    st.session_state.chat_history.append({"role": "AI", "text": get_ai_response(q, u_data['Route'])})
                    st.rerun()

# ==================== ADMIN DASHBOARD ====================

def admin_dashboard():
    b_db = st.session_state.buses_db
    s_db = st.session_state.students_db
    
    col1, col2 = st.columns([5, 1])
    with col1: st.markdown('<h2 style="color: #06b6d4;">🏢 Admin Authority Dashboard</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout"): st.session_state.clear(); st.rerun()

    if st.session_state.sos_active:
        st.markdown(f'<div class="sos-active">🚨 SOS ALERT: Emergency reported by Driver on {st.session_state.sos_details.get("Bus_ID")} ({st.session_state.sos_details.get("Route")}). Rescue dispatched!</div>', unsafe_allow_html=True)
        if st.button("Resolve SOS"): st.session_state.sos_active = False; st.rerun()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Fleet", len(b_db))
    c2.metric("Revenue Compliance", f"{len(s_db[s_db['Payment_Status'] == 'Paid']) / len(s_db) * 100:.1f}%")
    surge_count = len(b_db[b_db['Current_Occupancy'] >= 38])
    c3.metric("Surge Warnings (Overloaded)", surge_count)
    c4.metric("Open ERP Tickets", len(st.session_state.issues_db[st.session_state.issues_db['Status'] == 'Open/Ticketed']))

    t1, t2, t3, t4 = st.tabs(["🌍 Live Fleet & Rescue", "📈 AI Demand & Surge", "💰 Revenue & Access", "🎟️ ERP & Drivers"])
    
    with t1:
        st.markdown("### Live Bird's-Eye View")
        b_db['Color'] = b_db['Current_Occupancy'].apply(lambda x: [16, 185, 129, 200] if x < 35 else [239, 68, 68, 220])
        l = pdk.Layer('ScatterplotLayer', data=b_db, get_position='[Longitude, Latitude]', get_fill_color='Color', get_radius=180, pickable=True)
        v = pdk.ViewState(latitude=23.81, longitude=90.41, zoom=10)
        st.pydeck_chart(pdk.Deck(layers=[l], initial_view_state=v, tooltip={"html": "<b>{Bus_ID}</b> ({Route})<br/>Load: {Current_Occupancy}/40<br/>Status: {Status}"}, map_style=None))
        
    with t2:
        st.markdown("### AI Demand Prediction & Dynamic Surge Control")
        if surge_count > 0: st.markdown('<div class="alert-card">⚠️ <b>Surge Detected:</b> AI has automatically signaled standby buses to dispatch to high-load routes.</div>', unsafe_allow_html=True)
        route_load = b_db.groupby('Route').agg({'Current_Occupancy': 'sum', 'Total_Capacity': 'sum'}).reset_index()
        fig = px.bar(route_load, x='Route', y=['Current_Occupancy', 'Total_Capacity'], barmode='group', title="Tomorrow's Predicted Allocation vs Capacity")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
        
    with t3:
        st.markdown("### Smart Access & Revenue Audit")
        colA, colB = st.columns(2)
        with colA:
            fig2 = px.pie(s_db, names='Payment_Status', title="Student Payment Compliance", color_discrete_sequence=['#10b981', '#ef4444'])
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig2, use_container_width=True)
        with colB:
            st.markdown("#### Unauthorized Boarding Attempts (Live)")
            st.dataframe(pd.DataFrame({"Time": ["10:12 AM", "10:15 AM"], "Location": ["Mirpur-10", "Dhanmondi"], "Status": ["Blocked", "Blocked"]}), hide_index=True)
            
    with t4:
        st.markdown("### ERP Sync & Ticket Management")
        st.button("🔄 Force Sync University Routine")
        st.dataframe(st.session_state.issues_db, hide_index=True, use_container_width=True)
        
        st.markdown("### Driver Performance Report")
        perf = b_db[['Driver_Name', 'Route', 'Punctuality', 'Speed']].drop_duplicates('Driver_Name').head(5)
        st.dataframe(perf.style.background_gradient(cmap='Greens', subset=['Punctuality']), hide_index=True, use_container_width=True)

# ==================== DRIVER DASHBOARD ====================

def driver_dashboard():
    u_data = st.session_state.user_data
    s_db = st.session_state.students_db
    
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f'<h2 style="color: #10b981;">🚍 Cockpit: {u_data["Driver_Name"]} (Bus {u_data["Bus_ID"]})</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout"): st.session_state.clear(); st.rerun()

    c1, c2, c3, c4 = st.columns(4)
    occ = random.randint(15, 38)
    c1.metric("👥 Live Occupancy Tracker", f"{occ}/40")
    c2.metric("🙋‍♂️ Mid-Route Requests", random.randint(2, 8))
    c3.metric("🚦 Schedule Health", "On Time" if random.random() > 0.2 else "5 Min Delay")
    
    with c4:
        if st.button("🚨 One-Tap SOS"):
            st.session_state.sos_active = True
            st.session_state.sos_details = {"Bus_ID": u_data["Bus_ID"], "Route": u_data["Route"]}
            st.rerun()

    t1, t2 = st.tabs(["🔍 Smart Access Signal", "🗺️ AI Smart Routing"])
    
    with t1:
        st.markdown("### Student Boarding Scanner")
        sid = st.text_input("Tap Student RFID / Enter ID", placeholder="DIU2023XXXXXXX")
        if st.button("🔍 Verify Access", type="primary"):
            if sid:
                student = s_db[s_db['Student_ID'] == sid]
                if not student.empty:
                    s_data = student.iloc[0]
                    if s_data['Route'] == u_data['Route'] and s_data['Payment_Status'] == 'Paid':
                        st.markdown('<div class="scanner-verified">✅ ACCESS GRANTED<br><span style="font-size:1rem;color:white;">Paid • Correct Route</span></div>', unsafe_allow_html=True)
                    else:
                        rsn = "Payment Due" if s_data['Payment_Status'] != 'Paid' else f"Wrong Route ({s_data['Route']})"
                        st.markdown(f'<div class="scanner-denied">❌ ACCESS DENIED<br><span style="font-size:1rem;color:white;">{rsn}</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="scanner-denied">❌ INVALID ID</div>', unsafe_allow_html=True)
                    
    with t2:
        st.markdown("### AI Smart Routing (Alternative Path)")
        st.info("🚦 Heavy traffic detected ahead. AI suggests taking the bypass route.")
        mock_route = pd.DataFrame({'lat': [23.81, 23.82, 23.83], 'lon': [90.41, 90.40, 90.42]})
        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(latitude=23.82, longitude=90.41, zoom=12, pitch=45),
            layers=[pdk.Layer('PathLayer', data=[{"path": mock_route.values.tolist(), "color": [6, 182, 212]}], get_path="path", get_color="color", width_scale=20, width_min_pixels=5)]
        ))

# ==================== MAIN RUNNER ====================

def main():
    init_session()
    inject_custom_css()
    if not st.session_state.logged_in: login_screen()
    else:
        role = st.session_state.user_role
        if role == "Student": student_dashboard()
        elif role == "Admin": admin_dashboard()
        elif role == "Driver": driver_dashboard()

if __name__ == "__main__":
    main()

