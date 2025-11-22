"""
SANA Herbs Routes - SHI (SANA Herb Index)
Score and search herbs and supplements
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class Herb(BaseModel):
    id: str
    name: str
    latin_name: str
    common_names: List[str]
    shi_score: float = Field(..., ge=0, le=100)
    evidence_score: float
    safety_score: float
    quality_score: float
    traditional_uses: List[str]
    conditions: List[str]
    evidence_summary: str
    dosage_range: str
    form: List[str]
    contraindications: List[str]
    interactions: List[str]


class HerbRanking(BaseModel):
    herb_id: str
    herb_name: str
    condition: str
    shi_score: float
    evidence_level: str
    effect_size: Optional[float]
    study_count: int


# ============================================================================
# MOCK DATA
# ============================================================================

HERBS = [
    {
        "id": "herb_001",
        "name": "Ashwagandha",
        "latin_name": "Withania somnifera",
        "common_names": ["Indian Ginseng", "Winter Cherry"],
        "shi_score": 82,
        "evidence_score": 78,
        "safety_score": 88,
        "quality_score": 80,
        "traditional_uses": ["Adaptogen", "Vitality", "Stress resistance"],
        "conditions": ["anxiety", "stress", "fatigue", "sleep"],
        "evidence_summary": "Strong evidence for anxiety and stress reduction. Moderate evidence for cognitive enhancement.",
        "dosage_range": "300-600mg standardized extract daily",
        "form": ["capsule", "powder", "tincture"],
        "contraindications": ["Pregnancy", "Thyroid disorders", "Autoimmune conditions"],
        "interactions": ["Thyroid medications", "Sedatives", "Immunosuppressants"]
    },
    {
        "id": "herb_002",
        "name": "Rhodiola",
        "latin_name": "Rhodiola rosea",
        "common_names": ["Golden Root", "Arctic Root"],
        "shi_score": 79,
        "evidence_score": 75,
        "safety_score": 90,
        "quality_score": 72,
        "traditional_uses": ["Adaptogen", "Mental performance", "Physical endurance"],
        "conditions": ["fatigue", "stress", "depression", "cognitive"],
        "evidence_summary": "Good evidence for fatigue and mental performance. Emerging evidence for depression.",
        "dosage_range": "200-600mg standardized extract daily",
        "form": ["capsule", "tablet", "tincture"],
        "contraindications": ["Bipolar disorder"],
        "interactions": ["Antidepressants", "Stimulants"]
    },
    {
        "id": "herb_003",
        "name": "Valerian",
        "latin_name": "Valeriana officinalis",
        "common_names": ["Garden Valerian", "All-Heal"],
        "shi_score": 71,
        "evidence_score": 68,
        "safety_score": 82,
        "quality_score": 63,
        "traditional_uses": ["Sleep aid", "Calming", "Nervine"],
        "conditions": ["insomnia", "anxiety", "restlessness"],
        "evidence_summary": "Moderate evidence for sleep improvement. Mixed results in clinical trials.",
        "dosage_range": "300-600mg before bed",
        "form": ["capsule", "tea", "tincture"],
        "contraindications": ["Pregnancy", "Liver disease"],
        "interactions": ["Sedatives", "Alcohol", "Benzodiazepines"]
    },
    {
        "id": "herb_004",
        "name": "Turmeric",
        "latin_name": "Curcuma longa",
        "common_names": ["Curcumin", "Indian Saffron"],
        "shi_score": 85,
        "evidence_score": 82,
        "safety_score": 92,
        "quality_score": 81,
        "traditional_uses": ["Anti-inflammatory", "Digestive", "Wound healing"],
        "conditions": ["inflammation", "arthritis", "digestive", "mood"],
        "evidence_summary": "Strong evidence for inflammation and arthritis. Bioavailability requires enhancement.",
        "dosage_range": "500-2000mg curcumin with piperine daily",
        "form": ["capsule", "powder", "paste"],
        "contraindications": ["Gallbladder disease", "Bleeding disorders"],
        "interactions": ["Blood thinners", "Diabetes medications"]
    },
    {
        "id": "herb_005",
        "name": "St. John's Wort",
        "latin_name": "Hypericum perforatum",
        "common_names": ["Klamath Weed", "Goatweed"],
        "shi_score": 76,
        "evidence_score": 80,
        "safety_score": 58,
        "quality_score": 75,
        "traditional_uses": ["Mood support", "Nervine", "Wound healing"],
        "conditions": ["depression", "anxiety", "seasonal_affective"],
        "evidence_summary": "Strong evidence for mild-moderate depression. Significant drug interactions.",
        "dosage_range": "300mg 3x daily (standardized to 0.3% hypericin)",
        "form": ["capsule", "tincture", "tea"],
        "contraindications": ["Pregnancy", "Bipolar disorder", "Photosensitivity"],
        "interactions": ["Antidepressants", "Birth control", "Blood thinners", "HIV medications", "Many others"]
    },
    {
        "id": "herb_006",
        "name": "Passionflower",
        "latin_name": "Passiflora incarnata",
        "common_names": ["Maypop", "Purple Passionflower"],
        "shi_score": 74,
        "evidence_score": 70,
        "safety_score": 85,
        "quality_score": 67,
        "traditional_uses": ["Calming", "Sleep", "Anxiety relief"],
        "conditions": ["anxiety", "insomnia", "nervousness"],
        "evidence_summary": "Moderate evidence for anxiety. Often combined with other herbs for sleep.",
        "dosage_range": "250-500mg extract or 1-2 cups tea daily",
        "form": ["capsule", "tea", "tincture"],
        "contraindications": ["Pregnancy", "Surgery (stop 2 weeks before)"],
        "interactions": ["Sedatives", "Blood thinners"]
    },
    {
        "id": "herb_007",
        "name": "Ginkgo",
        "latin_name": "Ginkgo biloba",
        "common_names": ["Maidenhair Tree"],
        "shi_score": 77,
        "evidence_score": 73,
        "safety_score": 75,
        "quality_score": 83,
        "traditional_uses": ["Cognitive function", "Circulation", "Memory"],
        "conditions": ["cognitive", "memory", "circulation", "tinnitus"],
        "evidence_summary": "Moderate evidence for cognitive function in elderly. Limited evidence for healthy adults.",
        "dosage_range": "120-240mg standardized extract daily",
        "form": ["capsule", "tablet", "tincture"],
        "contraindications": ["Bleeding disorders", "Surgery", "Seizure disorders"],
        "interactions": ["Blood thinners", "NSAIDs", "Anticonvulsants"]
    },
    {
        "id": "herb_008",
        "name": "Echinacea",
        "latin_name": "Echinacea purpurea",
        "common_names": ["Purple Coneflower", "American Coneflower"],
        "shi_score": 72,
        "evidence_score": 65,
        "safety_score": 88,
        "quality_score": 63,
        "traditional_uses": ["Immune support", "Cold prevention", "Wound healing"],
        "conditions": ["immune", "cold", "upper_respiratory"],
        "evidence_summary": "Mixed evidence for cold prevention and duration. Generally safe for short-term use.",
        "dosage_range": "300-500mg 3x daily at cold onset",
        "form": ["capsule", "tincture", "tea"],
        "contraindications": ["Autoimmune conditions", "Allergies to daisies"],
        "interactions": ["Immunosuppressants"]
    }
]

HERB_RANKINGS = {
    "anxiety": [
        {"herb_id": "herb_001", "herb_name": "Ashwagandha", "shi_score": 82, "evidence_level": "strong", "effect_size": 0.52, "study_count": 89},
        {"herb_id": "herb_005", "herb_name": "St. John's Wort", "shi_score": 76, "evidence_level": "strong", "effect_size": 0.45, "study_count": 67},
        {"herb_id": "herb_006", "herb_name": "Passionflower", "shi_score": 74, "evidence_level": "moderate", "effect_size": 0.38, "study_count": 34},
    ],
    "sleep": [
        {"herb_id": "herb_003", "herb_name": "Valerian", "shi_score": 71, "evidence_level": "moderate", "effect_size": 0.32, "study_count": 67},
        {"herb_id": "herb_006", "herb_name": "Passionflower", "shi_score": 74, "evidence_level": "moderate", "effect_size": 0.35, "study_count": 28},
        {"herb_id": "herb_001", "herb_name": "Ashwagandha", "shi_score": 82, "evidence_level": "moderate", "effect_size": 0.30, "study_count": 23},
    ],
    "stress": [
        {"herb_id": "herb_001", "herb_name": "Ashwagandha", "shi_score": 82, "evidence_level": "strong", "effect_size": 0.58, "study_count": 95},
        {"herb_id": "herb_002", "herb_name": "Rhodiola", "shi_score": 79, "evidence_level": "strong", "effect_size": 0.48, "study_count": 56},
    ],
    "inflammation": [
        {"herb_id": "herb_004", "herb_name": "Turmeric", "shi_score": 85, "evidence_level": "strong", "effect_size": 0.62, "study_count": 234},
    ]
}


# ============================================================================
# ROUTES
# ============================================================================

@router.get("/search", response_model=List[Herb])
async def search_herbs(
    q: Optional[str] = None,
    condition: Optional[str] = None,
    min_shi_score: Optional[float] = None,
    limit: int = Query(default=20, le=100)
):
    """
    Search herbs and supplements

    **SHI (SANA Herb Index) Components:**
    - Evidence Score (40%): Quality of clinical evidence
    - Safety Score (35%): Safety profile and interactions
    - Quality Score (25%): Standardization and quality control

    **Search by:**
    - Keyword (name, latin name, common names)
    - Condition
    - Minimum SHI score
    """
    results = HERBS

    if q:
        q_lower = q.lower()
        results = [
            h for h in results
            if q_lower in h["name"].lower() or
               q_lower in h["latin_name"].lower() or
               any(q_lower in cn.lower() for cn in h["common_names"])
        ]

    if condition:
        results = [h for h in results if condition.lower() in h["conditions"]]

    if min_shi_score:
        results = [h for h in results if h["shi_score"] >= min_shi_score]

    # Sort by SHI score
    results.sort(key=lambda x: x["shi_score"], reverse=True)

    return [Herb(**h) for h in results[:limit]]


@router.get("/rankings")
async def get_herb_rankings(condition: str):
    """
    Get ranked herbs for a specific condition

    Rankings based on:
    - SHI score
    - Evidence level for specific condition
    - Effect size from meta-analyses
    - Number of supporting studies
    """
    rankings = HERB_RANKINGS.get(condition.lower())
    if not rankings:
        raise HTTPException(status_code=404, detail=f"No rankings for condition: {condition}")

    return {
        "condition": condition,
        "rankings": [HerbRanking(condition=condition, **r) for r in rankings],
        "methodology": "SHI score weighted by condition-specific evidence"
    }


@router.get("/{herb_id}", response_model=Herb)
async def get_herb_detail(herb_id: str):
    """
    Get detailed herb information

    Includes:
    - Full SHI breakdown
    - Evidence summary
    - Dosing guidelines
    - Safety information
    - Drug interactions
    """
    herb = next((h for h in HERBS if h["id"] == herb_id), None)
    if not herb:
        raise HTTPException(status_code=404, detail="Herb not found")

    return Herb(**herb)


@router.get("/{herb_id}/studies")
async def get_herb_studies(herb_id: str, limit: int = 10):
    """
    Get clinical studies for a herb

    Returns:
    - Study summaries
    - Quality ratings
    - Key findings
    """
    herb = next((h for h in HERBS if h["id"] == herb_id), None)
    if not herb:
        raise HTTPException(status_code=404, detail="Herb not found")

    # Mock study data
    studies = [
        {
            "title": f"Randomized controlled trial of {herb['name']} for anxiety",
            "year": 2023,
            "journal": "Journal of Clinical Psychiatry",
            "n": 256,
            "quality": "high",
            "finding": "Significant reduction in anxiety scores vs placebo"
        },
        {
            "title": f"Systematic review of {herb['name']} safety and efficacy",
            "year": 2022,
            "journal": "Phytomedicine",
            "n": 1847,
            "quality": "high",
            "finding": "Well-tolerated with moderate evidence of efficacy"
        }
    ]

    return {
        "herb_id": herb_id,
        "herb_name": herb["name"],
        "studies": studies[:limit],
        "total_studies": 45
    }


@router.post("/compare")
async def compare_herbs(herb_ids: List[str]):
    """
    Compare multiple herbs side-by-side

    Compares:
    - SHI scores
    - Evidence profiles
    - Safety profiles
    - Use cases
    """
    herbs = [h for h in HERBS if h["id"] in herb_ids]

    if len(herbs) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 valid herb IDs")

    comparison = {
        "herbs": [
            {
                "id": h["id"],
                "name": h["name"],
                "shi_score": h["shi_score"],
                "evidence_score": h["evidence_score"],
                "safety_score": h["safety_score"],
                "conditions": h["conditions"]
            }
            for h in herbs
        ],
        "best_for": {},
        "safety_notes": []
    }

    # Determine best for each condition
    all_conditions = set()
    for h in herbs:
        all_conditions.update(h["conditions"])

    for condition in all_conditions:
        matching = [h for h in herbs if condition in h["conditions"]]
        if matching:
            best = max(matching, key=lambda x: x["shi_score"])
            comparison["best_for"][condition] = best["name"]

    return comparison
