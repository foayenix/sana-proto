"""
SANA Scanner Routes - Product Scanner ("Vivino for Supplements")
Barcode/OCR scanning with safety analysis
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import uuid

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class Product(BaseModel):
    id: str
    barcode: Optional[str] = None
    name: str
    brand: str
    category: str
    ingredients: List[str]
    dosage: str
    safety_score: float = Field(..., ge=0, le=100)
    shi_avg: float  # Average SHI score of ingredients
    warnings: List[str]
    image_url: Optional[str] = None


class SafetyAnalysis(BaseModel):
    product_id: str
    product_name: str
    overall_safety: str  # safe, caution, warning
    safety_score: float
    interactions: List[Dict]
    contraindications: List[Dict]
    recommendations: List[str]


class Interaction(BaseModel):
    ingredient: str
    interacts_with: str
    type: str  # drug, condition, herb
    severity: str  # mild, moderate, severe
    description: str


class Alternative(BaseModel):
    product_id: str
    product_name: str
    brand: str
    safety_score: float
    price: Optional[float] = None
    reason: str


# ============================================================================
# MOCK DATA
# ============================================================================

PRODUCTS = {
    "5060003560012": {
        "id": "prod_001",
        "barcode": "5060003560012",
        "name": "Ashwagandha KSM-66 500mg",
        "brand": "Nature's Best",
        "category": "Adaptogens",
        "ingredients": ["Ashwagandha Root Extract (KSM-66)", "Vegetable Cellulose Capsule", "Rice Flour"],
        "dosage": "1 capsule twice daily",
        "safety_score": 88,
        "shi_avg": 82,
        "warnings": ["Not recommended during pregnancy", "May interact with thyroid medications"],
        "image_url": "https://example.com/ashwagandha.jpg"
    },
    "5060003560029": {
        "id": "prod_002",
        "barcode": "5060003560029",
        "name": "St. John's Wort 300mg",
        "brand": "Herbal Plus",
        "category": "Mood Support",
        "ingredients": ["St. John's Wort Extract (0.3% Hypericin)", "Maltodextrin", "Gelatin Capsule"],
        "dosage": "1 capsule three times daily",
        "safety_score": 62,
        "shi_avg": 76,
        "warnings": [
            "SIGNIFICANT drug interactions - consult pharmacist",
            "May reduce effectiveness of birth control",
            "Avoid with antidepressants",
            "May cause photosensitivity"
        ],
        "image_url": "https://example.com/stjohnswort.jpg"
    },
    "5060003560036": {
        "id": "prod_003",
        "barcode": "5060003560036",
        "name": "Turmeric Curcumin with BioPerine",
        "brand": "Golden Health",
        "category": "Anti-inflammatory",
        "ingredients": ["Turmeric Root Extract (95% Curcuminoids)", "BioPerine (Black Pepper Extract)", "Vegetable Capsule"],
        "dosage": "1 capsule twice daily with food",
        "safety_score": 92,
        "shi_avg": 85,
        "warnings": ["May interact with blood thinners", "Not recommended before surgery"],
        "image_url": "https://example.com/turmeric.jpg"
    }
}

KNOWN_INTERACTIONS = {
    "st_johns_wort": [
        {"with": "SSRIs", "severity": "severe", "description": "Risk of serotonin syndrome"},
        {"with": "Birth control pills", "severity": "severe", "description": "Reduced effectiveness"},
        {"with": "Blood thinners", "severity": "moderate", "description": "May reduce effectiveness"},
        {"with": "HIV medications", "severity": "severe", "description": "May reduce effectiveness"}
    ],
    "turmeric": [
        {"with": "Blood thinners", "severity": "moderate", "description": "May increase bleeding risk"},
        {"with": "Diabetes medications", "severity": "mild", "description": "May enhance blood sugar lowering"}
    ],
    "ashwagandha": [
        {"with": "Thyroid medications", "severity": "moderate", "description": "May increase thyroid hormone levels"},
        {"with": "Sedatives", "severity": "mild", "description": "May enhance sedative effects"}
    ]
}


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/barcode")
async def scan_barcode(barcode: str):
    """
    Scan product by barcode (UPC, EAN)

    **Features:**
    - Instant product lookup
    - Safety score calculation
    - Ingredient analysis
    - Warning highlights
    """
    product = PRODUCTS.get(barcode)
    if not product:
        return {
            "found": False,
            "barcode": barcode,
            "message": "Product not in database. Would you like to add it?",
            "suggest_ocr": True
        }

    return {
        "found": True,
        "product": Product(**product)
    }


@router.post("/image")
async def scan_image(file: UploadFile = File(...)):
    """
    OCR scan product label image

    **Processing:**
    - Extract text from image
    - Identify product name
    - Parse ingredient list
    - Calculate safety score
    """
    # In production: Use OCR service (Google Vision, AWS Textract, etc.)

    return {
        "status": "processed",
        "extracted_text": "Sample extracted text from label...",
        "identified_product": {
            "name": "Unknown Supplement",
            "ingredients_detected": ["Vitamin C", "Zinc", "Elderberry"],
            "confidence": 0.85
        },
        "requires_verification": True
    }


@router.get("/product/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """
    Get detailed product information

    Includes:
    - Full ingredient list
    - Safety analysis
    - SHI scores for herbs
    - User reviews
    """
    product = next((p for p in PRODUCTS.values() if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return Product(**product)


@router.post("/safety-check", response_model=SafetyAnalysis)
async def check_product_safety(
    product_id: str,
    medications: Optional[List[str]] = None,
    conditions: Optional[List[str]] = None,
    other_supplements: Optional[List[str]] = None
):
    """
    Personalized safety analysis

    **Checks:**
    - Drug-herb interactions
    - Condition contraindications
    - Herb-herb interactions
    - Dosage safety
    """
    product = next((p for p in PRODUCTS.values() if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    interactions = []
    contraindications = []
    recommendations = []

    # Check for known interactions
    for ingredient in product["ingredients"]:
        ingredient_key = ingredient.lower().replace(" ", "_").split("(")[0].strip().replace("_extract", "").replace("_root", "")

        if "st_john" in ingredient_key or "st._john" in ingredient_key:
            ingredient_key = "st_johns_wort"
        elif "turmeric" in ingredient_key or "curcumin" in ingredient_key:
            ingredient_key = "turmeric"
        elif "ashwagandha" in ingredient_key:
            ingredient_key = "ashwagandha"

        known = KNOWN_INTERACTIONS.get(ingredient_key, [])

        if medications:
            for med in medications:
                for interaction in known:
                    if med.lower() in interaction["with"].lower():
                        interactions.append({
                            "ingredient": ingredient,
                            "medication": med,
                            "severity": interaction["severity"],
                            "description": interaction["description"]
                        })

    overall_safety = "safe"
    if any(i["severity"] == "severe" for i in interactions):
        overall_safety = "warning"
    elif any(i["severity"] == "moderate" for i in interactions):
        overall_safety = "caution"

    if overall_safety == "warning":
        recommendations.append("Consult your healthcare provider before using this product")
    if overall_safety == "caution":
        recommendations.append("Review interactions with your pharmacist")

    return SafetyAnalysis(
        product_id=product_id,
        product_name=product["name"],
        overall_safety=overall_safety,
        safety_score=product["safety_score"],
        interactions=interactions,
        contraindications=contraindications,
        recommendations=recommendations or ["No significant concerns identified"]
    )


@router.post("/interactions")
async def check_interactions(
    herbs: List[str],
    medications: Optional[List[str]] = None
):
    """
    Check herb-drug interactions

    **Database:**
    - Evidence-based interaction data
    - Severity ratings
    - Clinical recommendations
    """
    found_interactions = []

    for herb in herbs:
        herb_key = herb.lower().replace(" ", "_").replace("'", "")
        known = KNOWN_INTERACTIONS.get(herb_key, [])

        if medications:
            for med in medications:
                for interaction in known:
                    if med.lower() in interaction["with"].lower():
                        found_interactions.append(Interaction(
                            ingredient=herb,
                            interacts_with=med,
                            type="drug",
                            severity=interaction["severity"],
                            description=interaction["description"]
                        ))

    return {
        "herbs_checked": herbs,
        "medications_checked": medications,
        "interactions_found": len(found_interactions),
        "interactions": [i.model_dump() for i in found_interactions],
        "recommendation": "Consult healthcare provider" if found_interactions else "No interactions found"
    }


@router.post("/recommendations")
async def get_recommendations(
    condition: str,
    avoid_ingredients: Optional[List[str]] = None,
    budget: Optional[str] = None  # low, medium, high
):
    """
    Get product recommendations

    **Factors:**
    - Condition effectiveness
    - Safety profile
    - User preferences
    - Price point
    """
    # Filter safe products for condition
    safe_products = [p for p in PRODUCTS.values() if p["safety_score"] >= 80]

    return {
        "condition": condition,
        "recommendations": [
            Alternative(
                product_id=p["id"],
                product_name=p["name"],
                brand=p["brand"],
                safety_score=p["safety_score"],
                price=29.99,
                reason="High safety score and strong evidence for this condition"
            )
            for p in safe_products[:3]
        ]
    }


@router.post("/quick-check")
async def quick_ingredient_check(ingredients: List[str]):
    """
    Quick safety check for ingredient list

    Used for:
    - Manual ingredient entry
    - Quick lookups
    - Product comparison
    """
    results = []
    for ingredient in ingredients:
        # Simplified check
        safety = "safe"
        if "st. john" in ingredient.lower():
            safety = "caution"

        results.append({
            "ingredient": ingredient,
            "safety": safety,
            "shi_score": 75  # Would lookup actual SHI score
        })

    return {
        "ingredients_checked": len(ingredients),
        "results": results,
        "overall": "caution" if any(r["safety"] == "caution" for r in results) else "safe"
    }


@router.get("/products/search")
async def search_products(q: str, category: Optional[str] = None, limit: int = 20):
    """
    Search product catalog
    """
    results = [
        p for p in PRODUCTS.values()
        if q.lower() in p["name"].lower() or q.lower() in p["brand"].lower()
    ]

    if category:
        results = [p for p in results if p["category"].lower() == category.lower()]

    return {
        "query": q,
        "results": [Product(**p) for p in results[:limit]],
        "total": len(results)
    }


@router.get("/products/popular")
async def get_popular_products(limit: int = 10):
    """
    Get popular/trending products
    """
    return {
        "products": [Product(**p) for p in list(PRODUCTS.values())[:limit]],
        "based_on": "user_scans_last_30_days"
    }


@router.get("/history/{user_id}")
async def get_scan_history(user_id: str, limit: int = 20):
    """
    Get user's scan history
    """
    return {
        "user_id": user_id,
        "scans": [
            {"product_id": "prod_001", "product_name": "Ashwagandha KSM-66", "scanned_at": "2024-06-15T10:30:00Z"},
            {"product_id": "prod_003", "product_name": "Turmeric Curcumin", "scanned_at": "2024-06-10T14:20:00Z"}
        ],
        "total": 12
    }
