import os
import asyncio
from moviepy.editor import (
    AudioFileClip, ColorClip, CompositeVideoClip, 
    concatenate_videoclips, ImageClip
)
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger(__name__)

class SimpleVideoService:
    def __init__(self):
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Video settings
        self.video_size = (1280, 720)  # HD resolution
        self.background_color = (52, 152, 219)  # Modern blue
        self.text_color = (255, 255, 255)  # White text
    
    async def create_video(self, summary_text: str, audio_path: str, video_id: str) -> str:
        """Create video with narration and simple text slides"""
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
    
    def _create_text_image(self, text: str, filename: str) -> str:
        """Create a visually appealing text image using PIL"""
        try:
            # Create image with gradient background
            img = Image.new('RGB', self.video_size, self.background_color)
            draw = ImageDraw.Draw(img)
            
            # Create a subtle gradient effect
            for y in range(self.video_size[1]):
                # Create a subtle gradient from top to bottom
                factor = y / self.video_size[1]
                r = int(self.background_color[0] * (1 - factor * 0.1))
                g = int(self.background_color[1] * (1 - factor * 0.1))
                b = int(self.background_color[2] * (1 - factor * 0.1))
                draw.line([(0, y), (self.video_size[0], y)], fill=(r, g, b))
            
            # Try to use a better font with larger size
            font_size = 60
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    try:
                        font = ImageFont.truetype("C:/Windows/Fonts/calibri.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
            
            # Split text into lines for better readability
            words = text.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + " " + word if current_line else word
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] < self.video_size[0] - 100:  # Leave 50px margin on each side
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # Calculate total text height
            line_height = font_size + 10
            total_height = len(lines) * line_height
            
            # Calculate starting Y position to center all lines
            start_y = (self.video_size[1] - total_height) // 2
            
            # Draw each line with shadow effect
            for i, line in enumerate(lines):
                y_pos = start_y + i * line_height
                
                # Draw text shadow (slight offset)
                shadow_offset = 3
                draw.text((shadow_offset, y_pos + shadow_offset), line, 
                         fill=(0, 0, 0, 128), font=font)
                
                # Draw main text
                draw.text((0, y_pos), line, fill=self.text_color, font=font)
            
            # Add a subtle border/frame
            border_width = 5
            draw.rectangle([(border_width, border_width), 
                          (self.video_size[0] - border_width, self.video_size[1] - border_width)], 
                         outline=(255, 255, 255, 50), width=border_width)
            
            # Save image with high quality
            image_path = os.path.join(self.output_dir, filename)
            img.save(image_path, quality=95)
            return image_path
            
        except Exception as e:
            logger.error(f"Error creating text image: {e}")
            # Create a simple colored background as fallback
            img = Image.new('RGB', self.video_size, self.background_color)
            image_path = os.path.join(self.output_dir, filename)
            img.save(image_path)
            return image_path
    
    def _create_video_sync(self, summary_text: str, audio_path: str, video_id: str) -> str:
        """Synchronous video creation using simple images"""
        try:
            # Load audio to get duration
            audio = AudioFileClip(audio_path)
            total_duration = audio.duration
            
            # Split summary into sentences for slides
            sentences = [s.strip() + '.' for s in summary_text.split('.') if s.strip()]
            
            if not sentences:
                sentences = [summary_text]
            
            # Calculate duration per slide with minimum duration for readability
            slide_duration = max(4.0, total_duration / len(sentences))
            
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
                
                # Create text image
                image_filename = f"{video_id}_slide_{i}.png"
                image_path = self._create_text_image(sentence, image_filename)
                
                # Create video clip from image
                try:
                    slide = ImageClip(image_path, duration=duration)
                    video_clips.append(slide)
                except Exception as e:
                    logger.error(f"Error creating slide {i}: {e}")
                    # Create a simple colored background as fallback
                    background = ColorClip(
                        size=self.video_size,
                        color=self.background_color,
                        duration=duration
                    )
                    video_clips.append(background)
                
                current_time += duration
                
                # Clean up image file
                try:
                    os.remove(image_path)
                except:
                    pass
            
            # Concatenate all slides
            if video_clips:
                final_video = concatenate_videoclips(video_clips)
                
                # Set audio
                final_video = final_video.set_audio(audio)
                
                # Export video
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
                    preset='ultrafast'
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
