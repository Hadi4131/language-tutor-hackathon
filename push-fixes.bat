@echo off
echo ========================================
echo Pushing Fixes to GitHub
echo ========================================
echo.

cd /d "c:\Users\Sayed\Downloads\Google AI Hackathon"

echo Checking Git status...
git status

echo.
echo Adding fixed files...
git add backend/core/config.py
git add backend/main.py
git add backend/.env.example

echo.
echo Creating commit for deployment fixes...
git commit -m "Fix: Make VERTEX_API_KEY optional and fix regex warning"

echo.
echo ========================================
echo Ready to push fixes to GitHub!
echo ========================================
echo.
echo You will need to authenticate with GitHub.
echo Use your Personal Access Token as the password.
echo.
pause

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo Done! 
echo.
echo Next Steps:
echo 1. Render will auto-deploy the fix
echo 2. Add environment variables in Render dashboard:
echo    - GOOGLE_API_KEY (required)
echo    - ELEVENLABS_API_KEY (required)  
echo    - MONGODB_URI (required)
echo    - Do NOT add VERTEX_API_KEY (it's optional)
echo.
echo ========================================
pause
