# 🔧 FIXED Startup Guide - All Issues Resolved

## ✅ Issues Fixed:

1. **✅ Pydantic validation error** - Updated `@root_validator` to `@model_validator`
2. **✅ agentops dependency** - Already installed and available
3. **✅ Frontend start script** - This is a Vite project, use `npm run dev` instead of `npm start`

## 🚀 Corrected Startup Commands

### **Step 1: Create Environment Files (If Not Done)**

Create these 4 `.env` files with your API keys:

**Backend/memory_management/.env:**
```
MONGODB_URL=mongodb://localhost:27017/
MEMORY_DB_NAME=gurukul
MEMORY_API_KEYS=memory_api_key_dev:development_user
MEMORY_API_HOST=0.0.0.0
MEMORY_API_PORT=8003
```

**Backend/api_data/.env:**
```
GROQ_API_KEY=your_actual_groq_key_here
MONGODB_URL=mongodb://localhost:27017/
```

**Backend/Financial_simulator/Financial_simulator/.env:**
```
OPENAI_API_KEY=your_actual_openai_key_here
MONGODB_URL=mongodb://localhost:27017/
```

**Backend/pipline-24-master/.env:**
```
OPENAI_API_KEY=your_actual_openai_key_here
CHROMA_PERSIST_DIRECTORY=knowledge_store
```

### **Step 2: Install All Dependencies**

Run these commands to install all required dependencies:

```bash
# Memory Management API dependencies
cd memory_management
pip install fastapi uvicorn pydantic pymongo python-dotenv python-dateutil structlog
cd ..

# API Data Service dependencies
cd api_data
pip install fastapi uvicorn python-dotenv pymongo requests groq langchain chromadb sentence-transformers
cd ..

# Financial Simulator dependencies (agentops already installed)
cd Financial_simulator/Financial_simulator
pip install fastapi uvicorn langgraph langchain openai python-dotenv agentops
cd ../..

# Lesson Generator dependencies
cd pipline-24-master
pip install fastapi uvicorn python-dotenv requests torch transformers gtts
cd ..

# Frontend dependencies (Vite project)
cd ../gurukul_frontend-main
npm install
cd ../Backend
```

### **Step 3: Start All Services (5 Terminals)**

Open 5 separate terminal windows and run these commands:

#### **Terminal 1: Memory Management API (Port 8003)**
```bash
cd Backend/memory_management
python run_server.py
```

**Expected Output:**
```
🚀 Starting Memory Management API Server
✅ Database connection successful
INFO:     Uvicorn running on http://0.0.0.0:8003
```

**Test:** http://localhost:8003/memory/health

---

#### **Terminal 2: API Data Service (Port 8001)**
```bash
cd Backend/api_data
python api.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001
```

**Test:** http://localhost:8001/health

---

#### **Terminal 3: Financial Simulator (Port 8002)**
```bash
cd Backend/Financial_simulator/Financial_simulator
python langgraph_api.py
```

**Expected Output:**
```
✅ AgentOps initialized successfully
INFO:     Uvicorn running on http://0.0.0.0:8002
```

**Test:** http://localhost:8002/

---

#### **Terminal 4: Lesson Generator (Port 8000)**
```bash
cd Backend/pipline-24-master
python app.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test:** http://localhost:8000/

---

#### **Terminal 5: Frontend (Port 3000) - CORRECTED COMMAND**
```bash
cd gurukul_frontend-main
npm run dev
```

**Expected Output:**
```
  VITE v6.3.1  ready in 1234 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Test:** http://localhost:3000

## ✅ **Verification Checklist**

Open these URLs in your browser to verify all services:

1. [ ] **Memory Management API**: http://localhost:8003/memory/health
   - Should show: `{"status": "healthy", "database": "connected"}`

2. [ ] **API Data Service**: http://localhost:8001/health
   - Should show: `{"status": "ok"}`

3. [ ] **Financial Simulator**: http://localhost:8002/
   - Should show: `{"message": "FastAPI application for Financial Crew simulation"}`

4. [ ] **Lesson Generator**: http://localhost:8000/
   - Should show: `{"message": "Welcome to the Gurukul AI-Lesson Generator API"}`

5. [ ] **Frontend (Vite)**: http://localhost:3000
   - Should show: Gurukul login/dashboard page

## 🧪 **Quick Test Commands**

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

**Expected Response:**
```json
{
  "success": true,
  "message": "Memory chunk created successfully",
  "data": {
    "memory_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
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

## 🚨 **Troubleshooting Remaining Issues**

### **If MongoDB Connection Fails:**
```bash
# Option 1: Install MongoDB locally
# Download from: https://www.mongodb.com/try/download/community

# Option 2: Use MongoDB Atlas (Recommended)
# 1. Go to https://cloud.mongodb.com
# 2. Create free account and cluster
# 3. Get connection string
# 4. Update all .env files with:
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
```

### **If Port Already in Use:**
```bash
# Check what's using the port
netstat -ano | findstr :8003

# Kill the process
taskkill /PID <PID> /F
```

### **If API Keys Missing:**
- **OpenAI API Key**: https://platform.openai.com/api-keys
- **Groq API Key**: https://console.groq.com/keys

### **If Python Packages Still Missing:**
```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 🎯 **Success Indicators**

When everything works correctly:

✅ **All 5 URLs respond without errors**
✅ **No error messages in any terminal**
✅ **Frontend loads with Vite dev server**
✅ **You can interact with the Gurukul interface**
✅ **Memory API test returns success**
✅ **Chat API responds to test messages**

## 📱 **Using the Application**

1. **Open Frontend**: http://localhost:3000
2. **Create Account**: Register new user
3. **Login**: Use your credentials
4. **Select Persona**: Choose Financial Advisor, Math Tutor, etc.
5. **Start Chatting**: AI will remember your preferences across sessions!
6. **Test Memory**: Ask AI to remember something, then reference it later

## 🔄 **Stopping All Services**

To stop all services:
1. **Press Ctrl+C** in each terminal window
2. **Close all terminal windows**
3. **Or kill processes via Task Manager**

---

## 🎉 **All Issues Fixed!**

**Key Changes Made:**
1. **Fixed Pydantic validators** in `Backend/memory_management/models.py`
2. **Confirmed agentops** is already installed
3. **Corrected frontend command** from `npm start` to `npm run dev` (Vite project)

**Your complete Gurukul Unified Agent Mind system should now start successfully! 🚀**

**Next Step: Once all services are running, give Akash the Memory API integration package to connect the memory system to the frontend! 🎯**
