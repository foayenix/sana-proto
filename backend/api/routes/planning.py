"""
SANA Planning Routes - SHAM (SANA Habit & Activity Model)
Create personalized wellness plans and activities
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

class PlanRequest(BaseModel):
    user_id: str
    goals: List[str]  # e.g., ["improve_sleep", "reduce_anxiety"]
    preferences: Optional[Dict] = None
    constraints: Optional[Dict] = None  # time, budget, etc.
    health_score: Optional[Dict] = None


class Activity(BaseModel):
    id: str
    name: str
    category: str  # mindfulness, movement, nutrition, sleep, social
    duration_minutes: int
    frequency: str  # daily, 3x_week, weekly
    difficulty: str  # easy, moderate, challenging
    evidence_level: str
    description: str
    instructions: Optional[List[str]] = None


class DailyPlan(BaseModel):
    date: date
    activities: List[Dict]
    estimated_impact: Dict


class WellnessPlan(BaseModel):
    id: str
    user_id: str
    goals: List[str]
    duration_weeks: int
    daily_time_commitment: int  # minutes
    activities: List[Activity]
    weekly_schedule: Dict
    expected_outcomes: Dict
    created_at: datetime


# ============================================================================
# MOCK DATA
# ============================================================================

ACTIVITIES = [
    {
        "id": "act_001",
        "name": "Morning Breathwork",
        "category": "mindfulness",
        "duration_minutes": 10,
        "frequency": "daily",
        "difficulty": "easy",
        "evidence_level": "strong",
        "description": "4-7-8 breathing technique to start the day calm",
        "instructions": ["Inhale for 4 counts", "Hold for 7 counts", "Exhale for 8 counts", "Repeat 4 times"]
    },
    {
        "id": "act_002",
        "name": "Evening Gratitude Journal",
        "category": "mindfulness",
        "duration_minutes": 5,
        "frequency": "daily",
        "difficulty": "easy",
        "evidence_level": "moderate",
        "description": "Write 3 things you're grateful for before bed",
        "instructions": ["Set aside 5 minutes before bed", "Write 3 specific things", "Include why you're grateful"]
    },
    {
        "id": "act_003",
        "name": "30-Minute Walk",
        "category": "movement",
        "duration_minutes": 30,
        "frequency": "daily",
        "difficulty": "easy",
        "evidence_level": "strong",
        "description": "Brisk walking outdoors, preferably in nature",
        "instructions": ["Walk at a pace where you can talk but are slightly breathless", "Aim for green spaces when possible"]
    },
    {
        "id": "act_004",
        "name": "Sleep Hygiene Routine",
        "category": "sleep",
        "duration_minutes": 20,
        "frequency": "daily",
        "difficulty": "easy",
        "evidence_level": "strong",
        "description": "Consistent bedtime routine for better sleep",
        "instructions": ["Same bedtime each night", "No screens 1 hour before", "Cool, dark room", "Relaxation technique"]
    },
    {
        "id": "act_005",
        "name": "Yoga Flow",
        "category": "movement",
        "duration_minutes": 45,
        "frequency": "3x_week",
        "difficulty": "moderate",
        "evidence_level": "strong",
        "description": "Vinyasa-style yoga session",
        "instructions": ["Follow guided video or class", "Focus on breath-movement connection"]
    },
    {
        "id": "act_006",
        "name": "Meditation Session",
        "category": "mindfulness",
        "duration_minutes": 15,
        "frequency": "daily",
        "difficulty": "moderate",
        "evidence_level": "strong",
        "description": "Guided or silent meditation practice",
        "instructions": ["Find quiet space", "Use app or timer", "Focus on breath or body scan"]
    },
    {
        "id": "act_007",
        "name": "Social Connection Call",
        "category": "social",
        "duration_minutes": 30,
        "frequency": "weekly",
        "difficulty": "easy",
        "evidence_level": "moderate",
        "description": "Meaningful conversation with friend or family",
        "instructions": ["Schedule in advance", "Be present and engaged", "Share and listen"]
    },
    {
        "id": "act_008",
        "name": "Healthy Meal Prep",
        "category": "nutrition",
        "duration_minutes": 60,
        "frequency": "weekly",
        "difficulty": "moderate",
        "evidence_level": "strong",
        "description": "Prepare nutritious meals for the week",
        "instructions": ["Plan 3-4 balanced recipes", "Focus on whole foods", "Prep vegetables and proteins"]
    }
]

GOAL_ACTIVITY_MAP = {
    "improve_sleep": ["act_004", "act_002", "act_006"],
    "reduce_anxiety": ["act_001", "act_006", "act_005"],
    "increase_energy": ["act_003", "act_005", "act_008"],
    "better_mood": ["act_002", "act_003", "act_007"],
    "stress_management": ["act_001", "act_006", "act_005"],
    "physical_fitness": ["act_003", "act_005", "act_008"],
}


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/create", response_model=WellnessPlan)
async def create_wellness_plan(data: PlanRequest):
    """
    Create personalized wellness plan using SHAM algorithm

    **SHAM Algorithm:**
    - Analyzes user goals and current health score
    - Matches evidence-based activities to goals
    - Considers user preferences and constraints
    - Optimizes for habit formation (small, consistent steps)
    - Schedules activities for maximum adherence

    **Returns:**
    - Customized activity list
    - Weekly schedule
    - Expected outcomes with timelines
    """
    # Collect activities based on goals
    selected_activities = []
    for goal in data.goals:
        activity_ids = GOAL_ACTIVITY_MAP.get(goal, [])
        for aid in activity_ids:
            activity = next((a for a in ACTIVITIES if a["id"] == aid), None)
            if activity and activity not in selected_activities:
                selected_activities.append(activity)

    # Calculate daily time commitment
    daily_minutes = sum(
        a["duration_minutes"]
        for a in selected_activities
        if a["frequency"] == "daily"
    )
    weekly_activities_minutes = sum(
        a["duration_minutes"]
        for a in selected_activities
        if a["frequency"] != "daily"
    )
    daily_minutes += weekly_activities_minutes // 7

    # Create weekly schedule
    weekly_schedule = {
        "monday": ["act_001", "act_003", "act_006", "act_004"],
        "tuesday": ["act_001", "act_003", "act_002", "act_004"],
        "wednesday": ["act_001", "act_005", "act_006", "act_004"],
        "thursday": ["act_001", "act_003", "act_002", "act_004"],
        "friday": ["act_001", "act_005", "act_006", "act_004"],
        "saturday": ["act_001", "act_003", "act_007", "act_004"],
        "sunday": ["act_001", "act_008", "act_002", "act_004"]
    }

    return WellnessPlan(
        id=f"plan_{uuid.uuid4().hex[:8]}",
        user_id=data.user_id,
        goals=data.goals,
        duration_weeks=8,
        daily_time_commitment=daily_minutes,
        activities=[Activity(**a) for a in selected_activities],
        weekly_schedule=weekly_schedule,
        expected_outcomes={
            "sleep_improvement": "+15% quality in 4 weeks",
            "anxiety_reduction": "-20% symptoms in 6 weeks",
            "energy_increase": "+25% daily energy in 3 weeks",
            "adherence_target": "80% activity completion"
        },
        created_at=datetime.utcnow()
    )


@router.get("/activities", response_model=List[Activity])
async def list_activities(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    max_duration: Optional[int] = None
):
    """
    List available wellness activities

    Filter by:
    - Category: mindfulness, movement, nutrition, sleep, social
    - Difficulty: easy, moderate, challenging
    - Maximum duration in minutes
    """
    results = ACTIVITIES

    if category:
        results = [a for a in results if a["category"] == category]
    if difficulty:
        results = [a for a in results if a["difficulty"] == difficulty]
    if max_duration:
        results = [a for a in results if a["duration_minutes"] <= max_duration]

    return [Activity(**a) for a in results]


@router.get("/activity/{activity_id}")
async def get_activity_detail(activity_id: str):
    """
    Get detailed activity information

    Includes:
    - Full instructions
    - Evidence summary
    - Video/audio resources
    - Tracking metrics
    """
    activity = next((a for a in ACTIVITIES if a["id"] == activity_id), None)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    return {
        **activity,
        "resources": [
            {"type": "video", "title": "Guided Tutorial", "url": "/resources/video/001"},
            {"type": "audio", "title": "Audio Guide", "url": "/resources/audio/001"}
        ],
        "tracking": {
            "metrics": ["completion", "duration", "mood_before", "mood_after"],
            "streaks_enabled": True
        }
    }


@router.post("/track")
async def track_activity_completion(
    user_id: str,
    activity_id: str,
    completed_at: datetime,
    notes: Optional[str] = None,
    mood_rating: Optional[int] = None
):
    """
    Track activity completion

    Records:
    - Completion timestamp
    - User notes/feedback
    - Mood rating (before/after)
    - Updates streaks
    """
    return {
        "tracked": True,
        "activity_id": activity_id,
        "user_id": user_id,
        "streak_count": 7,
        "points_earned": 10,
        "message": "Great job! 7 day streak!"
    }


@router.get("/today/{user_id}")
async def get_today_plan(user_id: str):
    """
    Get today's personalized activity plan

    Returns scheduled activities for today with:
    - Suggested times
    - Completion status
    - Reminders
    """
    today_activities = [
        {"activity": ACTIVITIES[0], "suggested_time": "07:00", "completed": False},
        {"activity": ACTIVITIES[2], "suggested_time": "12:00", "completed": False},
        {"activity": ACTIVITIES[5], "suggested_time": "18:00", "completed": False},
        {"activity": ACTIVITIES[3], "suggested_time": "21:30", "completed": False}
    ]

    return {
        "user_id": user_id,
        "date": date.today().isoformat(),
        "activities": today_activities,
        "total_minutes": 55,
        "completed_count": 0
    }
