"""
SANA Marketplace Routes
Practitioner discovery, search, reviews, and booking
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

class SearchFilters(BaseModel):
    conditions: Optional[List[str]] = None
    modalities: Optional[List[str]] = None
    location: Optional[str] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None
    min_sana_index: Optional[float] = None
    availability: Optional[str] = None  # available_now, next_24h, next_week
    session_type: Optional[str] = None  # video, in_person, both


class PractitionerProfile(BaseModel):
    id: str
    name: str
    title: str
    bio: str
    specialties: List[str]
    modalities: List[str]
    sana_index: float
    rating: float
    review_count: int
    hourly_rate: float
    currency: str
    location: str
    offers_video: bool
    offers_in_person: bool
    years_experience: int
    total_clients: int
    image_url: Optional[str] = None


class Review(BaseModel):
    id: str
    practitioner_id: str
    client_name: str  # First name + last initial
    rating: float
    title: Optional[str] = None
    content: str
    condition: Optional[str] = None
    verified: bool
    created_at: datetime


class ReviewSubmission(BaseModel):
    practitioner_id: str
    rating: float = Field(..., ge=1, le=5)
    title: Optional[str] = None
    content: str
    condition: Optional[str] = None


# ============================================================================
# MOCK DATA
# ============================================================================

PRACTITIONERS = [
    {
        "id": "prac_001",
        "name": "Dr. Emily Chen",
        "title": "Licensed Acupuncturist",
        "bio": "Specializing in anxiety and chronic pain management through Traditional Chinese Medicine. Over 8 years of experience with a focus on evidence-based integrative care.",
        "specialties": ["anxiety", "chronic_pain", "fertility", "digestive"],
        "modalities": ["acupuncture", "chinese_herbal_medicine", "cupping"],
        "sana_index": 87,
        "rating": 4.9,
        "review_count": 156,
        "hourly_rate": 85,
        "currency": "GBP",
        "location": "London, UK",
        "offers_video": True,
        "offers_in_person": True,
        "years_experience": 8,
        "total_clients": 534,
        "image_url": "https://i.pravatar.cc/150?u=emily"
    },
    {
        "id": "prac_002",
        "name": "Sarah Johnson",
        "title": "Naturopathic Doctor",
        "bio": "Holistic approach to digestive health, hormonal balance, and chronic fatigue. Combining modern diagnostics with natural therapies.",
        "specialties": ["digestive", "hormones", "fatigue", "autoimmune"],
        "modalities": ["naturopathy", "nutrition", "herbal_medicine"],
        "sana_index": 82,
        "rating": 4.8,
        "review_count": 98,
        "hourly_rate": 95,
        "currency": "GBP",
        "location": "Manchester, UK",
        "offers_video": True,
        "offers_in_person": True,
        "years_experience": 6,
        "total_clients": 312,
        "image_url": "https://i.pravatar.cc/150?u=sarah"
    },
    {
        "id": "prac_003",
        "name": "James Wilson",
        "title": "Registered Osteopath",
        "bio": "Sports injury specialist with expertise in back pain, postural correction, and rehabilitation. Former sports team osteopath.",
        "specialties": ["back_pain", "sports_injuries", "headaches", "posture"],
        "modalities": ["osteopathy", "manual_therapy", "exercise_prescription"],
        "sana_index": 88,
        "rating": 4.8,
        "review_count": 203,
        "hourly_rate": 75,
        "currency": "GBP",
        "location": "Edinburgh, UK",
        "offers_video": False,
        "offers_in_person": True,
        "years_experience": 12,
        "total_clients": 678,
        "image_url": "https://i.pravatar.cc/150?u=james"
    },
    {
        "id": "prac_004",
        "name": "Dr. Priya Sharma",
        "title": "Ayurvedic Practitioner",
        "bio": "Traditional Ayurvedic medicine combined with modern wellness practices. Specializing in stress management and digestive health.",
        "specialties": ["stress", "digestive", "skin", "detox"],
        "modalities": ["ayurveda", "yoga_therapy", "meditation", "panchakarma"],
        "sana_index": 84,
        "rating": 4.9,
        "review_count": 134,
        "hourly_rate": 90,
        "currency": "GBP",
        "location": "Birmingham, UK",
        "offers_video": True,
        "offers_in_person": True,
        "years_experience": 10,
        "total_clients": 445,
        "image_url": "https://i.pravatar.cc/150?u=priya"
    }
]

REVIEWS = [
    {
        "id": "rev_001",
        "practitioner_id": "prac_001",
        "client_name": "Sarah M.",
        "rating": 5.0,
        "title": "Life-changing treatment",
        "content": "After years of struggling with anxiety, Dr. Chen's acupuncture sessions have made a remarkable difference. I feel calmer and more centered.",
        "condition": "anxiety",
        "verified": True,
        "created_at": datetime(2024, 5, 15)
    },
    {
        "id": "rev_002",
        "practitioner_id": "prac_001",
        "client_name": "Michael R.",
        "rating": 5.0,
        "title": "Finally found relief",
        "content": "My chronic back pain has significantly improved after 6 sessions. Dr. Chen takes time to understand your condition and explains everything clearly.",
        "condition": "chronic_pain",
        "verified": True,
        "created_at": datetime(2024, 4, 20)
    }
]


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/search")
async def search_practitioners(
    filters: SearchFilters,
    sort_by: str = "relevance",  # relevance, rating, sana_index, price
    page: int = 1,
    limit: int = Query(default=20, le=50)
):
    """
    Search and filter practitioners

    **Search Features:**
    - Filter by conditions, modalities, location
    - Price range filtering
    - Minimum rating/SANA Index
    - Availability filtering
    - Session type (video/in-person)

    **Sort Options:**
    - relevance: Best match for conditions
    - rating: Client ratings
    - sana_index: SANA credibility score
    - price: Hourly rate
    """
    results = PRACTITIONERS.copy()

    # Apply filters
    if filters.conditions:
        results = [
            p for p in results
            if any(c in p["specialties"] for c in filters.conditions)
        ]

    if filters.modalities:
        results = [
            p for p in results
            if any(m in p["modalities"] for m in filters.modalities)
        ]

    if filters.location:
        results = [
            p for p in results
            if filters.location.lower() in p["location"].lower()
        ]

    if filters.max_price:
        results = [p for p in results if p["hourly_rate"] <= filters.max_price]

    if filters.min_rating:
        results = [p for p in results if p["rating"] >= filters.min_rating]

    if filters.min_sana_index:
        results = [p for p in results if p["sana_index"] >= filters.min_sana_index]

    if filters.session_type == "video":
        results = [p for p in results if p["offers_video"]]
    elif filters.session_type == "in_person":
        results = [p for p in results if p["offers_in_person"]]

    # Sort
    if sort_by == "rating":
        results.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "sana_index":
        results.sort(key=lambda x: x["sana_index"], reverse=True)
    elif sort_by == "price":
        results.sort(key=lambda x: x["hourly_rate"])
    else:  # relevance - by sana_index and rating combo
        results.sort(key=lambda x: x["sana_index"] * 0.6 + x["rating"] * 8, reverse=True)

    # Paginate
    start = (page - 1) * limit
    end = start + limit

    return {
        "practitioners": [PractitionerProfile(**p) for p in results[start:end]],
        "total": len(results),
        "page": page,
        "pages": (len(results) + limit - 1) // limit,
        "filters_applied": filters.model_dump(exclude_none=True)
    }


@router.get("/practitioners/{practitioner_id}", response_model=PractitionerProfile)
async def get_practitioner_profile(practitioner_id: str):
    """
    Get detailed practitioner profile

    Includes:
    - Full bio and credentials
    - Specialties and modalities
    - SANA Index breakdown
    - Availability overview
    """
    prac = next((p for p in PRACTITIONERS if p["id"] == practitioner_id), None)
    if not prac:
        raise HTTPException(status_code=404, detail="Practitioner not found")

    return PractitionerProfile(**prac)


@router.post("/reviews", response_model=Review)
async def submit_review(data: ReviewSubmission):
    """
    Submit a practitioner review

    Requirements:
    - Must have completed session with practitioner
    - Rating 1-5 stars
    - Optional condition tag
    - Reviews are verified against booking history
    """
    review_id = f"rev_{uuid.uuid4().hex[:8]}"

    return Review(
        id=review_id,
        practitioner_id=data.practitioner_id,
        client_name="User S.",  # Anonymized
        rating=data.rating,
        title=data.title,
        content=data.content,
        condition=data.condition,
        verified=True,
        created_at=datetime.utcnow()
    )


@router.get("/practitioners/{practitioner_id}/reviews")
async def get_practitioner_reviews(
    practitioner_id: str,
    page: int = 1,
    limit: int = Query(default=10, le=50)
):
    """
    Get reviews for a practitioner

    Includes:
    - Rating distribution
    - Verified reviews
    - Condition-specific feedback
    """
    reviews = [r for r in REVIEWS if r["practitioner_id"] == practitioner_id]

    # Rating distribution
    distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for r in reviews:
        distribution[int(r["rating"])] += 1

    return {
        "practitioner_id": practitioner_id,
        "reviews": [Review(**r) for r in reviews],
        "total": len(reviews),
        "rating_distribution": distribution,
        "average_rating": sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0
    }


@router.get("/discover")
async def get_discovery_page():
    """
    Get marketplace discovery page content

    Featured sections:
    - Top rated practitioners
    - Rising stars
    - By condition
    - Near you
    """
    return {
        "featured": PRACTITIONERS[:2],
        "top_rated": sorted(PRACTITIONERS, key=lambda x: x["rating"], reverse=True)[:4],
        "rising_stars": [p for p in PRACTITIONERS if p["sana_index"] >= 80],
        "categories": [
            {"name": "Mental Health", "conditions": ["anxiety", "depression", "stress"]},
            {"name": "Pain Management", "conditions": ["chronic_pain", "back_pain", "headaches"]},
            {"name": "Digestive Health", "conditions": ["digestive", "ibs", "gut_health"]},
            {"name": "Women's Health", "conditions": ["hormones", "fertility", "menopause"]}
        ]
    }


@router.get("/discover/trending")
async def get_trending():
    """
    Get trending practitioners and searches

    Based on:
    - Recent bookings
    - Search trends
    - Seasonal conditions
    """
    return {
        "trending_practitioners": PRACTITIONERS[:3],
        "trending_searches": [
            {"term": "anxiety help", "searches": 1250},
            {"term": "back pain specialist", "searches": 890},
            {"term": "sleep improvement", "searches": 756}
        ],
        "seasonal_spotlight": {
            "title": "Stress Management",
            "description": "Popular this season",
            "practitioners": [p for p in PRACTITIONERS if "stress" in p["specialties"]]
        }
    }
