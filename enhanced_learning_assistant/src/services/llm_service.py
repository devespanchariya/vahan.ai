import logging
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAIError

# Load environment variables from .env file
load_dotenv()

class LLMService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama3-8b-8192")

        if not self.api_key:
            self.logger.error("GROQ_API_KEY is not set. Please check your .env file.")
            raise ValueError("GROQ_API_KEY is required.")
        else:
            self.logger.debug(f"GROQ_API_KEY loaded: {self.api_key[:4]}***")

        try:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        except Exception as e:
            self.logger.exception("Failed to initialize AsyncOpenAI client")
            raise

    async def generate_content(self, prompt: str, max_tokens: int = 300) -> str:
        """
        Generate content using Groq's LLM via OpenAI-compatible client.
        """
        try:
            self.logger.info(f"Using model: {self.model}")
            self.logger.debug(f"Prompt: {prompt[:200]}...")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=max_tokens
            )

            generated_text = response.choices[0].message.content
            self.logger.info("LLM generation successful")
            self.logger.debug(f"Output: {generated_text[:300]}")

            return generated_text

        except OpenAIError:
            self.logger.exception("OpenAI/Groq API error")
            return "LLM service encountered an API error."
        except Exception:
            self.logger.exception("Unexpected error during content generation")
            return "Content generation failed. Please try again later."
