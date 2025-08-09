from fastapi import APIRouter
from .agents.researcher import ResearcherAgent
from .agents.marketer import MarketerAgent

router = APIRouter(prefix="/workflows", tags=["Workflows"])

@router.post("/lead_machine")
def lead_machine(keyword: str):
    research = ResearcherAgent().run(f"Find leads for {keyword}")
    campaign = MarketerAgent().run(f"Outreach for {keyword}", {"research": research})
    return {"research": research, "campaign": campaign}
