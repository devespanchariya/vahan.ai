import logging

class CitationService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def format_citations(self, research_data):
        """Format citations from research data in an appropriate style."""
        self.logger.info("Formatting citations from research data")
        
        # Handle empty or None research_data
        if not research_data:
            self.logger.warning("Empty research data provided for citation formatting")
            return "No citations available."
            
        citations = []
        
        try:
            # Process web sources
            web_sources = [item for item in research_data if isinstance(item, dict) and item.get("source_type") == "web"]
            for source in web_sources:
                try:
                    title = source.get('title', 'Untitled')
                    url = source.get('url', 'Unknown URL')
                    citation = f"{title}. Retrieved from {url}."
                    citations.append(citation)
                except Exception as e:
                    self.logger.error(f"Error formatting web citation: {e}")
            
            # Process video sources
            video_sources = [item for item in research_data if isinstance(item, dict) and item.get("source_type") == "video"]
            for source in video_sources:
                try:
                    creator = source.get('creator', 'Unknown Creator') 
                    published_date = source.get('published_date', 'n.d.')
                    title = source.get('title', 'Untitled')
                    url = source.get('url', '')
                    citation = f"{creator}. ({published_date}). {title} [Video]. YouTube. {url}."
                    citations.append(citation)
                except Exception as e:
                    self.logger.error(f"Error formatting video citation: {e}")
            
            # Process academic sources
            academic_sources = [item for item in research_data if isinstance(item, dict) and item.get("source_type") == "academic"]
            for source in academic_sources:
                try:
                    if "citation" in source:
                        citations.append(source["citation"])
                    else:
                        authors_list = source.get("authors", ["Unknown"])
                        # Handle both string and list authors
                        if isinstance(authors_list, str):
                            authors = authors_list
                        else:
                            authors = ", ".join(authors_list)
                        year = source.get('year', 'n.d.')
                        title = source.get('title', 'Untitled')
                        journal = source.get('journal', 'Unknown Journal')
                        doi = source.get('doi', 'Unknown DOI')
                        citation = f"{authors}. ({year}). {title}. {journal}. DOI: {doi}."
                        citations.append(citation)
                except Exception as e:
                    self.logger.error(f"Error formatting academic citation: {e}")
            
            # Format as numbered references
            if not citations:
                self.logger.warning("No citations were generated from the research data")
                return "No citations available."
                
            formatted_citations = []
            for i, citation in enumerate(citations, 1):
                formatted_citations.append(f"{i}. {citation}")
            
            return "\n".join(formatted_citations)
            
        except Exception as e:
            self.logger.error(f"Unexpected error in citation formatting: {e}")
            return "Citation formatting error occurred."