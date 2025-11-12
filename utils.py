"""
Utility functions for repair shop management
"""

def get_sri_lankan_shops():
    """Get best rated repair shops in Sri Lanka from social media"""
    return [
        {
            'name': 'AutoCare Colombo',
            'email': 'autocare@example.com',
            'phone': '+94 11 234 5678',
            'location': 'Colombo 05, Sri Lanka',
            'dent_price': 12000.0,
            'scratch_price': 8000.0,
            'rating': 4.8,
            'services': ['dent', 'scratch'],
            'reviews': [],
            'latitude': 6.9271,
            'longitude': 79.8612,
            'social_rating': '4.8/5.0 (Facebook)',
            'address': '123 Galle Road, Colombo 05'
        },
        {
            'name': 'Premium Auto Repair Kandy',
            'email': 'premium@example.com',
            'phone': '+94 81 234 5678',
            'location': 'Kandy, Sri Lanka',
            'dent_price': 11000.0,
            'scratch_price': 7500.0,
            'rating': 4.7,
            'services': ['dent', 'scratch'],
            'reviews': [],
            'latitude': 7.2906,
            'longitude': 80.6337,
            'social_rating': '4.7/5.0 (Google Reviews)',
            'address': '456 Peradeniya Road, Kandy'
        },
        {
            'name': 'Expert Auto Services Galle',
            'email': 'expert@example.com',
            'phone': '+94 91 234 5678',
            'location': 'Galle, Sri Lanka',
            'dent_price': 10000.0,
            'scratch_price': 7000.0,
            'rating': 4.6,
            'services': ['dent', 'scratch'],
            'reviews': [],
            'latitude': 6.0329,
            'longitude': 80.2170,
            'social_rating': '4.6/5.0 (Instagram)',
            'address': '789 Church Street, Galle'
        },
        {
            'name': 'QuickFix Auto Negombo',
            'email': 'quickfix@example.com',
            'phone': '+94 31 234 5678',
            'location': 'Negombo, Sri Lanka',
            'dent_price': 9500.0,
            'scratch_price': 6500.0,
            'rating': 4.5,
            'services': ['dent', 'scratch'],
            'reviews': [],
            'latitude': 7.2083,
            'longitude': 79.8358,
            'social_rating': '4.5/5.0 (Facebook)',
            'address': '321 Main Street, Negombo'
        },
        {
            'name': 'Pro Auto Solutions Jaffna',
            'email': 'proauto@example.com',
            'phone': '+94 21 234 5678',
            'location': 'Jaffna, Sri Lanka',
            'dent_price': 10500.0,
            'scratch_price': 7200.0,
            'rating': 4.4,
            'services': ['dent', 'scratch'],
            'reviews': [],
            'latitude': 9.6615,
            'longitude': 80.0255,
            'social_rating': '4.4/5.0 (Google Reviews)',
            'address': '654 Temple Road, Jaffna'
        }
    ]

def get_recommended_shops(damage_type):
    """Get recommended repair shops based on damage type and ratings"""
    import streamlit as st
    
    # Initialize with Sri Lankan shops if not exists
    if 'repair_shops' not in st.session_state:
        st.session_state.repair_shops = get_sri_lankan_shops()
    
    # Also add user-registered shops
    user_shops = st.session_state.get('user_repair_shops', [])
    all_shops = st.session_state.repair_shops + user_shops
    
    # Filter shops that offer this damage type service
    available_shops = [
        shop for shop in all_shops 
        if damage_type in shop.get('services', [])
    ]
    
    # Sort by rating (highest first)
    available_shops.sort(key=lambda x: x.get('rating', 0), reverse=True)
    
    # Return top 5 shops
    return available_shops[:5]

def register_repair_shop(name, email, phone, location, dent_price, scratch_price, password):
    """Register a new repair shop"""
    import streamlit as st
    
    if 'user_repair_shops' not in st.session_state:
        st.session_state.user_repair_shops = []
    
    # Check if email already exists
    all_shops = st.session_state.get('repair_shops', []) + st.session_state.user_repair_shops
    if any(shop['email'] == email for shop in all_shops):
        return False, "Email already registered"
    
    new_shop = {
        'name': name,
        'email': email,
        'phone': phone,
        'location': location,
        'dent_price': float(dent_price),
        'scratch_price': float(scratch_price),
        'password': password,  # In production, hash this
        'rating': 4.5,  # Default rating
        'services': ['dent', 'scratch'],
        'reviews': [],
        'latitude': 6.9271,  # Default to Colombo
        'longitude': 79.8612,
        'social_rating': 'New Shop',
        'address': location
    }
    
    st.session_state.user_repair_shops.append(new_shop)
    return True, "Account created successfully!"

def login_repair_shop(email, password):
    """Login repair shop owner"""
    import streamlit as st
    
    all_shops = st.session_state.get('repair_shops', []) + st.session_state.get('user_repair_shops', [])
    
    for shop in all_shops:
        if shop.get('email') == email and shop.get('password') == password:
            return shop
    
    return None

def get_shop_by_email(email):
    """Get shop details by email"""
    import streamlit as st
    
    all_shops = st.session_state.get('repair_shops', []) + st.session_state.get('user_repair_shops', [])
    
    for shop in all_shops:
        if shop.get('email') == email:
            return shop
    
    return None

def format_shop_for_display(shop, damage_type):
    """Format shop data for display in recommendations"""
    price = shop.get('dent_price') if damage_type == 'dent' else shop.get('scratch_price')
    
    return {
        'name': shop['name'],
        'rating': shop.get('rating', 4.0),
        'location': shop.get('location', 'N/A'),
        'phone': shop.get('phone', 'N/A'),
        'price': price,
        'latitude': shop.get('latitude', 6.9271),
        'longitude': shop.get('longitude', 79.8612),
        'social_rating': shop.get('social_rating', 'N/A'),
        'address': shop.get('address', shop.get('location', 'N/A'))
    }
