"""
SANA Scoring Routes - SISM (SANA Integrative Scoring Model)
Calculate holistic health scores across multiple domains
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import random

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class HealthScoreInput(BaseModel):
    user_id: str
    questionnaire_responses: Optional[Dict] = None
    wearable_data: Optional[Dict] = None
    journal_sentiment: Optional[float] = None  # -1 to 1


class DomainScore(BaseModel):
    domain: str
    score: float = Field(..., ge=0, le=100)
    trend: str  # up, down, stable
    data_sources: List[str]


class HealthScoreResponse(BaseModel):
    user_id: str
    overall_score: float = Field(..., ge=0, le=100)
    status: str  # Thriving, Good, Fair, Needs Attention
    biological_age: int
    chronological_age: int
    domains: List[DomainScore]
    top_levers: List[Dict]
    calculated_at: datetime


class Domain(BaseModel):
    id: str
    name: str
    description: str
    weight: float
    data_sources: List[str]


class QuestionnaireQuestion(BaseModel):
    id: str
    domain: str
    text: str
    type: str  # scale, choice, text
    options: Optional[List[str]] = None
    scale_min: Optional[int] = None
    scale_max: Optional[int] = None


# ============================================================================
# MOCK DATA
# ============================================================================

DOMAINS = [
    {"id": "physical", "name": "Physical Health", "description": "Body function, fitness, nutrition", "weight": 0.20, "data_sources": ["wearables", "questionnaire"]},
    {"id": "mental", "name": "Mental Wellbeing", "description": "Cognitive function, clarity, focus", "weight": 0.20, "data_sources": ["questionnaire", "journal"]},
    {"id": "emotional", "name": "Emotional Balance", "description": "Mood regulation, stress response", "weight": 0.20, "data_sources": ["journal", "questionnaire"]},
    {"id": "social", "name": "Social Connection", "description": "Relationships, community, support", "weight": 0.15, "data_sources": ["questionnaire"]},
    {"id": "sleep", "name": "Sleep Quality", "description": "Rest, recovery, circadian rhythm", "weight": 0.15, "data_sources": ["wearables", "questionnaire"]},
    {"id": "energy", "name": "Energy Levels", "description": "Vitality, stamina, motivation", "weight": 0.10, "data_sources": ["wearables", "journal"]},
]

QUESTIONNAIRE = [
    {"id": "q1", "domain": "physical", "text": "How would you rate your overall physical health?", "type": "scale", "scale_min": 1, "scale_max": 10},
    {"id": "q2", "domain": "physical", "text": "How many days per week do you exercise?", "type": "scale", "scale_min": 0, "scale_max": 7},
    {"id": "q3", "domain": "mental", "text": "How clear and focused do you feel mentally?", "type": "scale", "scale_min": 1, "scale_max": 10},
    {"id": "q4", "domain": "emotional", "text": "How well are you managing stress?", "type": "scale", "scale_min": 1, "scale_max": 10},
    {"id": "q5", "domain": "social", "text": "How satisfied are you with your social connections?", "type": "scale", "scale_min": 1, "scale_max": 10},
    {"id": "q6", "domain": "sleep", "text": "How would you rate your sleep quality?", "type": "scale", "scale_min": 1, "scale_max": 10},
    {"id": "q7", "domain": "energy", "text": "How energetic do you feel throughout the day?", "type": "scale", "scale_min": 1, "scale_max": 10},
]


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/calculate", response_model=HealthScoreResponse)
async def calculate_health_score(data: HealthScoreInput):
    """
    Calculate holistic health score using SISM algorithm

    **SISM Algorithm:**
    - Integrates data from multiple sources (wearables, questionnaires, journals)
    - Calculates domain-specific scores
    - Weighs domains based on evidence and user goals
    - Estimates biological age based on biomarkers
    - Identifies top improvement levers

    **Data Sources:**
    - Wearables: HRV, steps, sleep, heart rate
    - Questionnaire: Self-reported health metrics
    - Journal: Sentiment analysis, mood patterns
    """
    # Simulate SISM calculation
    domain_scores = []
    for domain in DOMAINS:
        base_score = random.uniform(65, 90)
        domain_scores.append(DomainScore(
            domain=domain["name"],
            score=round(base_score, 1),
            trend=random.choice(["up", "stable", "down"]),
            data_sources=domain["data_sources"]
        ))

    overall = sum(d.score * DOMAINS[i]["weight"] for i, d in enumerate(domain_scores))

    # Determine status
    if overall >= 80:
        status = "Thriving"
    elif overall >= 65:
        status = "Good"
    elif overall >= 50:
        status = "Fair"
    else:
        status = "Needs Attention"

    # Top levers (lowest scoring domains)
    sorted_domains = sorted(domain_scores, key=lambda x: x.score)
    top_levers = [
        {
            "domain": sorted_domains[0].domain,
            "current_score": sorted_domains[0].score,
            "recommendation": "Improve sleep consistency for better recovery",
            "impact": "high"
        },
        {
            "domain": sorted_domains[1].domain,
            "current_score": sorted_domains[1].score,
            "recommendation": "Add 10 minutes of daily mindfulness",
            "impact": "medium"
        },
        {
            "domain": sorted_domains[2].domain,
            "current_score": sorted_domains[2].score,
            "recommendation": "Increase social activities this week",
            "impact": "medium"
        }
    ]

    return HealthScoreResponse(
        user_id=data.user_id,
        overall_score=round(overall, 1),
        status=status,
        biological_age=32,
        chronological_age=38,
        domains=domain_scores,
        top_levers=top_levers,
        calculated_at=datetime.utcnow()
    )


@router.get("/domains", response_model=List[Domain])
async def list_domains():
    """
    List all health scoring domains

    Returns domain definitions including:
    - Domain name and description
    - Weight in overall score
    - Required data sources
    """
    return [Domain(**d) for d in DOMAINS]


@router.get("/questionnaire", response_model=List[QuestionnaireQuestion])
async def get_questionnaire():
    """
    Get health assessment questionnaire

    Returns questions for self-reported health metrics:
    - Physical health
    - Mental wellbeing
    - Emotional balance
    - Social connection
    - Sleep quality
    - Energy levels
    """
    return [QuestionnaireQuestion(**q) for q in QUESTIONNAIRE]


@router.get("/history/{user_id}")
async def get_score_history(user_id: str, days: int = 30):
    """
    Get historical health scores

    - Returns score timeline
    - Shows trends per domain
    - Identifies patterns
    """
    history = []
    for i in range(days):
        history.append({
            "date": datetime(2024, 1, 1).isoformat(),
            "overall_score": round(random.uniform(70, 85), 1),
            "status": "Good"
        })
    return {"user_id": user_id, "history": history}
