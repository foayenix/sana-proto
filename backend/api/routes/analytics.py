"""
SANA Analytics Routes
Dashboards for practitioners, clients, and platform
"""

from fastapi import APIRouter
from typing import Optional, List
from datetime import datetime, date

router = APIRouter()


# ============================================================================
# ROUTES
# ============================================================================

@router.get("/practitioner/{practitioner_id}/dashboard")
async def get_practitioner_dashboard(practitioner_id: str, period: str = "month"):
    """
    Get practitioner analytics dashboard

    **Metrics:**
    - Client stats
    - Session counts
    - Revenue
    - Outcome improvements
    - SANA Index trend
    """
    return {
        "practitioner_id": practitioner_id,
        "period": period,
        "overview": {
            "total_clients": 156,
            "active_clients": 89,
            "new_clients_period": 7,
            "sessions_period": 67,
            "revenue_period": 5695.00,
            "avg_session_rating": 4.7
        },
        "sana_index": {
            "current": 87,
            "change": +3,
            "percentile": 92,
            "trend": [75, 78, 80, 82, 85, 87]
        },
        "outcomes": {
            "clients_improved": 72,
            "avg_improvement_pct": 34,
            "conditions": [
                {"name": "Anxiety", "improvement": 38, "clients": 45},
                {"name": "Chronic Pain", "improvement": 32, "clients": 28},
                {"name": "Sleep", "improvement": 41, "clients": 34}
            ]
        },
        "revenue": {
            "total": 5695.00,
            "by_week": [1200, 1450, 1380, 1665],
            "pending_payouts": 1250.00
        },
        "top_conditions": [
            {"condition": "anxiety", "count": 45},
            {"condition": "chronic_pain", "count": 28},
            {"condition": "sleep", "count": 34},
            {"condition": "stress", "count": 22}
        ]
    }


@router.get("/client/{client_id}/dashboard")
async def get_client_dashboard(client_id: str):
    """
    Get client analytics dashboard

    **Metrics:**
    - Health score trends
    - Session history
    - Progress tracking
    - Wearable summaries
    """
    return {
        "client_id": client_id,
        "health_score": {
            "current": 78,
            "change": +5,
            "trend": [68, 70, 72, 74, 76, 78],
            "status": "Thriving"
        },
        "domains": {
            "physical": 82,
            "mental": 75,
            "emotional": 78,
            "social": 72,
            "sleep": 80,
            "energy": 76
        },
        "sessions": {
            "total": 24,
            "this_month": 4,
            "upcoming": 2,
            "practitioners": ["Dr. Emily Chen", "Sarah Johnson"]
        },
        "progress": {
            "conditions_tracked": ["anxiety", "sleep"],
            "improvements": [
                {"condition": "anxiety", "baseline": 45, "current": 72, "change": +27},
                {"condition": "sleep", "baseline": 52, "current": 80, "change": +28}
            ]
        },
        "wearables": {
            "steps_avg": 8432,
            "sleep_avg": 7.2,
            "hrv_avg": 45,
            "active_devices": ["Apple Health", "Oura Ring"]
        }
    }


@router.get("/platform/overview")
async def get_platform_overview(period: str = "month"):
    """
    Get platform-wide analytics (admin only)

    **Metrics:**
    - User growth
    - Session volume
    - Revenue
    - Practitioner stats
    - Outcome analytics
    """
    return {
        "period": period,
        "users": {
            "total": 15420,
            "clients": 14200,
            "practitioners": 1220,
            "new_period": 890,
            "active_period": 5670
        },
        "sessions": {
            "total_period": 12450,
            "avg_per_day": 415,
            "completion_rate": 0.94,
            "video_pct": 0.72
        },
        "revenue": {
            "gmv": 1058250.00,
            "platform_revenue": 158737.50,
            "avg_session_value": 85.00
        },
        "outcomes": {
            "total_measured": 8750,
            "avg_improvement": 0.32,
            "conditions_tracked": 45
        },
        "practitioners": {
            "avg_sana_index": 68,
            "top_10_pct_count": 122,
            "new_verifications": 45
        },
        "engagement": {
            "daily_active_users": 3450,
            "monthly_active_users": 8920,
            "avg_session_duration": 52
        }
    }


@router.get("/practitioner/{practitioner_id}/outcomes")
async def get_practitioner_outcomes(practitioner_id: str, condition: Optional[str] = None):
    """
    Get detailed outcome analytics for practitioner

    **Evidence-based metrics:**
    - Client improvement rates
    - Condition-specific outcomes
    - Comparison to benchmarks
    """
    outcomes = {
        "anxiety": {"improvement": 0.72, "clients": 45, "benchmark": 0.58},
        "chronic_pain": {"improvement": 0.65, "clients": 28, "benchmark": 0.52},
        "sleep": {"improvement": 0.78, "clients": 34, "benchmark": 0.61},
        "stress": {"improvement": 0.68, "clients": 22, "benchmark": 0.55}
    }

    if condition:
        outcomes = {condition: outcomes.get(condition, {})}

    return {
        "practitioner_id": practitioner_id,
        "outcomes": outcomes,
        "total_clients_measured": 129,
        "overall_improvement": 0.71,
        "platform_benchmark": 0.57,
        "above_benchmark_pct": "+14%"
    }


@router.get("/practitioner/{practitioner_id}/revenue")
async def get_revenue_analytics(practitioner_id: str, period: str = "month"):
    """
    Get revenue analytics for practitioner

    **Financial metrics:**
    - Revenue by period
    - Session breakdown
    - Payout history
    """
    return {
        "practitioner_id": practitioner_id,
        "period": period,
        "revenue": {
            "total": 5695.00,
            "sessions": 67,
            "avg_per_session": 85.00,
            "by_type": {
                "initial": 1700.00,
                "follow_up": 3995.00
            }
        },
        "trend": [
            {"month": "Jan", "revenue": 4200},
            {"month": "Feb", "revenue": 4650},
            {"month": "Mar", "revenue": 5100},
            {"month": "Apr", "revenue": 5320},
            {"month": "May", "revenue": 5450},
            {"month": "Jun", "revenue": 5695}
        ],
        "payouts": {
            "total_paid": 28450.00,
            "pending": 1250.00,
            "next_payout": "2024-07-01"
        }
    }
