# AI Video Generator

Transform your text into engaging explainer videos with AI-powered summarization and multi-language narration.

## Features

- **Multiple Input Methods**: 
  - Drag & drop file upload (PDF, TXT, DOC, DOCX)
  - Direct text input/paste
- **Text Summarization**: Uses HuggingFace's BART model to extract key points
- **Multi-language TTS**: Supports English, Hindi, Tamil, and Spanish narration
- **Enhanced Video Creation**: Generates engaging videos with animated characters, visual scenes, and dynamic backgrounds
- **Simple Interface**: Clean, responsive web interface
- **Download Support**: Download generated videos for offline use

## Architecture

```
ai-video-gen/
├── backend/           # FastAPI Python backend
│   ├── main.py       # API endpoints
│   ├── services/     # Core AI services
│   │   ├── enhanced_video_service.py  # Character animations & scenes
│   │   ├── simple_video_service.py    # Basic video generation
│   │   ├── summarization_service.py   # Text summarization
│   │   └── tts_service.py            # Text-to-speech
│   └── outputs/      # Generated files
└── frontend/         # HTML/CSS/JS interface
    ├── index.html    # Main UI
    ├── style.css     # Styling
    └── script.js     # API integration
```

## Enhanced Video Features

The enhanced video service creates engaging visual content with:

- **Character Animations**: Animated character silhouettes with different poses
- **Scene Types**: Intro, content, highlight, and conclusion scenes with unique visual styles
- **Dynamic Backgrounds**: Gradient backgrounds with geometric patterns and effects
- **Visual Elements**: Scene-specific elements like banners, boxes, circles, and stars
- **Enhanced Typography**: Text with shadows, highlights, and scene-appropriate styling
- **Color Schemes**: Different color palettes for each scene type (blue, green, purple)
- **Visual Effects**: Borders, corner decorations, and professional finishing touches

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Install dependencies and setup
python setup.py

# Run both backend and frontend
python setup.py --run
```

### Option 2: Manual Setup
1. **Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Start Backend Server**
```bash
cd backend
python main.py
```

3. **Start Frontend Server** (in a new terminal)
```bash
cd frontend
python -m http.server 3000
```

4. **Access Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Setup Script Options
- `python setup.py` - Install dependencies only
- `python setup.py --backend` - Start backend server only
- `python setup.py --frontend` - Start frontend server only
- `python setup.py --run` - Start both servers

## Usage

1. **Choose Input Method**:
   - **Upload Files**: Drag & drop PDF, TXT, DOC, or DOCX files
   - **Paste Text**: Directly paste your content in the text area
2. Select narration language
3. Click "Generate Video"
4. Wait for AI processing (summarization → TTS → video creation)
5. Watch and download your generated video

## Demo Flow

1. **Input**: User pastes long text (books, articles, study materials) in the frontend
2. **Language Selection**: Choose narration language (English, Hindi, Tamil, Spanish)
3. **Processing**: Backend processes the text through the AI pipeline:
   - **Summarization**: BART model extracts key points
   - **TTS**: Google TTS converts summary to speech
   - **Video Creation**: Enhanced service generates videos with characters, scenes, and animations
4. **Output**: Video automatically loads in the frontend for playback and download

## API Endpoints

- `POST /generate-video` - Generate video from text (returns video file directly)
- `GET /download/{video_id}` - Download generated video (legacy endpoint)
- `GET /health` - Health check

### Generate Video Request
```json
{
  "text": "Your long input text here...",
  "language": "en"
}
```

### Supported Languages
- `en` - English 🇺🇸
- `hi` - Hindi 🇮🇳  
- `ta` - Tamil 🇮🇳
- `es` - Spanish 🇪🇸

## Technologies

- **Backend**: FastAPI, HuggingFace Transformers, gTTS, MoviePy
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **AI Models**: facebook/bart-large-cnn for summarization

## Scalability & Future Vision

### Current Features
- ✅ Multi-language text-to-speech support
- ✅ AI-powered text summarization
- ✅ Automated video generation with slides
- ✅ Clean, responsive web interface
- ✅ Direct video download functionality

### Future Enhancements
- 🔄 **Personalized Summaries**: Different summarization styles for students vs. researchers
- 🔄 **Adaptive Video Styles**: Educational slides, cinematic visuals, news bulletin formats
- 🔄 **Cloud Deployment**: Global access with scalable infrastructure
- 🔄 **Custom Backgrounds**: User-uploadable images and themes
- 🔄 **Advanced Animations**: Smooth transitions and visual effects
- 🔄 **Batch Processing**: Generate multiple videos from a document
- 🔄 **API Rate Limiting**: Production-ready request management
- 🔄 **Video Caching**: Optimize performance for repeated requests