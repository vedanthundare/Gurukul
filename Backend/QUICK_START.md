# 🚀 Gurukul Unified Agent Mind - Quick Start Guide

## 📋 What You Have

Your project consists of **4 backend services** + **1 frontend**:

### Backend Services:
1. **Memory Management API** (Port 8003) - Stores user memories and interactions
2. **API Data Service** (Port 8001) - RAG, chatbot, PDF/image processing  
3. **Financial Simulator** (Port 8002) - LangGraph financial simulation
4. **Lesson Generator** (Port 8000) - AI lesson generation with TTS

### Frontend:
- **React Application** (Port 3000) - Main Gurukul interface

## ⚡ Super Quick Start (Windows)

### Option 1: Use the Startup Script
```bash
# Navigate to Backend directory
cd Backend

# Run the startup script
start_all_services.bat
```

This will open 4 terminal windows, one for each backend service.

### Option 2: Manual Startup (Recommended for first time)

**Open 5 separate terminal/command prompt windows:**

#### Terminal 1: Memory Management API
```bash
cd Backend/memory_management
pip install -r requirements.txt
python run_server.py
```

#### Terminal 2: API Data Service  
```bash
cd Backend/api_data
pip install fastapi uvicorn python-dotenv pymongo requests groq langchain chromadb
python api.py
```

#### Terminal 3: Financial Simulator
```bash
cd Backend/Financial_simulator/Financial_simulator
pip install -r requirements.txt
python langgraph_api.py
```

#### Terminal 4: Lesson Generator
```bash
cd Backend/pipline-24-master
pip install fastapi uvicorn python-dotenv requests torch transformers
python app.py
```

#### Terminal 5: Frontend
```bash
cd gurukul_frontend-main
npm install
npm start
```

## ✅ Verify Everything is Running

### Check Backend Services:
Open these URLs in your browser:

1. **Memory Management**: http://localhost:8003/memory/health
   - Should show: `{"status": "healthy", "database": "connected"}`

2. **API Data Service**: http://localhost:8001/health  
   - Should show: `{"status": "ok"}`

3. **Financial Simulator**: http://localhost:8002/
   - Should show: `{"message": "FastAPI application for Financial Crew simulation"}`

4. **Lesson Generator**: http://localhost:8000/
   - Should show: `{"message": "Welcome to the Gurukul AI-Lesson Generator API"}`

### Check Frontend:
- **Frontend**: http://localhost:3000
  - Should show the Gurukul login page

## 🔧 Environment Setup (Important!)

### Required API Keys:

Create these `.env` files with your API keys:

#### Backend/memory_management/.env
```bash
MONGODB_URL=mongodb://localhost:27017/
MEMORY_DB_NAME=gurukul
MEMORY_API_KEYS=memory_api_key_dev:development_user
```

#### Backend/api_data/.env
```bash
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URL=mongodb://localhost:27017/
```

#### Backend/Financial_simulator/Financial_simulator/.env
```bash
OPENAI_API_KEY=your_openai_key_here
MONGODB_URL=mongodb://localhost:27017/
```

#### Backend/pipline-24-master/.env
```bash
OPENAI_API_KEY=your_openai_key_here
CHROMA_PERSIST_DIRECTORY=knowledge_store
```

### Get API Keys:
- **OpenAI API Key**: https://platform.openai.com/api-keys
- **Groq API Key**: https://console.groq.com/keys

## 🧪 Test the Integration

### Test Memory Management API:
```bash
curl -X POST "http://localhost:8003/memory" \
  -H "Authorization: Bearer memory_api_key_dev" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "persona_id": "financial_advisor", 
    "content": "User prefers conservative investments",
    "content_type": "preference"
  }'
```

### Test Chat API:
```bash
curl -X POST "http://localhost:8001/chatpost" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "type": "chat_message"
  }'
```

## 🚨 Common Issues & Solutions

### Issue 1: Port Already in Use
```bash
# Check what's using the port
netstat -ano | findstr :8003

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Issue 2: MongoDB Not Running
```bash
# Install MongoDB Community Edition
# Or use MongoDB Atlas (cloud) connection string
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
```

### Issue 3: Python Packages Missing
```bash
# Install missing packages
pip install fastapi uvicorn python-dotenv pymongo

# Or create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Issue 4: Node.js Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rmdir /s node_modules
del package-lock.json
npm install
```

## 📊 Service Status Check

Create this batch file to check all services:

**check_services.bat:**
```batch
@echo off
echo Checking Gurukul Services...
echo ============================

curl -s http://localhost:8003/memory/health && echo ✅ Memory Management API - Running || echo ❌ Memory Management API - Not responding
curl -s http://localhost:8001/health && echo ✅ API Data Service - Running || echo ❌ API Data Service - Not responding  
curl -s http://localhost:8002/ && echo ✅ Financial Simulator - Running || echo ❌ Financial Simulator - Not responding
curl -s http://localhost:8000/ && echo ✅ Lesson Generator - Running || echo ❌ Lesson Generator - Not responding
curl -s http://localhost:3000 && echo ✅ Frontend - Running || echo ❌ Frontend - Not responding

pause
```

## 🎯 What Should Work After Setup

1. **Memory System**: AI remembers user preferences and conversation history
2. **Chat Interface**: Users can chat with different AI personas
3. **Financial Simulation**: AI provides financial advice and simulations
4. **Lesson Generation**: AI creates educational content with TTS
5. **PDF/Image Processing**: Users can upload and process documents

## 📱 Using the Application

1. **Open Frontend**: http://localhost:3000
2. **Login/Register**: Create a user account
3. **Select Persona**: Choose Financial Advisor, Math Tutor, etc.
4. **Start Chatting**: AI will remember your preferences
5. **Upload Files**: Process PDFs and images for learning
6. **Generate Lessons**: Create AI-powered educational content

## 🔄 Development Workflow

### Making Changes:
1. **Backend Changes**: Restart the specific service
2. **Frontend Changes**: Hot reload should work automatically
3. **Database Changes**: Check MongoDB for stored data

### Debugging:
1. **Check Logs**: Each terminal window shows service logs
2. **API Documentation**: 
   - Memory API: http://localhost:8003/memory/docs
   - Other APIs: Check their respective `/docs` endpoints
3. **Browser Console**: Check for frontend errors

## 🚀 Next Steps

1. **Test Basic Functionality**: Chat with different personas
2. **Integrate Memory API**: Use the provided integration package for Akash
3. **Customize Personas**: Modify persona configurations
4. **Add Features**: Extend functionality as needed
5. **Deploy**: Set up production environment

## 📞 Need Help?

1. **Check Service Health**: Use the URLs above
2. **Review Logs**: Check terminal outputs for errors
3. **Verify Environment**: Ensure all `.env` files are configured
4. **Test APIs**: Use the curl commands to test individual services

---

**Your complete Gurukul Unified Agent Mind system should now be running! 🎉**

**All Services Running = Ready to integrate Memory Management API with frontend! 🚀**
