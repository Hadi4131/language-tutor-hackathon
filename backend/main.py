from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from database.mongo import db
from api.conversation import router as conversation_router
from api.gamification import router as gamification_router
from api.personality import router as personality_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db.connect()
    yield
    # Shutdown
    db.close()

app = FastAPI(title="Language Learning Companion API", lifespan=lifespan)

# CORS Middleware - MUST be before routes
# Allow frontend URLs (both local and production)
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "https://*.vercel.app",  # Vercel deployments
    "https://*.vercel.com",
]

# Add specific production URL if set
production_frontend = os.getenv("FRONTEND_URL")
if production_frontend:
    allowed_origins.append(production_frontend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow all Vercel subdomains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(conversation_router, prefix="/api/v1")
app.include_router(gamification_router, prefix="/api/v1")
app.include_router(personality_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Language Learning Companion API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
