"""
DIU Smart Transport Management System
A comprehensive transport management solution with AI-powered features
Author: Expert Python Full-Stack Developer
"""

import streamlit as st
import pandas as pd
import numpy as np
import randomstreamlit

import string
from datetime import datetime, time, timedelta
import pydeck as pdk
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import hashlib
import time as time_module

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="DIU Smart Transport",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS - GLASSMORPHISM DESIGN ====================
def inject_custom_css():
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Main Background */
        .stApp {
            background: linear-gradient(135deg, #0a1628 0%, #1a2332 50%, #0f1922 100%);
            background-attachment: fixed;
        }
        
        /* Glassmorphism Card */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        
        /* Login Container */
        .login-container {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 3rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            max-width: 450px;
            margin: 0 auto;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #ffffff;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        .main-title {
            background: linear-gradient(135deg, #39b54a 0%, #5dd9e8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            color: rgba(255, 255, 255, 0.7);
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #39b54a 0%, #2d9a3a 100%);
            color: white;
            border: None;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(57, 181, 74, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(57, 181, 74, 0.5);
        }
        
        /* Metrics */
        .metric-card {
            background: rgba(57, 181, 74, 0.1);
            border-left: 4px solid #39b54a;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 0.5rem 0;
        }
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            color: white;
            padding: 0.75rem;
        }
        
        /* Dashboard Cards */
        .dashboard-card {
            background: linear-gradient(135deg, rgba(57, 181, 74, 0.1) 0%, rgba(93, 217, 232, 0.1) 100%);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 1rem;
        }
        
        /* Status Badge */
        .status-badge {
            display: inline-block;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        
        .status-active {
            background: rgba(57, 181, 74, 0.2);
            color: #39b54a;
            border: 1px solid #39b54a;
        }
        
        .status-warning {
            background: rgba(255, 193, 7, 0.2);
            color: #ffc107;
            border: 1px solid #ffc107;
        }
        
        /* Scanner Result */
        .scanner-verified {
            background: linear-gradient(135deg, rgba(57, 181, 74, 0.3) 0%, rgba(57, 181, 74, 0.1) 100%);
            border: 3px solid #39b54a;
            border-radius: 20px;
            padding: 3rem;
            text-align: center;
            font-size: 2.5rem;
            font-weight: 800;
            color: #39b54a;
            margin: 2rem 0;
            animation: pulse 1.5s infinite;
        }
        
        .scanner-denied {
            background: linear-gradient(135deg, rgba(220, 53, 69, 0.3) 0%, rgba(220, 53, 69, 0.1) 100%);
            border: 3px solid #dc3545;
            border-radius: 20px;
            padding: 3rem;
            text-align: center;
            font-size: 2.5rem;
            font-weight: 800;
            color: #dc3545;
            margin: 2rem 0;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        
        /* Chatbot Popover */
        .chatbot-message {
            background: rgba(57, 181, 74, 0.1);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 3px solid #39b54a;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(57, 181, 74, 0.5);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(57, 181, 74, 0.7);
        }
    </style>
    """, unsafe_allow_html=True)

# ==================== DATA GENERATION FUNCTIONS ====================

@st.cache_data
def generate_routes():
    """Generate route data"""
    routes = [
        "Dhanmondi", "Narayanganj", "Uttara", "Savar", 
        "Mirpur-14", "Mirpur-12", "Mirpur-1", "Gabtoli"
    ]
    return routes

@st.cache_data
def generate_buses():
    """Generate 80 buses with realistic data"""
    routes = generate_routes()
    buses = []
    
    # Base coordinates for Dhaka University area
    base_coords = {
        "Dhanmondi": (23.7461, 90.3742),
        "Narayanganj": (23.6238, 90.5000),
        "Uttara": (23.8759, 90.3795),
        "Savar": (23.8583, 90.2667),
        "Mirpur-14": (23.8103, 90.3667),
        "Mirpur-12": (23.8256, 90.3689),
        "Mirpur-1": (23.7956, 90.3537),
        "Gabtoli": (23.7783, 90.3494)
    }
    
    driver_names = [
        "Karim Ahmed", "Abdul Jabbar", "Rashed Khan", "Habib Rahman",
        "Mizanur Islam", "Shafiqul Islam", "Jahangir Alam", "Rafiqul Haque",
        "Monir Hossain", "Kamrul Islam", "Faruk Ahmed", "Badrul Alam",
        "Nazrul Islam", "Anwar Hossain", "Delwar Hossain", "Mostafa Kamal"
    ]
    
    bus_id = 1
    for route in routes:
        # 10-12 buses per route
        num_buses = random.randint(10, 12)
        base_lat, base_lon = base_coords[route]
        
        for i in range(num_buses):
            # Route prefix (first letter)
            prefix = route[0]
            
            # Add some random variation to coordinates (simulate buses along route)
            lat_offset = random.uniform(-0.05, 0.05)
            lon_offset = random.uniform(-0.05, 0.05)
            
            bus = {
                "Bus_ID": f"{prefix}{i+1:02d}",
                "Route": route,
                "Total_Capacity": 40,
                "Current_Occupancy": random.randint(5, 35),
                "Driver_Name": random.choice(driver_names),
                "Latitude": base_lat + lat_offset,
                "Longitude": base_lon + lon_offset,
                "Speed": random.randint(15, 45),  # km/h
                "Status": random.choice(["Active", "Active", "Active", "Maintenance"]),
                "Last_Updated": datetime.now()
            }
            buses.append(bus)
            bus_id += 1
    
    return pd.DataFrame(buses)

@st.cache_data
def generate_students():
    """Generate 300 students"""
    routes = generate_routes()
    departments = ["CSE", "CIS", "EEE", "Civil", "BBA", "English", "LLB", "Pharmacy"]
    students = []
    
    first_names = [
        "Arafat", "Nusrat", "Tanvir", "Farhana", "Rakib", "Tasnim", "Kamal", "Sadiya",
        "Rifat", "Jannatul", "Sabbir", "Lamia", "Nahid", "Rafia", "Shakib", "Mehjabin",
        "Fahim", "Sadia", "Rafi", "Nishat", "Samir", "Tanha", "Asif", "Nabila"
    ]
    
    last_names = [
        "Rahman", "Islam", "Ahmed", "Khan", "Hossain", "Ali", "Uddin", "Akter",
        "Khatun", "Begum", "Chowdhury", "Hassan", "Mahmud", "Sultana", "Mia"
    ]
    
    for i in range(300):
        student_id = f"DIU{random.randint(20, 23)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
        
        student = {
            "Student_ID": student_id,
            "Password": hashlib.md5("diu123".encode()).hexdigest(),
            "Name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "Phone": f"+880{random.randint(1700000000, 1999999999)}",
            "Semester": random.choice(["Spring", "Summer", "Fall"]) + f" {random.randint(1, 12)}",
            "Department": random.choice(departments),
            "Route": random.choice(routes),
            "Seat_Locked": random.choice([True, False]),
            "Locked_Bus": None
        }
        students.append(student)
    
    return pd.DataFrame(students)

@st.cache_data
def generate_routine():
    """Generate class routine data for demand prediction"""
    departments = ["CSE", "CIS", "EEE", "Civil", "BBA", "English", "LLB", "Pharmacy"]
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday"]
    time_slots = ["08:00", "09:30", "11:00", "12:30", "14:00", "15:30", "17:00"]
    
    routine = []
    for dept in departments:
        for day in days:
            num_classes = random.randint(3, 5)
            for _ in range(num_classes):
                class_entry = {
                    "Department": dept,
                    "Day": day,
                    "Time": random.choice(time_slots),
                    "Expected_Students": random.randint(30, 120),
                    "Room": f"Room {random.randint(101, 599)}"
                }
                routine.append(class_entry)
    
    return pd.DataFrame(routine)

# ==================== AUTHENTICATION FUNCTIONS ====================

def hash_password(password):
    """Hash password using MD5"""
    return hashlib.md5(password.encode()).hexdigest()

def authenticate_user(user_id, password, role):
    """Authenticate user based on role"""
    if role == "Student":
        students_db = st.session_state.students_db
        student = students_db[students_db['Student_ID'] == user_id]
        
        if not student.empty:
            hashed_pw = hash_password(password)
            if student.iloc[0]['Password'] == hashed_pw:
                return True, student.iloc[0].to_dict()
        return False, None
    
    elif role == "Admin":
        # Admin credentials
        if user_id == "admin" and password == "admin@diu2024":
            return True, {"Name": "Admin", "Role": "Admin"}
        return False, None
    
    elif role == "Driver":
        # Driver credentials (check against bus drivers)
        buses_db = st.session_state.buses_db
        driver = buses_db[buses_db['Driver_Name'].str.lower().str.replace(" ", "") == user_id.lower()]
        
        if not driver.empty and password == "driver123":
            return True, {
                "Name": driver.iloc[0]['Driver_Name'],
                "Bus_ID": driver.iloc[0]['Bus_ID'],
                "Route": driver.iloc[0]['Route']
            }
        return False, None
    
    return False, None

# ==================== LOGIN SCREEN ====================

def login_screen():
    """Display login interface"""
    st.markdown('<h1 class="main-title">🚌 DIU Smart Transport</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Intelligent Transport Management System</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        st.markdown("### 🔐 Login to Your Account")
        
        role = st.selectbox(
            "Select Role",
            ["Student", "Admin", "Driver"],
            key="role_select"
        )
        
        if role == "Student":
            st.info("📝 Demo: Use any Student ID from generated data, Password: `diu123`")
            user_id = st.text_input("Student ID", placeholder="DIU2023XXXXXXX")
        elif role == "Admin":
            st.info("👨‍💼 Demo: ID: `admin`, Password: `admin@diu2024`")
            user_id = st.text_input("Admin ID", placeholder="admin")
        else:
            st.info("🚗 Demo: Use driver name (no spaces, lowercase), Password: `driver123`")
            user_id = st.text_input("Driver ID", placeholder="karimahmed")
        
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Login", use_container_width=True):
            if user_id and password:
                success, user_data = authenticate_user(user_id, password, role)
                
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_role = role
                    st.session_state.user_data = user_data
                    st.success(f"✅ Welcome, {user_data['Name']}!")
                    time_module.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
            else:
                st.warning("⚠️ Please enter both User ID and Password")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== STUDENT DASHBOARD ====================

def student_dashboard():
    """Student panel with live map, chatbot, and seat locking"""
    user_data = st.session_state.user_data
    buses_db = st.session_state.buses_db
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<h1 class="main-title">🎓 Student Dashboard</h1>', unsafe_allow_html=True)
        st.markdown(f"### Welcome, {user_data['Name']}")
        st.markdown(f"**Route:** {user_data['Route']} | **Department:** {user_data['Department']}")
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown("---")
    
    # Filter buses for student's route
    route_buses = buses_db[buses_db['Route'] == user_data['Route']].copy()
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.metric("🚌 Active Buses", len(route_buses[route_buses['Status'] == 'Active']))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        avg_occupancy = route_buses['Current_Occupancy'].mean()
        st.metric("👥 Avg Occupancy", f"{avg_occupancy:.0f}/40")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        available_seats = (route_buses['Total_Capacity'] - route_buses['Current_Occupancy']).sum()
        st.metric("💺 Available Seats", int(available_seats))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.metric("⏱️ Next Bus ETA", f"{random.randint(3, 15)} min")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main Content
    tab1, tab2, tab3 = st.tabs(["🗺️ Live Map", "🔒 Seat Locking", "📊 My Stats"])
    
    with tab1:
        st.markdown("### 🗺️ Real-Time Bus Tracking")
        
        # Prepare data for PyDeck
        if not route_buses.empty:
            # Calculate available seats and ETA for tooltip
            route_buses['Available_Seats'] = route_buses['Total_Capacity'] - route_buses['Current_Occupancy']
            route_buses['ETA'] = route_buses.apply(lambda x: f"{random.randint(5, 20)} min", axis=1)
            
            # Create PyDeck layer with custom tooltips
            layer = pdk.Layer(
                'ScatterplotLayer',
                data=route_buses,
                get_position='[Longitude, Latitude]',
                get_color='[57, 181, 74, 200]',
                get_radius=200,
                pickable=True,
                auto_highlight=True,
            )
            
            # Add text labels
            text_layer = pdk.Layer(
                'TextLayer',
                data=route_buses,
                get_position='[Longitude, Latitude]',
                get_text='Bus_ID',
                get_color='[255, 255, 255, 255]',
                get_size=16,
                get_alignment_baseline="'bottom'",
            )
            
            # View state centered on route
            view_state = pdk.ViewState(
                latitude=route_buses['Latitude'].mean(),
                longitude=route_buses['Longitude'].mean(),
                zoom=11,
                pitch=0,
            )
            
            # Tooltip
            tooltip = {
                "html": "<b>Bus:</b> {Bus_ID}<br/>"
                        "<b>Speed:</b> {Speed} km/h<br/>"
                        "<b>Available Seats:</b> {Available_Seats}<br/>"
                        "<b>ETA:</b> {ETA}",
                "style": {
                    "backgroundColor": "rgba(10, 22, 40, 0.9)",
                    "color": "white",
                    "border": "1px solid #39b54a"
                }
            }
            
            # Render map
            st.pydeck_chart(pdk.Deck(
                layers=[layer, text_layer],
                initial_view_state=view_state,
                tooltip=tooltip,
                map_style=None,
            ))
            
            # Bus details table
            st.markdown("#### 🚌 Bus Details")
            display_df = route_buses[['Bus_ID', 'Driver_Name', 'Current_Occupancy', 'Available_Seats', 'Speed', 'Status']].copy()
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.warning("No active buses on your route at the moment.")
    
    with tab2:
        st.markdown("### 🔒 Virtual Seat Locking")
        st.info("Reserve your seat before the bus arrives to ensure guaranteed boarding.")
        
        if not route_buses.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                selected_bus = st.selectbox(
                    "Select Bus",
                    route_buses['Bus_ID'].tolist(),
                    key="seat_lock_bus"
                )
            
            with col2:
                bus_info = route_buses[route_buses['Bus_ID'] == selected_bus].iloc[0]
                st.metric("Available Seats", int(bus_info['Available_Seats']))
            
            if st.button("🔐 Lock Seat", use_container_width=True):
                if bus_info['Available_Seats'] > 0:
                    st.success(f"✅ Seat locked on Bus {selected_bus}! Show this confirmation to the driver.")
                    st.balloons()
                else:
                    st.error("❌ No seats available on this bus.")
        else:
            st.warning("No buses available for seat locking.")
    
    with tab3:
        st.markdown("### 📊 Your Travel Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.metric("🎯 Total Trips", random.randint(45, 120))
            st.metric("⏰ Avg Commute Time", f"{random.randint(25, 45)} min")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.metric("💰 Monthly Savings", f"৳{random.randint(1200, 2500)}")
            st.metric("🌱 CO₂ Saved", f"{random.randint(15, 35)} kg")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Chatbot Popover (Bottom-right floating)
    with st.popover("🤖 AI Assistant", use_container_width=False):
        st.markdown("### 💬 Smart Transport Assistant")
        st.markdown("Ask me anything about bus schedules, routes, or seat availability!")
        
        user_question = st.text_input("Your question:", placeholder="When is the next Mirpur bus?")
        
        if st.button("Send", use_container_width=True):
            if user_question:
                # Simulate AI response
                st.markdown('<div class="chatbot-message">', unsafe_allow_html=True)
                
                if "next bus" in user_question.lower() or "eta" in user_question.lower():
                    response = f"🚌 The next bus on {user_data['Route']} route will arrive in approximately {random.randint(5, 15)} minutes. Bus ID: {route_buses.iloc[0]['Bus_ID']}"
                elif "seat" in user_question.lower():
                    response = f"💺 Currently {int(route_buses['Available_Seats'].sum())} seats are available across all buses on your route."
                elif "schedule" in user_question.lower():
                    response = "📅 Buses run every 15-20 minutes during peak hours (8 AM - 10 AM, 4 PM - 6 PM) and every 30 minutes otherwise."
                else:
                    response = "I can help you with:\n- Bus schedules and ETAs\n- Seat availability\n- Route information\n- Fare details"
                
                st.markdown(f"**Assistant:** {response}")
                st.markdown('</div>', unsafe_allow_html=True)

# ==================== ADMIN DASHBOARD ====================

def admin_dashboard():
    """Admin command center with analytics and fleet monitoring"""
    buses_db = st.session_state.buses_db
    students_db = st.session_state.students_db
    routine_db = st.session_state.routine_db
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h1 class="main-title">🏢 Admin Command Center</h1>', unsafe_allow_html=True)
        st.markdown("### Transport Management Dashboard")
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown("---")
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        active_buses = len(buses_db[buses_db['Status'] == 'Active'])
        st.metric("🚌 Active Buses", f"{active_buses}/{len(buses_db)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.metric("👥 Total Students", len(students_db))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        total_occupancy = buses_db['Current_Occupancy'].sum()
        st.metric("👨‍🎓 Current Load", total_occupancy)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        total_capacity = buses_db['Total_Capacity'].sum()
        utilization = (total_occupancy / total_capacity) * 100
        st.metric("📊 Fleet Utilization", f"{utilization:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        surge_routes = len(buses_db[buses_db['Current_Occupancy'] > 35])
        st.metric("⚠️ Surge Alerts", surge_routes)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Fleet Monitor", "📈 AI Demand Prediction", "💰 Financial Analytics", "📊 Reports"])
    
    with tab1:
        st.markdown("### 🌍 Global Fleet Monitoring")
        
        # All buses map with PyDeck
        if not buses_db.empty:
            buses_db['Available_Seats'] = buses_db['Total_Capacity'] - buses_db['Current_Occupancy']
            
            # Color code by occupancy level
            def get_color(occupancy):
                if occupancy < 20:
                    return [57, 181, 74, 200]  # Green
                elif occupancy < 30:
                    return [255, 193, 7, 200]  # Yellow
                else:
                    return [220, 53, 69, 200]  # Red
            
            buses_db['color'] = buses_db['Current_Occupancy'].apply(
                lambda x: get_color(x)
            )
            
            layer = pdk.Layer(
                'ScatterplotLayer',
                data=buses_db,
                get_position='[Longitude, Latitude]',
                get_fill_color='color',
                get_radius=150,
                pickable=True,
                auto_highlight=True,
            )
            
            text_layer = pdk.Layer(
                'TextLayer',
                data=buses_db,
                get_position='[Longitude, Latitude]',
                get_text='Bus_ID',
                get_color='[255, 255, 255, 255]',
                get_size=14,
                get_alignment_baseline="'bottom'",
            )
            
            view_state = pdk.ViewState(
                latitude=23.8103,
                longitude=90.4125,
                zoom=10,
                pitch=0,
            )
            
            tooltip = {
                "html": "<b>Bus ID:</b> {Bus_ID}<br/>"
                        "<b>Route:</b> {Route}<br/>"
                        "<b>Driver:</b> {Driver_Name}<br/>"
                        "<b>Occupancy:</b> {Current_Occupancy}/{Total_Capacity}<br/>"
                        "<b>Speed:</b> {Speed} km/h<br/>"
                        "<b>Status:</b> {Status}",
                "style": {
                    "backgroundColor": "rgba(10, 22, 40, 0.95)",
                    "color": "white",
                    "border": "1px solid #39b54a"
                }
            }
            
            st.pydeck_chart(pdk.Deck(
                layers=[layer, text_layer],
                initial_view_state=view_state,
                tooltip=tooltip,
                map_style=none,
            ))
            
            # Fleet status by route
            st.markdown("#### 📊 Route-wise Fleet Status")
            
            route_stats = buses_db.groupby('Route').agg({
                'Bus_ID': 'count',
                'Current_Occupancy': 'sum',
                'Total_Capacity': 'sum'
            }).reset_index()
            
            route_stats.columns = ['Route', 'Buses', 'Current_Load', 'Total_Capacity']
            route_stats['Utilization %'] = ((route_stats['Current_Load'] / route_stats['Total_Capacity']) * 100).round(1)
            
            st.dataframe(route_stats, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("### 📈 AI-Powered Demand Prediction")
        st.info("Using machine learning to predict student traffic patterns based on class schedules")
        
        # Aggregate routine data by day and time
        demand_by_time = routine_db.groupby(['Day', 'Time'])['Expected_Students'].sum().reset_index()
        
        # Simple demand prediction simulation
        routes = generate_routes()
        
        prediction_data = []
        for route in routes:
            route_students = len(students_db[students_db['Route'] == route])
            route_buses = len(buses_db[buses_db['Route'] == route])
            
            # Simulate peak hour demand
            peak_demand = int(route_students * random.uniform(0.6, 0.9))
            required_buses = int(np.ceil(peak_demand / 40))
            
            prediction_data.append({
                'Route': route,
                'Current_Buses': route_buses,
                'Predicted_Peak_Load': peak_demand,
                'Required_Buses': required_buses,
                'Gap': required_buses - route_buses,
                'Status': '✅ Optimal' if required_buses <= route_buses else '⚠️ Shortage'
            })
        
        prediction_df = pd.DataFrame(prediction_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Current vs Required Buses")
            
            import plotly.graph_objects as go
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Current Buses',
                x=prediction_df['Route'],
                y=prediction_df['Current_Buses'],
                marker_color='#39b54a'
            ))
            fig.add_trace(go.Bar(
                name='Required Buses',
                x=prediction_df['Route'],
                y=prediction_df['Required_Buses'],
                marker_color='#5dd9e8'
            ))
            
            fig.update_layout(
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Predicted Peak Load")
            
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=prediction_df['Route'],
                y=prediction_df['Predicted_Peak_Load'],
                mode='lines+markers',
                line=dict(color='#39b54a', width=3),
                marker=dict(size=10)
            ))
            
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=400,
                yaxis_title="Students"
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("#### Detailed Prediction Analysis")
        st.dataframe(prediction_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### 💰 Financial & Access Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.metric("💵 Total Revenue (Daily)", f"৳{random.randint(45000, 75000):,}")
            st.metric("📊 Revenue Compliance", f"{random.randint(92, 99)}%")
            st.metric("💳 Digital Payments", f"{random.randint(65, 85)}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.metric("🎫 Total Boardings", random.randint(1200, 2500))
            st.metric("✅ Authorized Access", f"{random.randint(95, 99)}%")
            st.metric("❌ Denied Access", random.randint(5, 25))
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Revenue by route (simulated)
        st.markdown("#### Revenue by Route")
        
        revenue_data = []
        for route in routes:
            revenue_data.append({
                'Route': route,
                'Trips': random.randint(80, 150),
                'Revenue': random.randint(5000, 12000),
                'Compliance': random.randint(90, 100)
            })
        
        revenue_df = pd.DataFrame(revenue_data)
        
        import plotly.express as px
        
        fig = px.bar(
            revenue_df,
            x='Route',
            y='Revenue',
            color='Compliance',
            color_continuous_scale='Greens',
            title='Daily Revenue by Route'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 📊 System Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Generate Report")
            report_type = st.selectbox(
                "Report Type",
                ["Daily Operations", "Fleet Performance", "Revenue Analysis", "Student Usage"]
            )
            
            date_range = st.date_input("Date Range", [])
            
            if st.button("📄 Generate Report", use_container_width=True):
                st.success("✅ Report generated successfully!")
                st.download_button(
                    label="📥 Download PDF",
                    data="Sample report data",
                    file_name=f"{report_type.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
        
        with col2:
            st.markdown("#### Quick Stats")
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown(f"**Total Routes:** {len(routes)}")
            st.markdown(f"**Total Buses:** {len(buses_db)}")
            st.markdown(f"**Active Students:** {len(students_db)}")
            st.markdown(f"**System Uptime:** 99.8%")
            st.markdown('</div>', unsafe_allow_html=True)

# ==================== DRIVER DASHBOARD ====================

def driver_dashboard():
    """Driver panel with simplified UI and student scanner"""
    user_data = st.session_state.user_data
    students_db = st.session_state.students_db
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h1 class="main-title">🚍 Driver Dashboard</h1>', unsafe_allow_html=True)
        st.markdown(f"### Welcome, {user_data['Name']}")
        st.markdown(f"**Bus:** {user_data['Bus_ID']} | **Route:** {user_data['Route']}")
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown("---")
    
    # Quick Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        current_load = random.randint(15, 35)
        st.metric("👥 Current Load", f"{current_load}/40")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.metric("📍 Next Stop", "Mirpur-10")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.metric("✅ Scans Today", random.randint(45, 120))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main Content
    tab1, tab2 = st.tabs(["🔍 Student Scanner", "📊 Route Info"])
    
    with tab1:
        st.markdown("### 🔍 Smart Student Scanner")
        st.markdown("Scan student ID to verify authorization")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            student_id_input = st.text_input(
                "Enter Student ID",
                placeholder="DIU2023XXXXXXX",
                key="scanner_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            scan_button = st.button("🔍 SCAN", use_container_width=True, type="primary")
        
        if scan_button and student_id_input:
            # Check if student exists
            student = students_db[students_db['Student_ID'] == student_id_input]
            
            if not student.empty:
                student_data = student.iloc[0]
                
                # Check if route matches
                if student_data['Route'] == user_data['Route']:
                    st.markdown(
                        '<div class="scanner-verified">✅ VERIFIED</div>',
                        unsafe_allow_html=True
                    )
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                        st.markdown(f"**Name:** {student_data['Name']}")
                        st.markdown(f"**Department:** {student_data['Department']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                        st.markdown(f"**Route:** {student_data['Route']}")
                        st.markdown(f"**Semester:** {student_data['Semester']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                        st.markdown(f"**Seat Locked:** {'Yes' if student_data['Seat_Locked'] else 'No'}")
                        st.markdown(f"**Status:** <span class='status-badge status-active'>Active</span>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.success("✅ Student authorized for boarding")
                else:
                    st.markdown(
                        '<div class="scanner-denied">❌ DENIED</div>',
                        unsafe_allow_html=True
                    )
                    st.error(f"⚠️ Wrong Route! Student route: {student_data['Route']}, Your route: {user_data['Route']}")
            else:
                st.markdown(
                    '<div class="scanner-denied">❌ NOT FOUND</div>',
                    unsafe_allow_html=True
                )
                st.error("❌ Student ID not found in system")
        
        # Recent scans
        st.markdown("---")
        st.markdown("#### 📜 Recent Scans")
        
        recent_scans = pd.DataFrame({
            'Time': [f"{random.randint(8, 17)}:{random.randint(10, 59)}" for _ in range(5)],
            'Student_ID': [f"DIU{random.randint(2020, 2023)}{random.randint(1000, 9999)}" for _ in range(5)],
            'Status': random.choices(['✅ Verified', '❌ Denied'], weights=[9, 1], k=5)
        })
        
        st.dataframe(recent_scans, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("### 📍 Route Information")
        
        route_students = students_db[students_db['Route'] == user_data['Route']]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.metric("👨‍🎓 Total Students on Route", len(route_students))
            st.metric("🎯 Expected Peak Load", f"{int(len(route_students) * 0.7)}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.metric("⏰ Average Trip Time", f"{random.randint(35, 55)} min")
            st.metric("⛽ Fuel Efficiency", f"{random.randint(8, 12)} km/L")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Department breakdown
        st.markdown("#### 🎓 Student Distribution by Department")
        dept_counts = route_students['Department'].value_counts().reset_index()
        dept_counts.columns = ['Department', 'Students']
        
        import plotly.express as px
        
        fig = px.pie(
            dept_counts,
            values='Students',
            names='Department',
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== MAIN APPLICATION ====================

def main():
    """Main application logic"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Generate databases (cached)
    if 'buses_db' not in st.session_state:
        st.session_state.buses_db = generate_buses()
    
    if 'students_db' not in st.session_state:
        st.session_state.students_db = generate_students()
    
    if 'routine_db' not in st.session_state:
        st.session_state.routine_db = generate_routine()
    
    # Inject CSS
    inject_custom_css()
    
    # Route to appropriate screen
    if not st.session_state.logged_in:
        login_screen()
    else:
        role = st.session_state.user_role
        
        if role == "Student":
            student_dashboard()
        elif role == "Admin":
            admin_dashboard()
        elif role == "Driver":
            driver_dashboard()

if __name__ == "__main__":
    main()
