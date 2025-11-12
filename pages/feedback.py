import streamlit as st
import sys
sys.path.append('.')
from utils import register_repair_shop, login_repair_shop, get_shop_by_email

def show():
    st.markdown("""
    <style>
        .header-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            color: white;
            margin: -1rem -1rem 2rem -1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .header-section h1 {
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        .header-section p {
            margin: 0.5rem 0 0 0;
            opacity: 0.95;
            font-size: 1rem;
            font-weight: 400;
        }
        
        .form-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            margin: 2rem 0;
            border: 2px solid rgba(102, 126, 234, 0.2);
        }
        
        .shop-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2.5rem;
            border-radius: 16px;
            color: white;
            margin: 1.5rem 0;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .shop-card h2 {
            color: white;
            margin: 0 0 1rem 0;
            font-size: 1.8rem;
            font-weight: 700;
        }
        
        .price-card {
            background: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            border: 1px solid #e8e8e8;
            text-align: center;
        }
        
        .stat-card {
            background: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            border: 1px solid #e8e8e8;
        }
        
        .nav-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            transition: all 0.3s;
        }
        
        .nav-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }
        
        .stTextInput>div>div>input {
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 0.5rem;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #764ba2;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        }
        
        .stNumberInput>div>div>input {
            border: 2px solid #667eea;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional Header
    st.markdown("""
    <div class="header-section">
        <h1>Repair Shop Portal</h1>
        <p>Manage your shop profile, pricing, and services</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional Navigation
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Home", use_container_width=True, key="nav_feedback_home"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        if st.button("Damage Detection", use_container_width=True, key="nav_feedback_damage"):
            st.session_state.current_page = 'damage'
            st.rerun()
    with col3:
        if st.button("Tire Analysis", use_container_width=True, key="nav_feedback_tire"):
            st.session_state.current_page = 'tire'
            st.rerun()
    with col4:
        if st.button("Market Price", use_container_width=True, key="nav_feedback_market"):
            st.session_state.current_page = 'market'
            st.rerun()
    
    # Initialize session state
    if 'repair_shop_logged_in' not in st.session_state:
        st.session_state.repair_shop_logged_in = False
    if 'current_shop_email' not in st.session_state:
        st.session_state.current_shop_email = None
    
    # Check if logged in
    if st.session_state.repair_shop_logged_in and st.session_state.current_shop_email:
        # Show dashboard
        show_dashboard()
    else:
        # Show login/signup options
        tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])
        
        with tab1:
            show_login()
        
        with tab2:
            show_signup()

def show_login():
    """Show login form"""
    st.markdown("### Sign In")
    st.markdown("""
    <div style="background: #e3f2fd; border-left: 4px solid #2196F3; padding: 1.25rem 1.5rem; border-radius: 8px; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
        <p style="margin: 0; color: #1565c0; font-weight: 500;">Sign in to manage your repair shop and update your prices</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="your@email.com")
        password = st.text_input("🔒 Password", type="password")
        submit = st.form_submit_button("Sign In", use_container_width=True, type="primary")
        
        if submit:
            shop = login_repair_shop(email, password)
            if shop:
                st.session_state.repair_shop_logged_in = True
                st.session_state.current_shop_email = email
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid email or password")

def show_signup():
    """Show signup form"""
    st.markdown("### Create Account")
    st.markdown("""
    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 1.25rem 1.5rem; border-radius: 8px; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
        <p style="margin: 0; color: #e65100; font-weight: 500;">Create an account to list your repair shop and set your prices for dent and scratch repairs</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Shop Name *", placeholder="ABC Auto Repair")
            email = st.text_input("Email *", placeholder="your@email.com")
            phone = st.text_input("Phone *", placeholder="+1234567890")
            location = st.text_input("Location *", placeholder="City, State")
        
        with col2:
            st.markdown("### Set Your Prices")
            dent_price = st.number_input("Dent Repair Price ($) *", min_value=0.0, value=150.0, step=10.0)
            scratch_price = st.number_input("Scratch Repair Price ($) *", min_value=0.0, value=100.0, step=10.0)
            password = st.text_input("Password *", type="password")
            confirm_password = st.text_input("Confirm Password *", type="password")
        
        submit = st.form_submit_button("Create Account", use_container_width=True, type="primary")
        
        if submit:
            # Validation
            if not all([name, email, phone, location, password]):
                st.error("❌ Please fill all required fields")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            else:
                success, message = register_repair_shop(
                    name, email, phone, location, 
                    dent_price, scratch_price, password
                )
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                    st.info("🎉 You can now sign in with your credentials!")
                else:
                    st.error(f"❌ {message}")

def show_dashboard():
    """Show repair shop dashboard"""
    shop = get_shop_by_email(st.session_state.current_shop_email)
    
    if not shop:
        st.error("Shop not found")
        return
    
    st.markdown(f"""
    <div class="shop-card">
        <h2>Welcome, {shop['name']}!</h2>
        <p style="font-size: 1.1rem; margin: 0.5rem 0; opacity: 0.95;">📍 {shop['location']} | 📞 {shop['phone']}</p>
        <p style="font-size: 1rem; margin: 0.5rem 0; opacity: 0.9;">⭐ Rating: {shop['rating']}/5.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    if st.button("Logout", use_container_width=True):
        st.session_state.repair_shop_logged_in = False
        st.session_state.current_shop_email = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Update Your Prices")
    
    with st.form("update_prices"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_dent_price = st.number_input(
                "Dent Repair Price ($)", 
                min_value=0.0, 
                value=float(shop['dent_price']), 
                step=10.0
            )
        
        with col2:
            new_scratch_price = st.number_input(
                "Scratch Repair Price ($)", 
                min_value=0.0, 
                value=float(shop['scratch_price']), 
                step=10.0
            )
        
        update = st.form_submit_button("Update Prices", use_container_width=True, type="primary")
        
        if update:
            shop['dent_price'] = new_dent_price
            shop['scratch_price'] = new_scratch_price
            st.success("✅ Prices updated successfully!")
            st.balloons()
            st.rerun()
    
    # Current prices display
    st.markdown("### Current Pricing")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="price-card">
            <h3 style="color: #333; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">Dent Repair</h3>
            <p style="font-size: 2.5rem; font-weight: 700; margin: 0; color: #667eea;">${shop['dent_price']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="price-card">
            <h3 style="color: #333; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">Scratch Repair</h3>
            <p style="font-size: 2.5rem; font-weight: 700; margin: 0; color: #667eea;">${shop['scratch_price']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Shop statistics
    st.markdown("### Shop Statistics")
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #1a1a1a; margin: 0 0 1.5rem 0; font-size: 1.3rem; font-weight: 700;">Your Shop Stats</h3>
        <p style="color: #555; font-size: 1rem; margin: 0.75rem 0;"><strong>Services Offered:</strong> Dent Repair, Scratch Repair</p>
        <p style="color: #555; font-size: 1rem; margin: 0.75rem 0;"><strong>Total Reviews:</strong> {len(shop.get('reviews', []))}</p>
        <p style="color: #555; font-size: 1rem; margin: 0.75rem 0;"><strong>Current Rating:</strong> {shop['rating']}/5.0</p>
        <p style="color: #555; font-size: 1rem; margin: 0.75rem 0;"><strong>Status:</strong> <span style="color: #4caf50; font-weight: 600;">Active</span></p>
    </div>
    """, unsafe_allow_html=True)
