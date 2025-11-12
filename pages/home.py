import streamlit as st

def show():
    st.markdown("""
    <style>
        @keyframes fadeInUp {
            from { 
                opacity: 0; 
                transform: translateY(30px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }
        
        .hero-container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            position: relative;
            overflow: hidden;
        }
        
        .hero-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M 100 0 L 0 0 0 100" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }
        
        .app-title {
            font-size: 4.5rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 1rem;
            letter-spacing: -1px;
            animation: fadeInUp 1s ease-out;
            z-index: 10;
            position: relative;
            text-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }
        
        .app-tagline {
            font-size: 1.5rem;
            color: rgba(255,255,255,0.9);
            margin-bottom: 3rem;
            animation: fadeInUp 1.2s ease-out;
            z-index: 10;
            position: relative;
            font-weight: 400;
            letter-spacing: 0.5px;
        }
        
        .video-container {
            width: 100%;
            max-width: 600px;
            margin: 2.5rem auto;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 12px 40px rgba(0,0,0,0.3);
            z-index: 10;
            position: relative;
            background: #000;
            aspect-ratio: 9 / 16;
        }
        
        .video-container iframe {
            width: 100%;
            height: 100%;
            border: none;
            display: block;
        }
        
        .lets-go-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.2rem 4rem;
            font-size: 1.1rem;
            font-weight: 600;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
            animation: fadeInUp 1.5s ease-out;
            z-index: 10;
            position: relative;
            letter-spacing: 0.5px;
            text-transform: none;
        }
        
        .lets-go-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(102, 126, 234, 0.5);
        }
        
        .lets-go-btn:active {
            transform: translateY(-1px);
        }
        
        .menu-container {
            width: 100%;
            max-width: 800px;
            margin: 2rem auto;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            z-index: 10;
            position: relative;
            animation: fadeInUp 0.5s ease-out;
        }
        
        .menu-title {
            font-size: 2rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .menu-buttons {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
            margin-top: 1rem;
        }
        
        .menu-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            text-align: center;
        }
        
        .menu-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize menu state
    if 'show_menu' not in st.session_state:
        st.session_state.show_menu = False
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="app-title">AutoXpert</h1>
        <p class="app-tagline">Smart Solutions for Your Vehicle Needs</p>
        
        <div class="video-container">
            <iframe 
                src="https://www.youtube.com/embed/3Q7Dpjjgt9w" 
                title="AutoXpert Animation"
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Let's Go Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Let's Go", key="lets_go", use_container_width=True, type="primary"):
            st.session_state.show_menu = True
            st.rerun()
    
    # Show Menu when Let's Go is clicked - All 4 buttons visible
    if st.session_state.show_menu:
        st.markdown("""
        <div class="menu-container">
            <h2 class="menu-title">Choose Your Service</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # All 4 buttons in a 2x2 grid - all always visible
        st.markdown("### Select a Service")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚗 Damage Detection", use_container_width=True, key="menu_damage", type="primary"):
                st.session_state.current_page = 'damage'
                st.rerun()
            
            if st.button("🛞 Tire Analysis", use_container_width=True, key="menu_tire", type="primary"):
                st.session_state.current_page = 'tire'
                st.rerun()
        
        with col2:
            if st.button("💰 Market Price", use_container_width=True, key="menu_market", type="primary"):
                st.session_state.current_page = 'market'
                st.rerun()
            
            if st.button("💬 Feedback", use_container_width=True, key="menu_feedback", type="primary"):
                st.session_state.current_page = 'feedback'
                st.rerun()
