# ✅ READY TO IMPLEMENT - Video Transfer System

## 🎯 **CORRECT CONFIGURATION**

Based on your system setup, here are the **DEFINITIVE** answers:

### 1. **System Location**
- **IP Address:** `192.168.0.121` ✅
- **Port:** `8001` ✅
- **Full URL:** `http://192.168.0.121:8001` ✅

### 2. **API Endpoint**
- **Endpoint:** `/receive-video` ✅
- **Full URL:** `http://192.168.0.121:8001/receive-video` ✅

### 3. **Authentication**
- **Method:** API key in header ✅
- **Header:** `x-api-key` ✅
- **Key:** `shashank_ka_vision786` ✅

### 4. **System Status**
- **Location:** Your main system (Backend/api_data/api.py) ✅
- **Status:** Ready when you start the backend server ✅

## 🚀 **IMPLEMENTATION STEPS**

### Step 1: Start Your Main System
```bash
cd Backend/api_data
python api.py
```
This starts the receiving system on `192.168.0.121:8001`

### Step 2: Add Code to Your AnimateDiff System (192.168.0.121:8501)

Add this to your AnimateDiff system:

```python
import requests
import os
import json
from datetime import datetime

# Configuration
MAIN_SYSTEM_URL = "http://192.168.0.121:8001"
MAIN_SYSTEM_ENDPOINT = f"{MAIN_SYSTEM_URL}/receive-video"
API_KEY = "shashank_ka_vision786"

async def send_video_to_main_system(video_file_path, subject, topic, prompt, metadata=None):
    """Send generated video to main system"""
    video_metadata = {
        "subject": subject,
        "topic": topic,
        "prompt": prompt,
        "generated_at": datetime.now().isoformat(),
        "file_size": os.path.getsize(video_file_path),
        "system_info": "AnimateDiff_192.168.0.121:8501",
        **(metadata or {})
    }
    
    print(f"🎬 Sending video to main system: {MAIN_SYSTEM_ENDPOINT}")
    
    with open(video_file_path, 'rb') as video_file:
        files = {'video': ('generated_video.mp4', video_file, 'video/mp4')}
        data = {'metadata': json.dumps(video_metadata)}
        headers = {'x-api-key': API_KEY}
        
        response = requests.post(
            MAIN_SYSTEM_ENDPOINT, 
            files=files, 
            data=data, 
            headers=headers, 
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Video successfully sent! Video ID: {result['video_id']}")
            return result
        else:
            raise Exception(f"Failed to send video: {response.status_code} - {response.text}")

# Modify your existing /generate-video endpoint:
@app.post("/generate-video")
async def generate_video(request: VideoRequest):
    try:
        # Your existing video generation code...
        # video_path = your_video_generation_function(request)
        
        # After successful generation, send to main system
        transfer_result = await send_video_to_main_system(
            video_file_path=video_path,
            subject=getattr(request, 'subject', 'Unknown'),
            topic=getattr(request, 'topic', 'Unknown'),
            prompt=request.prompt,
            metadata={
                "num_frames": request.num_frames,
                "guidance_scale": request.guidance_scale,
                "steps": request.steps,
                "seed": request.seed,
                "fps": request.fps
            }
        )
        
        return {
            "success": True,
            "message": "Video generated and sent to main system",
            "video_id": transfer_result.get("video_id"),
            "access_url": transfer_result.get("access_url"),
            "local_path": video_path
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Step 3: Test the System
```bash
python verify_production_system.py
```

### Step 4: Test from Frontend
Your React frontend will now automatically:
1. Generate lesson content
2. Send to AnimateDiff for video generation
3. AnimateDiff sends video to main system
4. Frontend fetches video from main system

## 📋 **EXPECTED WORKFLOW**

```
1. Frontend → AnimateDiff: "Generate video for Math/Triangles"
2. AnimateDiff → Generates video
3. AnimateDiff → Main System: POST /receive-video (video file)
4. Main System → Stores video, returns video_id
5. AnimateDiff → Frontend: Returns video_id and access_url
6. Frontend → Main System: GET /videos/{video_id}
7. Main System → Frontend: Returns video file
8. Frontend → Displays video to user
```

## 🧪 **TESTING COMMANDS**

### Test 1: Verify Main System
```bash
curl http://192.168.0.121:8001/videos
```

### Test 2: Test Video Upload
```bash
python verify_production_system.py
```

### Test 3: Test Frontend Integration
1. Start backend: `python Backend/api_data/api.py`
2. Start frontend: `npm start` in "new frontend"
3. Generate a lesson with video

## ✅ **READY TO GO**

All configuration is correct and ready to implement:
- ✅ IP: 192.168.0.121
- ✅ Port: 8001  
- ✅ Endpoint: /receive-video
- ✅ API Key: shashank_ka_vision786
- ✅ Backend code: Already implemented
- ✅ Frontend code: Already updated
- ✅ Transfer code: Ready to add to AnimateDiff

**Just follow the implementation steps above!**
