@echo off
echo.
echo ========================================
echo    GURUKUL EDGE CASE TESTING SUITE
echo ========================================
echo.

cd /d "%~dp0\api_data"

echo 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)
echo ✅ Python is available

echo.
echo 🔍 Checking required packages...
python -c "import requests, json, time, threading" >nul 2>&1
if errorlevel 1 (
    echo ❌ Required packages not found
    echo Installing required packages...
    pip install requests aiohttp
    if errorlevel 1 (
        echo ❌ Failed to install packages
        pause
        exit /b 1
    )
)
echo ✅ Required packages are available

echo.
echo 🔍 Checking service availability...
python -c "import requests; requests.get('http://localhost:8002/docs', timeout=5)" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Financial Simulator service (port 8002) not accessible
    echo Please ensure the service is running
)

python -c "import requests; requests.get('http://localhost:8000/docs', timeout=5)" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Lesson Generator service (port 8000) not accessible
    echo Please ensure the service is running
)

echo.
echo 🚀 Starting Edge Case Testing Suite...
echo.
echo This will run comprehensive tests including:
echo   - Bursty workload scenarios
echo   - High latency agent testing
echo   - Network connectivity edge cases
echo   - System monitoring and reporting
echo.
echo ⏱️  Expected duration: 15-30 minutes
echo.

set /p continue="Continue with testing? (Y/N): "
if /i not "%continue%"=="Y" (
    echo Testing cancelled
    pause
    exit /b 0
)

echo.
echo 🧪 Running comprehensive edge case tests...
python run_all_edge_case_tests.py

echo.
echo 📊 Test execution completed!
echo.
echo Generated files:
echo   - edge_case_test_report_*.json (Detailed test results)
echo   - edge_case_monitoring_dashboard.json (Real-time dashboard)
echo   - logs/ directory (Detailed system logs)
echo.

pause
