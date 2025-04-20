import aiohttp
import logging
from typing import List

class AcademicSource:
    def __init__(self):
        self.base_url = "https://api.openalex.org/works"
        self.logger = logging.getLogger(__name__)
        
    async def gather_information(self, queries: List[str], max_papers=3):
        """Gather information from OpenAlex based on queries."""
        self.logger.info(f"Gathering academic information for {len(queries)} queries")
        all_results = []

        async with aiohttp.ClientSession() as session:
            for query in queries:
                try:
                    paper_results = await self._search_papers(session, query, max_papers)
                    all_results.extend(paper_results)
                except Exception as e:
                    self.logger.error(f"Error searching OpenAlex for '{query}': {str(e)}")

        return self._process_results(all_results)
    
    async def _search_papers(self, session, query: str, max_papers: int):
        """Search OpenAlex for academic papers."""
        url = f"{self.base_url}?search={query}&per_page={max_papers}"
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"OpenAlex API error: {response.status}")
            data = await response.json()
            results = []

            for item in data.get("results", []):
                authors = [a["author"]["display_name"] for a in item.get("authorships", [])]
                results.append({
                    "id": item["id"],
                    "title": item["title"],
                    "authors": authors,
                    "journal": item["host_venue"]["display_name"] if item.get("host_venue") else "Unknown Journal",
                    "year": item["publication_year"],
                    "doi": item["doi"] or "N/A",
                    "url": item["id"],
                    "abstract": item.get("abstract", "Abstract not available."),
                    "query": query
                })

            return results

    def _process_results(self, results):
        """Process and structure academic paper results."""
        processed_data = []
        
        for result in results:
            authors_str = ", ".join(result["authors"])
            citation = f"{authors_str} ({result['year']}). {result['title']}. {result['journal']}. DOI: {result['doi']}"
            
            processed_data.append({
                "content": result["abstract"],
                "title": result["title"],
                "authors": result["authors"],
                "journal": result["journal"],
                "year": result["year"],
                "doi": result["doi"],
                "url": result["url"],
                "citation": citation,
                "source_type": "academic",
                "query": result["query"]
            })
            
        return processed_data
