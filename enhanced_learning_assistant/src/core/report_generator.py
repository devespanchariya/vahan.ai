from src.services.llm_service import LLMService
from src.services.citation_service import CitationService
import logging
import json

class ReportGenerator:
    def __init__(self, llm_service: LLMService, citation_service: CitationService):
        """Initializes the report generator with necessary services."""
        self.llm_service = llm_service
        self.citation_service = citation_service
        self.logger = logging.getLogger(__name__)

    def _condense_research_data(self, research_data, limit=2000): 
        condensed = ""
        for item in research_data:
            section = f"Title: {item.get('title', '')}\nContent: {item.get('content', '')[:300]}\n\n"  
            if len(condensed + section) > limit:
                break
            condensed += section
        return condensed

    async def generate_report(self, topic, learning_objectives, research_data, user_preferences):
        """Generates an educational report based on research data and user preferences."""
        MAX_CHARS = 2000
        # Only truncate research items, not convert list to string!
        if len(research_data) > 10:
            self.logger.warning("Truncating research items to fit within token limit.")
            research_data = research_data[:10]
        
        # Decode user preferences if necessary
        if isinstance(user_preferences, str):
            try:
                user_preferences = json.loads(user_preferences)
            except json.JSONDecodeError:
                self.logger.warning("Could not decode user preferences JSON.")
                user_preferences = {}
        
        self.logger.info(f"Generating educational report for topic: {topic}")
        self.logger.debug(f"User preferences: {user_preferences}")

        # Extract user preferences safely
        knowledge_level = "intermediate"
        interests = []
        preferred_formats = []
        
        # Try to extract values with proper error handling
        try:
            if isinstance(user_preferences, dict):
                knowledge_level = user_preferences.get('prior knowledge level', 'intermediate')
                interests = user_preferences.get('specific interests', [])
                preferred_formats = user_preferences.get('preferred learning formats', [])
        except Exception as e:
            self.logger.warning(f"Error extracting user preferences: {e}")

        # Condense research data and format citations
        try:
            citations = self.citation_service.format_citations(research_data)
            condensed_data = self._condense_research_data(research_data)
        except Exception as e:
            self.logger.error(f"Error formatting research data: {e}")
            citations = "Citation formatting failed."
            condensed_data = "Data condensing failed."

        # Construct the prompt for the LLM model
        prompt = f"""
        Generate a comprehensive educational report on the topic: '{topic}'
        that addresses these learning objectives: '{learning_objectives}'.

        Tailor the report to a {knowledge_level} knowledge level.
        Focus on these specific interests: {', '.join(interests) if isinstance(interests, list) else str(interests)}
        Include content in these preferred formats: {', '.join(preferred_formats) if isinstance(preferred_formats, list) else str(preferred_formats)}

        Based on this research data:
        {condensed_data}

        Create a report with:
        1. A clear introduction explaining the topic's importance
        2. Logically structured sections with progressive learning flow
        3. Visual aids and diagrams described in markdown format
        4. Examples and applications
        5. Citations for all factual information
        6. A conclusion summarizing key takeaways
        7. Recommended additional resources

        Use markdown formatting for structure.
        Include these citations appropriately: {citations[:500]}... (truncated)
        """

        self.logger.debug(f"Final LLM prompt: {prompt[:500]}...")

        try:
            # Generate the report content using LLM - now correctly awaits the async function
            report_content = await self.llm_service.generate_content(prompt, 4000)
            self.logger.debug(f"Raw report content: {report_content[:500]}...")

            # Format the report with citations
            final_report = self._format_report(report_content, citations)
            return final_report

        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            return "Content generation failed internally"

    def _format_report(self, report_content, citations):
        """Format the report with proper structure and citations."""
        # Check if there are already references/citations sections in the content
        if "## References" in report_content or "## Citations" in report_content:
            self.logger.info("Report already contains references/citations section")
            # If there are duplicate citations, try to remove them
            if report_content.count("## References") > 1 or report_content.count("## Citations") > 1:
                # Keep only the first instance of references/citations section
                pattern1 = "## References"
                pattern2 = "## Citations"
                
                if pattern1 in report_content:
                    split_index = report_content.find(pattern1)
                    report_content = report_content[:split_index]
                elif pattern2 in report_content:
                    split_index = report_content.find(pattern2)
                    report_content = report_content[:split_index]
        
        # Ensure there's a line break before adding references
        if not report_content.endswith("\n\n"):
            report_content += "\n\n"
        
        # Add references section
        report_content += "## References\n\n"
        report_content += citations
        
        return report_content
    async def modify_report(self, original_report, feedback, research_data):
        """Modify an existing report based on user feedback."""
        self.logger.info("Modifying report based on user feedback")

        # Construct the prompt for modification
        prompt = f"""
Modify this educational report:

{original_report[:1000]}... (truncated)

Based on this user feedback:
{feedback}

And using this research data if needed:
{research_data[:500]}... (truncated)

Make targeted modifications that address the feedback while maintaining the
report's overall structure and quality. Ensure all new information includes
proper citations.
"""

        try:
            # Generate the modified report using LLM - now correctly awaits the async function
            modified_report = await self.llm_service.generate_content(prompt, 4000)
            return modified_report
        except Exception as e:
            self.logger.error(f"Error modifying report: {str(e)}")
            return "Report modification failed internally"