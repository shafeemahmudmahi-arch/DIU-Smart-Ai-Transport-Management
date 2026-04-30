"""
DIU Smart Transport Management System
A comprehensive transport management solution with AI-powered features
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import string
from datetime import datetime, time, timedelta
import pydeck as pdk
from sklearn.linear_model import LinearRegression
import hashlib
import time as time_module
import plotly.graph_objects as go
import plotly.express as px

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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        

