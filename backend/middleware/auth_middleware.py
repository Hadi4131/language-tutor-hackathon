from fastapi import Header, HTTPException, Depends
import firebase_admin
from firebase_admin import auth, credentials
from core.config import settings
import os

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    # Try to get the path from settings or use default
    service_account_path = getattr(settings, 'FIREBASE_ADMIN_SDK_PATH', None)
    
    if service_account_path and os.path.exists(service_account_path):
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
    else:
        # Fallback: try default location
        default_path = "./firebase-admin-sdk.json"
        if os.path.exists(default_path):
            cred = credentials.Certificate(default_path)
            firebase_admin.initialize_app(cred)
        else:
            print("WARNING: Firebase Admin SDK not initialized - no service account key found")


async def verify_firebase_token(authorization: str = Header(None)):
    """
    Verify Firebase ID token from Authorization header
    Returns the user's Firebase UID
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization header")
    
    try:
        # Extract token from "Bearer <token>" format
        if authorization.startswith("Bearer "):
            token = authorization.split("Bearer ")[1]
        else:
            token = authorization
        
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        user_uid = decoded_token['uid']
        
        return user_uid
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication: {str(e)}")


async def get_current_user_from_token(authorization: str = Header(None)):
    """
    Get current user UID from Firebase token
    Can be used as a dependency in routes
    """
    return await verify_firebase_token(authorization)
