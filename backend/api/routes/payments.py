"""
SANA Payments Routes
Stripe integration, subscriptions, and practitioner payouts
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class PaymentIntent(BaseModel):
    id: str
    amount: float
    currency: str
    status: str
    client_secret: str
    booking_id: Optional[str] = None


class PaymentConfirmation(BaseModel):
    payment_id: str
    status: str
    amount: float
    currency: str
    receipt_url: Optional[str] = None
    booking_id: Optional[str] = None


class SubscriptionCreate(BaseModel):
    user_id: str
    tier: str  # basic, professional, enterprise
    payment_method_id: str


class Subscription(BaseModel):
    id: str
    user_id: str
    tier: str
    status: str
    amount: float
    currency: str
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool


class PayoutBalance(BaseModel):
    practitioner_id: str
    available: float
    pending: float
    currency: str
    last_payout_date: Optional[datetime] = None
    next_payout_date: Optional[datetime] = None


# ============================================================================
# PRICING
# ============================================================================

SUBSCRIPTION_TIERS = {
    "free": {"name": "Free", "price": 0, "clients": 5, "bookings_per_month": 20},
    "basic": {"name": "Basic", "price": 29, "clients": 50, "bookings_per_month": 100},
    "professional": {"name": "Professional", "price": 79, "clients": 200, "bookings_per_month": -1},
    "enterprise": {"name": "Enterprise", "price": 199, "clients": -1, "bookings_per_month": -1}
}


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/create-intent", response_model=PaymentIntent)
async def create_payment_intent(
    amount: float,
    currency: str = "gbp",
    booking_id: Optional[str] = None,
    user_id: Optional[str] = None
):
    """
    Create a Stripe payment intent

    Flow:
    1. Create payment intent with amount
    2. Return client_secret for frontend
    3. Frontend confirms with Stripe.js
    4. Webhook confirms payment
    """
    intent_id = f"pi_{uuid.uuid4().hex[:24]}"
    client_secret = f"{intent_id}_secret_{uuid.uuid4().hex[:16]}"

    return PaymentIntent(
        id=intent_id,
        amount=amount,
        currency=currency,
        status="requires_payment_method",
        client_secret=client_secret,
        booking_id=booking_id
    )


@router.post("/{payment_id}/confirm", response_model=PaymentConfirmation)
async def confirm_payment(payment_id: str):
    """
    Confirm a payment (called after Stripe confirms)

    Actions:
    - Update payment status
    - Confirm booking if applicable
    - Send confirmation emails
    - Update practitioner balance
    """
    return PaymentConfirmation(
        payment_id=payment_id,
        status="succeeded",
        amount=85.00,
        currency="GBP",
        receipt_url=f"https://pay.stripe.com/receipts/{payment_id}",
        booking_id="book_001"
    )


@router.post("/{payment_id}/refund")
async def refund_payment(
    payment_id: str,
    amount: Optional[float] = None,  # None = full refund
    reason: Optional[str] = None
):
    """
    Refund a payment

    Options:
    - Full refund (default)
    - Partial refund (specify amount)

    Refund policies apply based on:
    - Time before appointment
    - Cancellation reason
    """
    return {
        "payment_id": payment_id,
        "refund_id": f"re_{uuid.uuid4().hex[:24]}",
        "amount_refunded": amount or 85.00,
        "status": "succeeded",
        "reason": reason
    }


@router.post("/subscriptions", response_model=Subscription)
async def create_subscription(data: SubscriptionCreate):
    """
    Create a new subscription

    **Tiers:**
    - Free: £0/month - 5 clients, 20 bookings/month
    - Basic: £29/month - 50 clients, 100 bookings/month
    - Professional: £79/month - 200 clients, unlimited bookings
    - Enterprise: £199/month - Unlimited everything, dedicated support
    """
    tier_info = SUBSCRIPTION_TIERS.get(data.tier)
    if not tier_info:
        raise HTTPException(status_code=400, detail="Invalid subscription tier")

    sub_id = f"sub_{uuid.uuid4().hex[:24]}"

    return Subscription(
        id=sub_id,
        user_id=data.user_id,
        tier=data.tier,
        status="active",
        amount=tier_info["price"],
        currency="GBP",
        current_period_start=datetime.utcnow(),
        current_period_end=datetime(2024, 8, 15),  # +1 month
        cancel_at_period_end=False
    )


@router.get("/subscriptions/{user_id}")
async def get_subscription(user_id: str):
    """
    Get user's current subscription

    Returns:
    - Subscription details
    - Usage stats
    - Upgrade options
    """
    return {
        "subscription": Subscription(
            id="sub_demo123",
            user_id=user_id,
            tier="professional",
            status="active",
            amount=79.0,
            currency="GBP",
            current_period_start=datetime(2024, 6, 15),
            current_period_end=datetime(2024, 7, 15),
            cancel_at_period_end=False
        ),
        "usage": {
            "clients_used": 89,
            "clients_limit": 200,
            "bookings_this_month": 67,
            "bookings_limit": -1
        },
        "upgrade_options": [
            {"tier": "enterprise", "price": 199, "savings": "Best for growing practices"}
        ]
    }


@router.put("/subscriptions/{subscription_id}/cancel")
async def cancel_subscription(subscription_id: str, immediate: bool = False):
    """
    Cancel a subscription

    Options:
    - At period end (default): Access until current period ends
    - Immediate: Access ends now, prorated refund
    """
    return {
        "subscription_id": subscription_id,
        "status": "canceled" if immediate else "active",
        "cancel_at_period_end": not immediate,
        "access_until": datetime(2024, 7, 15).isoformat()
    }


@router.get("/payouts/balance/{practitioner_id}", response_model=PayoutBalance)
async def get_payout_balance(practitioner_id: str):
    """
    Get practitioner's payout balance

    Shows:
    - Available balance (ready for payout)
    - Pending balance (clearing)
    - Payout schedule
    """
    return PayoutBalance(
        practitioner_id=practitioner_id,
        available=1250.00,
        pending=340.00,
        currency="GBP",
        last_payout_date=datetime(2024, 6, 1),
        next_payout_date=datetime(2024, 7, 1)
    )


@router.post("/payouts/{practitioner_id}/request")
async def request_payout(practitioner_id: str, amount: Optional[float] = None):
    """
    Request a payout

    Options:
    - Full available balance (default)
    - Specific amount

    Payouts processed within 2-3 business days
    """
    return {
        "payout_id": f"po_{uuid.uuid4().hex[:24]}",
        "practitioner_id": practitioner_id,
        "amount": amount or 1250.00,
        "currency": "GBP",
        "status": "pending",
        "estimated_arrival": datetime(2024, 7, 5).isoformat()
    }


@router.get("/payouts/{practitioner_id}/history")
async def get_payout_history(practitioner_id: str, limit: int = 10):
    """
    Get payout history

    Shows:
    - Past payouts
    - Amounts and dates
    - Status
    """
    return {
        "practitioner_id": practitioner_id,
        "payouts": [
            {"id": "po_001", "amount": 1450.00, "date": "2024-06-01", "status": "paid"},
            {"id": "po_002", "amount": 1320.00, "date": "2024-05-01", "status": "paid"},
            {"id": "po_003", "amount": 1180.00, "date": "2024-04-01", "status": "paid"},
        ],
        "total_paid_out": 12450.00,
        "this_year": 8450.00
    }


@router.get("/pricing")
async def get_pricing():
    """
    Get subscription pricing information
    """
    return {
        "tiers": SUBSCRIPTION_TIERS,
        "currency": "GBP",
        "billing": "monthly",
        "features_comparison": {
            "free": ["5 clients", "20 bookings/month", "Basic analytics"],
            "basic": ["50 clients", "100 bookings/month", "Outcome tracking", "Custom branding"],
            "professional": ["200 clients", "Unlimited bookings", "Full analytics", "Priority support"],
            "enterprise": ["Unlimited", "Dedicated support", "API access", "Custom integrations"]
        }
    }
