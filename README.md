# AutoXpert - Vehicle Damage Identification & Repair Shop Recommendation

A comprehensive Streamlit application for vehicle damage identification, tire condition analysis, and market price prediction using AI models.

## 🚀 Features

1. **Damage Detection**: Upload vehicle damage images to identify dents or scratches
2. **Tire Analysis**: Predict tire condition, replacement time, and remaining safe distance
3. **Market Price Prediction**: Get accurate vehicle valuation based on brand, year, and condition

## 📋 Prerequisites

- Python 3.8 or higher
- OpenRouter API key (for AI model access)
- Internet connection

## 🛠️ Installation & Setup

### Step 1: Create Project Folder

1. Open your terminal/command prompt
2. Navigate to your desired location:
   ```bash
   cd "C:\Users\Manoj Aberathna\Desktop\New folder"
   ```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up OpenRouter API Key

1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Create a `.streamlit/secrets.toml` file in your project root:

**Windows:**
```bash
mkdir .streamlit
```

**Create `secrets.toml` file:**
```toml
OPENROUTER_API_KEY = "your-api-key-here"
```

**OR** set as environment variable:
```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="your-api-key-here"

# Windows CMD
set OPENROUTER_API_KEY=your-api-key-here

# Mac/Linux
export OPENROUTER_API_KEY="your-api-key-here"
```

## 🏃 Running Locally

### Method 1: Using Streamlit Command

```bash
streamlit run app.py
```

### Method 2: Using Python

```bash
python -m streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 📁 Project Structure

```
AutoXpert/
│
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .streamlit/
│   └── secrets.toml      # API keys (create this)
│
└── pages/
    ├── __init__.py
    ├── home.py           # Landing page with animation
    ├── damage_detection.py  # Damage identification component
    ├── tire_analysis.py     # Tire condition analysis
    └── market_price.py      # Market price prediction
```

## 🚀 Deployment to Streamlit Cloud

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Sign up or log in
3. Click "New repository"
4. Name it: `autoxpert-app`
5. Make it **Public** (required for free Streamlit Cloud)
6. Click "Create repository"

### Step 2: Upload Your Code

**Option A: Using GitHub Desktop**
1. Download [GitHub Desktop](https://desktop.github.com/)
2. Clone your repository
3. Copy all project files to the repository folder
4. Commit and push

**Option B: Using Git Command Line**

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AutoXpert app"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/autoxpert-app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `autoxpert-app`
5. Branch: `main`
6. Main file path: `app.py`
7. Click "Deploy"

### Step 4: Add Secrets to Streamlit Cloud

1. In your Streamlit Cloud app dashboard
2. Click "Settings" (⚙️ icon)
3. Go to "Secrets" tab
4. Add your OpenRouter API key:

```toml
OPENROUTER_API_KEY = "your-api-key-here"
```

5. Click "Save"
6. Your app will automatically redeploy

## 📱 How to Use the App

### 1. Landing Page
- View the animated welcome screen
- Click "Let's Go" to start

### 2. Damage Detection
- Upload a clear image of vehicle damage
- System identifies if it's a dent or scratch
- Get repair recommendations

### 3. Tire Analysis
- Upload a side view of your tire
- Get condition assessment
- See remaining safe distance
- Know when to replace

### 4. Market Price
- Select vehicle brand (Toyota, Mitsubishi, Suzuki)
- Enter model year and mileage
- Upload vehicle image
- Get market value estimate

## 🔧 Troubleshooting

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "API key not found"
**Solution:** 
- Check `.streamlit/secrets.toml` file exists
- Verify API key is correct
- For Streamlit Cloud, add key in Settings > Secrets

### Issue: "App won't start"
**Solution:**
- Check Python version: `python --version` (should be 3.8+)
- Make sure you're in the project directory
- Try: `streamlit run app.py --server.port 8501`

### Issue: "Image upload not working"
**Solution:**
- Check file format (PNG, JPG, JPEG only)
- Ensure image file size is reasonable (< 10MB)
- Try a different image

## 💡 Customization

### Change Colors
Edit the CSS in each page file (`pages/*.py`) to change color schemes.

### Add More Brands
Edit `pages/market_price.py` and add brands to the selectbox:
```python
brand = st.selectbox(
    "Select Brand",
    ["Toyota", "Mitsubishi", "Suzuki", "Honda", "Nissan"],  # Add more here
)
```

### Modify Models
Change the OpenRouter model in each analysis function:
```python
"model": "openai/gpt-4-vision-preview"  # Change to your preferred model
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
3. Check OpenRouter documentation: [openrouter.ai/docs](https://openrouter.ai/docs)

## 📄 License

This project is open source and available for educational purposes.

## 🎉 You're All Set!

Your AutoXpert app is ready to use. Start by running it locally, then deploy to Streamlit Cloud for the world to see!

---

**Happy Coding! 🚗✨**

