"""
SANA Index Routes
Practitioner credibility scoring with outcome-weighted methodology
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import uuid

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class SanaIndexInput(BaseModel):
    practitioner_id: str
    credentials: Optional[Dict] = None
    treatment_data: Optional[Dict] = None
    outcome_data: Optional[Dict] = None
    profile_data: Optional[Dict] = None
    review_data: Optional[Dict] = None


class SanaIndexBreakdown(BaseModel):
    credentials_score: float = Field(..., ge=0, le=20)
    credentials_details: Dict
    volume_score: float = Field(..., ge=0, le=20)
    volume_details: Dict
    outcomes_score: float = Field(..., ge=0, le=40)
    outcomes_details: Dict
    completeness_score: float = Field(..., ge=0, le=10)
    completeness_details: Dict
    satisfaction_score: float = Field(..., ge=0, le=10)
    satisfaction_details: Dict


class SanaIndexResponse(BaseModel):
    practitioner_id: str
    sana_index: float = Field(..., ge=0, le=100)
    percentile: int
    badge: Optional[str]  # Top 10%, Rising Star, etc.
    breakdown: SanaIndexBreakdown
    trend: str  # up, stable, down
    calculated_at: datetime


class LeaderboardEntry(BaseModel):
    rank: int
    practitioner_id: str
    name: str
    specialty: str
    sana_index: float
    badge: Optional[str]
    change: int  # rank change from last period


# ============================================================================
# MOCK DATA
# ============================================================================

PRACTITIONERS_INDEX = [
    {
        "practitioner_id": "prac_001",
        "name": "Dr. Emily Chen",
        "specialty": "Acupuncture",
        "sana_index": 87,
        "credentials_score": 18,
        "volume_score": 17,
        "outcomes_score": 36,
        "completeness_score": 8,
        "satisfaction_score": 8,
        "trend": "up",
        "percentile": 92
    },
    {
        "practitioner_id": "prac_002",
        "name": "Sarah Johnson",
        "specialty": "Naturopathy",
        "sana_index": 82,
        "credentials_score": 16,
        "volume_score": 15,
        "outcomes_score": 34,
        "completeness_score": 9,
        "satisfaction_score": 8,
        "trend": "stable",
        "percentile": 85
    },
    {
        "practitioner_id": "prac_003",
        "name": "James Wilson",
        "specialty": "Osteopathy",
        "sana_index": 88,
        "credentials_score": 19,
        "volume_score": 18,
        "outcomes_score": 35,
        "completeness_score": 8,
        "satisfaction_score": 8,
        "trend": "up",
        "percentile": 94
    },
    {
        "practitioner_id": "prac_004",
        "name": "Dr. Priya Sharma",
        "specialty": "Ayurveda",
        "sana_index": 84,
        "credentials_score": 17,
        "volume_score": 16,
        "outcomes_score": 34,
        "completeness_score": 9,
        "satisfaction_score": 8,
        "trend": "up",
        "percentile": 88
    },
    {
        "practitioner_id": "prac_005",
        "name": "Michael Roberts",
        "specialty": "Herbal Medicine",
        "sana_index": 79,
        "credentials_score": 15,
        "volume_score": 14,
        "outcomes_score": 32,
        "completeness_score": 10,
        "satisfaction_score": 8,
        "trend": "stable",
        "percentile": 78
    }
]


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/calculate", response_model=SanaIndexResponse)
async def calculate_sana_index(data: SanaIndexInput):
    """
    Calculate SANA Index for a practitioner

    **SANA Index Methodology:**

    | Component | Weight | Description |
    |-----------|--------|-------------|
    | Credentials | 20% | Education, licenses, certifications |
    | Volume | 20% | Treatment volume and experience |
    | **Outcomes** | **40%** | Client health improvements (key differentiator) |
    | Completeness | 10% | Profile and data quality |
    | Satisfaction | 10% | Client ratings and reviews |

    **Outcome Score (40% weight):**
    - Based on actual measured health improvements
    - Uses WHO-5, DASS-21, VAS, and CAM-specific PROMs
    - Compares to condition-specific benchmarks
    - Requires minimum sample size for reliability
    """
    # Find existing or calculate new
    existing = next(
        (p for p in PRACTITIONERS_INDEX if p["practitioner_id"] == data.practitioner_id),
        None
    )

    if existing:
        breakdown = SanaIndexBreakdown(
            credentials_score=existing["credentials_score"],
            credentials_details={
                "degrees": 2,
                "licenses": 1,
                "certifications": 3,
                "verified": True
            },
            volume_score=existing["volume_score"],
            volume_details={
                "total_clients": 156,
                "active_clients": 89,
                "sessions_this_year": 534,
                "years_experience": 8
            },
            outcomes_score=existing["outcomes_score"],
            outcomes_details={
                "avg_improvement": 0.72,
                "clients_measured": 134,
                "conditions_tracked": ["anxiety", "chronic_pain", "sleep"],
                "benchmark_comparison": "+15% above average"
            },
            completeness_score=existing["completeness_score"],
            completeness_details={
                "profile_complete": True,
                "bio_length": 450,
                "specialties_listed": 4,
                "availability_set": True
            },
            satisfaction_score=existing["satisfaction_score"],
            satisfaction_details={
                "avg_rating": 4.9,
                "review_count": 156,
                "response_rate": 0.95,
                "repeat_client_rate": 0.68
            }
        )

        badge = None
        if existing["percentile"] >= 90:
            badge = "Top 10%"
        elif existing["trend"] == "up" and existing["percentile"] >= 70:
            badge = "Rising Star"

        return SanaIndexResponse(
            practitioner_id=data.practitioner_id,
            sana_index=existing["sana_index"],
            percentile=existing["percentile"],
            badge=badge,
            breakdown=breakdown,
            trend=existing["trend"],
            calculated_at=datetime.utcnow()
        )
    else:
        # New practitioner - calculate from input data
        cred_score = 10.0  # Default starting score
        vol_score = 5.0
        out_score = 15.0
        comp_score = 5.0
        sat_score = 5.0

        total = cred_score + vol_score + out_score + comp_score + sat_score

        return SanaIndexResponse(
            practitioner_id=data.practitioner_id,
            sana_index=total,
            percentile=25,
            badge="New Practitioner",
            breakdown=SanaIndexBreakdown(
                credentials_score=cred_score,
                credentials_details={"status": "pending_verification"},
                volume_score=vol_score,
                volume_details={"status": "building_history"},
                outcomes_score=out_score,
                outcomes_details={"status": "collecting_data"},
                completeness_score=comp_score,
                completeness_details={"status": "profile_incomplete"},
                satisfaction_score=sat_score,
                satisfaction_details={"status": "awaiting_reviews"}
            ),
            trend="stable",
            calculated_at=datetime.utcnow()
        )


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    specialty: Optional[str] = None,
    location: Optional[str] = None,
    limit: int = Query(default=20, le=100)
):
    """
    Get top practitioners by SANA Index

    Leaderboard features:
    - Overall rankings
    - Specialty-specific rankings
    - Location-based rankings
    - Rank change indicators
    """
    practitioners = sorted(PRACTITIONERS_INDEX, key=lambda x: x["sana_index"], reverse=True)

    if specialty:
        practitioners = [p for p in practitioners if specialty.lower() in p["specialty"].lower()]

    leaderboard = []
    for i, p in enumerate(practitioners[:limit]):
        badge = None
        if i < len(practitioners) * 0.1:
            badge = "Top 10%"
        elif p["trend"] == "up":
            badge = "Rising"

        leaderboard.append(LeaderboardEntry(
            rank=i + 1,
            practitioner_id=p["practitioner_id"],
            name=p["name"],
            specialty=p["specialty"],
            sana_index=p["sana_index"],
            badge=badge,
            change=1 if p["trend"] == "up" else (0 if p["trend"] == "stable" else -1)
        ))

    return leaderboard


@router.get("/{practitioner_id}")
async def get_practitioner_index(practitioner_id: str):
    """
    Get SANA Index for a specific practitioner

    Returns full breakdown with:
    - Score components
    - Historical trend
    - Peer comparison
    """
    prac = next(
        (p for p in PRACTITIONERS_INDEX if p["practitioner_id"] == practitioner_id),
        None
    )

    if not prac:
        raise HTTPException(status_code=404, detail="Practitioner not found")

    return {
        "practitioner_id": practitioner_id,
        "name": prac["name"],
        "specialty": prac["specialty"],
        "sana_index": prac["sana_index"],
        "percentile": prac["percentile"],
        "trend": prac["trend"],
        "components": {
            "credentials": {"score": prac["credentials_score"], "max": 20, "weight": "20%"},
            "volume": {"score": prac["volume_score"], "max": 20, "weight": "20%"},
            "outcomes": {"score": prac["outcomes_score"], "max": 40, "weight": "40%"},
            "completeness": {"score": prac["completeness_score"], "max": 10, "weight": "10%"},
            "satisfaction": {"score": prac["satisfaction_score"], "max": 10, "weight": "10%"}
        },
        "peer_comparison": {
            "specialty_avg": 75,
            "platform_avg": 68,
            "your_rank": f"#{PRACTITIONERS_INDEX.index(prac) + 1} in {prac['specialty']}"
        }
    }


@router.get("/{practitioner_id}/history")
async def get_index_history(practitioner_id: str, months: int = 6):
    """
    Get SANA Index history over time

    Shows:
    - Monthly score changes
    - Component trends
    - Key events affecting score
    """
    history = []
    base_score = 75

    for i in range(months):
        history.append({
            "month": f"2024-{(12 - months + i + 1):02d}",
            "sana_index": base_score + i * 2,
            "outcomes_score": 28 + i * 1.5,
            "events": ["Completed 50 sessions"] if i == 2 else []
        })

    return {
        "practitioner_id": practitioner_id,
        "history": history,
        "growth_rate": "+12% over 6 months"
    }
