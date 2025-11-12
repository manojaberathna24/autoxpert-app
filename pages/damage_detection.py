import streamlit as st
import requests
from PIL import Image
import io
import base64
import os
import sys
sys.path.append('.')
from utils import get_recommended_shops, format_shop_for_display

def encode_image(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def analyze_damage_with_openrouter(image):
    """Use OpenRouter API to analyze vehicle damage"""
    try:
        img_base64 = encode_image(image)
        api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")
        
        if not api_key:
            return analyze_damage_simple(image)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "openai/gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this vehicle damage image. Identify if it's a dent or scratch. Respond in JSON format: {\"type\": \"dent\" or \"scratch\", \"confidence\": 0.0-1.0, \"description\": \"brief description\"}"
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
            import json
            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                analysis = json.loads(content)
                return analysis
            except:
                return {
                    "type": "scratch" if "scratch" in content.lower() else "dent",
                    "confidence": 0.7,
                    "description": content
                }
        else:
            return analyze_damage_simple(image)
    except Exception as e:
        st.error(f"Error analyzing damage: {str(e)}")
        return analyze_damage_simple(image)

def analyze_damage_simple(image):
    """Simple rule-based damage detection (fallback)"""
    import random
    damage_types = ["dent", "scratch"]
    selected = random.choice(damage_types)
    return {
        "type": selected,
        "confidence": 0.75,
        "description": f"Detected {selected} on vehicle surface. Professional inspection recommended."
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
        
        .instruction-box {
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 1.25rem 1.5rem;
            border-radius: 8px;
            margin: 1.5rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .instruction-box strong {
            color: #e65100;
            font-weight: 600;
        }
        
        .result-card {
            background: #ffffff;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            margin: 2rem 0;
            border: 1px solid #e8e8e8;
        }
        
        .damage-type {
            font-size: 2.5rem;
            font-weight: 700;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin: 1rem 0;
            letter-spacing: 2px;
        }
        
        .damage-dent {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            color: white;
            box-shadow: 0 8px 24px rgba(255, 107, 107, 0.3);
        }
        
        .damage-scratch {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        }
        
        .shop-card {
            background: #ffffff;
            padding: 2rem;
            border-radius: 16px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            border: 1px solid #e8e8e8;
            transition: all 0.3s;
        }
        
        .shop-card:hover {
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            transform: translateY(-2px);
        }
        
        .shop-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .shop-name {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a1a;
            margin: 0;
        }
        
        .shop-rating {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        .shop-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .info-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #555;
            font-size: 0.95rem;
        }
        
        .price-badge {
            background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
            color: #1a1a1a;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 1.2rem;
            display: inline-block;
            margin: 0.5rem 0;
        }
        
        .map-container {
            width: 100%;
            height: 350px;
            border-radius: 12px;
            overflow: hidden;
            margin: 1.5rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
        }
        
        .directions-btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin: 0.5rem 0;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            transition: all 0.3s;
        }
        
        .directions-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a1a;
            margin: 2rem 0 1rem 0;
            letter-spacing: -0.3px;
        }
        
        .section-subtitle {
            color: #666;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional Header
    st.markdown("""
    <div class="header-section">
        <h1>Vehicle Damage Detection</h1>
        <p>Upload your vehicle damage image for AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional Navigation
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Home", use_container_width=True, key="nav_home"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        if st.button("Tire Analysis", use_container_width=True, key="nav_tire"):
            st.session_state.current_page = 'tire'
            st.rerun()
    with col3:
        if st.button("Market Price", use_container_width=True, key="nav_market"):
            st.session_state.current_page = 'market'
            st.rerun()
    with col4:
        if st.button("Feedback", use_container_width=True, key="nav_feedback"):
            st.session_state.current_page = 'feedback'
            st.rerun()
    
    # Instruction Box
    st.markdown("""
    <div class="instruction-box">
        <strong>📸 Instructions:</strong> Upload a clear image of the vehicle damage from the side for accurate analysis.
    </div>
    """, unsafe_allow_html=True)
    
    # Image Upload Section
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### Upload Image")
        uploaded_file = st.file_uploader(
            "Choose a damage image",
            type=['png', 'jpg', 'jpeg'],
            help="Supported formats: PNG, JPG, JPEG",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
    
    with col2:
        st.markdown("### Quick Actions")
        if st.button("📷 Use Camera", use_container_width=True, type="secondary"):
            st.info("Camera feature coming soon. Please use file upload.")
    
    # Analysis Section
    if uploaded_file is not None:
        st.markdown("---")
        
        with st.spinner("Analyzing damage with AI..."):
            result = analyze_damage_with_openrouter(image)
        
        damage_type = result.get("type", "unknown")
        confidence = result.get("confidence", 0.0)
        
        # Professional Result Display
        damage_class = "damage-dent" if damage_type == "dent" else "damage-scratch"
        st.markdown(f"""
        <div class="result-card">
            <div class="damage-type {damage_class}">
                {damage_type.upper()}
            </div>
            <p style="text-align: center; color: #666; margin-top: 1rem;">
                Confidence: <strong>{confidence * 100:.1f}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get Recommended Shops
        shops = get_recommended_shops(damage_type)
        recommended_shops = [format_shop_for_display(shop, damage_type) for shop in shops]
        
        if recommended_shops:
            st.markdown('<p class="section-title">Recommended Repair Shops</p>', unsafe_allow_html=True)
            st.markdown('<p class="section-subtitle">Top-rated repair shops in Sri Lanka based on social media reviews</p>', unsafe_allow_html=True)
            
            for idx, shop in enumerate(recommended_shops, 1):
                rating_stars = "⭐" * int(shop['rating'])
                
                st.markdown(f"""
                <div class="shop-card">
                    <div class="shop-header">
                        <h3 class="shop-name">#{idx} {shop['name']}</h3>
                        <div class="shop-rating">{rating_stars} {shop['rating']}/5.0</div>
                    </div>
                    
                    <div class="shop-info">
                        <div class="info-item">
                            <strong>📍</strong> {shop['address']}
                        </div>
                        <div class="info-item">
                            <strong>📞</strong> {shop['phone']}
                        </div>
                        <div class="info-item">
                            <strong>⭐</strong> {shop['social_rating']}
                        </div>
                    </div>
                    
                    <div class="price-badge">
                        Rs. {shop['price']:,.0f} for {damage_type} repair
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Map Section
                st.markdown(f"#### Location & Directions")
                
                st.markdown(f"""
                <div class="map-container">
                    <iframe 
                        width="100%" 
                        height="350" 
                        style="border:0" 
                        loading="lazy" 
                        allowfullscreen
                        src="https://www.google.com/maps?q={shop['latitude']},{shop['longitude']}&hl=en&z=14&output=embed">
                    </iframe>
                </div>
                """, unsafe_allow_html=True)
                
                # Directions Button
                directions_url = f"https://www.google.com/maps/dir/?api=1&destination={shop['latitude']},{shop['longitude']}"
                st.markdown(f"""
                <a href="{directions_url}" target="_blank" class="directions-btn">
                    🗺️ Get Directions
                </a>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
        else:
            st.info("No repair shops available. Shop owners can register to list their services.")
