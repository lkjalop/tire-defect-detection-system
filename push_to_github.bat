@echo off
echo ===========================================
echo   GitHub Push Script
echo ===========================================
echo.

REM Set Git path
set GIT="C:\Program Files\Git\bin\git.exe"

echo Checking Git installation...
%GIT% --version
if %errorlevel% neq 0 (
    echo Git not found! Please install Git first.
    pause
    exit /b 1
)

echo.
echo Committing files...
%GIT% commit -m "Initial commit: Enterprise tire defect detection system - Complete Edge AI IoT solution for manufacturing - YOLOv8 computer vision with sub-500ms inference - Enterprise security and container deployment - Developed for David Linthicum Enterprise AI Architecture Program"

echo.
echo Adding remote repository...
%GIT% remote add origin https://github.com/lkjalop/tire-defect-detection-system.git

echo.
echo Setting main branch...
%GIT% branch -M main

echo.
echo Pushing to GitHub...
%GIT% push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ===========================================
    echo   SUCCESS! Code pushed to GitHub!
    echo ===========================================
    echo.
    echo Your repository is live at:
    echo https://github.com/lkjalop/tire-defect-detection-system
    echo.
    echo Next: Run setup_demo.bat to test the system
) else (
    echo ===========================================
    echo   Push failed - you may need to authenticate
    echo ===========================================
    echo.
    echo Try visiting: https://github.com/lkjalop/tire-defect-detection-system
    echo And follow GitHub's authentication instructions
)

echo.
pause
