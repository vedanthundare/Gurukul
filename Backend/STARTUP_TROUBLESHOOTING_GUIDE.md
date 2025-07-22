# 🚀 Gurukul Backend Startup Troubleshooting Guide

## ✅ Issues Fixed

### 1. Frontend npm Script Issue
**Problem**: "Missing script: 'start'" error in "new frontend" directory
**Solution**: Added `"start": "vite"` script to package.json

### 2. Backend Path Issues  
**Problem**: setup_and_run.bat referenced non-existent directories (api_data/, pipline-24-master/)
**Solution**: Updated script to use correct directory structure:
- Base_backend/ (Port 8000)
- dedicated_chatbot_service/ (Port 8001) 
- Financial_simulator/ (Port 8002)
- memory_management/ (Port 8003)
- akash/ (Port 8004)
- subject_generation/ (Port 8005)
- orchestration/unified_orchestration_system/ (Port 8006)

### 3. Missing Environment Files
**Problem**: dedicated_chatbot_service/.env was missing
**Solution**: Created .env file with required configuration

## 🎯 Current System Status

### ✅ All Service Files Exist
- Base_backend/api.py ✅
- dedicated_chatbot_service/chatbot_api.py ✅
- Financial_simulator/langgraph_api.py ✅
- memory_management/run_server.py ✅
- akash/main.py ✅
- subject_generation/app.py ✅
- orchestration/unified_orchestration_system/simple_api.py ✅

### ✅ All Requirements Files Exist
- All services have requirements.txt files ✅

### ✅ All Environment Files Exist
- All services have .env files ✅

### ✅ All Ports Available
- Ports 8000-8006 and 3000 are available ✅

## 🚀 How to Start the System

### Option 1: Use Corrected Setup Script (Recommended)
```bash
cd Backend
setup_and_run.bat
```
This will:
1. Create any missing .env files
2. Install Python dependencies for all services
3. Install frontend dependencies
4. Start all 7 backend services + frontend
5. Perform health checks

### Option 2: Use Service Startup Script
```bash
cd Backend
start_all_services.bat
```
This starts only the backend services (assumes dependencies are installed).

### Option 3: Manual Startup (For Debugging)
Open 8 separate terminals:

**Terminal 1 - Base Backend (Port 8000):**
```bash
cd Backend/Base_backend
python api.py
```

**Terminal 2 - Dedicated Chatbot (Port 8001):**
```bash
cd Backend/dedicated_chatbot_service
python chatbot_api.py
```

**Terminal 3 - Financial Simulator (Port 8002):**
```bash
cd Backend/Financial_simulator
python langgraph_api.py
```

**Terminal 4 - Memory Management (Port 8003):**
```bash
cd Backend/memory_management
python run_server.py
```

**Terminal 5 - Akash Service (Port 8004):**
```bash
cd Backend/akash
python main.py
```

**Terminal 6 - Subject Generation (Port 8005):**
```bash
cd Backend/subject_generation
python app.py
```

**Terminal 7 - Wellness API (Port 8006):**
```bash
cd Backend/orchestration/unified_orchestration_system
python simple_api.py --port 8006
```

**Terminal 8 - Frontend (Port 3000):**
```bash
cd "new frontend"
npm start
```

## 🔍 Health Check URLs

After starting services, verify they're running:

- Base Backend: http://localhost:8000/health
- Dedicated Chatbot: http://localhost:8001/health  
- Financial Simulator: http://localhost:8002/health
- Memory Management: http://localhost:8003/memory/health
- Akash Service: http://localhost:8004/health
- Subject Generation: http://localhost:8005/health
- Wellness API: http://localhost:8006/
- Frontend: http://localhost:3000

## 🧘 Orchestration Integration

The system includes unified orchestration integration:
- Integration Status: http://localhost:8000/integration-status
- Enhanced Lesson Generation: http://localhost:8000/lessons/enhanced
- User Progress Tracking: http://localhost:8000/user-progress/{user_id}
- WellnessBot endpoints: http://localhost:8006/wellness, http://localhost:8006/docs

## 🔧 Troubleshooting

### If Services Don't Start:
1. Check if Python and Node.js are installed
2. Verify all .env files have valid API keys
3. Ensure MongoDB is running (if using local MongoDB)
4. Check if ports are already in use
5. Run: `python test_service_startup.py` for detailed diagnostics

### If Orchestration Features Don't Work:
1. Add GEMINI_API_KEY to Base_backend/.env
2. Add GEMINI_API_KEY to Backend/orchestration/unified_orchestration_system/.env
3. Run test: `cd Backend/Base_backend && python test_orchestration_integration.py`

### Common Issues:
- **Port conflicts**: Stop existing services or change ports
- **Missing API keys**: Update .env files with actual API keys
- **Import errors**: Install missing Python packages
- **Frontend issues**: Ensure Node.js 16+ is installed

## 📋 Next Steps After Startup

1. Wait 20-30 seconds for all services to start
2. Check all health check URLs
3. Open http://localhost:3000 in browser
4. Look for "AI Enhanced" indicator in Subject Explorer
5. Test WellnessBot in Agent Simulator (should show "API Connected")
6. Create account and start using Gurukul!

## 🎉 Success Indicators

✅ All 8 services running (7 backend + 1 frontend)
✅ All health checks return 200 OK
✅ Frontend loads without errors
✅ Orchestration integration active
✅ WellnessBot shows "API Connected"
✅ Subject Explorer shows "AI Enhanced" features
