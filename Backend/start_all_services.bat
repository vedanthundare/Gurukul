@echo off
echo ========================================
echo    Gurukul Unified Agent Mind
echo    Starting All Backend Services
echo ========================================
echo.

REM Set the base directory
set BASE_DIR=%~dp0

echo 🚀 Starting all backend services with orchestration...
echo.

REM Start Base Backend with Orchestration (Port 8000) - Main API
echo � Starting Base Backend with Orchestration on port 8000...
start "Base Backend (Main API)" cmd /k "cd /d %BASE_DIR%Base_backend && python api.py"
timeout /t 4 /nobreak >nul

REM Start Dedicated Chatbot Service (Port 8001)
echo 🤖 Starting Dedicated Chatbot Service on port 8001...
start "Dedicated Chatbot Service" cmd /k "cd /d %BASE_DIR%dedicated_chatbot_service && python chatbot_api.py"
timeout /t 3 /nobreak >nul

REM Start Financial Simulator (Port 8002)
echo 💰 Starting Financial Simulator on port 8002...
start "Financial Simulator" cmd /k "cd /d %BASE_DIR%Financial_simulator && python langgraph_api.py"
timeout /t 3 /nobreak >nul

REM Start Memory Management API (Port 8003)
echo � Starting Memory Management API on port 8003...
start "Memory Management API" cmd /k "cd /d %BASE_DIR%memory_management && python run_server.py"
timeout /t 3 /nobreak >nul

REM Start Akash Service (Port 8004)
echo 🧠 Starting Akash Service on port 8004...
start "Akash Service" cmd /k "cd /d %BASE_DIR%akash && python main.py"
timeout /t 3 /nobreak >nul

REM Start Subject Generation Service (Port 8005)
echo 📖 Starting Subject Generation Service on port 8005...
start "Subject Generation" cmd /k "cd /d %BASE_DIR%subject_generation && python app.py"
timeout /t 3 /nobreak >nul

REM Start Wellness API (Unified Orchestration System) (Port 8006)
echo 🧘 Starting Wellness API (Unified Orchestration) on port 8006...
start "Wellness API" cmd /k "cd /d %BASE_DIR%orchestration\unified_orchestration_system && python simple_api.py --port 8006"
timeout /t 4 /nobreak >nul

echo.
echo ✅ All 7 backend services are starting...
echo.
echo 🌐 Service URLs:
echo    Base Backend (Main API):     http://localhost:8000/health
echo    Dedicated Chatbot Service:   http://localhost:8001/health
echo    Financial Simulator:         http://localhost:8002/health
echo    Memory Management API:       http://localhost:8003/memory/health
echo    Akash Service:               http://localhost:8004/health
echo    Subject Generation:          http://localhost:8005/health
echo    Wellness API (Orchestration): http://localhost:8006/
echo.
echo 🚀 Orchestration Integration Status:
echo    Integration Status:          http://localhost:8000/integration-status
echo    Enhanced Lesson Generation:  http://localhost:8000/lessons/enhanced
echo    User Progress Tracking:      http://localhost:8000/user-progress/{user_id}
echo.
echo 📋 Next Steps:
echo    1. Wait 20-30 seconds for all services to start
echo    2. Check the service URLs above to verify they're running
echo    3. Verify orchestration integration status
echo    4. Start the frontend: cd "new frontend" && npm start
echo    5. Open http://localhost:3000 in your browser
echo    6. Look for "AI Enhanced" indicator in Subject Explorer
echo    7. Test WellnessBot in Agent Simulator (should show "API Connected")
echo.
echo 🔧 To stop all services: Close all the opened terminal windows
echo.
echo 💡 Troubleshooting:
echo    - If orchestration features don't work, add GEMINI_API_KEY to Base_backend/.env
echo    - Check Backend/Base_backend/ORCHESTRATION_INTEGRATION_GUIDE.md for setup
echo    - Run test: cd Backend/Base_backend && python test_orchestration_integration.py
echo    - For WellnessBot: Ensure GEMINI_API_KEY is set in Backend/orchestration/unified_orchestration_system/.env
echo    - WellnessBot endpoints: http://localhost:8006/wellness, http://localhost:8006/docs
echo.
pause
