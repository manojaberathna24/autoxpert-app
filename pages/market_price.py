import streamlit as st
import requests
from PIL import Image
import io
import base64
import os
import json

def encode_image(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def predict_price_with_openrouter(image, brand, model_year=None, mileage=None):
    """Use OpenRouter API to predict vehicle market price"""
    try:
        img_base64 = encode_image(image)
        api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")
        
        if not api_key:
            return predict_price_simple(brand, model_year, mileage)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        context = f"Brand: {brand}"
        if model_year:
            context += f", Model Year: {model_year}"
        if mileage:
            context += f", Mileage: {mileage} km"
        
        payload = {
            "model": "openai/gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Analyze this vehicle image and estimate its market value. 
                            Context: {context}
                            Consider the vehicle's condition, age, brand, and market factors.
                            Respond in JSON format: {{
                                "estimated_price": number in USD,
                                "price_range_min": minimum estimate,
                                "price_range_max": maximum estimate,
                                "condition": "excellent/good/fair/poor",
                                "factors": ["list of factors affecting price"],
                                "description": "detailed analysis"
                            }}"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                analysis = json.loads(content)
                return analysis
            except:
                return predict_price_simple(brand, model_year, mileage)
        else:
            return predict_price_simple(brand, model_year, mileage)
    except Exception as e:
        st.error(f"Error predicting price: {str(e)}")
        return predict_price_simple(brand, model_year, mileage)

def predict_price_simple(brand, model_year=None, mileage=None):
    """Simple price prediction based on brand (fallback)"""
    import random
    
    # Base prices by brand (in USD)
    base_prices = {
        "Toyota": 15000,
        "Mitsubishi": 12000,
        "Suzuki": 8000
    }
    
    base = base_prices.get(brand, 10000)
    
    # Adjust for model year
    if model_year:
        current_year = 2024
        age = current_year - model_year
        depreciation = base * (age * 0.1)  # 10% per year
        base = max(base - depreciation, base * 0.3)  # Minimum 30% of base
    
    # Adjust for mileage
    if mileage:
        mileage_depreciation = base * (mileage / 200000) * 0.3  # Up to 30% for high mileage
        base = max(base - mileage_depreciation, base * 0.5)
    
    # Add some randomness
    price = base * random.uniform(0.9, 1.1)
    min_price = price * 0.85
    max_price = price * 1.15
    
    conditions = ["excellent", "good", "fair", "poor"]
    condition = random.choice(["excellent", "good"]) if price > base * 0.9 else random.choice(["fair", "poor"])
    
    return {
        "estimated_price": round(price, 0),
        "price_range_min": round(min_price, 0),
        "price_range_max": round(max_price, 0),
        "condition": condition,
        "factors": [
            f"Brand: {brand}",
            f"Model Year: {model_year or 'Unknown'}",
            f"Mileage: {mileage or 'Unknown'} km",
            f"Condition: {condition}"
        ],
        "description": f"Estimated market value for {brand} vehicle based on provided information."
    }

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
        
        .price-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2.5rem;
            border-radius: 16px;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .price-amount {
            font-size: 3.5rem;
            font-weight: 800;
            margin: 1rem 0;
            letter-spacing: -1px;
        }
        
        .price-range {
            font-size: 1.1rem;
            opacity: 0.95;
            font-weight: 400;
        }
        
        .factor-box {
            background: #ffffff;
            padding: 1.25rem 1.5rem;
            border-radius: 10px;
            margin: 0.75rem 0;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            color: #333;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional Header
    st.markdown("""
    <div class="header-section">
        <h1>Vehicle Market Price Prediction</h1>
        <p>AI-powered vehicle valuation based on brand, condition, and market data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional Navigation
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Home", use_container_width=True, key="nav_market_home"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        if st.button("Damage Detection", use_container_width=True, key="nav_market_damage"):
            st.session_state.current_page = 'damage'
            st.rerun()
    with col3:
        if st.button("Tire Analysis", use_container_width=True, key="nav_market_tire"):
            st.session_state.current_page = 'tire'
            st.rerun()
    with col4:
        if st.button("Feedback", use_container_width=True, key="nav_market_feedback"):
            st.session_state.current_page = 'feedback'
            st.rerun()
    
    # Vehicle Information Form
    st.markdown("### Vehicle Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        brand = st.selectbox(
            "Select Brand",
            ["Toyota", "Mitsubishi", "Suzuki"],
            help="Select your vehicle brand"
        )
    
    with col2:
        model_year = st.number_input(
            "Model Year",
            min_value=1990,
            max_value=2024,
            value=2020,
            step=1,
            help="Enter the model year of your vehicle"
        )
    
    with col3:
        mileage = st.number_input(
            "Mileage (km)",
            min_value=0,
            max_value=500000,
            value=50000,
            step=1000,
            help="Enter current mileage in kilometers"
        )
    
    # Image Upload Section
    st.markdown("### Upload Vehicle Image")
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a vehicle image",
            type=['png', 'jpg', 'jpeg'],
            key="vehicle_upload",
            help="Supported formats: PNG, JPG, JPEG",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Vehicle Image", use_container_width=True)
    
    with col2:
        st.markdown("### Quick Actions")
        if st.button("📷 Use Camera", use_container_width=True, type="secondary", key="vehicle_camera"):
            st.info("Camera feature coming soon. Please use file upload.")
    
    # Price Prediction
    if uploaded_file is not None:
        st.markdown("---")
        st.markdown('<p style="font-size: 1.5rem; font-weight: 700; color: #1a1a1a; margin: 2rem 0 1rem 0;">Price Prediction</p>', unsafe_allow_html=True)
        
        with st.spinner("Analyzing vehicle and predicting market price..."):
            result = predict_price_with_openrouter(image, brand, model_year, mileage)
        
        estimated_price = result.get("estimated_price", 0)
        min_price = result.get("price_range_min", 0)
        max_price = result.get("price_range_max", 0)
        condition = result.get("condition", "unknown")
        factors = result.get("factors", [])
        description = result.get("description", "No description available")
        
        # Professional Price Display
        st.markdown(f"""
        <div class="price-card">
            <h2 style="margin: 0 0 1rem 0; font-size: 1.5rem; font-weight: 600;">Estimated Market Value</h2>
            <div class="price-amount">${estimated_price:,.0f}</div>
            <div class="price-range">Range: ${min_price:,.0f} - ${max_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Condition Badge
        condition_colors = {
            "excellent": "#4caf50",
            "good": "#2196f3",
            "fair": "#ff9800",
            "poor": "#f44336"
        }
        condition_color = condition_colors.get(condition, "#666")
        st.markdown(f"""
        <div style="background: {condition_color}; color: white; padding: 0.75rem 1.5rem; border-radius: 8px; display: inline-block; font-weight: 600; margin: 1rem 0;">
            Condition: {condition.capitalize()}
        </div>
        """, unsafe_allow_html=True)
        
        # Factors
        st.markdown("### Price Factors")
        for factor in factors:
            st.markdown(f'<div class="factor-box">{factor}</div>', unsafe_allow_html=True)
        
        # Description
        st.markdown("### Analysis")
        st.info(description)
        
        # Recommendations
        st.markdown("### Recommendations")
        if condition == "excellent":
            st.success("""
            Your vehicle is in excellent condition! 
            - Consider getting a professional inspection for maximum value
            - Maintain service records to justify premium pricing
            - Market timing is favorable for selling
            """)
        elif condition == "good":
            st.info("""
            Your vehicle is in good condition.
            - Minor improvements could increase value by 5-10%
            - Clean and detail the vehicle before selling
            - Consider getting a pre-sale inspection
            """)
        else:
            st.warning("""
            Your vehicle may need some attention.
            - Consider repairs if cost is less than value increase
            - Be transparent about condition when selling
            - Price competitively based on condition
            """)

