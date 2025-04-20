import os
import asyncio
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
from src.services.llm_service import LLMService
from src.services.citation_service import CitationService
from src.core.research_engine import ResearchEngine
from src.core.interactive_questioner import InteractiveQuestioner
from src.core.report_generator import ReportGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize services
llm_service = LLMService()
citation_service = CitationService()

# Initialize core components
research_engine = ResearchEngine(llm_service)
interactive_questioner = InteractiveQuestioner(llm_service)
report_generator = ReportGenerator(llm_service, citation_service)

# Create FastAPI app
app = FastAPI(
    title="Interactive Learning Assistant",
    description="AI-powered learning system that generates educational content",
    version="1.0.0"
)

# Define data models
class TopicRequest(BaseModel):
    topic: str
    learning_objectives: str

class QuestionResponse(BaseModel):
    answers: List[str]

class ReportRequest(BaseModel):
    topic: str
    learning_objectives: str
    responses: List[str]

class ReportModificationRequest(BaseModel):
    report_id: str
    feedback: str

class Report(BaseModel):
    id: str
    title: str
    content: str

# Store for reports (in-memory for prototype)
reports_store = {}

@app.post("/api/topics", response_model=List[str])
async def submit_topic(topic_request: TopicRequest):
    """
    Submit a topic and learning objectives to get initial questions
    """
    try:
        questions = await interactive_questioner.generate_initial_questions(
            topic_request.topic,
            topic_request.learning_objectives
        )
        return questions
    except Exception as e:
        logging.error(f"Error generating questions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate questions")

@app.post("/api/reports", response_model=Report)
async def generate_report(request: ReportRequest, background_tasks: BackgroundTasks):
    """
    Generate an educational report based on the topic and user responses
    """
    try:
        # Modify how research_data is extracted from the research engine result
        research_result = await research_engine.research_topic(
            request.topic,
            request.learning_objectives
        )

        # Extract the structured research data for report generation
        research_data = research_result["structured_data"]


        # Generate the same initial questions used during interaction
        questions = await interactive_questioner.generate_initial_questions(
            request.topic,
            request.learning_objectives
        )

        # Analyze user responses (now correctly awaited)
        user_preferences = await interactive_questioner.analyze_user_responses(
            questions[:len(request.responses)],
            request.responses
)


        # Generate the report
        report_content = await report_generator.generate_report(
            request.topic,
            request.learning_objectives,
            research_data,
            user_preferences
        )

        # Generate a unique ID for the report
        import uuid
        report_id = str(uuid.uuid4())

        # Store the report and research data
        reports_store[report_id] = {
            "content": report_content,
            "topic": request.topic,
            "learning_objectives": request.learning_objectives,
            "research_data": research_data
        }

        return Report(
            id=report_id,
            title=f"Report on {request.topic}",
            content=report_content
        )

    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate report")

@app.post("/api/reports/{report_id}/modify", response_model=Report)
async def modify_report(report_id: str, request: ReportModificationRequest):
    """
    Modify an existing report based on feedback
    """
    try:
        if report_id not in reports_store:
            raise HTTPException(status_code=404, detail="Report not found")

        original_report = reports_store[report_id]

        # Modify the report based on feedback
        modified_content = await report_generator.modify_report(
            original_report["content"],
            request.feedback,
            original_report["research_data"]
        )

        # Update stored report
        reports_store[report_id]["content"] = modified_content

        return Report(
            id=report_id,
            title=f"Report on {original_report['topic']} (Modified)",
            content=modified_content
        )

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error modifying report: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to modify report")

@app.get("/")
def root():
    return {"message": "🎓 Interactive Learning Assistant is up and running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
