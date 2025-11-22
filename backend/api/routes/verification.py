"""
SANA Verification Routes - SCVM (SANA Credential Vetting Model)
Verify practitioner qualifications and credentials
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

class CredentialVerifyRequest(BaseModel):
    practitioner_id: str
    credential_type: str  # degree, license, certification, insurance
    issuing_institution: str
    credential_number: Optional[str] = None
    issue_date: date
    expiry_date: Optional[date] = None
    document_url: Optional[str] = None


class VerificationResult(BaseModel):
    id: str
    practitioner_id: str
    credential_type: str
    status: str  # verified, pending, rejected, expired
    confidence_score: float = Field(..., ge=0, le=1)
    verified_at: Optional[datetime] = None
    verified_by: str  # automated, manual_review
    notes: Optional[str] = None


class Institution(BaseModel):
    id: str
    name: str
    type: str  # university, professional_body, regulatory
    country: str
    accredited: bool
    verification_api: bool


class CredentialType(BaseModel):
    id: str
    name: str
    category: str
    required_for: List[str]
    verification_method: str


# ============================================================================
# MOCK DATA
# ============================================================================

INSTITUTIONS = [
    {"id": "inst_001", "name": "University of Westminster", "type": "university", "country": "UK", "accredited": True, "verification_api": True},
    {"id": "inst_002", "name": "British Acupuncture Council", "type": "professional_body", "country": "UK", "accredited": True, "verification_api": True},
    {"id": "inst_003", "name": "General Chiropractic Council", "type": "regulatory", "country": "UK", "accredited": True, "verification_api": True},
    {"id": "inst_004", "name": "National Institute of Medical Herbalists", "type": "professional_body", "country": "UK", "accredited": True, "verification_api": False},
    {"id": "inst_005", "name": "Complementary & Natural Healthcare Council", "type": "regulatory", "country": "UK", "accredited": True, "verification_api": True},
    {"id": "inst_006", "name": "Federation of Holistic Therapists", "type": "professional_body", "country": "UK", "accredited": True, "verification_api": False},
]

CREDENTIAL_TYPES = [
    {"id": "cred_degree", "name": "Academic Degree", "category": "education", "required_for": ["all"], "verification_method": "institution_api"},
    {"id": "cred_license", "name": "Professional License", "category": "regulatory", "required_for": ["regulated_professions"], "verification_method": "regulatory_check"},
    {"id": "cred_cert", "name": "Professional Certification", "category": "certification", "required_for": ["specific_modalities"], "verification_method": "issuer_verification"},
    {"id": "cred_insurance", "name": "Professional Insurance", "category": "insurance", "required_for": ["all"], "verification_method": "policy_verification"},
    {"id": "cred_dbs", "name": "DBS Check", "category": "background", "required_for": ["all"], "verification_method": "dbs_service"},
]


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/verify", response_model=VerificationResult)
async def verify_credential(data: CredentialVerifyRequest):
    """
    Verify a practitioner credential using SCVM

    **SCVM Algorithm:**
    - Validates credential against issuing institution
    - Checks accreditation status of institution
    - Verifies document authenticity (when available)
    - Cross-references with regulatory databases
    - Calculates confidence score

    **Verification Methods:**
    - API verification (automated)
    - Document analysis (semi-automated)
    - Manual review (for edge cases)
    """
    # Simulate verification process
    institution = next((i for i in INSTITUTIONS if i["name"] == data.issuing_institution), None)

    if institution and institution["verification_api"]:
        # Automated verification
        return VerificationResult(
            id=f"ver_{uuid.uuid4().hex[:8]}",
            practitioner_id=data.practitioner_id,
            credential_type=data.credential_type,
            status="verified",
            confidence_score=0.95,
            verified_at=datetime.utcnow(),
            verified_by="automated",
            notes="Verified via institutional API"
        )
    else:
        # Manual review required
        return VerificationResult(
            id=f"ver_{uuid.uuid4().hex[:8]}",
            practitioner_id=data.practitioner_id,
            credential_type=data.credential_type,
            status="pending",
            confidence_score=0.0,
            verified_at=None,
            verified_by="manual_review",
            notes="Submitted for manual verification (2-3 business days)"
        )


@router.get("/institutions", response_model=List[Institution])
async def list_institutions(
    type: Optional[str] = None,
    country: Optional[str] = None,
    accredited_only: bool = True
):
    """
    List recognized credential-issuing institutions

    Filter by:
    - Type: university, professional_body, regulatory
    - Country
    - Accreditation status
    """
    results = INSTITUTIONS

    if type:
        results = [i for i in results if i["type"] == type]
    if country:
        results = [i for i in results if i["country"] == country]
    if accredited_only:
        results = [i for i in results if i["accredited"]]

    return [Institution(**i) for i in results]


@router.get("/credential-types", response_model=List[CredentialType])
async def list_credential_types(category: Optional[str] = None):
    """
    List supported credential types

    Categories:
    - education: Degrees, diplomas
    - regulatory: Licenses, registrations
    - certification: Professional certifications
    - insurance: Professional indemnity
    - background: DBS, references
    """
    results = CREDENTIAL_TYPES

    if category:
        results = [c for c in results if c["category"] == category]

    return [CredentialType(**c) for c in results]


@router.get("/status/{practitioner_id}")
async def get_verification_status(practitioner_id: str):
    """
    Get overall verification status for a practitioner

    Returns:
    - All verified credentials
    - Pending verifications
    - Overall verification score
    - Expiring credentials (warnings)
    """
    return {
        "practitioner_id": practitioner_id,
        "overall_status": "verified",
        "verification_score": 95,
        "credentials": [
            {"type": "degree", "status": "verified", "expiry": None},
            {"type": "license", "status": "verified", "expiry": "2025-06-30"},
            {"type": "insurance", "status": "verified", "expiry": "2024-12-31"},
            {"type": "dbs", "status": "verified", "expiry": "2026-03-15"},
        ],
        "warnings": [
            {"credential": "insurance", "message": "Expires in 45 days"}
        ]
    }


@router.post("/batch-verify")
async def batch_verify_credentials(practitioner_id: str, credentials: List[CredentialVerifyRequest]):
    """
    Verify multiple credentials at once

    Processes all credentials in parallel where possible
    """
    results = []
    for cred in credentials:
        result = await verify_credential(cred)
        results.append(result)

    verified_count = sum(1 for r in results if r.status == "verified")

    return {
        "practitioner_id": practitioner_id,
        "total": len(results),
        "verified": verified_count,
        "pending": len(results) - verified_count,
        "results": results
    }
