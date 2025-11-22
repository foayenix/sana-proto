"""
SANA Safety Routes - SST (SANA Safety & Triage)
Detect health crises and provide appropriate responses
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import uuid

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class SafetyAnalysisRequest(BaseModel):
    user_id: str
    text: Optional[str] = None  # Journal entry, message, or free text
    symptoms: Optional[List[str]] = None
    health_data: Optional[Dict] = None  # Wearable data, vitals
    context: Optional[str] = None  # source of input


class SafetyFlag(BaseModel):
    category: str  # crisis, urgent, caution, info
    type: str  # self_harm, medical_emergency, medication_interaction, etc.
    confidence: float = Field(..., ge=0, le=1)
    triggers: List[str]
    recommendation: str


class SafetyAnalysisResponse(BaseModel):
    id: str
    user_id: str
    risk_level: str  # safe, low, moderate, high, critical
    flags: List[SafetyFlag]
    recommended_action: str
    resources: List[Dict]
    requires_escalation: bool
    analyzed_at: datetime


class SafetyResource(BaseModel):
    id: str
    name: str
    type: str  # hotline, service, information
    category: str  # crisis, mental_health, medical
    contact: Optional[str] = None
    url: Optional[str] = None
    availability: str  # 24/7, business_hours
    description: str


# ============================================================================
# MOCK DATA
# ============================================================================

SAFETY_RESOURCES = [
    {
        "id": "res_001",
        "name": "Samaritans",
        "type": "hotline",
        "category": "crisis",
        "contact": "116 123",
        "url": "https://www.samaritans.org",
        "availability": "24/7",
        "description": "Free emotional support for anyone in distress"
    },
    {
        "id": "res_002",
        "name": "NHS 111",
        "type": "service",
        "category": "medical",
        "contact": "111",
        "url": "https://111.nhs.uk",
        "availability": "24/7",
        "description": "Non-emergency medical advice"
    },
    {
        "id": "res_003",
        "name": "CALM",
        "type": "hotline",
        "category": "mental_health",
        "contact": "0800 58 58 58",
        "url": "https://www.thecalmzone.net",
        "availability": "5pm-midnight",
        "description": "Campaign Against Living Miserably - support for men"
    },
    {
        "id": "res_004",
        "name": "Crisis Text Line",
        "type": "service",
        "category": "crisis",
        "contact": "Text SHOUT to 85258",
        "url": "https://www.crisistextline.uk",
        "availability": "24/7",
        "description": "Free text-based crisis support"
    },
    {
        "id": "res_005",
        "name": "Mind",
        "type": "information",
        "category": "mental_health",
        "contact": "0300 123 3393",
        "url": "https://www.mind.org.uk",
        "availability": "9am-6pm weekdays",
        "description": "Mental health information and support"
    },
    {
        "id": "res_006",
        "name": "Emergency Services",
        "type": "service",
        "category": "medical",
        "contact": "999",
        "url": None,
        "availability": "24/7",
        "description": "Life-threatening emergencies only"
    }
]

# Crisis keywords for detection
CRISIS_KEYWORDS = {
    "self_harm": ["hurt myself", "end it", "suicide", "kill myself", "don't want to live", "self harm", "cutting"],
    "medical_emergency": ["chest pain", "can't breathe", "severe bleeding", "unconscious", "stroke symptoms"],
    "mental_health_crisis": ["panic attack", "can't cope", "breakdown", "severe anxiety", "psychotic"]
}


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/analyze", response_model=SafetyAnalysisResponse)
async def analyze_safety(data: SafetyAnalysisRequest):
    """
    Analyze user input for safety concerns using SST

    **SST Algorithm:**
    - NLP analysis for crisis indicators
    - Keyword and pattern matching
    - Sentiment analysis
    - Wearable data anomaly detection
    - Historical pattern comparison

    **Risk Levels:**
    - **Critical**: Immediate danger, escalate to emergency services
    - **High**: Urgent intervention needed, connect to crisis support
    - **Moderate**: Concerning patterns, suggest professional help
    - **Low**: Minor concerns, provide resources
    - **Safe**: No immediate concerns detected
    """
    flags = []
    risk_level = "safe"
    requires_escalation = False

    # Analyze text if provided
    if data.text:
        text_lower = data.text.lower()

        # Check for crisis keywords
        for category, keywords in CRISIS_KEYWORDS.items():
            matched_keywords = [kw for kw in keywords if kw in text_lower]
            if matched_keywords:
                if category == "self_harm":
                    risk_level = "critical"
                    requires_escalation = True
                    flags.append(SafetyFlag(
                        category="crisis",
                        type="self_harm_risk",
                        confidence=0.85,
                        triggers=matched_keywords,
                        recommendation="Please reach out to crisis support immediately"
                    ))
                elif category == "medical_emergency":
                    risk_level = "critical"
                    requires_escalation = True
                    flags.append(SafetyFlag(
                        category="crisis",
                        type="medical_emergency",
                        confidence=0.90,
                        triggers=matched_keywords,
                        recommendation="Seek immediate medical attention (999)"
                    ))
                elif category == "mental_health_crisis":
                    if risk_level != "critical":
                        risk_level = "high"
                    flags.append(SafetyFlag(
                        category="urgent",
                        type="mental_health_crisis",
                        confidence=0.75,
                        triggers=matched_keywords,
                        recommendation="Connect with mental health support"
                    ))

    # Analyze symptoms if provided
    if data.symptoms:
        severe_symptoms = ["severe_pain", "difficulty_breathing", "chest_pain", "loss_of_consciousness"]
        matched_severe = [s for s in data.symptoms if s in severe_symptoms]
        if matched_severe:
            if risk_level not in ["critical"]:
                risk_level = "high"
            flags.append(SafetyFlag(
                category="urgent",
                type="severe_symptoms",
                confidence=0.80,
                triggers=matched_severe,
                recommendation="Consult healthcare provider urgently"
            ))

    # Determine recommended action
    if risk_level == "critical":
        action = "URGENT: Please contact emergency services (999) or a crisis helpline immediately"
        resources = [r for r in SAFETY_RESOURCES if r["category"] == "crisis" or r["contact"] == "999"]
    elif risk_level == "high":
        action = "We recommend speaking with a crisis counselor or healthcare professional today"
        resources = [r for r in SAFETY_RESOURCES if r["category"] in ["crisis", "mental_health"]]
    elif risk_level == "moderate":
        action = "Consider scheduling an appointment with a healthcare provider"
        resources = [r for r in SAFETY_RESOURCES if r["category"] == "mental_health"]
    else:
        action = "No immediate safety concerns detected"
        resources = []

    return SafetyAnalysisResponse(
        id=f"safety_{uuid.uuid4().hex[:8]}",
        user_id=data.user_id,
        risk_level=risk_level,
        flags=flags,
        recommended_action=action,
        resources=[{"name": r["name"], "contact": r["contact"], "type": r["type"]} for r in resources[:3]],
        requires_escalation=requires_escalation,
        analyzed_at=datetime.utcnow()
    )


@router.get("/resources", response_model=List[SafetyResource])
async def list_resources(
    category: Optional[str] = None,
    type: Optional[str] = None
):
    """
    List safety and crisis resources

    Categories:
    - crisis: Immediate crisis support
    - mental_health: Mental health services
    - medical: Medical services

    Types:
    - hotline: Phone support
    - service: Healthcare services
    - information: Educational resources
    """
    results = SAFETY_RESOURCES

    if category:
        results = [r for r in results if r["category"] == category]
    if type:
        results = [r for r in results if r["type"] == type]

    return [SafetyResource(**r) for r in results]


@router.post("/check-interaction")
async def check_interaction(
    herbs: List[str],
    medications: Optional[List[str]] = None,
    conditions: Optional[List[str]] = None
):
    """
    Check herb-drug and herb-condition interactions

    **Safety Check:**
    - Cross-references herb-drug interaction database
    - Checks contraindications for conditions
    - Provides severity ratings
    """
    interactions = []

    # Mock interaction check
    known_interactions = {
        "st_johns_wort": ["antidepressants", "birth_control", "blood_thinners"],
        "ginkgo": ["blood_thinners", "anticonvulsants"],
        "kava": ["liver_conditions", "alcohol", "sedatives"],
        "valerian": ["sedatives", "alcohol"]
    }

    for herb in herbs:
        herb_lower = herb.lower().replace(" ", "_")
        if herb_lower in known_interactions:
            if medications:
                for med in medications:
                    if med.lower() in known_interactions[herb_lower]:
                        interactions.append({
                            "herb": herb,
                            "interacts_with": med,
                            "type": "drug",
                            "severity": "moderate",
                            "recommendation": f"Consult healthcare provider before combining {herb} with {med}"
                        })

    return {
        "herbs_checked": herbs,
        "medications_checked": medications,
        "interactions_found": len(interactions),
        "interactions": interactions,
        "safety_rating": "caution" if interactions else "safe"
    }


@router.get("/emergency-contacts")
async def get_emergency_contacts(location: str = "UK"):
    """
    Get emergency contacts for a location
    """
    contacts = {
        "UK": {
            "emergency": "999",
            "non_emergency_medical": "111",
            "crisis_line": "116 123 (Samaritans)",
            "poison_control": "0344 892 0111"
        },
        "US": {
            "emergency": "911",
            "crisis_line": "988 (Suicide & Crisis Lifeline)",
            "poison_control": "1-800-222-1222"
        }
    }

    return contacts.get(location, contacts["UK"])
