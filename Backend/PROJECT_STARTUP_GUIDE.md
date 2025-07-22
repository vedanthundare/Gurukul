# Gurukul Unified Agent Mind - Complete Project Startup Guide

## 📋 Project Overview

Your project consists of multiple backend services and a React frontend:

### Backend Services:
1. **Memory Management API** (Port 8003) - Our new memory system
2. **API Data Service** (Port 8001) - RAG, chatbot, PDF/image processing
3. **Financial Simulator** (Port 8002) - LangGraph financial simulation
4. **Lesson Generator** (Port 8000) - AI lesson generation with TTS

### Frontend:
- **React Application** - Main Gurukul interface

## 🚀 Complete Startup Instructions

### Prerequisites

1. **Python 3.9+** installed
2. **Node.js 16+** and npm installed
3. **MongoDB** running (local or Atlas)
4. **Git** installed

### Step 1: Environment Setup

#### 1.1 Create Environment Files

**For Memory Management API:**
```bash
cd Backend/memory_management
cp .env.example .env
```

Edit `.env` with your settings:
```bash
# Database Configuration
MONGODB_URL=mongodb://localhost:27017/
MEMORY_DB_NAME=gurukul
MEMORY_RETENTION_DAYS=365

# API Configuration
MEMORY_API_HOST=0.0.0.0
MEMORY_API_PORT=8003
MEMORY_API_KEYS=memory_api_key_dev:development_user,memory_api_key_prod:production_user

# Rate Limiting
MEMORY_RATE_LIMIT_REQUESTS=1000
MEMORY_RATE_LIMIT_WINDOW=3600
```

**For other backend services, create `.env` files in each directory:**

```bash
# Backend/api_data/.env
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URL=mongodb://localhost:27017/

# Backend/Financial_simulator/Financial_simulator/.env
OPENAI_API_KEY=your_openai_key_here
MONGODB_URL=mongodb://localhost:27017/

# Backend/pipline-24-master/.env
OPENAI_API_KEY=your_openai_key_here
CHROMA_PERSIST_DIRECTORY=knowledge_store
```

#### 1.2 Install Python Dependencies

**For each backend service:**

```bash
# Memory Management API
cd Backend/memory_management
pip install -r requirements.txt

# API Data Service
cd Backend/api_data
pip install fastapi uvicorn python-dotenv pymongo requests groq langchain chromadb

# Financial Simulator
cd Backend/Financial_simulator/Financial_simulator
pip install -r requirements.txt

# Lesson Generator
cd Backend/pipline-24-master
pip install fastapi uvicorn python-dotenv requests torch transformers
```

### Step 2: Start Backend Services

Open **4 separate terminal windows** and start each service:

#### Terminal 1: Memory Management API (Port 8003)
```bash
cd Backend/memory_management
python run_server.py
```

Expected output:
```
🚀 Starting Memory Management API Server
✅ Database connection successful
🌐 Server configuration:
   Host: 0.0.0.0
   Port: 8003
INFO:     Uvicorn running on http://0.0.0.0:8003
```

#### Terminal 2: API Data Service (Port 8001)
```bash
cd Backend/api_data
python api.py
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
```

#### Terminal 3: Financial Simulator (Port 8002)
```bash
cd Backend/Financial_simulator/Financial_simulator
python langgraph_api.py
```

Expected output:
```
✅ AgentOps initialized successfully
INFO:     Uvicorn running on http://0.0.0.0:8002
```

#### Terminal 4: Lesson Generator (Port 8000)
```bash
cd Backend/pipline-24-master
python app.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Start Frontend

#### Terminal 5: React Frontend
```bash
cd gurukul_frontend-main
npm install
npm start
```

Expected output:
```
Local:            http://localhost:3000
On Your Network:  http://192.168.x.x:3000
```

### Step 4: Verify All Services

#### 4.1 Check Backend Health

Open your browser and test each service:

1. **Memory Management API**: http://localhost:8003/memory/health
   ```json
   {"status": "healthy", "database": "connected", "timestamp": "2023-12-01T12:00:00Z"}
   ```

2. **API Data Service**: http://localhost:8001/health
   ```json
   {"status": "ok"}
   ```

3. **Financial Simulator**: http://localhost:8002/
   ```json
   {"message": "FastAPI application for Financial Crew simulation"}
   ```

4. **Lesson Generator**: http://localhost:8000/
   ```json
   {"message": "Welcome to the Gurukul AI-Lesson Generator API"}
   ```

#### 4.2 Check Frontend

Open http://localhost:3000 - you should see the Gurukul login page.

### Step 5: Test Integration

#### 5.1 Test Memory Management API

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
      "importance": 8
    }
  }'
```

