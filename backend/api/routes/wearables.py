"""
SANA Wearables Routes
Device integrations for health data
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
import uuid

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class WearableProvider(BaseModel):
    id: str
    name: str
    logo_url: str
    data_types: List[str]
    oauth_url: Optional[str] = None
    is_available: bool = True


class WearableConnection(BaseModel):
    id: str
    user_id: str
    provider: str
    is_connected: bool
    last_sync: Optional[datetime] = None
    data_types: List[str]


class DailySummary(BaseModel):
    date: date
    steps: Optional[int] = None
    active_minutes: Optional[int] = None
    calories_burned: Optional[int] = None
    sleep_hours: Optional[float] = None
    sleep_score: Optional[int] = None
    hrv: Optional[int] = None
    resting_hr: Optional[int] = None
    stress_score: Optional[int] = None


# ============================================================================
# MOCK DATA
# ============================================================================

PROVIDERS = [
    {
        "id": "apple_health",
        "name": "Apple Health",
        "logo_url": "/images/apple-health.png",
        "data_types": ["steps", "heart_rate", "sleep", "hrv", "workouts", "mindfulness"],
        "is_available": True
    },
    {
        "id": "fitbit",
        "name": "Fitbit",
        "logo_url": "/images/fitbit.png",
        "data_types": ["steps", "heart_rate", "sleep", "stress", "spo2"],
        "oauth_url": "https://www.fitbit.com/oauth2/authorize",
        "is_available": True
    },
    {
        "id": "oura",
        "name": "Oura Ring",
        "logo_url": "/images/oura.png",
        "data_types": ["sleep", "hrv", "readiness", "activity", "temperature"],
        "oauth_url": "https://cloud.ouraring.com/oauth/authorize",
        "is_available": True
    },
    {
        "id": "whoop",
        "name": "WHOOP",
        "logo_url": "/images/whoop.png",
        "data_types": ["strain", "recovery", "sleep", "hrv", "heart_rate"],
        "oauth_url": "https://api.prod.whoop.com/oauth/authorize",
        "is_available": True
    },
    {
        "id": "garmin",
        "name": "Garmin",
        "logo_url": "/images/garmin.png",
        "data_types": ["steps", "heart_rate", "sleep", "stress", "body_battery", "workouts"],
        "oauth_url": "https://connect.garmin.com/oauthConfirm",
        "is_available": True
    },
    {
        "id": "google_fit",
        "name": "Google Fit",
        "logo_url": "/images/google-fit.png",
        "data_types": ["steps", "heart_rate", "sleep", "workouts"],
        "oauth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "is_available": True
    }
]


# ============================================================================
# ROUTES
# ============================================================================

@router.get("/providers", response_model=List[WearableProvider])
async def list_providers():
    """
    List available wearable providers

    **Supported Devices:**
    - Apple Health (iOS)
    - Fitbit
    - Oura Ring
    - WHOOP
    - Garmin
    - Google Fit
    """
    return [WearableProvider(**p) for p in PROVIDERS]


@router.post("/connect", response_model=WearableConnection)
async def connect_wearable(user_id: str, provider: str):
    """
    Connect a wearable device

    OAuth flow:
    1. Get provider OAuth URL
    2. User authorizes in browser
    3. Callback stores tokens
    4. Initial data sync
    """
    provider_info = next((p for p in PROVIDERS if p["id"] == provider), None)
    if not provider_info:
        raise HTTPException(status_code=404, detail="Provider not found")

    connection_id = f"wc_{uuid.uuid4().hex[:8]}"

    return WearableConnection(
        id=connection_id,
        user_id=user_id,
        provider=provider,
        is_connected=True,
        last_sync=datetime.utcnow(),
        data_types=provider_info["data_types"]
    )


@router.get("/connections/{user_id}")
async def list_connections(user_id: str):
    """
    List user's wearable connections

    Shows:
    - Connected devices
    - Connection status
    - Last sync time
    """
    # Mock connections
    connections = [
        WearableConnection(
            id="wc_001",
            user_id=user_id,
            provider="apple_health",
            is_connected=True,
            last_sync=datetime(2024, 6, 20, 8, 0),
            data_types=["steps", "heart_rate", "sleep", "hrv"]
        ),
        WearableConnection(
            id="wc_002",
            user_id=user_id,
            provider="oura",
            is_connected=True,
            last_sync=datetime(2024, 6, 20, 7, 30),
            data_types=["sleep", "hrv", "readiness"]
        )
    ]

    return {
        "user_id": user_id,
        "connections": connections,
        "total_connected": len(connections)
    }


@router.post("/sync/{connection_id}")
async def sync_wearable(connection_id: str):
    """
    Trigger manual data sync

    Fetches latest data from provider:
    - Steps and activity
    - Sleep data
    - Heart rate and HRV
    - Other metrics
    """
    return {
        "connection_id": connection_id,
        "status": "syncing",
        "message": "Sync started. Data will be available shortly.",
        "estimated_time": "30 seconds"
    }


@router.get("/summaries/{user_id}")
async def get_daily_summaries(
    user_id: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 7
):
    """
    Get daily health summaries from wearables

    Aggregated data from all connected devices:
    - Steps and activity
    - Sleep quality
    - Heart metrics
    - Stress levels
    """
    summaries = [
        DailySummary(
            date=date(2024, 6, 20),
            steps=8432,
            active_minutes=45,
            calories_burned=2150,
            sleep_hours=7.5,
            sleep_score=82,
            hrv=48,
            resting_hr=58,
            stress_score=35
        ),
        DailySummary(
            date=date(2024, 6, 19),
            steps=10245,
            active_minutes=62,
            calories_burned=2380,
            sleep_hours=6.8,
            sleep_score=75,
            hrv=42,
            resting_hr=60,
            stress_score=42
        ),
        DailySummary(
            date=date(2024, 6, 18),
            steps=6890,
            active_minutes=32,
            calories_burned=1950,
            sleep_hours=8.2,
            sleep_score=88,
            hrv=52,
            resting_hr=56,
            stress_score=28
        )
    ]

    return {
        "user_id": user_id,
        "summaries": summaries[:limit],
        "averages": {
            "steps": 8522,
            "sleep_hours": 7.5,
            "hrv": 47,
            "sleep_score": 82
        }
    }


@router.delete("/connections/{connection_id}")
async def disconnect_wearable(connection_id: str):
    """
    Disconnect a wearable device

    Actions:
    - Revoke OAuth tokens
    - Remove connection record
    - Historical data preserved
    """
    return {
        "connection_id": connection_id,
        "disconnected": True,
        "message": "Device disconnected. Historical data preserved."
    }


@router.get("/data/{user_id}/{data_type}")
async def get_specific_data(
    user_id: str,
    data_type: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """
    Get specific wearable data type

    **Data Types:**
    - steps: Daily step count
    - sleep: Sleep duration and stages
    - hrv: Heart rate variability
    - heart_rate: Resting and active HR
    - stress: Stress scores (where available)
    """
    data_map = {
        "steps": [
            {"date": "2024-06-20", "value": 8432},
            {"date": "2024-06-19", "value": 10245},
            {"date": "2024-06-18", "value": 6890}
        ],
        "hrv": [
            {"date": "2024-06-20", "value": 48, "unit": "ms"},
            {"date": "2024-06-19", "value": 42, "unit": "ms"},
            {"date": "2024-06-18", "value": 52, "unit": "ms"}
        ],
        "sleep": [
            {"date": "2024-06-20", "total_hours": 7.5, "deep": 1.5, "rem": 2.0, "light": 4.0, "score": 82},
            {"date": "2024-06-19", "total_hours": 6.8, "deep": 1.2, "rem": 1.8, "light": 3.8, "score": 75}
        ]
    }

    return {
        "user_id": user_id,
        "data_type": data_type,
        "data": data_map.get(data_type, [])
    }
