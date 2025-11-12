"""
Quick setup verification script
Run this to check if everything is set up correctly
"""

import sys
import importlib

def check_imports():
    """Check if all required packages are installed"""
    print("🔍 Checking required packages...")
    
    required_packages = {
        'streamlit': 'Streamlit',
        'PIL': 'Pillow',
        'requests': 'Requests',
        'numpy': 'NumPy'
    }
    
    missing = []
    for module, name in required_packages.items():
        try:
            importlib.import_module(module)
            print(f"  ✅ {name} installed")
        except ImportError:
            print(f"  ❌ {name} NOT installed")
            missing.append(name)
    
    return len(missing) == 0

def check_files():
    """Check if all required files exist"""
    print("\n📁 Checking project files...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'pages/__init__.py',
        'pages/home.py',
        'pages/damage_detection.py',
        'pages/tire_analysis.py',
        'pages/market_price.py'
    ]
    
    import os
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file} exists")
        else:
            print(f"  ❌ {file} NOT found")
            missing.append(file)
    
    return len(missing) == 0

def check_api_key():
    """Check if API key is configured"""
    print("\n🔑 Checking API key configuration...")
    
    import os
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    
    # Try to read from secrets file
    try:
        import streamlit as st
        from pathlib import Path
        secrets_path = Path(".streamlit/secrets.toml")
        if secrets_path.exists():
            print("  ✅ .streamlit/secrets.toml file exists")
            # Try to read it
            try:
                import toml
                secrets = toml.load(secrets_path)
                if secrets.get("OPENROUTER_API_KEY"):
                    print("  ✅ API key found in secrets.toml")
                    return True
                else:
                    print("  ⚠️  secrets.toml exists but no API key found")
            except:
                print("  ⚠️  Could not read secrets.toml (toml package may be missing)")
        else:
            print("  ⚠️  .streamlit/secrets.toml not found")
    except:
        pass
    
    if api_key:
        print("  ✅ API key found in environment variable")
        return True
    else:
        print("  ⚠️  No API key found (set OPENROUTER_API_KEY or create .streamlit/secrets.toml)")
        return False

def main():
    print("=" * 50)
    print("AutoXpert Setup Verification")
    print("=" * 50)
    
    packages_ok = check_imports()
    files_ok = check_files()
    api_key_ok = check_api_key()
    
    print("\n" + "=" * 50)
    print("Summary:")
    print("=" * 50)
    
    if packages_ok and files_ok:
        print("✅ All packages and files are ready!")
        if api_key_ok:
            print("✅ API key is configured!")
            print("\n🎉 You're ready to run the app!")
            print("   Run: streamlit run app.py")
        else:
            print("⚠️  API key not configured (app will use fallback mode)")
            print("   Get your key from: https://openrouter.ai/")
            print("   Then create .streamlit/secrets.toml with your key")
    else:
        print("❌ Some issues found. Please fix them before running the app.")
        if not packages_ok:
            print("   Install missing packages: pip install -r requirements.txt")
        if not files_ok:
            print("   Some project files are missing")
    
    print("=" * 50)

if __name__ == "__main__":
    main()

