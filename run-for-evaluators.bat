@echo off
echo ========================================
echo Shoonya Wipe - National Submission
echo NIST SP 800-88r2 Compliant E-Waste Solution
echo ========================================
echo.

echo Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not running
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Docker is installed and running
echo.

echo Pulling Shoonya Wipe image...
docker pull jessicaagarwal/shoonya-wipe:latest

echo.
echo Starting Shoonya Wipe application...
docker run -d -p 5000:5000 --name shoonya-wipe jessicaagarwal/shoonya-wipe:latest

echo.
echo ========================================
echo Application is starting...
echo.
echo Once started, open your browser to:
echo http://localhost:5000
echo.
echo Features to test:
echo 1. Device Scanning
echo 2. NIST Compliance Form
echo 3. Wipe Simulation
echo 4. Certificate Generation
echo 5. Digital Signature Verification
echo ========================================
echo.

echo Waiting for application to start...
timeout /t 10 /nobreak >nul

echo.
echo Opening browser...
start http://localhost:5000

echo.
echo To stop the application, run:
echo docker stop shoonya-wipe
echo docker rm shoonya-wipe
echo.
pause
