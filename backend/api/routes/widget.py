"""
SANA Widget Routes
Embeddable booking widget for practitioner websites
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, date
import uuid
import secrets

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class WidgetConfig(BaseModel):
    id: str
    practitioner_id: str
    widget_key: str
    slug: str
    theme: str
    primary_color: str
    show_reviews: bool
    show_price: bool
    allowed_domains: List[str]
    is_active: bool


class WidgetCreateRequest(BaseModel):
    practitioner_id: str
    slug: Optional[str] = None
    theme: str = "light"
    primary_color: str = "#4A7C59"
    show_reviews: bool = True
    show_price: bool = True
    allowed_domains: Optional[List[str]] = None


class PublicPractitioner(BaseModel):
    name: str
    title: str
    bio: str
    sana_index: float
    rating: float
    review_count: int
    hourly_rate: float
    currency: str
    specialties: List[str]
    image_url: Optional[str] = None


class AvailabilitySlot(BaseModel):
    date: date
    time: str
    duration: int
    available: bool


# ============================================================================
# MOCK DATA
# ============================================================================

WIDGET_CONFIGS = {
    "wid_001": {
        "id": "wid_001",
        "practitioner_id": "prac_001",
        "widget_key": "sk_live_abc123xyz789",
        "slug": "dr-emily-chen",
        "theme": "light",
        "primary_color": "#4A7C59",
        "show_reviews": True,
        "show_price": True,
        "allowed_domains": ["emilychenacupuncture.com", "localhost"],
        "is_active": True
    }
}


# ============================================================================
# ROUTES - CONFIGURATION
# ============================================================================

@router.post("/config", response_model=WidgetConfig)
async def create_widget_config(data: WidgetCreateRequest):
    """
    Create widget configuration for practitioner

    **Widget Features:**
    - Customizable theme and colors
    - Show/hide pricing and reviews
    - Domain restrictions for security
    - Unique widget key and shareable slug
    """
    widget_id = f"wid_{uuid.uuid4().hex[:8]}"
    widget_key = f"sk_live_{secrets.token_urlsafe(24)}"
    slug = data.slug or f"practitioner-{uuid.uuid4().hex[:6]}"

    config = WidgetConfig(
        id=widget_id,
        practitioner_id=data.practitioner_id,
        widget_key=widget_key,
        slug=slug,
        theme=data.theme,
        primary_color=data.primary_color,
        show_reviews=data.show_reviews,
        show_price=data.show_price,
        allowed_domains=data.allowed_domains or [],
        is_active=True
    )

    WIDGET_CONFIGS[widget_id] = config.model_dump()
    return config


@router.get("/config/{widget_id}", response_model=WidgetConfig)
async def get_widget_config(widget_id: str):
    """
    Get widget configuration
    """
    config = WIDGET_CONFIGS.get(widget_id)
    if not config:
        raise HTTPException(status_code=404, detail="Widget not found")
    return WidgetConfig(**config)


@router.put("/config/{widget_id}")
async def update_widget_config(widget_id: str, updates: Dict):
    """
    Update widget configuration

    Updatable fields:
    - theme, primary_color
    - show_reviews, show_price
    - allowed_domains
    - is_active
    """
    config = WIDGET_CONFIGS.get(widget_id)
    if not config:
        raise HTTPException(status_code=404, detail="Widget not found")

    for key, value in updates.items():
        if key in config and key not in ["id", "widget_key", "practitioner_id"]:
            config[key] = value

    return WidgetConfig(**config)


@router.get("/config/{widget_id}/embed-code")
async def get_embed_code(widget_id: str):
    """
    Get embed codes for website integration

    **Integration Options:**
    - Iframe embed
    - JavaScript widget
    - Direct link
    """
    config = WIDGET_CONFIGS.get(widget_id)
    if not config:
        raise HTTPException(status_code=404, detail="Widget not found")

    widget_key = config["widget_key"]
    slug = config["slug"]

    return {
        "iframe": f'<iframe src="https://sana.health/widget/{widget_key}" style="width: 100%; min-height: 600px; border: none;"></iframe>',
        "javascript": f'''<div id="sana-widget"></div>
<script src="https://sana.health/widget/embed.js"></script>
<script>
  SANAWidget.init({{
    key: '{widget_key}',
    container: '#sana-widget',
    style: 'inline',
    theme: '{config["theme"]}'
  }});
</script>''',
        "direct_link": f"https://sana.health/book/{slug}"
    }


@router.get("/config/{widget_id}/links")
async def get_shareable_links(widget_id: str):
    """
    Get shareable booking links
    """
    config = WIDGET_CONFIGS.get(widget_id)
    if not config:
        raise HTTPException(status_code=404, detail="Widget not found")

    return {
        "booking_page": f"https://sana.health/book/{config['slug']}",
        "widget_embed": f"https://sana.health/widget/{config['widget_key']}",
        "qr_code_url": f"https://sana.health/api/v1/widget/qr/{config['slug']}"
    }


# ============================================================================
# ROUTES - PUBLIC (No Auth Required)
# ============================================================================

@router.get("/public/{widget_key}")
async def get_public_widget_data(widget_key: str):
    """
    Get widget data for public display (no auth)

    Returns:
    - Practitioner profile
    - Services offered
    - Pricing
    - Reviews (if enabled)
    """
    config = next((c for c in WIDGET_CONFIGS.values() if c["widget_key"] == widget_key), None)
    if not config:
        raise HTTPException(status_code=404, detail="Widget not found")

    practitioner = PublicPractitioner(
        name="Dr. Emily Chen",
        title="Licensed Acupuncturist",
        bio="Specializing in anxiety and chronic pain management through Traditional Chinese Medicine.",
        sana_index=87,
        rating=4.9,
        review_count=156,
        hourly_rate=85,
        currency="GBP",
        specialties=["anxiety", "chronic_pain", "fertility"],
        image_url="https://i.pravatar.cc/150?u=emily"
    )

    response = {
        "practitioner": practitioner.model_dump(),
        "services": [
            {"name": "Initial Consultation", "duration": 90, "price": 120},
            {"name": "Follow-up Session", "duration": 60, "price": 85},
            {"name": "Quick Check-in", "duration": 30, "price": 50}
        ],
        "theme": config["theme"],
        "primary_color": config["primary_color"]
    }

    if config["show_reviews"]:
        response["reviews"] = [
            {"rating": 5, "text": "Life-changing treatment!", "author": "Sarah M."},
            {"rating": 5, "text": "Finally found relief.", "author": "Michael R."}
        ]

    if not config["show_price"]:
        for service in response["services"]:
            del service["price"]

    return response


@router.get("/public/{widget_key}/availability")
async def get_public_availability(
    widget_key: str,
    start_date: Optional[date] = None,
    service_duration: int = 60
):
    """
    Get available time slots (no auth)

    Returns next 14 days of availability
    """
    config = next((c for c in WIDGET_CONFIGS.values() if c["widget_key"] == widget_key), None)
    if not config:
        raise HTTPException(status_code=404, detail="Widget not found")

    # Generate mock availability
    slots = [
        AvailabilitySlot(date=date(2024, 7, 15), time="09:00", duration=60, available=True),
        AvailabilitySlot(date=date(2024, 7, 15), time="10:00", duration=60, available=False),
        AvailabilitySlot(date=date(2024, 7, 15), time="11:00", duration=60, available=True),
        AvailabilitySlot(date=date(2024, 7, 15), time="14:00", duration=60, available=True),
        AvailabilitySlot(date=date(2024, 7, 16), time="09:00", duration=60, available=True),
        AvailabilitySlot(date=date(2024, 7, 16), time="10:00", duration=60, available=True),
    ]

    return {
        "practitioner_id": config["practitioner_id"],
        "slots": [s.model_dump() for s in slots],
        "timezone": "Europe/London"
    }


@router.post("/public/{widget_key}/book")
async def create_public_booking(
    widget_key: str,
    client_name: str,
    client_email: str,
    client_phone: Optional[str],
    date: date,
    time: str,
    service_type: str = "follow_up"
):
    """
    Create booking from public widget (no auth)

    Flow:
    1. Validate slot availability
    2. Create guest or link to existing user
    3. Create booking
    4. Send confirmation email
    5. Create payment intent
    """
    config = next((c for c in WIDGET_CONFIGS.values() if c["widget_key"] == widget_key), None)
    if not config:
        raise HTTPException(status_code=404, detail="Widget not found")

    booking_id = f"book_{uuid.uuid4().hex[:8]}"

    return {
        "booking_id": booking_id,
        "status": "pending_payment",
        "practitioner": "Dr. Emily Chen",
        "date": str(date),
        "time": time,
        "service": service_type,
        "price": 85.00,
        "currency": "GBP",
        "payment_url": f"https://sana.health/pay/{booking_id}",
        "confirmation_sent": True
    }


@router.get("/book/{slug}")
async def get_booking_page(slug: str):
    """
    Get shareable booking page data

    Used for direct booking links like:
    https://sana.health/book/dr-emily-chen
    """
    config = next((c for c in WIDGET_CONFIGS.values() if c["slug"] == slug), None)
    if not config:
        raise HTTPException(status_code=404, detail="Practitioner not found")

    return {
        "slug": slug,
        "widget_key": config["widget_key"],
        "practitioner_name": "Dr. Emily Chen",
        "page_title": "Book with Dr. Emily Chen",
        "redirect_to": f"/widget/{config['widget_key']}"
    }
