"""
SANA Freemium Routes
Usage tracking and tier management
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

class FeatureUsage(BaseModel):
    feature: str
    used: int
    limit: int  # -1 = unlimited
    remaining: int
    reset_date: str


class UsageSummary(BaseModel):
    user_id: str
    tier: str
    features: List[FeatureUsage]
    period: str
    period_start: datetime
    period_end: datetime


class TierLimits(BaseModel):
    tier: str
    name: str
    price: float
    currency: str = "GBP"
    limits: Dict[str, int]
    features: List[str]


class UpgradePrompt(BaseModel):
    show_prompt: bool
    feature: str
    current_tier: str
    recommended_tier: str
    message: str
    cta_text: str
    cta_url: str


# ============================================================================
# TIER CONFIGURATION
# ============================================================================

TIERS = {
    "free": {
        "name": "Free",
        "price": 0,
        "currency": "GBP",
        "limits": {
            "clients": 5,
            "bookings_per_month": 20,
            "soap_notes": 10,
            "ai_suggestions": 20,
            "voice_transcriptions": 5,
            "outcome_tracking": 5,
            "messages_per_month": 50,
            "storage_mb": 100
        },
        "features": [
            "Basic practice management",
            "5 active clients",
            "20 bookings/month",
            "Basic analytics",
            "Email support"
        ]
    },
    "basic": {
        "name": "Basic",
        "price": 29,
        "currency": "GBP",
        "limits": {
            "clients": 50,
            "bookings_per_month": 100,
            "soap_notes": 50,
            "ai_suggestions": 100,
            "voice_transcriptions": 20,
            "outcome_tracking": 50,
            "messages_per_month": 500,
            "storage_mb": 1000
        },
        "features": [
            "50 active clients",
            "100 bookings/month",
            "Outcome tracking",
            "Custom branding",
            "Priority support",
            "Widget embedding"
        ]
    },
    "professional": {
        "name": "Professional",
        "price": 79,
        "currency": "GBP",
        "limits": {
            "clients": 200,
            "bookings_per_month": -1,  # Unlimited
            "soap_notes": -1,
            "ai_suggestions": -1,
            "voice_transcriptions": 100,
            "outcome_tracking": -1,
            "messages_per_month": -1,
            "storage_mb": 10000
        },
        "features": [
            "200 active clients",
            "Unlimited bookings",
            "Full AI assistant",
            "Advanced analytics",
            "API access",
            "Custom integrations",
            "Priority support"
        ]
    },
    "enterprise": {
        "name": "Enterprise",
        "price": 199,
        "currency": "GBP",
        "limits": {
            "clients": -1,
            "bookings_per_month": -1,
            "soap_notes": -1,
            "ai_suggestions": -1,
            "voice_transcriptions": -1,
            "outcome_tracking": -1,
            "messages_per_month": -1,
            "storage_mb": -1
        },
        "features": [
            "Unlimited everything",
            "Dedicated account manager",
            "Custom development",
            "SLA guarantee",
            "On-premise option",
            "HIPAA compliance",
            "Team management"
        ]
    }
}

# Mock usage data
USER_USAGE: Dict[str, Dict] = {
    "demo_user": {
        "tier": "professional",
        "period_start": datetime(2024, 6, 1),
        "period_end": datetime(2024, 7, 1),
        "usage": {
            "clients": 89,
            "bookings_per_month": 67,
            "soap_notes": 45,
            "ai_suggestions": 123,
            "voice_transcriptions": 12,
            "outcome_tracking": 78,
            "messages_per_month": 234,
            "storage_mb": 450
        }
    }
}


# ============================================================================
# ROUTES
# ============================================================================

@router.get("/usage/{user_id}", response_model=UsageSummary)
async def get_usage_summary(user_id: str):
    """
    Get user's usage summary

    Shows:
    - Current tier
    - Usage for each feature
    - Limits and remaining allowance
    - Period information
    """
    user_data = USER_USAGE.get(user_id, {
        "tier": "free",
        "period_start": datetime(2024, 6, 1),
        "period_end": datetime(2024, 7, 1),
        "usage": {k: 0 for k in TIERS["free"]["limits"].keys()}
    })

    tier = user_data["tier"]
    limits = TIERS[tier]["limits"]
    usage = user_data["usage"]

    features = []
    for feature, limit in limits.items():
        used = usage.get(feature, 0)
        remaining = -1 if limit == -1 else max(0, limit - used)
        features.append(FeatureUsage(
            feature=feature,
            used=used,
            limit=limit,
            remaining=remaining,
            reset_date="2024-07-01"
        ))

    return UsageSummary(
        user_id=user_id,
        tier=tier,
        features=features,
        period="2024-06",
        period_start=user_data["period_start"],
        period_end=user_data["period_end"]
    )


@router.get("/usage/{user_id}/feature/{feature}")
async def get_feature_usage(user_id: str, feature: str):
    """
    Get usage for a specific feature

    Useful for:
    - Checking before performing action
    - Showing usage in UI
    - Warning when approaching limit
    """
    user_data = USER_USAGE.get(user_id, {"tier": "free", "usage": {}})
    tier = user_data["tier"]
    limits = TIERS[tier]["limits"]

    if feature not in limits:
        raise HTTPException(status_code=404, detail="Feature not found")

    limit = limits[feature]
    used = user_data.get("usage", {}).get(feature, 0)
    remaining = -1 if limit == -1 else max(0, limit - used)

    return {
        "feature": feature,
        "used": used,
        "limit": limit,
        "remaining": remaining,
        "at_limit": remaining == 0 and limit != -1,
        "percentage_used": round(used / limit * 100, 1) if limit > 0 else 0
    }


@router.post("/usage/{user_id}/track")
async def track_usage(user_id: str, feature: str, count: int = 1):
    """
    Track feature usage

    Called when user performs action:
    - Creates booking
    - Generates SOAP note
    - Sends message
    - etc.
    """
    if user_id not in USER_USAGE:
        USER_USAGE[user_id] = {
            "tier": "free",
            "period_start": datetime.utcnow(),
            "period_end": datetime(2024, 7, 1),
            "usage": {k: 0 for k in TIERS["free"]["limits"].keys()}
        }

    user_data = USER_USAGE[user_id]
    tier = user_data["tier"]
    limits = TIERS[tier]["limits"]

    if feature not in limits:
        raise HTTPException(status_code=404, detail="Feature not found")

    limit = limits[feature]
    current = user_data["usage"].get(feature, 0)

    # Check if at limit
    if limit != -1 and current >= limit:
        return {
            "tracked": False,
            "at_limit": True,
            "message": f"You've reached your {feature} limit. Upgrade to continue.",
            "upgrade_url": "/upgrade"
        }

    # Track usage
    user_data["usage"][feature] = current + count
    USER_USAGE[user_id] = user_data

    return {
        "tracked": True,
        "feature": feature,
        "new_count": user_data["usage"][feature],
        "remaining": -1 if limit == -1 else limit - user_data["usage"][feature]
    }


@router.get("/limits", response_model=Dict[str, TierLimits])
async def get_all_limits():
    """
    Get limits for all tiers

    Used for:
    - Pricing page
    - Tier comparison
    - Upgrade decisions
    """
    return {
        tier: TierLimits(
            tier=tier,
            name=data["name"],
            price=data["price"],
            currency=data["currency"],
            limits=data["limits"],
            features=data["features"]
        )
        for tier, data in TIERS.items()
    }


@router.get("/limits/{tier}", response_model=TierLimits)
async def get_tier_limits(tier: str):
    """
    Get limits for specific tier
    """
    if tier not in TIERS:
        raise HTTPException(status_code=404, detail="Tier not found")

    data = TIERS[tier]
    return TierLimits(
        tier=tier,
        name=data["name"],
        price=data["price"],
        currency=data["currency"],
        limits=data["limits"],
        features=data["features"]
    )


@router.get("/upgrade-prompt/{user_id}", response_model=UpgradePrompt)
async def get_upgrade_prompt(user_id: str, feature: Optional[str] = None):
    """
    Get contextual upgrade prompt

    Returns personalized upgrade message based on:
    - Current usage patterns
    - Feature that triggered prompt
    - User's tier
    """
    user_data = USER_USAGE.get(user_id, {"tier": "free", "usage": {}})
    current_tier = user_data["tier"]

    # Determine recommended tier
    if current_tier == "free":
        recommended = "basic"
    elif current_tier == "basic":
        recommended = "professional"
    else:
        recommended = "enterprise"

    feature_messages = {
        "clients": "Grow your practice with more client capacity",
        "bookings_per_month": "Handle more appointments without limits",
        "soap_notes": "Generate unlimited AI-powered clinical notes",
        "ai_suggestions": "Get unlimited AI diagnosis suggestions",
        "voice_transcriptions": "Transcribe more sessions effortlessly"
    }

    message = feature_messages.get(
        feature,
        f"Unlock more features with {TIERS[recommended]['name']}"
    )

    return UpgradePrompt(
        show_prompt=current_tier != "enterprise",
        feature=feature or "general",
        current_tier=current_tier,
        recommended_tier=recommended,
        message=message,
        cta_text=f"Upgrade to {TIERS[recommended]['name']} - £{TIERS[recommended]['price']}/mo",
        cta_url=f"/upgrade?tier={recommended}"
    )


@router.get("/pricing")
async def get_pricing_info():
    """
    Get pricing page information

    Includes:
    - All tiers with pricing
    - Feature comparison
    - Popular tier highlight
    """
    return {
        "tiers": [
            {
                "tier": tier,
                "name": data["name"],
                "price": data["price"],
                "currency": data["currency"],
                "features": data["features"],
                "popular": tier == "professional",
                "cta": "Start Free Trial" if tier != "free" else "Get Started"
            }
            for tier, data in TIERS.items()
        ],
        "comparison": {
            "clients": {"free": 5, "basic": 50, "professional": 200, "enterprise": "Unlimited"},
            "bookings": {"free": 20, "basic": 100, "professional": "Unlimited", "enterprise": "Unlimited"},
            "ai_features": {"free": "Limited", "basic": "Standard", "professional": "Full", "enterprise": "Full + Custom"},
            "support": {"free": "Email", "basic": "Priority", "professional": "Priority", "enterprise": "Dedicated"}
        },
        "faq": [
            {"q": "Can I change plans?", "a": "Yes, upgrade or downgrade anytime."},
            {"q": "Is there a free trial?", "a": "Yes, 14 days free on paid plans."},
            {"q": "What payment methods?", "a": "Credit card, PayPal, bank transfer (Enterprise)."}
        ]
    }


@router.get("/warning/{user_id}/{feature}")
async def get_usage_warning(user_id: str, feature: str):
    """
    Get usage warning for feature

    Returns warning when:
    - 80% of limit used
    - 90% of limit used
    - At limit
    """
    user_data = USER_USAGE.get(user_id, {"tier": "free", "usage": {}})
    tier = user_data["tier"]
    limits = TIERS[tier]["limits"]

    if feature not in limits:
        return {"warning": False}

    limit = limits[feature]
    if limit == -1:
        return {"warning": False, "unlimited": True}

    used = user_data.get("usage", {}).get(feature, 0)
    percentage = used / limit * 100

    if percentage >= 100:
        return {
            "warning": True,
            "level": "critical",
            "message": f"You've reached your {feature} limit",
            "action": "upgrade"
        }
    elif percentage >= 90:
        return {
            "warning": True,
            "level": "high",
            "message": f"You've used {int(percentage)}% of your {feature} allowance",
            "action": "consider_upgrade"
        }
    elif percentage >= 80:
        return {
            "warning": True,
            "level": "medium",
            "message": f"You've used {int(percentage)}% of your {feature} allowance",
            "action": "monitor"
        }

    return {"warning": False, "percentage": percentage}
