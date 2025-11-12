# Complete Deployment Guide - Step by Step

## 🎯 Overview
This guide will take you from zero to a fully deployed Streamlit application.

---

## Part 1: Local Setup (0 to Running Locally)

### Step 1: Verify Python Installation

**Check if Python is installed:**
```bash
python --version
```

**If not installed:**
1. Download from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation again

### Step 2: Open Project Folder

**Windows:**
1. Open File Explorer
2. Navigate to: `C:\Users\Manoj Aberathna\Desktop\New folder`
3. Right-click in the folder → "Open in Terminal" or "Open PowerShell here"

**Or use Command Prompt:**
```bash
cd "C:\Users\Manoj Aberathna\Desktop\New folder"
```

### Step 3: Create Virtual Environment

**Windows PowerShell:**
```powershell
python -m venv venv
```

**Activate it:**
```powershell
.\venv\Scripts\Activate.ps1
```

**If you get an error about execution policy:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Then activate again:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**You should see `(venv)` in your terminal prompt now!**

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Wait for installation to complete. You should see "Successfully installed..."**

### Step 5: Get OpenRouter API Key

1. Go to [openrouter.ai](https://openrouter.ai/)
2. Click "Sign Up" (or "Log In" if you have an account)
3. After logging in, go to "Keys" section
4. Click "Create Key"
5. Copy the API key (starts with `sk-or-v1-...`)

### Step 6: Set Up API Key

**Option A: Create secrets file (Recommended for local)**

1. Create `.streamlit` folder:
   ```bash
   mkdir .streamlit
   ```

2. Create `secrets.toml` file inside `.streamlit` folder:
   ```bash
   # Windows PowerShell
   New-Item -Path .streamlit\secrets.toml -ItemType File
   
   # Or just create it manually in File Explorer
   ```

3. Open `secrets.toml` in a text editor and add:
   ```toml
   OPENROUTER_API_KEY = "your-api-key-here"
   ```
   Replace `your-api-key-here` with your actual key.

**Option B: Set Environment Variable**

**Windows PowerShell:**
```powershell
$env:OPENROUTER_API_KEY="your-api-key-here"
```

**Windows CMD:**
```cmd
set OPENROUTER_API_KEY=your-api-key-here
```

**Mac/Linux:**
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

### Step 7: Run the App Locally

```bash
streamlit run app.py
```

**What happens:**
- Streamlit starts a local server
- Your browser should open automatically
- If not, go to: `http://localhost:8501`

**You should see:**
- The AutoXpert landing page with animation
- "Let's Go" button
- Beautiful UI matching your images!

### Step 8: Test the App

1. Click "Let's Go"
2. Try uploading an image in Damage Detection
3. Test Tire Analysis
4. Test Market Price Prediction

**If everything works, you're ready to deploy!**

---

## Part 2: Deploy to Streamlit Cloud

### Step 1: Create GitHub Account

1. Go to [github.com](https://github.com)
2. Click "Sign up"
3. Choose a username, email, password
4. Verify your email

### Step 2: Create New Repository

1. After logging in, click the "+" icon (top right)
2. Click "New repository"
3. Repository name: `autoxpert-app`
4. Description: "Vehicle damage identification and repair shop recommendation app"
5. Make it **Public** (required for free Streamlit Cloud)
6. **DO NOT** check "Initialize with README" (we already have files)
7. Click "Create repository"

### Step 3: Install Git (If Not Installed)

**Check if Git is installed:**
```bash
git --version
```

**If not installed:**
1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Install with default settings
3. Restart terminal

### Step 4: Upload Code to GitHub

**In your project folder (where app.py is):**

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: AutoXpert vehicle analysis app"

# Add your GitHub repository as remote
# REPLACE YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/autoxpert-app.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**You'll be asked for GitHub username and password:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your password)

**To create Personal Access Token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Give it a name: "Streamlit Deployment"
4. Select scopes: `repo` (full control)
5. Generate and **copy the token** (you won't see it again!)
6. Use this token as password when pushing

### Step 5: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in"
3. Sign in with your GitHub account
4. Click "New app"
5. Fill in the form:
   - **Repository**: Select `autoxpert-app`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: `autoxpert-app` (or your preferred name)
6. Click "Deploy"

**Wait 2-3 minutes for deployment...**

### Step 6: Add Secrets to Streamlit Cloud

1. In Streamlit Cloud dashboard, find your app
2. Click the "⋮" (three dots) menu
3. Click "Settings"
4. Go to "Secrets" tab
5. Paste this:

```toml
OPENROUTER_API_KEY = "your-api-key-here"
```

6. Replace `your-api-key-here` with your actual OpenRouter API key
7. Click "Save"

**Your app will automatically redeploy!**

### Step 7: Access Your Live App

1. Go back to your app in Streamlit Cloud
2. Click "Open app" or visit: `https://autoxpert-app.streamlit.app`
3. **Your app is now live! 🎉**

---

## Part 3: Making Updates

### Update Code Locally

1. Make changes to your files
2. Test locally:
   ```bash
   streamlit run app.py
   ```

### Push Updates to GitHub

```bash
# Add changed files
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push
```

**Streamlit Cloud will automatically redeploy!**

---

## 🎓 Quick Reference Commands

### Local Development
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell
venv\Scripts\activate.bat    # Windows CMD
source venv/bin/activate     # Mac/Linux

# Run app
streamlit run app.py

# Install new package
pip install package-name
pip freeze > requirements.txt
```

### Git Commands
```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "Your message"

# Push
git push

# Pull updates
git pull
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "streamlit: command not found"
**Solution:**
```bash
pip install streamlit
```

### Issue 2: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue 3: "API key not working"
**Solution:**
- Check if key is correct in `.streamlit/secrets.toml`
- Verify key is active on OpenRouter dashboard
- For Streamlit Cloud, check Settings > Secrets

### Issue 4: "Port already in use"
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Issue 5: "Git push rejected"
**Solution:**
```bash
git pull origin main --rebase
git push
```

---

## ✅ Checklist

Before deploying, make sure:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] OpenRouter API key obtained
- [ ] Secrets file created (`.streamlit/secrets.toml`)
- [ ] App runs locally without errors
- [ ] GitHub account created
- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed on Streamlit Cloud
- [ ] Secrets added to Streamlit Cloud
- [ ] App works on live URL

---

## 🎉 Congratulations!

You now have:
- ✅ A working local Streamlit app
- ✅ A live deployed app on Streamlit Cloud
- ✅ Knowledge to update and maintain it

**Your AutoXpert app is ready to help users with their vehicle needs!**

---

## 📞 Need Help?

1. Check error messages carefully
2. Review this guide again
3. Check Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)
4. Check OpenRouter docs: [openrouter.ai/docs](https://openrouter.ai/docs)

**Good luck with your project! 🚗✨**

