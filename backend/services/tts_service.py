import os
import asyncio
from gtts import gTTS
import logging

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.language_map = {
            "en": "en",      # English
            "hi": "hi",      # Hindi
            "ta": "ta",      # Tamil
            "es": "es"       # Spanish
        }
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def text_to_speech(self, text: str, language: str, video_id: str) -> str:
        """Convert text to speech and save as audio file"""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, 
                self._create_audio_sync, 
                text, 
                language, 
                video_id
            )
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            raise
    
    def _create_audio_sync(self, text: str, language: str, video_id: str) -> str:
        """Synchronous TTS creation"""
        try:
            # Map language code
            tts_language = self.language_map.get(language, "en")
            
            # Create TTS object
            tts = gTTS(
                text=text,
                lang=tts_language,
                slow=False,
                tld='com'
            )
            
            # Save audio file
            audio_path = os.path.join(self.output_dir, f"{video_id}_narration.mp3")
            tts.save(audio_path)
            
            logger.info(f"Audio saved to {audio_path}")
            return audio_path
            
        except Exception as e:
            logger.error(f"Error creating audio: {e}")
            raise
    
    def get_supported_languages(self) -> dict:
        """Return supported languages"""
        return {
            "en": "English",
            "hi": "हिन्दी (Hindi)",
            "ta": "தமிழ் (Tamil)",
            "es": "Español (Spanish)"
        }