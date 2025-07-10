# Video Transfer System Configuration - ANSWERS

## 🎯 **System Configuration**
Based on your setup analysis, here are the **CORRECT** configuration details:

## ✅ **DEFINITIVE ANSWERS**

### 1. **System Location**
- **Exact IP address of receiving system:** `192.168.0.121`
- **Exact port number:** `8001`
- **Full URL:** `http://192.168.0.121:8001`

### 2. **API Endpoint**
- **Exact endpoint URL:** `/receive-video`
- **Full endpoint:** `http://192.168.0.121:8001/receive-video`

### 3. **Authentication**
- **Authentication method:** API key in header
- **Header name:** `x-api-key`
- **API key value:** `shashank_ka_vision786`

### 4. **System Status**
- **System location:** Your main system (where Backend/api_data/api.py runs)
- **Port:** 8001 (configured in your backend)
- **Status:** Ready when you start your backend server

### 5. **Request Format**
- **Method:** POST
- **Content-Type:** multipart/form-data
- **Required format:**
  ```
  POST http://192.168.0.121:8001/receive-video
  Headers:
    x-api-key: shashank_ka_vision786
    Content-Type: multipart/form-data

  Body:
    video: (video file - video/mp4)
    metadata: {
      "subject": "Mathematics",
      "topic": "Triangles",
      "prompt": "Educational video about triangles",
      "generated_at": "2024-01-01T12:00:00",
      "file_size": 1024000,
      "system_info": "AnimateDiff_192.168.0.121:8501",
      "num_frames": 16,
      "guidance_scale": 7.5,
      "steps": 25,
      "seed": 333,
      "fps": 8
    }
  ```

### 6. **Response Format**
- **Success Response:**
  ```json
  {
    "success": true,
    "message": "Video received and stored successfully",
    "video_id": "unique-uuid",
    "access_url": "/videos/unique-uuid",
    "filename": "unique-uuid_timestamp.mp4",
    "file_size": 1024000
  }
  ```

## 📋 **FINAL CONFIGURATION**

```python
# CORRECT settings for your AnimateDiff system:
PRODUCTION_TEAM_IP = "192.168.0.121"     # ✅ CORRECT
PRODUCTION_TEAM_PORT = "8001"            # ✅ CORRECT
RECEIVE_ENDPOINT = "/receive-video"       # ✅ CORRECT
API_KEY = "shashank_ka_vision786"        # ✅ CORRECT
```

## 🚀 **Implementation Steps**

### Step 1: Start Your Backend Server
```bash
cd Backend/api_data
python api.py
```
This starts your receiving system on `192.168.0.121:8001`

### Step 2: Add POST Code to AnimateDiff System
Use the code from `video_transfer_endpoints.py` in your AnimateDiff system

### Step 3: Test the Connection
```bash
python verify_production_system.py
```

### Step 4: Generate and Transfer Video
Your AnimateDiff system will now automatically send videos to your main system

## 🎯 **System Architecture**
```
AnimateDiff System (192.168.0.121:8501)
    ↓ [generates video]
    ↓ [POST /receive-video]
Main System (192.168.0.121:8001)
    ↓ [stores video]
    ↓ [GET /videos/{id}]
Frontend (localhost:5173)
```