#### 5.2 Test API Data Service

```bash
curl -X POST "http://localhost:8001/chatpost" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "type": "chat_message"
  }'
```

#### 5.3 Test Financial Simulator

```bash
curl -X POST "http://localhost:8002/start-simulation" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "user_name": "Test User",
    "income": 5000,
    "expenses": [{"name": "rent", "amount": 1500}],
    "total_expenses": 1500,
    "goal": "Save for house",
    "financial_type": "conservative",
    "risk_level": "low"
  }'
```

## 🔧 Service Details

### Port Mapping
- **3000**: React Frontend
- **8000**: Lesson Generator API
- **8001**: API Data Service (RAG, Chat, PDF/Image)
- **8002**: Financial Simulator (LangGraph)
- **8003**: Memory Management API

### API Endpoints Summary

#### Memory Management API (8003)
- `GET /memory/health` - Health check
- `POST /memory` - Store memory
- `GET /memory?persona={id}` - Get persona memories
- `POST /memory/interaction` - Store interaction

#### API Data Service (8001)
- `GET /health` - Health check
- `POST /chatpost` - Send chat message
- `GET /chatbot` - Get chat response
- `POST /process-pdf` - Process PDF files
- `POST /process-img` - Process images

#### Financial Simulator (8002)
- `POST /start-simulation` - Start financial simulation
- `GET /simulation-status/{task_id}` - Check simulation status
- `POST /user/learning` - Teacher agent queries
- `POST /pdf/chat` - Upload PDF for learning

#### Lesson Generator (8000)
- `POST /lessons` - Create lesson (async)
- `GET /lessons/status/{task_id}` - Check lesson status
- `GET /lessons/{subject}/{topic}` - Get existing lesson
- `POST /lessons/generate-tts` - Generate TTS audio

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using the port
netstat -tulpn | grep 8003

# Kill the process
kill -9 <process_id>
```

#### 2. MongoDB Connection Issues
```bash
# Start MongoDB locally
mongod --dbpath /path/to/your/db

# Or use MongoDB Atlas connection string
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
```

#### 3. Python Dependencies Missing
```bash
# Install missing packages
pip install fastapi uvicorn python-dotenv pymongo

# Or install from requirements.txt
pip install -r requirements.txt
```

#### 4. Frontend Build Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Service Startup Order

**Recommended startup order:**
1. Start MongoDB
2. Start Memory Management API (8003)
3. Start API Data Service (8001)
4. Start Financial Simulator (8002)
5. Start Lesson Generator (8000)
6. Start React Frontend (3000)

### Environment Variables Checklist

- [ ] MongoDB connection string configured
- [ ] API keys for external services (OpenAI, Groq)
- [ ] Memory API keys configured
- [ ] All .env files created from templates
- [ ] Ports not conflicting with other services

## 📊 Service Status Dashboard

Create this simple script to check all services:

```bash
#!/bin/bash
echo "Checking Gurukul Services..."
echo "=============================="

services=(
  "Memory Management:http://localhost:8003/memory/health"
  "API Data Service:http://localhost:8001/health"
  "Financial Simulator:http://localhost:8002/"
  "Lesson Generator:http://localhost:8000/"
  "Frontend:http://localhost:3000"
)

for service in "${services[@]}"; do
  name="${service%%:*}"
  url="${service##*:}"
  
  if curl -s "$url" > /dev/null; then
    echo "✅ $name - Running"
  else
    echo "❌ $name - Not responding"
  fi
done
```

## 🎯 Next Steps

1. **Test each service individually** using the health check endpoints
2. **Integrate Memory Management API** into your frontend using the provided integration package
3. **Configure authentication** and user management
4. **Set up production environment** with proper security and monitoring
5. **Deploy to cloud services** when ready

Your complete Gurukul system should now be running with all services integrated! 🚀
