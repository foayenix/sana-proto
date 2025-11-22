"""
SANA Evidence Routes - Health Graph
Evidence engine and knowledge base of interventions
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class Intervention(BaseModel):
    id: str
    name: str
    modality: str  # acupuncture, herbal, nutrition, etc.
    conditions: List[str]
    evidence_level: str  # strong, moderate, limited, emerging
    effect_size: float  # Cohen's d or similar
    study_count: int
    meta_analysis: bool
    safety_rating: str  # high, moderate, caution
    description: str


class Condition(BaseModel):
    id: str
    name: str
    icd10_code: Optional[str]
    category: str
    prevalence: str
    top_interventions: List[str]


class SearchResult(BaseModel):
    interventions: List[Intervention]
    total: int
    query: str


class EvidenceSummary(BaseModel):
    condition: str
    interventions_count: int
    strongest_evidence: List[Dict]
    meta_analyses: int
    total_participants: int


# ============================================================================
# MOCK DATA
# ============================================================================

INTERVENTIONS = [
    {
        "id": "int_001",
        "name": "Acupuncture",
        "modality": "Traditional Chinese Medicine",
        "conditions": ["chronic_pain", "anxiety", "migraine", "nausea"],
        "evidence_level": "strong",
        "effect_size": 0.68,
        "study_count": 456,
        "meta_analysis": True,
        "safety_rating": "high",
        "description": "Traditional needle therapy targeting specific acupoints"
    },
    {
        "id": "int_002",
        "name": "Mindfulness-Based Stress Reduction",
        "modality": "Mind-Body",
        "conditions": ["anxiety", "depression", "stress", "chronic_pain"],
        "evidence_level": "strong",
        "effect_size": 0.74,
        "study_count": 312,
        "meta_analysis": True,
        "safety_rating": "high",
        "description": "8-week structured program combining meditation and yoga"
    },
    {
        "id": "int_003",
        "name": "Ashwagandha (Withania somnifera)",
        "modality": "Herbal Medicine",
        "conditions": ["anxiety", "stress", "fatigue", "sleep"],
        "evidence_level": "moderate",
        "effect_size": 0.52,
        "study_count": 89,
        "meta_analysis": True,
        "safety_rating": "high",
        "description": "Adaptogenic herb from Ayurvedic tradition"
    },
    {
        "id": "int_004",
        "name": "Massage Therapy",
        "modality": "Bodywork",
        "conditions": ["chronic_pain", "anxiety", "sleep", "muscle_tension"],
        "evidence_level": "moderate",
        "effect_size": 0.45,
        "study_count": 234,
        "meta_analysis": True,
        "safety_rating": "high",
        "description": "Manual manipulation of soft tissue"
    },
    {
        "id": "int_005",
        "name": "Cognitive Behavioral Therapy",
        "modality": "Psychotherapy",
        "conditions": ["anxiety", "depression", "insomnia", "phobias"],
        "evidence_level": "strong",
        "effect_size": 0.82,
        "study_count": 1245,
        "meta_analysis": True,
        "safety_rating": "high",
        "description": "Structured therapy addressing thought patterns"
    },
    {
        "id": "int_006",
        "name": "Omega-3 Fatty Acids",
        "modality": "Nutrition",
        "conditions": ["depression", "inflammation", "cardiovascular"],
        "evidence_level": "moderate",
        "effect_size": 0.38,
        "study_count": 567,
        "meta_analysis": True,
        "safety_rating": "high",
        "description": "Essential fatty acids from fish or algae"
    },
    {
        "id": "int_007",
        "name": "Yoga",
        "modality": "Mind-Body",
        "conditions": ["anxiety", "chronic_pain", "flexibility", "stress"],
        "evidence_level": "moderate",
        "effect_size": 0.48,
        "study_count": 423,
        "meta_analysis": True,
        "safety_rating": "high",
        "description": "Physical postures, breathing, and meditation"
    },
    {
        "id": "int_008",
        "name": "Valerian Root",
        "modality": "Herbal Medicine",
        "conditions": ["insomnia", "anxiety", "sleep"],
        "evidence_level": "limited",
        "effect_size": 0.32,
        "study_count": 67,
        "meta_analysis": False,
        "safety_rating": "moderate",
        "description": "Traditional sleep aid herb"
    }
]

CONDITIONS = [
    {"id": "anxiety", "name": "Anxiety Disorders", "icd10_code": "F41", "category": "Mental Health", "prevalence": "18%", "top_interventions": ["CBT", "MBSR", "Acupuncture"]},
    {"id": "depression", "name": "Major Depression", "icd10_code": "F32", "category": "Mental Health", "prevalence": "8%", "top_interventions": ["CBT", "Omega-3", "Exercise"]},
    {"id": "chronic_pain", "name": "Chronic Pain", "icd10_code": "G89", "category": "Musculoskeletal", "prevalence": "20%", "top_interventions": ["Acupuncture", "Massage", "Yoga"]},
    {"id": "insomnia", "name": "Insomnia", "icd10_code": "G47", "category": "Sleep", "prevalence": "30%", "top_interventions": ["CBT-I", "Valerian", "Meditation"]},
    {"id": "stress", "name": "Chronic Stress", "icd10_code": "F43", "category": "Mental Health", "prevalence": "25%", "top_interventions": ["MBSR", "Ashwagandha", "Yoga"]},
    {"id": "migraine", "name": "Migraine", "icd10_code": "G43", "category": "Neurological", "prevalence": "12%", "top_interventions": ["Acupuncture", "Magnesium", "Biofeedback"]},
]


# ============================================================================
# ROUTES
# ============================================================================

@router.get("/interventions/{domain}")
async def get_interventions_by_domain(
    domain: str,
    evidence_level: Optional[str] = None,
    limit: int = Query(default=20, le=100)
):
    """
    Get evidence-based interventions for a health domain

    **Health Graph Engine:**
    - Knowledge base of CAM interventions
    - Evidence levels based on systematic reviews
    - Effect sizes from meta-analyses
    - Safety ratings from pharmacovigilance data

    **Domains:** anxiety, depression, chronic_pain, insomnia, stress, etc.
    """
    results = [
        i for i in INTERVENTIONS
        if domain in i["conditions"]
    ]

    if evidence_level:
        results = [i for i in results if i["evidence_level"] == evidence_level]

    return {
        "domain": domain,
        "interventions": [Intervention(**i) for i in results[:limit]],
        "total": len(results)
    }


@router.get("/conditions")
async def list_conditions(category: Optional[str] = None):
    """
    List all supported health conditions

    Returns:
    - ICD-10 codes
    - Category classification
    - Prevalence data
    - Top evidence-based interventions
    """
    results = CONDITIONS
    if category:
        results = [c for c in CONDITIONS if c["category"].lower() == category.lower()]

    return {
        "conditions": [Condition(**c) for c in results],
        "total": len(results)
    }


@router.get("/search")
async def search_interventions(
    q: str = Query(..., min_length=2),
    modality: Optional[str] = None,
    evidence_min: Optional[str] = None
):
    """
    Search interventions by keyword

    Full-text search across:
    - Intervention names
    - Descriptions
    - Associated conditions
    - Modalities
    """
    q_lower = q.lower()
    results = [
        i for i in INTERVENTIONS
        if q_lower in i["name"].lower() or
           q_lower in i["description"].lower() or
           any(q_lower in c for c in i["conditions"])
    ]

    if modality:
        results = [i for i in results if modality.lower() in i["modality"].lower()]

    return SearchResult(
        interventions=[Intervention(**i) for i in results],
        total=len(results),
        query=q
    )


@router.get("/summary/{condition}")
async def get_evidence_summary(condition: str):
    """
    Get evidence summary for a condition

    Aggregated view including:
    - Total interventions with evidence
    - Strongest evidence rankings
    - Meta-analysis count
    - Total research participants
    """
    matching = [i for i in INTERVENTIONS if condition in i["conditions"]]

    return EvidenceSummary(
        condition=condition,
        interventions_count=len(matching),
        strongest_evidence=[
            {"name": i["name"], "effect_size": i["effect_size"], "level": i["evidence_level"]}
            for i in sorted(matching, key=lambda x: x["effect_size"], reverse=True)[:3]
        ],
        meta_analyses=sum(1 for i in matching if i["meta_analysis"]),
        total_participants=sum(i["study_count"] * 150 for i in matching)  # Estimate
    )


@router.get("/intervention/{intervention_id}")
async def get_intervention_detail(intervention_id: str):
    """
    Get detailed information about an intervention

    Includes:
    - Full description
    - Evidence breakdown
    - Safety information
    - Dosing/protocol (if applicable)
    - Contraindications
    """
    intervention = next((i for i in INTERVENTIONS if i["id"] == intervention_id), None)
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention not found")

    return {
        **intervention,
        "studies": [
            {"title": "RCT on anxiety reduction", "year": 2023, "n": 245, "outcome": "positive"},
            {"title": "Systematic review", "year": 2022, "n": 1200, "outcome": "positive"},
        ],
        "contraindications": ["Pregnancy (consult provider)", "Blood thinners (some herbs)"],
        "protocol": "Typical course: 6-12 sessions over 8 weeks"
    }
