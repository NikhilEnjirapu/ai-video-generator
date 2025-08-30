import os
import asyncio
from moviepy.editor import (
    TextClip, AudioFileClip, CompositeVideoClip, 
    ColorClip, concatenate_videoclips
)
import logging

logger = logging.getLogger(__name__)

class VideoService:
    def __init__(self):
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Video settings
        self.video_size = (1280, 720)  # HD resolution
        self.background_color = (41, 128, 185)  # Professional blue
        self.text_color = 'white'
        self.font_size = 48
        self.font = 'Arial-Bold'
    
    async def create_video(self, summary_text: str, audio_path: str, video_id: str) -> str:
        """Create video with narration and text slides"""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, 
                self._create_video_sync, 
                summary_text, 
                audio_path, 
                video_id
            )
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            raise
    
    def _create_video_sync(self, summary_text: str, audio_path: str, video_id: str) -> str:
        """Synchronous video creation"""
        try:
            # Load audio to get duration
            audio = AudioFileClip(audio_path)
            total_duration = audio.duration
            
            # Split summary into sentences for slides
            sentences = [s.strip() + '.' for s in summary_text.split('.') if s.strip()]
            
            if not sentences:
                sentences = [summary_text]
            
            # Calculate duration per slide
            slide_duration = max(3.0, total_duration / len(sentences))
            
            # Create video clips for each sentence
            video_clips = []
            current_time = 0
            
            for i, sentence in enumerate(sentences):
                # Determine actual duration for this slide
                if i == len(sentences) - 1:
                    # Last slide gets remaining time
                    duration = total_duration - current_time
                else:
                    duration = min(slide_duration, total_duration - current_time)
                
                if duration <= 0:
                    break
                
                # Create background
                background = ColorClip(
                    size=self.video_size,
                    color=self.background_color,
                    duration=duration
                )
                
                # Create text clip with Windows-compatible settings
                try:
                    text_clip = TextClip(
                        sentence,
                        fontsize=self.font_size,
                        color=self.text_color,
                        size=self.video_size,
                        method='caption',
                        font='Arial'  # Use a standard Windows font
                    ).set_duration(duration)
                except Exception as text_error:
                    logger.warning(f"Text clip creation failed: {text_error}")
                    # Create a simple text clip without advanced formatting
                    try:
                        text_clip = TextClip(
                            sentence,
                            fontsize=36,
                            color='white',
                            size=self.video_size,
                            method='caption'
                        ).set_duration(duration)
                    except Exception as fallback_error:
                        logger.error(f"Fallback text clip also failed: {fallback_error}")
                        # Create a minimal video with just background and audio
                        slide = background
                        video_clips.append(slide)
                        current_time += duration
                        continue
                
                # Center the text
                text_clip = text_clip.set_position('center')
                
                # Composite video and text
                slide = CompositeVideoClip([background, text_clip])
                video_clips.append(slide)
                
                current_time += duration
            
            # Concatenate all slides
            if video_clips:
                final_video = concatenate_videoclips(video_clips)
                
                # Set audio
                final_video = final_video.set_audio(audio)
                
                # Export video with Windows-compatible settings
                video_path = os.path.join(self.output_dir, f"{video_id}.mp4")
                final_video.write_videofile(
                    video_path,
                    fps=24,
                    codec='libx264',
                    audio_codec='aac',
                    temp_audiofile='temp-audio.m4a',
                    remove_temp=True,
                    verbose=False,
                    logger=None,
                    preset='ultrafast'  # Faster encoding
                )
                
                # Cleanup
                final_video.close()
                audio.close()
                for clip in video_clips:
                    clip.close()
                
                logger.info(f"Video saved to {video_path}")
                return video_path
            else:
                raise Exception("No video clips were created")
                
        except Exception as e:
            logger.error(f"Error in video creation: {e}")
            raise