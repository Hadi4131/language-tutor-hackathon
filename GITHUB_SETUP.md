# GitHub Setup Guide

## 🔒 Security is Set Up!

I've created `.gitignore` files to protect your API keys:
- ✅ `.env` files are ignored
- ✅ `firebase-admin-sdk.json` is ignored
- ✅ Created `.env.example` templates for documentation

**Your secrets are safe!** They will NOT be uploaded to GitHub.

---

## 📤 Upload to GitHub (Manual Method)

Since Git is not installed on your system, follow these steps to create a GitHub repository:

### Step 1: Create GitHub Repository

1. Go to https://github.com
2. Sign in (or create account)
3. Click the **"+"** icon (top right) → **"New repository"**
4. Fill in:
   - **Repository name**: `ai-language-tutor` (or your choice)
   - **Description**: "AI-powered English learning app with voice feedback"
   - **Visibility**: Public or Private
   - **DO NOT** initialize with README (we already have one)
5. Click **"Create repository"**

### Step 2: Prepare Your Files

1. **Delete these files** from your project folder (they contain secrets):
   ```
   backend/.env
   backend/firebase-admin-sdk.json
   frontend/.env.local
   frontend/.env.production
   ```

2. **Verify .gitignore files exist:**
   - `.gitignore` (root)
   - `backend/.gitignore`
   - `frontend/.gitignore`

### Step 3: Upload to GitHub

**Option A: Using GitHub Web Interface**
1. On your new GitHub repository page, click **"uploading an existing file"**
2. Drag and drop your **entire project folder**
3. Add commit message: "Initial commit: AI Language Tutor"
4. Click **"Commit changes"**

**Option B: Install Git and Use Commands**
1. Download Git: https://git-scm.com/downloads
2. After installing, restart PowerShell
3. Run these commands:
   ```bash
   cd "c:\Users\Sayed\Downloads\Google AI Hackathon"
   git init
   git add .
   git commit -m "Initial commit: AI Language Tutor"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ai-language-tutor.git
   git push -u origin main
   ```

---

## 🚀 After Uploading to GitHub

### Deploy Backend to Render

1. Go to https://render.com
2. Click **"New +"** → **"Web Service"**
3. Choose **"Build and deploy from Git repository"**
4. **Connect your GitHub** account
5. **Select** your `ai-language-tutor` repository
6. Configure:
   - **Name**: `language-tutor-backend`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. **Add Environment Variables** (from your local `.env` file):
   ```
   GOOGLE_API_KEY=<your_key>
   ELEVENLABS_API_KEY=<your_key>
   MONGODB_URI=<your_uri>
   GOOGLE_APPLICATION_CREDENTIALS=./firebase-admin-sdk.json
   FIREBASE_ADMIN_SDK_PATH=./firebase-admin-sdk.json
   ```
8. **Add Secret File** (Environment tab → Secret Files):
   - Filename: `firebase-admin-sdk.json`
   - Content: Copy-paste from your local file
9. Click **"Create Web Service"**
10. **Copy your backend URL**: `https://your-app.onrender.com`

### Deploy Frontend to Vercel

1. Go to https://vercel.com
2. Click **"Add New..."** → **"Project"**
3. **Import** your GitHub repository
4. Configure:
   - **Framework**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. **Add Environment Variables** (from your local `.env.local`):
   ```
   VITE_API_URL=<your_render_backend_url>
   VITE_FIREBASE_API_KEY=<your_key>
   VITE_FIREBASE_AUTH_DOMAIN=<your_domain>
   VITE_FIREBASE_PROJECT_ID=<your_id>
   VITE_FIREBASE_STORAGE_BUCKET=<your_bucket>
   VITE_FIREBASE_MESSAGING_SENDER_ID=<your_id>
   VITE_FIREBASE_APP_ID=<your_id>
   ```
6. Click **"Deploy"**
7. **Get your app URL**: `https://your-app.vercel.app`

### Update Firebase

1. Firebase Console → Authentication → Settings → Authorized domains
2. Add: `your-app.vercel.app`

---

## ✅ Verification

After deployment:
- [ ] Backend running on Render
- [ ] Frontend deployed on Vercel
- [ ] Can access app URL
- [ ] Firebase auth works
- [ ] Voice practice works

---

## 🔑 Security Reminders

**Files that ARE uploaded to GitHub:**
- ✅ All source code
- ✅ `.gitignore` files
- ✅ `.env.example` templates
- ✅ `README.md`, `DEPLOYMENT.md`

**Files that are NOT uploaded (protected by .gitignore):**
- ❌ `.env` files
- ❌ `firebase-admin-sdk.json`
- ❌ `node_modules/`
- ❌ `__pycache__/`

**When deploying:**
- Add environment variables in Render/Vercel dashboards
- Never paste API keys in GitHub issues or pull requests
- Use secret files feature in Render for Firebase SDK

---

## 📞 Need Help?

- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment steps
- Check [README.md](./README.md) for setup instructions
- Open an issue on GitHub if you encounter problems
