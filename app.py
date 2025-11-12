import streamlit as st
import requests
import json
from PIL import Image
import io
import base64
from pages import home, damage_detection, tire_analysis, market_price, feedback

# Page configuration
st.set_page_config(
    page_title="AutoXpert - Smart Vehicle Solutions",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar completely
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
    .stApp > header {
        display: none;
    }
    footer {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Professional Global CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        padding: 0;
    }
    
    .stApp {
        background: #f8f9fa;
    }
    
    /* Professional Button Styles */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Professional Input Styles */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border: 1.5px solid #e0e0e0;
        border-radius: 8px;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Professional Card Styles */
    .professional-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e8e8e8;
        transition: all 0.3s;
    }
    
    .professional-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Professional Navigation */
    .nav-button {
        background: #ffffff;
        border: 1.5px solid #e0e0e0;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .nav-button:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Navigation handler
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

# Main app routing
if st.session_state.current_page == 'home':
    home.show()
elif st.session_state.current_page == 'damage':
    damage_detection.show()
elif st.session_state.current_page == 'tire':
    tire_analysis.show()
elif st.session_state.current_page == 'market':
    market_price.show()
elif st.session_state.current_page == 'feedback':
    feedback.show()
