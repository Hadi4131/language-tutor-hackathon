# 🗣️ AI Language Tutor

An AI-powered English language learning application with real-time pronunciation feedback, grammar corrections, and personalized learning tips.

## ✨ Features

- 🎤 **Voice Recognition** - Real-time speech-to-text using Google Cloud Speech API
- 📊 **Pronunciation Scoring** - Get 0-100 scores with phoneme-level analysis
- 🧠 **AI Grammar Feedback** - Powered by Google Gemini 2.5 Flash
- 🔊 **Natural Voice Responses** - ElevenLabs text-to-speech
- 🔐 **User Authentication** - Firebase Auth (Email/Password + Google Sign-In)
- 💬 **Personalized Learning** - Tips and follow-up questions tailored to your level

## 🚀 Tech Stack

### Frontend
- React + Vite
- Firebase Authentication
- Tailwind CSS
- Axios for API calls
- Animated UI with wavy backgrounds

### Backend
- FastAPI (Python)
- Google Cloud Speech-to-Text
- Google Gemini AI
- ElevenLabs API
- MongoDB Atlas
- Firebase Admin SDK

## 📋 Prerequisites

Before you begin, you need:

1. **Firebase Project** - [Create one here](https://console.firebase.google.com)
2. **Google Cloud Project** - For Speech-to-Text and Gemini API
3. **ElevenLabs Account** - [Sign up here](https://elevenlabs.io)
4. **MongoDB Atlas** - [Free tier available](https://www.mongodb.com/cloud/atlas)

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-language-tutor.git
cd ai-language-tutor
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
```

**Required Environment Variables:**
- `GOOGLE_API_KEY` - From Google Cloud Console
- `ELEVENLABS_API_KEY` - From ElevenLabs dashboard
- `MONGODB_URI` - From MongoDB Atlas
- Download Firebase Admin SDK JSON and save as `firebase-admin-sdk.json`

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Edit .env.local and add your Firebase config
```

Get Firebase config from: Firebase Console → Project Settings → Your apps → Web app

### 4. Enable Firebase Authentication

1. Go to Firebase Console → Authentication
2. Enable **Email/Password** provider
3. Enable **Google** provider (add support email)

### 5. Run the Application

**Backend:**
```bash
cd backend
python main.py
```
Backend runs on http://localhost:8000

**Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs on http://localhost:5173

## 🌐 Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions on deploying to production.

**Quick Deploy:**
- Backend → [Render](https://render.com) (free tier)
- Frontend → [Vercel](https://vercel.com) (free tier)

## 🔒 Security Notes

**⚠️ NEVER commit these files:**
- `.env` files
- `firebase-admin-sdk.json`
- Any file containing API keys

These are already listed in `.gitignore`

**For Deployment:**
- Add environment variables in Render/Vercel dashboards
- Upload Firebase Admin SDK as a secret file in Render

## 📖 Usage

1. Visit http://localhost:5173
2. Sign up with email/password or Google
3. Click the microphone button
4. Speak in English
5. Get instant AI feedback on:
   - Pronunciation (0-100 score)
   - Grammar corrections
   - Learning tips
   - Follow-up questions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Cloud (Speech-to-Text, Gemini AI)
- ElevenLabs (Text-to-Speech)
- Firebase (Authentication)
- MongoDB Atlas (Database)

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**Built for the Google AI Hackathon 2024** 🚀
