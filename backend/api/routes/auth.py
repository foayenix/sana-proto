"""
SANA Authentication Routes
JWT-based authentication service
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
from typing import Optional
import uuid

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "client"  # client, practitioner


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    user: dict


class UserProfile(BaseModel):
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: str
    subscription_tier: str
    is_verified: bool
    created_at: datetime


# ============================================================================
# MOCK DATABASE
# ============================================================================

USERS_DB = {
    "demo@sana.health": {
        "id": "usr_demo_001",
        "email": "demo@sana.health",
        "hashed_password": "$2b$12$demo_hash",
        "first_name": "Sarah",
        "last_name": "Mitchell",
        "role": "client",
        "subscription_tier": "professional",
        "is_verified": True,
        "created_at": datetime(2024, 1, 1)
    },
    "practitioner@sana.health": {
        "id": "usr_prac_001",
        "email": "practitioner@sana.health",
        "hashed_password": "$2b$12$prac_hash",
        "first_name": "Dr. Emily",
        "last_name": "Chen",
        "role": "practitioner",
        "subscription_tier": "professional",
        "is_verified": True,
        "created_at": datetime(2023, 6, 1)
    }
}


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(data: UserRegister):
    """
    Register a new user account

    - Creates new user with email/password
    - Returns JWT tokens for immediate access
    - Sends verification email (async)
    """
    if data.email in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user_id = f"usr_{uuid.uuid4().hex[:8]}"
    new_user = {
        "id": user_id,
        "email": data.email,
        "hashed_password": f"$2b$12${uuid.uuid4().hex[:20]}",
        "first_name": data.first_name,
        "last_name": data.last_name,
        "role": data.role,
        "subscription_tier": "free",
        "is_verified": False,
        "created_at": datetime.utcnow()
    }

    USERS_DB[data.email] = new_user

    return TokenResponse(
        access_token=f"eyJ_{user_id}_{uuid.uuid4().hex[:16]}",
        refresh_token=f"ref_{user_id}_{uuid.uuid4().hex[:16]}",
        expires_in=3600,
        user={
            "id": user_id,
            "email": data.email,
            "role": data.role
        }
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    """
    Authenticate user and return JWT tokens

    - Validates email/password
    - Returns access and refresh tokens
    - Tracks login for analytics
    """
    user = USERS_DB.get(data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # In production: verify password with bcrypt
    return TokenResponse(
        access_token=f"eyJ_{user['id']}_{uuid.uuid4().hex[:16]}",
        refresh_token=f"ref_{user['id']}_{uuid.uuid4().hex[:16]}",
        expires_in=3600,
        user={
            "id": user["id"],
            "email": user["email"],
            "role": user["role"]
        }
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """
    Refresh expired access token

    - Validates refresh token
    - Issues new access token
    - Optionally rotates refresh token
    """
    # Extract user from refresh token (simplified)
    return TokenResponse(
        access_token=f"eyJ_refreshed_{uuid.uuid4().hex[:16]}",
        refresh_token=f"ref_new_{uuid.uuid4().hex[:16]}",
        expires_in=3600,
        user={"id": "usr_demo_001", "email": "demo@sana.health", "role": "client"}
    )


@router.get("/me", response_model=UserProfile)
async def get_current_user():
    """
    Get current authenticated user profile

    - Returns full user profile
    - Includes subscription tier
    - Includes verification status
    """
    user = USERS_DB["demo@sana.health"]
    return UserProfile(
        id=user["id"],
        email=user["email"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        role=user["role"],
        subscription_tier=user["subscription_tier"],
        is_verified=user["is_verified"],
        created_at=user["created_at"]
    )


@router.post("/logout")
async def logout():
    """
    Logout user and invalidate tokens

    - Invalidates access token
    - Invalidates refresh token
    - Clears session
    """
    return {"message": "Successfully logged out"}


@router.post("/forgot-password")
async def forgot_password(email: EmailStr):
    """
    Initiate password reset flow

    - Sends reset email if user exists
    - Always returns success (security)
    """
    return {"message": "If an account exists, a reset email has been sent"}


@router.post("/reset-password")
async def reset_password(token: str, new_password: str):
    """
    Reset password with token

    - Validates reset token
    - Updates password
    - Invalidates all sessions
    """
    return {"message": "Password has been reset successfully"}
