import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.summarization_service import SummarizationService
from services.tts_service import TTSService
from services.enhanced_video_service import EnhancedVideoService

app = FastAPI(title="AI Video Generator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
summarization_service = SummarizationService()
tts_service = TTSService()
video_service = EnhancedVideoService()

class VideoRequest(BaseModel):
    text: str
    language: str = "en"

class VideoResponse(BaseModel):
    video_id: str
    message: str

@app.get("/")
async def root():
    return {"message": "AI Video Generator API", "version": "1.0.0"}

@app.post("/generate-video")
async def generate_video(request: VideoRequest):
    try:
        # Validate input
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text input cannot be empty")
        
        if len(request.text) < 50:
            raise HTTPException(status_code=400, detail="Text must be at least 50 characters long")
        
        # Generate unique ID for this video
        video_id = str(uuid.uuid4())
        
        # Step 1: Summarize the text
        summary = await summarization_service.summarize(request.text)
        
        # Step 2: Convert summary to speech
        audio_path = await tts_service.text_to_speech(
            summary, 
            request.language, 
            video_id
        )
        
        # Step 3: Create video with narration and slides
        video_path = await video_service.create_video(
            summary, 
            audio_path, 
            video_id
        )
        
        # Return the video file directly
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename=f"ai_video_{video_id}.mp4"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating video: {str(e)}")

@app.get("/download/{video_id}")
async def download_video(video_id: str):
    video_path = f"outputs/{video_id}.mp4"
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"ai_video_{video_id}.mp4"
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)