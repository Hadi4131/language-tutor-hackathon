@echo off
echo ========================================
echo Pushing Code to GitHub
echo ========================================
echo.

cd /d "c:\Users\Sayed\Downloads\Google AI Hackathon"

echo Initializing Git repository...
git init

echo Configuring Git user...
git config user.name "Hadi4131"
git config user.email "hadi@example.com"

echo Adding all files (API keys are protected by .gitignore)...
git add .

echo Creating initial commit...
git commit -m "Initial commit: AI Language Tutor with Firebase Authentication"

echo Setting main branch...
git branch -M main

echo Adding remote repository...
git remote add origin https://github.com/Hadi4131/language-tutor-hackathon.git

echo.
echo ========================================
echo Ready to push to GitHub!
echo ========================================
echo.
echo You will need to authenticate with GitHub.
echo Please have your Personal Access Token ready.
echo.
echo Creating a Personal Access Token:
echo 1. Go to: https://github.com/settings/tokens
echo 2. Click "Generate new token" (classic)
echo 3. Select scopes: repo (all checkboxes)
echo 4. Generate and copy the token
echo.
pause

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo Done! Check your repository at:
echo https://github.com/Hadi4131/language-tutor-hackathon
echo ========================================
pause
