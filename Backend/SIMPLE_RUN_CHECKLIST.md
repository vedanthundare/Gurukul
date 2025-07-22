# ✅ Simple Checklist to Run Gurukul Project

## 🎯 Goal: Get all 5 services running (4 backend + 1 frontend)

### ⚡ Super Quick Option (Automated)

1. **Open Command Prompt as Administrator**
2. **Navigate to Backend folder:**
   ```bash
   cd "C:\Users\PC\Desktop\Vedant\gurukul\Unified-Agent-Mind--Domain-Memory-for-gurukul-Financial-Simulator\Backend"
   ```
3. **Run the automated setup:**
   ```bash
   setup_and_run.bat
   ```
4. **Wait 30 seconds, then open:** http://localhost:3000

---

### 📋 Manual Option (Step by Step)

#### Prerequisites Check:
- [ ] Python 3.9+ installed (`python --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] MongoDB running (or Atlas connection string ready)

#### Step 1: Get API Keys (Required!)
- [ ] **OpenAI API Key**: https://platform.openai.com/api-keys
- [ ] **Groq API Key**: https://console.groq.com/keys

#### Step 2: Create Environment Files

Create these 4 `.env` files with your API keys:

**File 1:** `Backend/memory_management/.env`
```
MONGODB_URL=mongodb://localhost:27017/
MEMORY_DB_NAME=gurukul
MEMORY_API_KEYS=memory_api_key_dev:development_user
MEMORY_API_HOST=0.0.0.0
MEMORY_API_PORT=8003
```

**File 2:** `Backend/api_data/.env`
```
GROQ_API_KEY=your_actual_groq_key_here
MONGODB_URL=mongodb://localhost:27017/
```

**File 3:** `Backend/Financial_simulator/Financial_simulator/.env`
```
OPENAI_API_KEY=your_actual_openai_key_here
MONGODB_URL=mongodb://localhost:27017/
```

**File 4:** `Backend/pipline-24-master/.env`
```
OPENAI_API_KEY=your_actual_openai_key_here
CHROMA_PERSIST_DIRECTORY=knowledge_store
```

#### Step 3: Open 5 Terminal Windows

**Terminal 1 - Memory Management API:**
```bash
cd Backend/memory_management
pip install fastapi uvicorn pydantic pymongo python-dotenv python-dateutil structlog
python run_server.py
```
✅ Check: http://localhost:8003/memory/health

**Terminal 2 - API Data Service:**
```bash
cd Backend/api_data
pip install fastapi uvicorn python-dotenv pymongo requests groq langchain chromadb
python api.py
```
✅ Check: http://localhost:8001/health

**Terminal 3 - Financial Simulator:**
```bash
cd Backend/Financial_simulator/Financial_simulator
pip install fastapi uvicorn langgraph langchain openai python-dotenv agentops
python langgraph_api.py
```
✅ Check: http://localhost:8002/

**Terminal 4 - Lesson Generator:**
```bash
cd Backend/pipline-24-master
pip install fastapi uvicorn python-dotenv requests torch transformers gtts
python app.py
```
✅ Check: http://localhost:8000/

**Terminal 5 - Frontend:**
```bash
cd gurukul_frontend-main
npm install
npm start
```
✅ Check: http://localhost:3000

---

### 🔍 Final Verification

Open these 5 URLs in your browser:

1. [ ] **Memory API**: http://localhost:8003/memory/health
   - Should show: `{"status": "healthy", "database": "connected"}`

2. [ ] **Data API**: http://localhost:8001/health
   - Should show: `{"status": "ok"}`

3. [ ] **Financial API**: http://localhost:8002/
   - Should show: `{"message": "FastAPI application for Financial Crew simulation"}`

4. [ ] **Lesson API**: http://localhost:8000/
   - Should show: `{"message": "Welcome to the Gurukul AI-Lesson Generator API"}`

5. [ ] **Frontend**: http://localhost:3000
   - Should show: Gurukul login page

---

### 🧪 Quick Test

Test the memory system:
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

Should return: `{"success": true, "message": "Memory chunk created successfully"}`

---

### 🚨 Common Issues & Quick Fixes

**Issue: Port already in use**
```bash
# Kill process using port 8003
netstat -ano | findstr :8003
taskkill /PID <PID> /F
```

**Issue: MongoDB not running**
- Install MongoDB locally OR
- Use MongoDB Atlas: https://cloud.mongodb.com
- Update MONGODB_URL in all .env files

**Issue: Missing API keys**
- Get OpenAI key: https://platform.openai.com/api-keys
- Get Groq key: https://console.groq.com/keys
- Update .env files with actual keys

**Issue: Python packages missing**
```bash
pip install fastapi uvicorn python-dotenv pymongo
```

**Issue: Node.js errors**
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

### 🎉 Success Indicators

When everything works:
- ✅ All 5 URLs respond correctly
- ✅ No error messages in terminals
- ✅ Frontend loads and shows login page
- ✅ You can create account and login
- ✅ Chat interface works
- ✅ Memory API test returns success

---

### 📱 Using the Application

1. **Open**: http://localhost:3000
2. **Register**: Create new account
3. **Login**: Use your credentials
4. **Chat**: Select persona and start chatting
5. **Test Memory**: Ask AI to remember something, then reference it later

---

### 🔄 Stopping Everything

To stop all services:
1. Press **Ctrl+C** in each terminal
2. Close all terminal windows
3. Or use Task Manager to kill Python/Node processes

---

### 📞 Need Help?

1. **Check terminal outputs** for error messages
2. **Verify .env files** have correct API keys
3. **Ensure MongoDB is running**
4. **Check no port conflicts**
5. **Follow detailed guide**: `RUN_ALL_STEP_BY_STEP.md`

---

**🚀 That's it! Your complete Gurukul system with memory management should now be running!**

**Next: Give Akash the Memory API integration package to connect everything together! 🎯**
