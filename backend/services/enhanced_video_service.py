import os
import asyncio
import random
from moviepy.editor import (
    AudioFileClip, ColorClip, CompositeVideoClip, 
    concatenate_videoclips, ImageClip, VideoClip, TextClip
)
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger(__name__)

class EnhancedVideoService:
    def __init__(self):
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Video settings
        self.video_size = (1280, 720)  # HD resolution
        
        # Color schemes for different scenes
        self.scene_colors = {
            'intro': (41, 128, 185),      # Blue
            'content': (52, 152, 219),    # Light blue
            'highlight': (46, 204, 113),  # Green
            'conclusion': (155, 89, 182), # Purple
            'neutral': (149, 165, 166)    # Gray
        }
        
        # Character positions and animations
        self.character_positions = [
            (200, 400), (400, 300), (600, 350), (800, 400),
            (300, 500), (500, 450), (700, 500), (900, 450)
        ]
    
    async def create_video(self, summary_text: str, audio_path: str, video_id: str) -> str:
        """Create enhanced video with characters, scenes, and animations"""
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, 
                self._create_video_sync, 
                summary_text, 
                audio_path, 
                video_id
            )
        except Exception as e:
            logger.error(f"Error creating enhanced video: {e}")
            raise
    
    def _create_character_scene(self, text: str, scene_type: str, filename: str) -> str:
        """Create a scene with animated characters and visual elements"""
        try:
            # Create base image
            img = Image.new('RGB', self.video_size, self.scene_colors[scene_type])
            draw = ImageDraw.Draw(img)
            
            # Create animated background pattern
            self._draw_animated_background(draw, scene_type)
            
            # Add character elements
            self._draw_characters(draw, scene_type)
            
            # Add visual elements based on scene type
            self._draw_scene_elements(draw, scene_type)
            
            # Add text with enhanced styling
            self._draw_enhanced_text(draw, text, scene_type)
            
            # Add visual effects
            self._add_visual_effects(draw, scene_type)
            
            # Save image
            image_path = os.path.join(self.output_dir, filename)
            img.save(image_path, quality=95)
            return image_path
            
        except Exception as e:
            logger.error(f"Error creating character scene: {e}")
            # Fallback to simple scene
            return self._create_fallback_scene(text, filename)
    
    def _draw_animated_background(self, draw: ImageDraw, scene_type: str):
        """Draw animated background patterns"""
        # Create gradient background
        for y in range(self.video_size[1]):
            factor = y / self.video_size[1]
            base_color = self.scene_colors[scene_type]
            
            # Create gradient effect
            r = int(base_color[0] * (1 - factor * 0.2))
            g = int(base_color[1] * (1 - factor * 0.2))
            b = int(base_color[2] * (1 - factor * 0.2))
            
            draw.line([(0, y), (self.video_size[0], y)], fill=(r, g, b))
        
        # Add geometric patterns
        if scene_type == 'intro':
            self._draw_intro_patterns(draw)
        elif scene_type == 'content':
            self._draw_content_patterns(draw)
        elif scene_type == 'highlight':
            self._draw_highlight_patterns(draw)
        elif scene_type == 'conclusion':
            self._draw_conclusion_patterns(draw)
    
    def _draw_intro_patterns(self, draw: ImageDraw):
        """Draw introduction scene patterns"""
        # Add floating circles
        for i in range(8):
            x = random.randint(100, self.video_size[0] - 100)
            y = random.randint(100, self.video_size[1] - 100)
            radius = random.randint(20, 60)
            color = (255, 255, 255, 30)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=color, outline=(255, 255, 255, 50))
    
    def _draw_content_patterns(self, draw: ImageDraw):
        """Draw content scene patterns"""
        # Add connecting lines
        for i in range(5):
            x1 = random.randint(50, self.video_size[0] - 50)
            y1 = random.randint(50, self.video_size[1] - 50)
            x2 = random.randint(50, self.video_size[0] - 50)
            y2 = random.randint(50, self.video_size[1] - 50)
            draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 20), width=2)
    
    def _draw_highlight_patterns(self, draw: ImageDraw):
        """Draw highlight scene patterns"""
        # Add star-like elements
        for i in range(6):
            x = random.randint(100, self.video_size[0] - 100)
            y = random.randint(100, self.video_size[1] - 100)
            self._draw_star(draw, x, y, 15, (255, 255, 255, 40))
    
    def _draw_conclusion_patterns(self, draw: ImageDraw):
        """Draw conclusion scene patterns"""
        # Add wave patterns
        for i in range(3):
            y_base = 100 + i * 200
            for x in range(0, self.video_size[0], 20):
                y = y_base + 20 * (x % 40) / 40
                draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 255, 255, 30))
    
    def _draw_star(self, draw: ImageDraw, x: int, y: int, size: int, color: tuple):
        """Draw a star shape"""
        points = []
        for i in range(10):
            angle = i * 36 * 3.14159 / 180
            radius = size if i % 2 == 0 else size // 2
            px = x + radius * (1 if i % 2 == 0 else 0.5) * (1 if i < 5 else -1)
            py = y + radius * (1 if i % 2 == 0 else 0.5) * (1 if i % 5 < 2.5 else -1)
            points.append((px, py))
        
        if len(points) >= 3:
            draw.polygon(points, fill=color)
    
    def _draw_characters(self, draw: ImageDraw, scene_type: str):
        """Draw animated character elements"""
        # Draw character silhouettes
        for i, pos in enumerate(self.character_positions[:4]):
            x, y = pos
            color = (255, 255, 255, 60)
            
            # Draw character body (circle)
            body_radius = 30
            draw.ellipse([x-body_radius, y-body_radius, x+body_radius, y+body_radius], 
                        fill=color, outline=(255, 255, 255, 100))
            
            # Draw character head
            head_radius = 15
            draw.ellipse([x-head_radius, y-body_radius-head_radius, 
                         x+head_radius, y-body_radius+head_radius], 
                        fill=color, outline=(255, 255, 255, 100))
            
            # Draw character arms
            arm_length = 25
            draw.line([(x-body_radius, y), (x-body_radius-arm_length, y-10)], 
                     fill=(255, 255, 255, 100), width=3)
            draw.line([(x+body_radius, y), (x+body_radius+arm_length, y-10)], 
                     fill=(255, 255, 255, 100), width=3)
    
    def _draw_scene_elements(self, draw: ImageDraw, scene_type: str):
        """Draw scene-specific visual elements"""
        if scene_type == 'intro':
            # Add title banner
            banner_y = 80
            draw.rectangle([(100, banner_y), (self.video_size[0]-100, banner_y+60)], 
                          fill=(255, 255, 255, 20), outline=(255, 255, 255, 50))
            
        elif scene_type == 'content':
            # Add content boxes
            for i in range(3):
                x = 150 + i * 300
                y = 150
                draw.rectangle([(x, y), (x+200, y+100)], 
                              fill=(255, 255, 255, 15), outline=(255, 255, 255, 40))
        
        elif scene_type == 'highlight':
            # Add highlight circles
            for i in range(3):
                x = 200 + i * 300
                y = 200
                draw.ellipse([(x-40, y-40), (x+40, y+40)], 
                            fill=(255, 255, 255, 25), outline=(255, 255, 255, 60))
        
        elif scene_type == 'conclusion':
            # Add conclusion elements
            center_x = self.video_size[0] // 2
            center_y = 200
            draw.ellipse([(center_x-60, center_y-60), (center_x+60, center_y+60)], 
                        fill=(255, 255, 255, 30), outline=(255, 255, 255, 70))
    
    def _draw_enhanced_text(self, draw: ImageDraw, text: str, scene_type: str):
        """Draw text with enhanced styling and effects"""
        try:
            # Choose font
            font_size = 48
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Split text into lines
            words = text.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + " " + word if current_line else word
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] < self.video_size[0] - 200:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # Calculate text position
            line_height = font_size + 15
            total_height = len(lines) * line_height
            start_y = (self.video_size[1] - total_height) // 2
            
            # Draw text with effects
            for i, line in enumerate(lines):
                y_pos = start_y + i * line_height
                
                # Calculate x position to center text
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x_pos = (self.video_size[0] - text_width) // 2
                
                # Draw text shadow
                shadow_offset = 4
                draw.text((x_pos + shadow_offset, y_pos + shadow_offset), line, 
                         fill=(0, 0, 0, 100), font=font)
                
                # Draw main text with scene-appropriate color
                text_color = self._get_text_color(scene_type)
                draw.text((x_pos, y_pos), line, fill=text_color, font=font)
                
                # Add text highlight effect
                if scene_type == 'highlight':
                    highlight_y = y_pos + font_size + 5
                    draw.line([(x_pos, highlight_y), (x_pos + text_width, highlight_y)], 
                             fill=(255, 255, 255, 80), width=3)
            
        except Exception as e:
            logger.error(f"Error drawing enhanced text: {e}")
    
    def _get_text_color(self, scene_type: str) -> tuple:
        """Get appropriate text color for scene type"""
        if scene_type == 'highlight':
            return (255, 255, 255)  # White for highlights
        else:
            return (255, 255, 255)  # White for most scenes
    
    def _add_visual_effects(self, draw: ImageDraw, scene_type: str):
        """Add final visual effects to the scene"""
        # Add subtle border
        border_width = 8
        border_color = (255, 255, 255, 30)
        draw.rectangle([(border_width, border_width), 
                       (self.video_size[0] - border_width, self.video_size[1] - border_width)], 
                      outline=border_color, width=border_width)
        
        # Add corner decorations
        corner_size = 40
        corner_color = (255, 255, 255, 40)
        
        # Top-left corner
        draw.arc([(10, 10), (10 + corner_size, 10 + corner_size)], 0, 90, fill=corner_color, width=3)
        # Top-right corner
        draw.arc([(self.video_size[0] - 10 - corner_size, 10), 
                  (self.video_size[0] - 10, 10 + corner_size)], 90, 180, fill=corner_color, width=3)
        # Bottom-left corner
        draw.arc([(10, self.video_size[1] - 10 - corner_size), 
                  (10 + corner_size, self.video_size[1] - 10)], 270, 360, fill=corner_color, width=3)
        # Bottom-right corner
        draw.arc([(self.video_size[0] - 10 - corner_size, self.video_size[1] - 10 - corner_size), 
                  (self.video_size[0] - 10, self.video_size[1] - 10)], 180, 270, fill=corner_color, width=3)
    
    def _create_fallback_scene(self, text: str, filename: str) -> str:
        """Create a simple fallback scene if enhanced scene creation fails"""
        img = Image.new('RGB', self.video_size, self.scene_colors['neutral'])
        draw = ImageDraw.Draw(img)
        
        # Simple text
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Center text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x_pos = (self.video_size[0] - text_width) // 2
        y_pos = (self.video_size[1] - 40) // 2
        
        draw.text((x_pos, y_pos), text, fill=(255, 255, 255), font=font)
        
        image_path = os.path.join(self.output_dir, filename)
        img.save(image_path)
        return image_path
    
    def _create_video_sync(self, summary_text: str, audio_path: str, video_id: str) -> str:
        """Create enhanced video with character scenes and animations"""
        try:
            # Load audio
            audio = AudioFileClip(audio_path)
            total_duration = audio.duration
            
            # Split summary into sentences
            sentences = [s.strip() + '.' for s in summary_text.split('.') if s.strip()]
            if not sentences:
                sentences = [summary_text]
            
            # Determine scene types for each sentence
            scene_types = self._assign_scene_types(len(sentences))
            
            # Calculate timing
            slide_duration = max(4.0, total_duration / len(sentences))
            
            # Create video clips
            video_clips = []
            current_time = 0
            
            for i, (sentence, scene_type) in enumerate(zip(sentences, scene_types)):
                # Calculate duration
                if i == len(sentences) - 1:
                    duration = total_duration - current_time
                else:
                    duration = min(slide_duration, total_duration - current_time)
                
                if duration <= 0:
                    break
                
                # Create enhanced scene
                image_filename = f"{video_id}_scene_{i}.png"
                image_path = self._create_character_scene(sentence, scene_type, image_filename)
                
                # Create video clip
                try:
                    slide = ImageClip(image_path, duration=duration)
                    video_clips.append(slide)
                except Exception as e:
                    logger.error(f"Error creating scene {i}: {e}")
                    # Fallback to simple background
                    background = ColorClip(
                        size=self.video_size,
                        color=self.scene_colors[scene_type],
                        duration=duration
                    )
                    video_clips.append(background)
                
                current_time += duration
                
                # Clean up image
                try:
                    os.remove(image_path)
                except:
                    pass
            
            # Create final video
            if video_clips:
                final_video = concatenate_videoclips(video_clips)
                final_video = final_video.set_audio(audio)
                
                # Export
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
                
                logger.info(f"Enhanced video saved to {video_path}")
                return video_path
            else:
                raise Exception("No video clips were created")
                
        except Exception as e:
            logger.error(f"Error in enhanced video creation: {e}")
            raise
    
    def _assign_scene_types(self, num_sentences: int) -> list:
        """Assign scene types to sentences for visual variety"""
        scene_types = []
        
        for i in range(num_sentences):
            if i == 0:
                scene_types.append('intro')
            elif i == num_sentences - 1:
                scene_types.append('conclusion')
            elif i % 3 == 0:
                scene_types.append('highlight')
            else:
                scene_types.append('content')
        
        return scene_types
