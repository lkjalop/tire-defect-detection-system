@echo off
echo ===========================================
echo   Quick Git Install and GitHub Push
echo ===========================================
echo.

echo Step 1: Installing Git for Windows...
echo Opening download page - please download and install Git
echo Download URL: https://git-scm.com/download/win
echo.
echo After installing Git:
echo 1. Choose all default options during installation
echo 2. Restart this terminal (close and reopen)
echo 3. Run this script again
echo.

REM Try to open the download page
start https://git-scm.com/download/win

echo.
echo Press any key after you've installed Git and restarted your terminal...
pause

echo.
echo ===========================================
echo   Configuring Git (First Time Setup)
echo ===========================================
echo.

REM Git configuration
set /p USERNAME="Enter your full name for Git: "
set /p EMAIL="Enter your email address: "

git config --global user.name "%USERNAME%"
git config --global user.email "%EMAIL%"

echo.
echo Git configured successfully!
echo.

echo ===========================================
echo   Pushing to GitHub Repository
echo ===========================================
echo.

REM Initialize repository
echo Initializing Git repository...
git init

echo.
echo Adding all files...
git add .

echo.
echo Creating initial commit...
git commit -m "Initial commit: Enterprise tire defect detection system

- Complete Edge AI IoT solution for manufacturing
- YOLOv8 computer vision with <500ms inference
- Enterprise security: authentication, rate limiting, audit logging
- Container-based deployment with Docker
- Real-time dashboard and REST API
- Developed for David Linthicum's Enterprise AI Architecture Program"

echo.
echo Adding remote repository...
git remote add origin https://github.com/lkjalop/tire-defect-detection-system.git

echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ===========================================
echo   SUCCESS! Project pushed to GitHub
echo ===========================================
echo.
echo Your repository is now live at:
echo https://github.com/lkjalop/tire-defect-detection-system
echo.
echo Next steps:
echo 1. Verify upload at the GitHub URL above
echo 2. Run setup_demo.bat to test the system
echo 3. Follow DEMO_GUIDE.md for presentation
echo.
pause
