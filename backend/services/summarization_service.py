import asyncio
from transformers import pipeline, AutoTokenizer
import logging

logger = logging.getLogger(__name__)

class SummarizationService:
    def __init__(self):
        self.model_name = "facebook/bart-large-cnn"
        self.summarizer = None
        self.tokenizer = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the summarization model and tokenizer"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.summarizer = pipeline(
                "summarization",
                model=self.model_name,
                tokenizer=self.tokenizer,
                device=-1,  # Use CPU
                framework="pt"
            )
            logger.info("Summarization model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading summarization model: {e}")
            raise
    
    def _chunk_text(self, text: str, max_chunk_length: int = 900) -> list:
        """Split text into chunks that fit the model's token limit"""
        # Split by sentences first
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Estimate tokens (rough approximation: 1 token per 4 characters)
            estimated_tokens = len(current_chunk + sentence) // 4
            
            if estimated_tokens > max_chunk_length and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    async def summarize(self, text: str) -> str:
        """Summarize the input text into key points"""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._summarize_sync, text)
        except Exception as e:
            logger.error(f"Error in summarization: {e}")
            raise
    
    def _summarize_sync(self, text: str) -> str:
        """Synchronous summarization logic"""
        try:
            # Clean and prepare text
            text = text.strip()
            if len(text) < 50:
                return text
            
            # Chunk the text if it's too long
            chunks = self._chunk_text(text)
            summaries = []
            
            for chunk in chunks:
                if len(chunk.strip()) < 50:
                    summaries.append(chunk)
                    continue
                
                # Generate summary for this chunk
                summary = self.summarizer(
                    chunk,
                    max_length=150,
                    min_length=30,
                    do_sample=False,
                    truncation=True
                )[0]['summary_text']
                
                summaries.append(summary)
            
            # Combine all summaries
            final_summary = " ".join(summaries)
            
            # If combined summary is still too long, summarize again
            if len(final_summary) > 1000:
                final_summary = self.summarizer(
                    final_summary,
                    max_length=200,
                    min_length=50,
                    do_sample=False,
                    truncation=True
                )[0]['summary_text']
            
            return final_summary
            
        except Exception as e:
            logger.error(f"Error in synchronous summarization: {e}")
            # Fallback: return first 500 characters if summarization fails
            return text[:500] + "..." if len(text) > 500 else text