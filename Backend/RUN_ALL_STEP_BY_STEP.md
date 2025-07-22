# 🚀 Step-by-Step Guide to Run All Gurukul Services

## 📋 Pre-Requirements Check

Before we start, let's make sure you have everything installed:

### 1. Check Python Installation
```bash
python --version
# Should show Python 3.9 or higher
```

### 2. Check Node.js Installation
```bash
node --version
npm --version
# Should show Node.js 16+ and npm 8+
```

### 3. Check if MongoDB is Running
```bash
# Try to connect to MongoDB
mongosh
# Or check if MongoDB service is running
```

If MongoDB is not installed, you can:
- **Option A**: Install MongoDB locally
- **Option B**: Use MongoDB Atlas (cloud) - Get connection string from https://cloud.mongodb.com

## 🔧 Step 1: Set Up Environment Variables

### Create .env files for each service:

#### 1.1 Memory Management API
```bash
cd Backend/memory_management
```

Create `.env` file:
```bash
# Copy this content to Backend/memory_management/.env
MONGODB_URL=mongodb://localhost:27017/
MEMORY_DB_NAME=gurukul
MEMORY_API_KEYS=memory_api_key_dev:development_user,memory_api_key_prod:production_user
MEMORY_API_HOST=0.0.0.0
MEMORY_API_PORT=8003
```

#### 1.2 API Data Service
```bash
cd Backend/api_data
```

Create `.env` file:
```bash
# Copy this content to Backend/api_data/.env
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URL=mongodb://localhost:27017/
```

**Get Groq API Key**: https://console.groq.com/keys

#### 1.3 Financial Simulator
```bash
cd Backend/Financial_simulator/Financial_simulator
```

Create `.env` file:
```bash
# Copy this content to Backend/Financial_simulator/Financial_simulator/.env
OPENAI_API_KEY=your_openai_key_here
MONGODB_URL=mongodb://localhost:27017/
```

**Get OpenAI API Key**: https://platform.openai.com/api-keys

#### 1.4 Lesson Generator
```bash
cd Backend/pipline-24-master
```

Create `.env` file:
```bash
# Copy this content to Backend/pipline-24-master/.env
OPENAI_API_KEY=your_openai_key_here
CHROMA_PERSIST_DIRECTORY=knowledge_store
```

## 🚀 Step 2: Install Dependencies and Start Services

### Open 5 Terminal Windows

I'll guide you through each terminal window:

---

### Terminal 1: Memory Management API (Port 8003)

```bash
# Navigate to memory management directory
cd Backend/memory_management

# Install dependencies
pip install fastapi uvicorn pydantic pymongo python-dotenv python-dateutil structlog

# Start the service
python run_server.py
```

**Expected Output:**
```
🚀 Starting Memory Management API Server
✅ Database connection successful
🌐 Server configuration:
   Host: 0.0.0.0
   Port: 8003
INFO:     Uvicorn running on http://0.0.0.0:8003
```

**Test it**: Open http://localhost:8003/memory/health in browser
Should show: `{"status": "healthy", "database": "connected"}`

---

### Terminal 2: API Data Service (Port 8001)

```bash
# Navigate to api_data directory
cd Backend/api_data

# Install dependencies
pip install fastapi uvicorn python-dotenv pymongo requests groq langchain chromadb sentence-transformers

# Start the service
python api.py
```

**Expected Output:**
```
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001
```

**Test it**: Open http://localhost:8001/health in browser
Should show: `{"status": "ok"}`

---

### Terminal 3: Financial Simulator (Port 8002)

```bash
# Navigate to financial simulator directory
cd Backend/Financial_simulator/Financial_simulator

# Install dependencies
pip install fastapi uvicorn langgraph langchain openai python-dotenv agentops

# Start the service
python langgraph_api.py
```

**Expected Output:**
```
✅ AgentOps initialized successfully
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8002
```

**Test it**: Open http://localhost:8002/ in browser
Should show: `{"message": "FastAPI application for Financial Crew simulation"}`

---

### Terminal 4: Lesson Generator (Port 8000)

