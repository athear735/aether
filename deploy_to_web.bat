@echo off
echo ========================================
echo   AETHER WEB DEPLOYMENT WIZARD
echo   AlgoRythm Tech - CEO: Sri Aasrith
echo ========================================
echo.

:: Check if Git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo Git is not installed. Please install Git first.
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/4] Initializing Git repository...
git init

echo.
echo [2/4] Adding files to repository...
git add .

echo.
echo [3/4] Creating initial commit...
git commit -m "AETHER - Advanced AI by AlgoRythm Tech"

echo.
echo [4/4] Ready for deployment!
echo.
echo ========================================
echo   NEXT STEPS TO GET ONLINE:
echo ========================================
echo.
echo 1. Create a GitHub account (if you don't have one):
echo    https://github.com/signup
echo.
echo 2. Create a new repository:
echo    https://github.com/new
echo    Name it: AETHER
echo.
echo 3. Push your code (copy these commands):
echo    git remote add origin https://github.com/YOUR_USERNAME/AETHER.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Deploy to Streamlit Cloud (FREE):
echo    - Go to: https://streamlit.io/cloud
echo    - Sign in with GitHub
echo    - Click "New app"
echo    - Select your AETHER repository
echo    - Main file: web/app.py
echo    - Click "Deploy"
echo.
echo 5. Your app will be live at:
echo    https://your-app-name.streamlit.app
echo.
echo ========================================
echo Press any key to open GitHub in your browser...
pause >nul
start https://github.com/new

echo.
echo After creating the repository, press any key to open Streamlit Cloud...
pause >nul
start https://streamlit.io/cloud

echo.
echo ========================================
echo   Deployment wizard completed!
echo   Your AETHER AI will be online soon!
echo ========================================
pause
