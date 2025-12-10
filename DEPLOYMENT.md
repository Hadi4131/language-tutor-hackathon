# AI Language Tutor - Deployment Guide

## 🚀 Quick Deployment Steps

### Step 1: Deploy Backend to Render

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub (recommended) or email

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Choose "Build and deploy from a Git repository"
   - Connect your GitHub account
   - Select your repository
   - OR use "Deploy from local" and upload manually

3. **Configure Service**
   - **Name**: `language-tutor-backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables** (Click "Environment" tab)
   ```
   GOOGLE_API_KEY=<your_google_api_key>
   ELEVENLABS_API_KEY=<your_elevenlabs_key>
   MONGODB_URI=<your_mongodb_atlas_uri>
   FIREBASE_ADMIN_SDK_PATH=./firebase-admin-sdk.json
   GOOGLE_APPLICATION_CREDENTIALS=./firebase-admin-sdk.json
   ```

5. **Upload Firebase Admin SDK**
   - In "Environment" tab, scroll to "Secret Files"
   - Click "Add Secret File"
   - Filename: `firebase-admin-sdk.json`
   - Copy-paste contents from your local `backend/firebase-admin-sdk.json`
   - Save

6. **Deploy!**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - **Copy your backend URL**: `https://language-tutor-backend-xxxx.onrender.com`

---

### Step 2: Deploy Frontend to Vercel

1. **Update .env.production**
   - Open `frontend/.env.production`
   - Replace `VITE_API_URL` with your Render backend URL from Step 1
   - Copy Firebase config from `.env.local`
   
   Example:
   ```
   VITE_API_URL=https://language-tutor-backend-xxxx.onrender.com
   VITE_FIREBASE_API_KEY=AIzaSy...
   VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   ... (rest of Firebase config)
   ```

2. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub

3. **Import Project**
   - Click "Add New..." → "Project"
   - Import your Git repository
   - OR drag & drop the `frontend` folder

4. **Configure Project**
   - **Framework Preset**: Vite
   - **Root Directory**: `./frontend` (if deploying whole repo)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. **Add Environment Variables**
   - In project settings, go to "Environment Variables"
   - Add all variables from `.env.production`
   - Make sure each variable is added for "Production" environment

6. **Deploy!**
   - Click "Deploy"
   - Wait for build (2-5 minutes)
   - **Get your live URL**: `https://your-app.vercel.app`

---

### Step 3: Configure Firebase for Production

1. **Add Authorized Domains**
   - Go to Firebase Console → Authentication → Settings
   - Scroll to "Authorized domains"
   - Click "Add domain"
   - Add your Vercel domain: `your-app.vercel.app`
   - Save

2. **Test Your App!**
   - Visit your Vercel URL
   - Try signing up with email/password
   - Try Google Sign-In
   - Test voice practice feature

---

## 📝 Post-Deployment Checklist

- [ ] Backend deployed to Render and running
- [ ] Frontend deployed to Vercel
- [ ] Firebase authorized domains updated
- [ ] Can sign up with email/password
- [ ] Can login with Google
- [ ] Voice practice works end-to-end
- [ ] Test on mobile device

---

## ⚠️ Important Notes

**Free Tier Limitations:**
- Render free tier: Backend sleeps after 15min inactivity
- First request after sleep takes ~30 seconds
- This is normal - subsequent requests are fast

**If Backend Doesn't Wake:**
- Check Render logs for errors
- Verify all environment variables are set
- Ensure Firebase Admin SDK file is uploaded

**If Frontend Shows Errors:**
- Check browser console for errors
- Verify VITE_API_URL is set correctly
- Ensure CORS is allowing your Vercel domain

---

## 🎉 Share Your App!

Once deployed, share your app URL:
`https://your-app.vercel.app`

Anyone can now:
- Sign up for an account
- Practice English with AI
- Get pronunciation feedback
- Improve their language skills!