```bash
# Navigate to lesson generator directory
cd Backend/pipline-24-master

# Install dependencies
pip install fastapi uvicorn python-dotenv requests torch transformers gtts

# Start the service
python app.py
```

**Expected Output:**
```
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it**: Open http://localhost:8000/ in browser
Should show: `{"message": "Welcome to the Gurukul AI-Lesson Generator API"}`

---

### Terminal 5: Frontend (Port 3000)

```bash
# Navigate to frontend directory
cd gurukul_frontend-main

# Install dependencies
npm install

# Start the frontend
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view gurukul-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Test it**: Open http://localhost:3000 in browser
Should show the Gurukul login page

## ✅ Step 3: Verify All Services Are Running

### Quick Health Check

Open these URLs in your browser tabs:

1. **Memory Management**: http://localhost:8003/memory/health ✅
2. **API Data Service**: http://localhost:8001/health ✅
3. **Financial Simulator**: http://localhost:8002/ ✅
4. **Lesson Generator**: http://localhost:8000/ ✅
5. **Frontend**: http://localhost:3000 ✅

### API Documentation (Optional)

Check the interactive API docs:

1. **Memory Management**: http://localhost:8003/memory/docs
2. **API Data Service**: http://localhost:8001/docs
3. **Financial Simulator**: http://localhost:8002/docs
4. **Lesson Generator**: http://localhost:8000/docs

## 🧪 Step 4: Test the Integration

### Test Memory Management API

Open a new terminal and run:

```bash
curl -X POST "http://localhost:8003/memory" \
  -H "Authorization: Bearer memory_api_key_dev" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "persona_id": "financial_advisor",
    "content": "User prefers conservative investment strategies",
    "content_type": "preference",
    "metadata": {
      "tags": ["investment", "conservative"],
      "importance": 8,
      "topic": "investment_strategy"
    }
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

### Test Chat API

```bash
curl -X POST "http://localhost:8001/chatpost" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "type": "chat_message"
  }'
```

## 🚨 Troubleshooting Common Issues

### Issue 1: Port Already in Use

```bash
# Check what's using the port
netstat -ano | findstr :8003

# Kill the process (Windows)
taskkill /PID <PID> /F

# Or use different ports by modifying the .env files
```

### Issue 2: MongoDB Connection Error

**Option A: Install MongoDB locally**
- Download from: https://www.mongodb.com/try/download/community
- Start MongoDB service

**Option B: Use MongoDB Atlas (Recommended)**
1. Go to https://cloud.mongodb.com
2. Create free account
3. Create cluster
4. Get connection string
5. Update all `.env` files with: `MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/`

### Issue 3: Missing API Keys

**Get OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env` files

**Get Groq API Key:**
1. Go to https://console.groq.com/keys
2. Create new API key
3. Add to `Backend/api_data/.env`

### Issue 4: Python Package Errors

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Issue 5: Node.js/npm Errors

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🎯 Success Indicators

When everything is working correctly:

✅ **All 5 services respond to health checks**
✅ **No error messages in terminal windows**
✅ **Frontend loads at http://localhost:3000**
✅ **You can create an account and login**
✅ **Chat interface is responsive**
✅ **Memory API stores and retrieves data**

## 📱 Using the Application

1. **Open Frontend**: http://localhost:3000
2. **Create Account**: Register a new user
3. **Login**: Use your credentials
4. **Select Persona**: Choose Financial Advisor, Math Tutor, etc.
5. **Start Chatting**: The AI will remember your preferences!
6. **Test Memory**: Ask the AI to remember something, then ask about it later

## 🔄 Stopping All Services

To stop all services:
1. **Press Ctrl+C** in each terminal window
2. **Close all terminal windows**
3. **Or use the task manager** to kill Python and Node processes

## 📞 Need Help?

If you encounter issues:

1. **Check the terminal outputs** for error messages
2. **Verify all .env files** are created with correct API keys
3. **Ensure MongoDB is running** or use Atlas connection
4. **Check port conflicts** - make sure no other services use these ports
5. **Verify Python and Node.js versions** meet requirements

---

**🎉 Congratulations! Your complete Gurukul Unified Agent Mind system is now running!**

**Next step: Give Akash the Memory API integration package to connect the memory system to the frontend! 🚀**
