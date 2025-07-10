# Video Transfer System Setup Guide

## Overview
This system allows the AnimateDiff video generation service (192.168.0.121:8501) to generate videos and transfer them to your main system (localhost:8001) for serving to the frontend.

## Architecture
```
Frontend (React) → Main System (localhost:8001) → AnimateDiff System (192.168.0.121:8501)
                ↑                                                    ↓
                └─────────── Video Transfer ←─────────────────────────┘
```

## Setup Instructions

### 1. AnimateDiff System (192.168.0.121:8501)

Add the following code to your AnimateDiff system:

```python
# Add to your existing AnimateDiff API
import requests
import os
import json
from datetime import datetime

MAIN_SYSTEM_URL = "http://192.168.0.121:8001"  # Your main system IP
MAIN_SYSTEM_ENDPOINT = f"{MAIN_SYSTEM_URL}/receive-video"

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
    
    with open(video_file_path, 'rb') as video_file:
        files = {'video': ('generated_video.mp4', video_file, 'video/mp4')}
        data = {'metadata': json.dumps(video_metadata)}
        headers = {'x-api-key': 'shashank_ka_vision786'}
        
        response = requests.post(MAIN_SYSTEM_ENDPOINT, files=files, data=data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to send video: {response.status_code} - {response.text}")

# Modify your existing /generate-video endpoint:
@app.post("/generate-video")
async def generate_video(request: VideoRequest):
    try:
        # Your existing video generation code...
        # video_path = generate_animatediff_video(...)
        
        # After successful generation, send to main system
        transfer_result = await send_video_to_main_system(
            video_file_path=video_path,
            subject=request.subject or "Unknown",
            topic=request.topic or "Unknown",
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

### 2. Main System (localhost:8001)

The main system has been updated with these new endpoints:

- `POST /receive-video` - Receives videos from AnimateDiff system
- `GET /videos/{video_id}` - Serves stored videos
- `GET /videos/{video_id}/info` - Gets video metadata
- `GET /videos` - Lists all stored videos

### 3. Frontend Updates

The frontend has been updated to:
- Handle both direct video responses and transferred video responses
- Automatically fetch videos from the main system when they're transferred
- Show appropriate success messages indicating the transfer method

## API Endpoints

### AnimateDiff System → Main System

**POST** `http://192.168.0.121:8001/receive-video`
```
Headers:
  x-api-key: shashank_ka_vision786
  Content-Type: multipart/form-data

Body:
  video: (video file)
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

Response:
{
  "success": true,
  "message": "Video received and stored successfully",
  "video_id": "uuid-here",
  "access_url": "/videos/uuid-here",
  "filename": "uuid-here_timestamp.mp4",
  "file_size": 1024000
}
```

### Frontend → Main System

**GET** `http://localhost:8001/videos/{video_id}`
```
Response: Video file (video/mp4)
```

**GET** `http://localhost:8001/videos/{video_id}/info`
```
Response:
{
  "success": true,
  "video_info": {
    "video_id": "uuid-here",
    "subject": "Mathematics",
    "topic": "Triangles",
    "prompt": "Educational video about triangles",
    "generated_at": "2024-01-01T12:00:00",
    "received_at": "2024-01-01T12:01:00",
    "file_size": 1024000,
    "filename": "uuid-here_timestamp.mp4"
  }
}
```

## Testing

Run the test script to verify everything works:

```bash
python test_video_transfer.py
```

## Troubleshooting

### Common Issues:

1. **404 errors on proxy endpoints**
   - Ensure main backend server is running on port 8001
   - Check that the API endpoints are properly configured

2. **CORS errors**
   - The backend now includes proper CORS headers
   - Ngrok requests include `ngrok-skip-browser-warning` header

3. **Connection failures**
   - Verify AnimateDiff service is running and accessible
   - Check network connectivity between systems
   - Ensure API key is correct: `shashank_ka_vision786`

4. **Video transfer failures**
   - Check that the `generated_videos` directory exists and is writable
   - Verify file permissions on both systems
   - Check available disk space

### Current Configuration:
- **Main System**: localhost:8001
- **AnimateDiff System**: 192.168.0.121:8501
- **Ngrok URL**: https://4e6b01c6e6f2.ngrok-free.app
- **API Key**: shashank_ka_vision786

## Startup Commands

1. **Start Main Backend Server:**
   ```bash
   cd Backend/api_data
   python api.py
   ```

2. **Start React Frontend:**
   ```bash
   cd "new frontend"
   npm start
   ```

3. **Ensure AnimateDiff Service is Running:**
   - On the other system (192.168.0.121:8501)
   - With ngrok tunnel active

## File Structure

```
Backend/
├── api_data/
│   └── api.py (updated with video endpoints)
├── generated_videos/ (created automatically)
new frontend/
├── src/
│   └── pages/
│       └── Subjects.jsx (updated with transfer logic)
video_transfer_endpoints.py (for AnimateDiff system)
test_video_transfer.py (testing script)
```
