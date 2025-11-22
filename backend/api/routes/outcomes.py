"""
SANA Outcomes Routes
Patient-Reported Outcome Measures (PROMs)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime, date
import uuid

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class Question(BaseModel):
    id: str
    text: str
    type: str  # scale, choice, text
    options: Optional[List[Dict]] = None
    scale_min: Optional[int] = None
    scale_max: Optional[int] = None
    scale_labels: Optional[Dict] = None


class Questionnaire(BaseModel):
    id: str
    name: str
    code: str  # WHO-5, DASS-21, VAS, CAM
    description: str
    questions: List[Question]
    scoring_method: str
    interpretation: Dict


class OutcomeSubmission(BaseModel):
    user_id: str
    questionnaire_code: str
    responses: Dict[str, int]  # question_id -> answer
    practitioner_id: Optional[str] = None
    condition: Optional[str] = None


class OutcomeResult(BaseModel):
    id: str
    user_id: str
    questionnaire_code: str
    total_score: float
    interpretation: str
    percentile: Optional[int] = None
    change_from_baseline: Optional[float] = None
    recorded_at: datetime


# ============================================================================
# MOCK DATA - QUESTIONNAIRES
# ============================================================================

QUESTIONNAIRES = {
    "WHO-5": {
        "id": "q_who5",
        "name": "WHO-5 Well-Being Index",
        "code": "WHO-5",
        "description": "A short questionnaire measuring current mental well-being",
        "questions": [
            {"id": "who5_1", "text": "I have felt cheerful and in good spirits", "type": "scale", "scale_min": 0, "scale_max": 5, "scale_labels": {"0": "At no time", "5": "All of the time"}},
            {"id": "who5_2", "text": "I have felt calm and relaxed", "type": "scale", "scale_min": 0, "scale_max": 5, "scale_labels": {"0": "At no time", "5": "All of the time"}},
            {"id": "who5_3", "text": "I have felt active and vigorous", "type": "scale", "scale_min": 0, "scale_max": 5, "scale_labels": {"0": "At no time", "5": "All of the time"}},
            {"id": "who5_4", "text": "I woke up feeling fresh and rested", "type": "scale", "scale_min": 0, "scale_max": 5, "scale_labels": {"0": "At no time", "5": "All of the time"}},
            {"id": "who5_5", "text": "My daily life has been filled with things that interest me", "type": "scale", "scale_min": 0, "scale_max": 5, "scale_labels": {"0": "At no time", "5": "All of the time"}}
        ],
        "scoring_method": "sum * 4 (0-100 scale)",
        "interpretation": {
            "0-28": "Poor well-being - consider professional support",
            "29-50": "Low well-being",
            "51-72": "Moderate well-being",
            "73-100": "High well-being"
        }
    },
    "DASS-21": {
        "id": "q_dass21",
        "name": "Depression Anxiety Stress Scale (DASS-21)",
        "code": "DASS-21",
        "description": "Measures depression, anxiety, and stress symptoms",
        "questions": [
            {"id": "dass_1", "text": "I found it hard to wind down", "type": "scale", "scale_min": 0, "scale_max": 3, "scale_labels": {"0": "Never", "3": "Almost always"}},
            {"id": "dass_2", "text": "I was aware of dryness of my mouth", "type": "scale", "scale_min": 0, "scale_max": 3, "scale_labels": {"0": "Never", "3": "Almost always"}},
            {"id": "dass_3", "text": "I couldn't seem to experience any positive feeling at all", "type": "scale", "scale_min": 0, "scale_max": 3, "scale_labels": {"0": "Never", "3": "Almost always"}},
            # ... more questions would be here
        ],
        "scoring_method": "subscale sums * 2",
        "interpretation": {
            "depression": {"0-9": "Normal", "10-13": "Mild", "14-20": "Moderate", "21-27": "Severe", "28+": "Extremely Severe"},
            "anxiety": {"0-7": "Normal", "8-9": "Mild", "10-14": "Moderate", "15-19": "Severe", "20+": "Extremely Severe"},
            "stress": {"0-14": "Normal", "15-18": "Mild", "19-25": "Moderate", "26-33": "Severe", "34+": "Extremely Severe"}
        }
    },
    "VAS": {
        "id": "q_vas",
        "name": "Visual Analogue Scale - Pain",
        "code": "VAS",
        "description": "Simple pain intensity measurement",
        "questions": [
            {"id": "vas_1", "text": "Rate your current pain level", "type": "scale", "scale_min": 0, "scale_max": 10, "scale_labels": {"0": "No pain", "10": "Worst pain imaginable"}}
        ],
        "scoring_method": "direct score (0-10)",
        "interpretation": {
            "0": "No pain",
            "1-3": "Mild pain",
            "4-6": "Moderate pain",
            "7-10": "Severe pain"
        }
    },
    "CAM": {
        "id": "q_cam",
        "name": "CAM-Specific Outcome Measure",
        "code": "CAM",
        "description": "Holistic outcome measure for complementary therapies",
        "questions": [
            {"id": "cam_1", "text": "Overall, how would you rate your health?", "type": "scale", "scale_min": 1, "scale_max": 5, "scale_labels": {"1": "Poor", "5": "Excellent"}},
            {"id": "cam_2", "text": "How much has your condition affected your daily activities?", "type": "scale", "scale_min": 1, "scale_max": 5, "scale_labels": {"1": "Severely", "5": "Not at all"}},
            {"id": "cam_3", "text": "How satisfied are you with your current energy levels?", "type": "scale", "scale_min": 1, "scale_max": 5, "scale_labels": {"1": "Very dissatisfied", "5": "Very satisfied"}},
            {"id": "cam_4", "text": "How would you rate your emotional wellbeing?", "type": "scale", "scale_min": 1, "scale_max": 5, "scale_labels": {"1": "Very poor", "5": "Excellent"}},
            {"id": "cam_5", "text": "How confident do you feel about managing your health?", "type": "scale", "scale_min": 1, "scale_max": 5, "scale_labels": {"1": "Not confident", "5": "Very confident"}}
        ],
        "scoring_method": "mean score (1-5)",
        "interpretation": {
            "1.0-2.0": "Poor outcomes",
            "2.1-3.0": "Below average",
            "3.1-4.0": "Good outcomes",
            "4.1-5.0": "Excellent outcomes"
        }
    }
}


# ============================================================================
# ROUTES
# ============================================================================

@router.get("/questionnaire/{type}", response_model=Questionnaire)
async def get_questionnaire(type: str):
    """
    Get questionnaire by type

    **Available Questionnaires:**
    - WHO-5: Well-Being Index (5 questions)
    - DASS-21: Depression, Anxiety, Stress (21 questions)
    - VAS: Visual Analogue Scale for Pain (1 question)
    - CAM: CAM-Specific Outcome Measure (5 questions)
    """
    questionnaire = QUESTIONNAIRES.get(type.upper())
    if not questionnaire:
        raise HTTPException(status_code=404, detail=f"Questionnaire {type} not found")

    return Questionnaire(**questionnaire)


@router.get("/questionnaires")
async def list_questionnaires():
    """
    List all available questionnaires

    Returns summary of each questionnaire type
    """
    return {
        "questionnaires": [
            {
                "code": q["code"],
                "name": q["name"],
                "description": q["description"],
                "question_count": len(q["questions"])
            }
            for q in QUESTIONNAIRES.values()
        ]
    }


@router.post("/submit", response_model=OutcomeResult)
async def submit_outcome(data: OutcomeSubmission):
    """
    Submit questionnaire responses

    **Scoring:**
    - Calculates total and subscale scores
    - Compares to baseline (if available)
    - Generates interpretation
    - Links to practitioner for outcome tracking
    """
    questionnaire = QUESTIONNAIRES.get(data.questionnaire_code.upper())
    if not questionnaire:
        raise HTTPException(status_code=404, detail="Questionnaire not found")

    # Calculate score (simplified)
    total_score = sum(data.responses.values())

    # Scale to 0-100 for WHO-5
    if data.questionnaire_code.upper() == "WHO-5":
        total_score = total_score * 4

    # Determine interpretation
    interpretation = "Moderate"  # Simplified - would lookup from interpretation dict

    result_id = f"out_{uuid.uuid4().hex[:8]}"

    return OutcomeResult(
        id=result_id,
        user_id=data.user_id,
        questionnaire_code=data.questionnaire_code,
        total_score=total_score,
        interpretation=interpretation,
        percentile=65,
        change_from_baseline=+12.5,
        recorded_at=datetime.utcnow()
    )


@router.get("/history/{user_id}")
async def get_outcome_history(
    user_id: str,
    questionnaire_code: Optional[str] = None,
    condition: Optional[str] = None
):
    """
    Get user's outcome history

    Shows:
    - Score trends over time
    - Improvement percentages
    - Condition-specific outcomes
    """
    history = [
        {"date": "2024-01-15", "code": "WHO-5", "score": 48, "interpretation": "Low well-being"},
        {"date": "2024-02-15", "code": "WHO-5", "score": 56, "interpretation": "Moderate well-being"},
        {"date": "2024-03-15", "code": "WHO-5", "score": 64, "interpretation": "Moderate well-being"},
        {"date": "2024-04-15", "code": "WHO-5", "score": 68, "interpretation": "Moderate well-being"},
        {"date": "2024-05-15", "code": "WHO-5", "score": 72, "interpretation": "Moderate well-being"},
        {"date": "2024-06-15", "code": "WHO-5", "score": 76, "interpretation": "High well-being"},
    ]

    return {
        "user_id": user_id,
        "history": history,
        "baseline": 48,
        "current": 76,
        "improvement": "+58%",
        "trend": "improving"
    }


@router.post("/schedule")
async def schedule_assessment(
    user_id: str,
    questionnaire_code: str,
    frequency: str,  # weekly, biweekly, monthly
    start_date: date,
    practitioner_id: Optional[str] = None
):
    """
    Schedule recurring outcome assessments

    **Frequency Options:**
    - weekly: Every 7 days
    - biweekly: Every 14 days
    - monthly: Every 30 days
    """
    schedule_id = f"sched_{uuid.uuid4().hex[:8]}"

    return {
        "schedule_id": schedule_id,
        "user_id": user_id,
        "questionnaire_code": questionnaire_code,
        "frequency": frequency,
        "start_date": str(start_date),
        "next_due": str(start_date),
        "reminder_enabled": True,
        "practitioner_id": practitioner_id
    }


@router.get("/practitioner/{practitioner_id}/outcomes")
async def get_practitioner_outcomes(practitioner_id: str, condition: Optional[str] = None):
    """
    Get aggregated outcomes for a practitioner

    **Outcome Analytics:**
    - Average improvement rates
    - Condition-specific success
    - Comparison to platform benchmarks
    """
    return {
        "practitioner_id": practitioner_id,
        "clients_measured": 134,
        "avg_improvement": 0.72,
        "platform_benchmark": 0.58,
        "above_benchmark": True,
        "by_condition": [
            {"condition": "anxiety", "clients": 45, "improvement": 0.78, "questionnaire": "DASS-21"},
            {"condition": "chronic_pain", "clients": 28, "improvement": 0.65, "questionnaire": "VAS"},
            {"condition": "wellbeing", "clients": 61, "improvement": 0.71, "questionnaire": "WHO-5"}
        ],
        "by_timeframe": [
            {"period": "4 weeks", "improvement": 0.35},
            {"period": "8 weeks", "improvement": 0.58},
            {"period": "12 weeks", "improvement": 0.72}
        ]
    }
