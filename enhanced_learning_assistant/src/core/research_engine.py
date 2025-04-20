from src.data.sources.web_source import WebSource
from src.data.sources.video_source import VideoSource
from src.data.sources.academic_source import AcademicSource
from src.services.llm_service import LLMService
import logging

class ResearchEngine:
    def __init__(self, llm_service):
        self.web_source = WebSource()
        self.video_source = VideoSource()
        self.academic_source = AcademicSource()
        self.llm_service = llm_service
        self.logger = logging.getLogger(__name__)

    async def research_topic(self, topic, learning_objectives):
        """Conducts comprehensive research on a given topic."""
        self.logger.info(f"Starting research on topic: {topic}")
        
        # Create research queries based on topic and objectives
        research_queries = await self._generate_research_queries(topic, learning_objectives)  # Await the call
        
        # Gather information from different sources
        web_data = await self.web_source.gather_information(research_queries)
        video_data = await self.video_source.gather_information(research_queries)
        academic_data = await self.academic_source.gather_information(research_queries)
        
        # Combine and synthesize the research data
        combined_data = self._combine_research_data(web_data, video_data, academic_data)
        synthesized_research = await self._synthesize_research(combined_data, topic, learning_objectives)  # Await the synthesis
        
        return synthesized_research
    
    async def _generate_research_queries(self, topic, learning_objectives):
        """Generate specific research queries based on the topic and learning objectives."""
        prompt = f"""
        Generate 5-7 specific research queries based on this topic: '{topic}' 
        and these learning objectives: '{learning_objectives}'.
        The queries should cover different aspects of the topic and help gather comprehensive information.
        Return only the queries as a list.
        """
        
        # Await the LLM service to get the generated queries
        queries = await self.llm_service.generate_content(prompt)  # Await the LLM response
        return self._parse_queries(queries)
    
    def _parse_queries(self, queries_text):
        """Parse the generated queries into a list."""
        return [q.strip() for q in queries_text.split('\n') if q.strip()]
    
    def _combine_research_data(self, web_data, video_data, academic_data):
        """Combine research data from different sources."""
        return {
            "web_data": web_data,
            "video_data": video_data,
            "academic_data": academic_data
        }
    
    async def _synthesize_research(self, combined_data, topic, learning_objectives):
        """Synthesize the research data into a coherent form."""
        try:
            prompt = f"""
            Synthesize the following research data into a coherent form that addresses the topic: '{topic}' 
            and these learning objectives: '{learning_objectives}'.
            
            Web data: {combined_data['web_data']}
            Video data: {combined_data['video_data']}
            Academic data: {combined_data['academic_data']}
            
            Focus on creating a comprehensive synthesis that highlights key information,
            identifies patterns across sources, and addresses the learning objectives.
            """
            
            # Await the LLM service to get the synthesized content
            synthesized_content = await self.llm_service.generate_content(prompt)  # Await the content synthesis
            
            # Return a structured format compatible with CitationService
            structured_data = []
            
            # Add web data as structured items
            for i, item in enumerate(combined_data['web_data']):
                if isinstance(item, dict):
                    structured_data.append(item)
                elif isinstance(item, str):
                    structured_data.append({
                        "source_type": "web",
                        "title": f"Web Source {i+1}",
                        "content": item,
                        "url": "https://example.com"
                    })
            
            # Similar for video and academic data
            for i, item in enumerate(combined_data['video_data']):
                if isinstance(item, dict):
                    structured_data.append(item)
                elif isinstance(item, str):
                    structured_data.append({
                        "source_type": "video",
                        "title": f"Video Source {i+1}",
                        "content": item,
                        "creator": "Unknown",
                        "published_date": "n.d.",
                        "url": "https://example.com/video"
                    })
            
            for i, item in enumerate(combined_data['academic_data']):
                if isinstance(item, dict):
                    structured_data.append(item)
                elif isinstance(item, str):
                    structured_data.append({
                        "source_type": "academic",
                        "title": f"Academic Source {i+1}",
                        "content": item,
                        "authors": ["Unknown Author"],
                        "year": "n.d.",
                        "journal": "Unknown Journal",
                        "doi": "Unknown DOI"
                    })
            
            return {
                "synthesized_content": synthesized_content,
                "structured_data": structured_data
            }
        except Exception as e:
            self.logger.error(f"Error in synthesis: {str(e)}")
            # If synthesis fails, return minimal structured data
            return {
                "synthesized_content": "Research synthesis could not be completed due to technical limitations.",
                "structured_data": []
            }
