import logging
import asyncio
from typing import List
from src.services.llm_service import LLMService

class InteractiveQuestioner:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.logger = logging.getLogger(__name__)

    async def generate_initial_questions(self, topic: str, learning_objectives: str) -> List[str]:
        self.logger.info(f"Generating initial questions for topic: {topic}")

        prompt = f"""
        Generate 3-5 clarifying questions to better understand the user's specific interests
        and needs regarding the topic: '{topic}' with learning objectives: '{learning_objectives}'.
        """

        try:
            self.logger.info("Calling LLM with prompt...")
            response = await self.llm_service.generate_content(prompt)
            self.logger.info("LLM call successful")

            # Return each question as a new line (split by '\n')
            return response.split('\n') if isinstance(response, str) else response
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return ["An error occurred while generating questions."]

    async def generate_followup_questions(self, topic: str, learning_objectives: str, initial_answers: str, research_data: str) -> List[str]:
        self.logger.info("Generating follow-up questions based on user responses")

        prompt = f"""
        Based on the user's responses to initial questions:
        {initial_answers}
        
        And considering the research gathered on topic '{topic}' with objectives '{learning_objectives}':
        {research_data[:500]}... (truncated)
        
        Generate 2 follow-up questions to further personalize the learning content.
        These questions should address gaps, clarify ambiguities, or explore areas of interest.

        Return each question on a new line.
        """

        try:
            response = await self.llm_service.generate_content(prompt)
            return self._parse_questions(response)
        except Exception as e:
            self.logger.error(f"Error generating follow-up questions: {e}")
            return ["An error occurred while generating follow-up questions."]

    async def analyze_user_responses(self, questions: List[str], answers: List[str]) -> str:
        self.logger.info("Analyzing user responses to customize learning content")

        qa_pairs = [f"Q: {q}\nA: {a}" for q, a in zip(questions, answers)]
        qa_text = "\n\n".join(qa_pairs)

        prompt = f"""
        Analyze the following question-answer pairs:

        {qa_text}

        Extract the following insights:
        1. User's specific interests within the topic
        2. Prior knowledge level (beginner, intermediate, advanced)
        3. Preferred learning formats or styles
        4. Specific applications or contexts they're interested in

        Return the analysis as a JSON object with these four keys.
        """

        try:
            analysis = await self.llm_service.generate_content(prompt)
            return self._parse_analysis(analysis)
        except Exception as e:
            self.logger.error(f"Error analyzing user responses: {e}")
            return "{}"

    def _parse_questions(self, questions_text: str) -> List[str]:
        return [q.strip() for q in questions_text.strip().split('\n') if q.strip()]

    def _parse_analysis(self, analysis_text: str) -> str:
        # You can use json.loads if needed, but for now just returning text
        return analysis_text
