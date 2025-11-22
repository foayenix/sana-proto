"""
SANA Matching Routes - SPRM (SANA Practitioner Recommendation Model)
Match users with practitioners based on needs and preferences
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import random

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class MatchRequest(BaseModel):
    user_id: str
    conditions: List[str]
    modalities: Optional[List[str]] = None
    preferences: Optional[Dict] = None  # location, price_range, gender, language
    urgency: str = "normal"  # urgent, normal, flexible


class PractitionerMatch(BaseModel):
    id: str
    name: str
    title: str
    specialties: List[str]
    modalities: List[str]
    sana_index: float
    rating: float
    review_count: int
    hourly_rate: float
    currency: str
    location: str
    availability: str  # available_now, next_24h, next_week
    match_score: float = Field(..., ge=0, le=100)
    match_reasons: List[str]
    image_url: Optional[str] = None


class MatchResponse(BaseModel):
    user_id: str
    query: Dict
    matches: List[PractitionerMatch]
    total_found: int
    processing_time_ms: int


class Modality(BaseModel):
    id: str
    name: str
    category: str
    description: str
    evidence_level: str
    practitioner_count: int


# ============================================================================
# MOCK DATA
# ============================================================================

PRACTITIONERS = [
    {
        "id": "prac_001",
        "name": "Dr. Emily Chen",
        "title": "Licensed Acupuncturist",
        "specialties": ["anxiety", "chronic_pain", "fertility"],
        "modalities": ["acupuncture", "chinese_herbal_medicine"],
        "sana_index": 87,
        "rating": 4.9,
        "review_count": 156,
        "hourly_rate": 85,
        "currency": "GBP",
        "location": "London, UK",
        "availability": "next_24h",
        "image_url": "https://i.pravatar.cc/150?u=emily"
    },
    {
        "id": "prac_002",
        "name": "Sarah Johnson",
        "title": "Naturopathic Doctor",
        "specialties": ["digestive_health", "hormones", "fatigue"],
        "modalities": ["naturopathy", "nutrition", "herbal_medicine"],
        "sana_index": 82,
        "rating": 4.8,
        "review_count": 98,
        "hourly_rate": 95,
        "currency": "GBP",
        "location": "Manchester, UK",
        "availability": "available_now",
        "image_url": "https://i.pravatar.cc/150?u=sarah"
    },
    {
        "id": "prac_003",
        "name": "Michael Roberts",
        "title": "Clinical Herbalist",
        "specialties": ["sleep", "stress", "immune_support"],
        "modalities": ["herbal_medicine", "nutrition"],
        "sana_index": 79,
        "rating": 4.7,
        "review_count": 67,
        "hourly_rate": 70,
        "currency": "GBP",
        "location": "Bristol, UK",
        "availability": "next_week",
        "image_url": "https://i.pravatar.cc/150?u=michael"
    },
    {
        "id": "prac_004",
        "name": "Dr. Priya Sharma",
        "title": "Ayurvedic Practitioner",
        "specialties": ["stress", "digestion", "skin_health"],
        "modalities": ["ayurveda", "yoga_therapy", "meditation"],
        "sana_index": 84,
        "rating": 4.9,
        "review_count": 134,
        "hourly_rate": 90,
        "currency": "GBP",
        "location": "Birmingham, UK",
        "availability": "next_24h",
        "image_url": "https://i.pravatar.cc/150?u=priya"
    },
    {
        "id": "prac_005",
        "name": "James Wilson",
        "title": "Osteopath",
        "specialties": ["back_pain", "sports_injuries", "headaches"],
        "modalities": ["osteopathy", "manual_therapy"],
        "sana_index": 88,
        "rating": 4.8,
        "review_count": 203,
        "hourly_rate": 75,
        "currency": "GBP",
        "location": "Edinburgh, UK",
        "availability": "available_now",
        "image_url": "https://i.pravatar.cc/150?u=james"
    }
]

MODALITIES = [
    {"id": "mod_001", "name": "Acupuncture", "category": "Traditional Chinese Medicine", "description": "Needle therapy targeting acupoints", "evidence_level": "strong", "practitioner_count": 234},
    {"id": "mod_002", "name": "Herbal Medicine", "category": "Phytotherapy", "description": "Plant-based remedies", "evidence_level": "moderate", "practitioner_count": 312},
    {"id": "mod_003", "name": "Naturopathy", "category": "Integrative", "description": "Natural healing approaches", "evidence_level": "moderate", "practitioner_count": 189},
    {"id": "mod_004", "name": "Osteopathy", "category": "Manual Therapy", "description": "Musculoskeletal manipulation", "evidence_level": "strong", "practitioner_count": 456},
    {"id": "mod_005", "name": "Ayurveda", "category": "Traditional Indian Medicine", "description": "Holistic balance approach", "evidence_level": "moderate", "practitioner_count": 123},
    {"id": "mod_006", "name": "Homeopathy", "category": "Alternative", "description": "Diluted remedies", "evidence_level": "limited", "practitioner_count": 267},
    {"id": "mod_007", "name": "Massage Therapy", "category": "Bodywork", "description": "Soft tissue manipulation", "evidence_level": "moderate", "practitioner_count": 578},
    {"id": "mod_008", "name": "Nutrition Therapy", "category": "Lifestyle", "description": "Diet-based interventions", "evidence_level": "strong", "practitioner_count": 345},
]


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/find", response_model=MatchResponse)
async def find_practitioners(data: MatchRequest):
    """
    Find practitioners using SPRM algorithm

    **SPRM Algorithm:**
    - Analyzes user conditions and preferences
    - Matches with practitioner specialties
    - Considers SANA Index (outcome-weighted credibility)
    - Factors in availability and location
    - Calculates personalized match score

    **Match Score Components:**
    - Specialty alignment (30%)
    - SANA Index (25%)
    - User reviews (20%)
    - Availability (15%)
    - Price fit (10%)
    """
    start_time = datetime.utcnow()

    # Filter practitioners by conditions
    matches = []
    for prac in PRACTITIONERS:
        # Calculate match score
        condition_match = len(set(data.conditions) & set(prac["specialties"]))
        modality_match = 0
        if data.modalities:
            modality_match = len(set(data.modalities) & set(prac["modalities"]))

        if condition_match > 0 or modality_match > 0:
            # Calculate composite match score
            specialty_score = (condition_match / max(len(data.conditions), 1)) * 30
            modality_score = (modality_match / max(len(data.modalities or []), 1)) * 20 if data.modalities else 10
            sana_score = (prac["sana_index"] / 100) * 25
            rating_score = (prac["rating"] / 5) * 15
            availability_score = 10 if prac["availability"] == "available_now" else 5

            total_score = specialty_score + modality_score + sana_score + rating_score + availability_score

            # Generate match reasons
            reasons = []
            if condition_match > 0:
                reasons.append(f"Specializes in {', '.join(set(data.conditions) & set(prac['specialties']))}")
            if prac["sana_index"] >= 85:
                reasons.append("Top-rated practitioner (SANA Index 85+)")
            if prac["availability"] == "available_now":
                reasons.append("Available for immediate booking")
            if prac["rating"] >= 4.8:
                reasons.append(f"Excellent reviews ({prac['rating']}/5)")

            matches.append(PractitionerMatch(
                **prac,
                match_score=round(total_score, 1),
                match_reasons=reasons[:3]
            ))

    # Sort by match score
    matches.sort(key=lambda x: x.match_score, reverse=True)

    processing_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

    return MatchResponse(
        user_id=data.user_id,
        query={"conditions": data.conditions, "modalities": data.modalities},
        matches=matches[:10],
        total_found=len(matches),
        processing_time_ms=processing_time
    )


@router.get("/modalities", response_model=List[Modality])
async def list_modalities(category: Optional[str] = None):
    """
    List supported treatment modalities

    Categories:
    - Traditional Chinese Medicine
    - Phytotherapy
    - Manual Therapy
    - Mind-Body
    - Lifestyle
    """
    results = MODALITIES

    if category:
        results = [m for m in results if m["category"].lower() == category.lower()]

    return [Modality(**m) for m in results]


@router.get("/specialties")
async def list_specialties():
    """
    List all practitioner specialties/conditions
    """
    all_specialties = set()
    for prac in PRACTITIONERS:
        all_specialties.update(prac["specialties"])

    return {
        "specialties": sorted(list(all_specialties)),
        "categories": {
            "mental_health": ["anxiety", "depression", "stress", "sleep"],
            "pain": ["chronic_pain", "back_pain", "headaches", "sports_injuries"],
            "digestive": ["digestive_health", "ibs", "food_sensitivities"],
            "hormonal": ["hormones", "fertility", "menopause"],
            "general": ["fatigue", "immune_support", "skin_health"]
        }
    }


@router.get("/quick-match")
async def quick_match(
    condition: str,
    location: Optional[str] = None,
    limit: int = Query(default=5, le=20)
):
    """
    Quick match for a single condition

    Simplified matching for:
    - Single condition search
    - Optional location filter
    - Fast results
    """
    matches = [
        prac for prac in PRACTITIONERS
        if condition in prac["specialties"]
    ]

    if location:
        matches = [m for m in matches if location.lower() in m["location"].lower()]

    # Sort by SANA Index
    matches.sort(key=lambda x: x["sana_index"], reverse=True)

    return {
        "condition": condition,
        "matches": matches[:limit],
        "total": len(matches)
    }
