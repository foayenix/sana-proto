"""
SANA Practice Management Routes
Scheduling, clients, sessions, and booking
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime, date, time
import uuid

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class AvailabilitySlot(BaseModel):
    day_of_week: int  # 0=Monday, 6=Sunday
    start_time: str  # HH:MM
    end_time: str
    is_available: bool = True


class AvailabilityRequest(BaseModel):
    practitioner_id: str
    slots: List[AvailabilitySlot]


class Client(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    conditions: List[str] = []
    notes: Optional[str] = None
    created_at: datetime


class Session(BaseModel):
    id: str
    client_id: str
    practitioner_id: str
    scheduled_at: datetime
    duration_minutes: int
    session_type: str  # initial, follow_up, review
    status: str  # scheduled, completed, cancelled, no_show
    notes: Optional[str] = None


class SOAPNote(BaseModel):
    subjective: str  # Patient's description
    objective: str   # Practitioner's observations
    assessment: str  # Diagnosis/analysis
    plan: str        # Treatment plan


class Booking(BaseModel):
    id: str
    client_id: str
    practitioner_id: str
    scheduled_at: datetime
    duration_minutes: int = 60
    session_type: str = "initial"
    price: float
    currency: str = "GBP"
    status: str = "pending"
    video_link: Optional[str] = None


# ============================================================================
# MOCK DATA
# ============================================================================

MOCK_CLIENTS = [
    {
        "id": "client_001",
        "first_name": "Sarah",
        "last_name": "Mitchell",
        "email": "sarah@example.com",
        "phone": "+44 7700 900123",
        "conditions": ["anxiety", "sleep"],
        "notes": "Prefers evening appointments",
        "created_at": datetime(2024, 1, 15)
    },
    {
        "id": "client_002",
        "first_name": "James",
        "last_name": "Wilson",
        "email": "james@example.com",
        "phone": "+44 7700 900456",
        "conditions": ["chronic_pain", "stress"],
        "notes": "",
        "created_at": datetime(2024, 2, 1)
    }
]

MOCK_SESSIONS = [
    {
        "id": "sess_001",
        "client_id": "client_001",
        "practitioner_id": "prac_001",
        "scheduled_at": datetime(2024, 6, 15, 10, 0),
        "duration_minutes": 60,
        "session_type": "follow_up",
        "status": "completed",
        "notes": "Good progress with anxiety management"
    }
]

MOCK_BOOKINGS = [
    {
        "id": "book_001",
        "client_id": "client_001",
        "practitioner_id": "prac_001",
        "scheduled_at": datetime(2024, 7, 20, 14, 0),
        "duration_minutes": 60,
        "session_type": "follow_up",
        "price": 85.0,
        "currency": "GBP",
        "status": "confirmed",
        "video_link": "https://meet.sana.health/sess_abc123"
    }
]


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/availability")
async def set_availability(data: AvailabilityRequest):
    """
    Set practitioner availability schedule

    Define recurring weekly availability:
    - Day of week (0=Monday through 6=Sunday)
    - Start and end times
    - Block out unavailable periods
    """
    return {
        "practitioner_id": data.practitioner_id,
        "slots_saved": len(data.slots),
        "message": "Availability updated successfully"
    }


@router.get("/calendar/{practitioner_id}")
async def get_calendar(
    practitioner_id: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """
    Get practitioner calendar with appointments

    Returns:
    - Available slots
    - Booked appointments
    - Blocked time
    """
    # Generate mock calendar
    available_slots = [
        {"date": "2024-07-15", "time": "09:00", "duration": 60, "available": True},
        {"date": "2024-07-15", "time": "10:00", "duration": 60, "available": False, "booking_id": "book_001"},
        {"date": "2024-07-15", "time": "11:00", "duration": 60, "available": True},
        {"date": "2024-07-15", "time": "14:00", "duration": 60, "available": True},
        {"date": "2024-07-15", "time": "15:00", "duration": 60, "available": True},
    ]

    return {
        "practitioner_id": practitioner_id,
        "start_date": start_date or date.today(),
        "slots": available_slots,
        "timezone": "Europe/London"
    }


@router.post("/clients", response_model=Client)
async def add_client(
    practitioner_id: str,
    first_name: str,
    last_name: str,
    email: str,
    phone: Optional[str] = None,
    conditions: List[str] = [],
    notes: Optional[str] = None
):
    """
    Add a new client to practitioner's roster

    Creates client record with:
    - Contact information
    - Health conditions
    - Notes
    """
    client_id = f"client_{uuid.uuid4().hex[:8]}"

    new_client = Client(
        id=client_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        conditions=conditions,
        notes=notes,
        created_at=datetime.utcnow()
    )

    return new_client


@router.get("/clients/{practitioner_id}")
async def list_clients(
    practitioner_id: str,
    status: Optional[str] = None,  # active, inactive, all
    limit: int = Query(default=50, le=200)
):
    """
    List practitioner's clients

    Filter by:
    - Status (active, inactive)
    - Search by name
    """
    return {
        "practitioner_id": practitioner_id,
        "clients": [Client(**c) for c in MOCK_CLIENTS],
        "total": len(MOCK_CLIENTS)
    }


@router.post("/sessions", response_model=Session)
async def create_session(
    client_id: str,
    practitioner_id: str,
    scheduled_at: datetime,
    duration_minutes: int = 60,
    session_type: str = "follow_up"
):
    """
    Create a new session

    Session types:
    - initial: First consultation
    - follow_up: Ongoing treatment
    - review: Progress review
    """
    session_id = f"sess_{uuid.uuid4().hex[:8]}"

    return Session(
        id=session_id,
        client_id=client_id,
        practitioner_id=practitioner_id,
        scheduled_at=scheduled_at,
        duration_minutes=duration_minutes,
        session_type=session_type,
        status="scheduled"
    )


@router.post("/sessions/{session_id}/notes")
async def add_soap_notes(session_id: str, notes: SOAPNote):
    """
    Add SOAP notes to a session

    **SOAP Format:**
    - **S**ubjective: Patient's description of symptoms/concerns
    - **O**bjective: Practitioner's clinical observations
    - **A**ssessment: Diagnosis or clinical impression
    - **P**lan: Treatment plan and recommendations
    """
    return {
        "session_id": session_id,
        "notes_saved": True,
        "soap": notes.model_dump(),
        "message": "SOAP notes saved successfully"
    }


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """
    Get session details

    Includes:
    - Session info
    - SOAP notes
    - Outcome data
    """
    session = next((s for s in MOCK_SESSIONS if s["id"] == session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return Session(**session)


@router.post("/bookings", response_model=Booking)
async def create_booking(
    client_id: str,
    practitioner_id: str,
    scheduled_at: datetime,
    duration_minutes: int = 60,
    session_type: str = "initial",
    price: float = 85.0
):
    """
    Create a new booking

    Booking flow:
    1. Check practitioner availability
    2. Create booking record
    3. Send confirmation to client
    4. Generate video call link (if applicable)
    """
    booking_id = f"book_{uuid.uuid4().hex[:8]}"
    video_link = f"https://meet.sana.health/{booking_id}"

    return Booking(
        id=booking_id,
        client_id=client_id,
        practitioner_id=practitioner_id,
        scheduled_at=scheduled_at,
        duration_minutes=duration_minutes,
        session_type=session_type,
        price=price,
        status="confirmed",
        video_link=video_link
    )


@router.put("/bookings/{booking_id}/reschedule")
async def reschedule_booking(booking_id: str, new_datetime: datetime):
    """
    Reschedule an existing booking

    - Validates new time availability
    - Sends notifications to both parties
    - Updates calendar
    """
    return {
        "booking_id": booking_id,
        "new_datetime": new_datetime.isoformat(),
        "status": "rescheduled",
        "message": "Booking rescheduled. Notifications sent."
    }


@router.put("/bookings/{booking_id}/cancel")
async def cancel_booking(booking_id: str, reason: Optional[str] = None):
    """
    Cancel a booking

    - Updates booking status
    - Initiates refund if applicable
    - Sends cancellation notifications
    """
    return {
        "booking_id": booking_id,
        "status": "cancelled",
        "reason": reason,
        "refund_initiated": True,
        "message": "Booking cancelled. Refund will be processed within 5-7 business days."
    }


@router.get("/dashboard/{practitioner_id}")
async def get_practice_dashboard(practitioner_id: str):
    """
    Get practice management dashboard

    Overview of:
    - Today's appointments
    - Upcoming week
    - Client stats
    - Recent activity
    """
    return {
        "practitioner_id": practitioner_id,
        "today": {
            "appointments": 4,
            "completed": 2,
            "upcoming": 2
        },
        "this_week": {
            "total_appointments": 18,
            "new_clients": 3,
            "revenue": 1530.0
        },
        "clients": {
            "total": 156,
            "active": 89,
            "new_this_month": 7
        },
        "next_appointment": MOCK_BOOKINGS[0] if MOCK_BOOKINGS else None
    }
