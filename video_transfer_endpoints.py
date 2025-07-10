"""
Video Transfer Endpoints for AnimateDiff System
Add these endpoints to your AnimateDiff system (192.168.0.121:8501)
"""

import requests
import os
import json
from datetime import datetime
from fastapi import HTTPException
from typing import Optional

# ========================================
# CONFIGURATION - CORRECT VALUES
# ========================================

# Production team's system (your main system)
PRODUCTION_TEAM_IP = "192.168.0.121"  # ✅ CORRECT: Your main system IP
PRODUCTION_TEAM_PORT = "8001"          # ✅ CORRECT: Backend API port

# Endpoint on their system
RECEIVE_ENDPOINT = "/receive-video"     # ✅ CORRECT: Implemented in Backend/api_data/api.py

# Authentication
API_KEY = "shashank_ka_vision786"      # ✅ CORRECT: Your API key

# ========================================
# CONSTRUCTED URLs (Don't change these)
# ========================================
MAIN_SYSTEM_URL = f"http://{PRODUCTION_TEAM_IP}:{PRODUCTION_TEAM_PORT}"
MAIN_SYSTEM_ENDPOINT = f"{MAIN_SYSTEM_URL}{RECEIVE_ENDPOINT}"

async def send_video_to_main_system(
    video_file_path: str,
    subject: str,
    topic: str,
    prompt: str,
    metadata: Optional[dict] = None
):
    """
    POST endpoint function to send generated video to main system
    Call this after video generation is complete
    """
    try:
        # Prepare metadata
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
        print(f"🎬 Video file: {video_file_path}")
        print(f"🎬 Metadata: {video_metadata}")
        
        # Prepare the multipart form data
        with open(video_file_path, 'rb') as video_file:
            files = {
                'video': ('generated_video.mp4', video_file, 'video/mp4')
            }
            
            data = {
                'metadata': json.dumps(video_metadata)
            }
            
            headers = {
                'x-api-key': API_KEY
            }
            
            # Send POST request to main system
            response = requests.post(
                MAIN_SYSTEM_ENDPOINT,
                files=files,
                data=data,
                headers=headers,
                timeout=60  # 1 minute timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Video successfully sent to main system!")
                print(f"🎬 Video ID: {result.get('video_id')}")
                print(f"🎬 Access URL: {result.get('access_url')}")
                return result
            else:
                error_msg = f"Failed to send video to main system: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                raise HTTPException(status_code=500, detail=error_msg)
                
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error sending video to main system: {str(e)}"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=503, detail=error_msg)
    except Exception as e:
        error_msg = f"Error sending video to main system: {str(e)}"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)


# Example usage in your existing video generation endpoint:
"""
# Add this to your existing /generate-video endpoint after video generation:

@app.post("/generate-video")
async def generate_video(request: VideoRequest):
    try:
        # Your existing video generation code here...
        # video_path = generate_animatediff_video(...)
        
        # After successful video generation, send to main system
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
        
        # Return both the video and transfer info
        return {
            "success": True,
            "message": "Video generated and sent to main system",
            "video_id": transfer_result.get("video_id"),
            "access_url": transfer_result.get("access_url"),
            "local_path": video_path
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

# Alternative: Manual trigger endpoint
# NOTE: Add this to your FastAPI app instance
# @app.post("/send-video-to-main")
async def manual_send_video(
    video_path: str,
    subject: str = "Manual Upload",
    topic: str = "Manual Upload",
    prompt: str = "Manually uploaded video"
):
    """
    Manual endpoint to send an existing video file to main system
    """
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail=f"Video file not found: {video_path}")
    
    result = await send_video_to_main_system(
        video_file_path=video_path,
        subject=subject,
        topic=topic,
        prompt=prompt
    )
    
    return {
        "success": True,
        "message": "Video sent to main system",
        "result": result
    }
