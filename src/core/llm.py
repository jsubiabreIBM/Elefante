"""
LLM Service for Elefante
Handles interactions with Language Models (OpenAI, etc.) for memory consolidation and curation.
"""

import json
import os
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from src.utils.config import get_config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class LLMService:
    """
    Service for interacting with LLMs.
    Currently supports OpenAI compatible APIs.
    """
    
    def __init__(self):
        self.config = get_config()
        self.client = None
        self.model = self.config.elefante.llm.model
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize OpenAI client"""
        api_key = self.config.elefante.llm.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("No LLM API key found. LLM features will be disabled.")
            return
            
        self.client = AsyncOpenAI(api_key=api_key)
        logger.info(f"LLM Service initialized with model: {self.model}")

    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a text response from the LLM"""
        if not self.client:
            return "LLM Service not configured."

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.config.elefante.llm.temperature,
                max_tokens=self.config.elefante.llm.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return f"Error generating response: {e}"

    async def extract_entities(self, content: str) -> List[Dict[str, str]]:
        """
        Extract entities and tags from content using LLM.
        Returns a list of dicts: {"name": "X", "type": "Y"}
        """
        if not self.client:
            return []

        system_prompt = """
        You are an expert knowledge graph engineer. Extract key entities from the user's text.
        Return ONLY a JSON array of objects with 'name' and 'type' fields.
        Types should be one of: person, project, technology, organization, location, event, concept, file, task.
        Example: [{"name": "Elefante", "type": "project"}, {"name": "Python", "type": "technology"}]
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            
            result = json.loads(response.choices[0].message.content)
            # Handle both {"entities": [...]} and [...] formats
            if "entities" in result:
                return result["entities"]
            elif isinstance(result, list):
                return result
            else:
                # Try to find a list in the values
                for val in result.values():
                    if isinstance(val, list):
                        return val
                return []
                
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return []

# Global singleton
_llm_service: Optional[LLMService] = None

def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
