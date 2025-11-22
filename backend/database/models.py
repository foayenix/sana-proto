"""
SANA Health Platform - Database Models
SQLAlchemy 2.0 ORM Models
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey, Enum, Table
)
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


# ============================================================================
# ENUMS
# ============================================================================

class UserRole(str, enum.Enum):
    CLIENT = "client"
    PRACTITIONER = "practitioner"
    RESEARCHER = "researcher"
    ADMIN = "admin"
    ENTERPRISE = "enterprise"


class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class AppointmentStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class SessionType(str, enum.Enum):
    VIDEO = "video"
    IN_PERSON = "in_person"
    PHONE = "phone"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REFUNDED = "refunded"
    FAILED = "failed"


# ============================================================================
# USER MODELS
# ============================================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.CLIENT)
    subscription_tier: Mapped[SubscriptionTier] = mapped_column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)

    # Profile
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))

    # Metadata
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    health_scores = relationship("HealthScore", back_populates="user")
    practitioner_profile = relationship("PractitionerProfile", back_populates="user", uselist=False)
    appointments = relationship("Appointment", back_populates="client", foreign_keys="Appointment.client_id")
    journal_entries = relationship("JournalEntry", back_populates="user")
    wearable_connections = relationship("WearableConnection", back_populates="user")


class PractitionerProfile(Base):
    __tablename__ = "practitioner_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True)

    # Professional Info
    title: Mapped[Optional[str]] = mapped_column(String(50))
    bio: Mapped[Optional[str]] = mapped_column(Text)
    specialties: Mapped[Optional[dict]] = mapped_column(JSON, default=list)
    modalities: Mapped[Optional[dict]] = mapped_column(JSON, default=list)

    # SANA Index Components
    sana_index: Mapped[float] = mapped_column(Float, default=0.0)
    credentials_score: Mapped[float] = mapped_column(Float, default=0.0)
    volume_score: Mapped[float] = mapped_column(Float, default=0.0)
    outcomes_score: Mapped[float] = mapped_column(Float, default=0.0)
    completeness_score: Mapped[float] = mapped_column(Float, default=0.0)
    satisfaction_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Stats
    years_experience: Mapped[int] = mapped_column(Integer, default=0)
    total_clients: Mapped[int] = mapped_column(Integer, default=0)
    total_sessions: Mapped[int] = mapped_column(Integer, default=0)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)

    # Practice Details
    hourly_rate: Mapped[Optional[float]] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(3), default="GBP")
    location: Mapped[Optional[str]] = mapped_column(String(255))
    offers_video: Mapped[bool] = mapped_column(Boolean, default=True)
    offers_in_person: Mapped[bool] = mapped_column(Boolean, default=False)

    # Verification
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    credentials: Mapped[Optional[dict]] = mapped_column(JSON, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="practitioner_profile")
    appointments = relationship("Appointment", back_populates="practitioner", foreign_keys="Appointment.practitioner_id")
    availability = relationship("Availability", back_populates="practitioner")
    reviews = relationship("Review", back_populates="practitioner")
    outcome_records = relationship("OutcomeRecord", back_populates="practitioner")


# ============================================================================
# HEALTH SCORING (SISM)
# ============================================================================

class HealthScore(Base):
    __tablename__ = "health_scores"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    # Overall Score
    overall: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="Unknown")

    # Domain Scores (0-100)
    physical: Mapped[float] = mapped_column(Float, default=0.0)
    mental: Mapped[float] = mapped_column(Float, default=0.0)
    emotional: Mapped[float] = mapped_column(Float, default=0.0)
    social: Mapped[float] = mapped_column(Float, default=0.0)
    sleep: Mapped[float] = mapped_column(Float, default=0.0)
    energy: Mapped[float] = mapped_column(Float, default=0.0)

    # Age Metrics
    biological_age: Mapped[Optional[int]] = mapped_column(Integer)
    chronological_age: Mapped[Optional[int]] = mapped_column(Integer)

    # Data Sources
    data_sources: Mapped[Optional[dict]] = mapped_column(JSON, default=dict)

    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="health_scores")


# ============================================================================
# PRACTICE MANAGEMENT
# ============================================================================

class Availability(Base):
    __tablename__ = "availability"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    practitioner_id: Mapped[str] = mapped_column(String(36), ForeignKey("practitioner_profiles.id"))

    day_of_week: Mapped[int] = mapped_column(Integer)  # 0=Monday, 6=Sunday
    start_time: Mapped[str] = mapped_column(String(5))  # HH:MM
    end_time: Mapped[str] = mapped_column(String(5))
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    practitioner = relationship("PractitionerProfile", back_populates="availability")


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    practitioner_id: Mapped[str] = mapped_column(String(36), ForeignKey("practitioner_profiles.id"))

    # Details
    scheduled_at: Mapped[datetime] = mapped_column(DateTime)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    session_type: Mapped[SessionType] = mapped_column(Enum(SessionType), default=SessionType.VIDEO)
    status: Mapped[AppointmentStatus] = mapped_column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING)

    # Payment
    price: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(3), default="GBP")
    payment_status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)

    # Notes
    client_notes: Mapped[Optional[str]] = mapped_column(Text)
    practitioner_notes: Mapped[Optional[str]] = mapped_column(Text)
    soap_notes: Mapped[Optional[dict]] = mapped_column(JSON)

    # Video Call
    video_link: Mapped[Optional[str]] = mapped_column(String(500))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client = relationship("User", back_populates="appointments", foreign_keys=[client_id])
    practitioner = relationship("PractitionerProfile", back_populates="appointments", foreign_keys=[practitioner_id])


# ============================================================================
# JOURNAL & REFLECTION (SIRM)
# ============================================================================

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    content: Mapped[str] = mapped_column(Text)
    mood: Mapped[Optional[str]] = mapped_column(String(50))
    tags: Mapped[Optional[dict]] = mapped_column(JSON, default=list)

    # AI Responses
    ai_responses: Mapped[Optional[dict]] = mapped_column(JSON, default=dict)
    selected_persona: Mapped[Optional[str]] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="journal_entries")


# ============================================================================
# REVIEWS & RATINGS
# ============================================================================

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    practitioner_id: Mapped[str] = mapped_column(String(36), ForeignKey("practitioner_profiles.id"))
    client_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    appointment_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("appointments.id"))

    rating: Mapped[float] = mapped_column(Float)  # 1-5
    title: Mapped[Optional[str]] = mapped_column(String(200))
    content: Mapped[Optional[str]] = mapped_column(Text)

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    practitioner = relationship("PractitionerProfile", back_populates="reviews")


# ============================================================================
# OUTCOMES & PROMS
# ============================================================================

class OutcomeRecord(Base):
    __tablename__ = "outcome_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    practitioner_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("practitioner_profiles.id"))

    # PROM Type
    prom_type: Mapped[str] = mapped_column(String(50))  # WHO-5, DASS-21, VAS, CAM
    condition: Mapped[Optional[str]] = mapped_column(String(100))

    # Scores
    baseline_score: Mapped[Optional[float]] = mapped_column(Float)
    current_score: Mapped[float] = mapped_column(Float)
    improvement_pct: Mapped[Optional[float]] = mapped_column(Float)

    # Raw Data
    responses: Mapped[Optional[dict]] = mapped_column(JSON)

    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    practitioner = relationship("PractitionerProfile", back_populates="outcome_records")


# ============================================================================
# WEARABLES
# ============================================================================

class WearableConnection(Base):
    __tablename__ = "wearable_connections"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    provider: Mapped[str] = mapped_column(String(50))  # apple_health, fitbit, oura, whoop, garmin
    access_token: Mapped[Optional[str]] = mapped_column(String(500))
    refresh_token: Mapped[Optional[str]] = mapped_column(String(500))
    token_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    is_connected: Mapped[bool] = mapped_column(Boolean, default=False)
    last_sync: Mapped[Optional[datetime]] = mapped_column(DateTime)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="wearable_connections")


class WearableData(Base):
    __tablename__ = "wearable_data"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    provider: Mapped[str] = mapped_column(String(50))

    # Data Type
    data_type: Mapped[str] = mapped_column(String(50))  # steps, hrv, sleep, heart_rate
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(20))

    recorded_at: Mapped[datetime] = mapped_column(DateTime)
    synced_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ============================================================================
# HERBS & SUPPLEMENTS (SHI)
# ============================================================================

class Herb(Base):
    __tablename__ = "herbs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name: Mapped[str] = mapped_column(String(200), index=True)
    latin_name: Mapped[Optional[str]] = mapped_column(String(200))
    common_names: Mapped[Optional[dict]] = mapped_column(JSON, default=list)

    # SHI Score Components
    shi_score: Mapped[float] = mapped_column(Float, default=0.0)
    evidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    safety_score: Mapped[float] = mapped_column(Float, default=0.0)
    quality_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Properties
    traditional_uses: Mapped[Optional[dict]] = mapped_column(JSON, default=list)
    conditions: Mapped[Optional[dict]] = mapped_column(JSON, default=list)
    contraindications: Mapped[Optional[dict]] = mapped_column(JSON, default=list)
    interactions: Mapped[Optional[dict]] = mapped_column(JSON, default=list)

    # Metadata
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ============================================================================
# PRODUCTS & SCANNER
# ============================================================================

class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Identifiers
    barcode: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(300), index=True)
    brand: Mapped[Optional[str]] = mapped_column(String(200))

    # Details
    category: Mapped[Optional[str]] = mapped_column(String(100))
    ingredients: Mapped[Optional[dict]] = mapped_column(JSON, default=list)
    dosage: Mapped[Optional[str]] = mapped_column(String(200))

    # Safety
    safety_score: Mapped[float] = mapped_column(Float, default=0.0)
    warnings: Mapped[Optional[dict]] = mapped_column(JSON, default=list)
    interactions: Mapped[Optional[dict]] = mapped_column(JSON, default=list)

    # Metadata
    image_url: Mapped[Optional[str]] = mapped_column(String(500))
    price: Mapped[Optional[float]] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ============================================================================
# ENTERPRISE
# ============================================================================

class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name: Mapped[str] = mapped_column(String(200))
    type: Mapped[str] = mapped_column(String(50))  # nhs, corporate, clinic, university

    # Configuration
    settings: Mapped[Optional[dict]] = mapped_column(JSON, default=dict)
    sso_config: Mapped[Optional[dict]] = mapped_column(JSON)

    # Subscription
    subscription_tier: Mapped[SubscriptionTier] = mapped_column(Enum(SubscriptionTier), default=SubscriptionTier.ENTERPRISE)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ============================================================================
# WIDGET
# ============================================================================

class WidgetConfig(Base):
    __tablename__ = "widget_configs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    practitioner_id: Mapped[str] = mapped_column(String(36), ForeignKey("practitioner_profiles.id"))

    # Widget Key
    widget_key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    slug: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True)

    # Styling
    theme: Mapped[str] = mapped_column(String(20), default="light")
    primary_color: Mapped[str] = mapped_column(String(7), default="#4A7C59")
    custom_css: Mapped[Optional[str]] = mapped_column(Text)

    # Settings
    show_reviews: Mapped[bool] = mapped_column(Boolean, default=True)
    show_price: Mapped[bool] = mapped_column(Boolean, default=True)
    allowed_domains: Mapped[Optional[dict]] = mapped_column(JSON, default=list)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ============================================================================
# PAYMENTS
# ============================================================================

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    # Stripe
    stripe_payment_intent_id: Mapped[Optional[str]] = mapped_column(String(100))

    # Amount
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(3), default="GBP")
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)

    # Reference
    appointment_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("appointments.id"))
    subscription_id: Mapped[Optional[str]] = mapped_column(String(36))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    # Stripe
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(100))
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(100))

    # Details
    tier: Mapped[SubscriptionTier] = mapped_column(Enum(SubscriptionTier))
    status: Mapped[str] = mapped_column(String(20), default="active")

    # Dates
    current_period_start: Mapped[datetime] = mapped_column(DateTime)
    current_period_end: Mapped[datetime] = mapped_column(DateTime)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ============================================================================
# MESSAGING
# ============================================================================

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    participant_1_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    participant_2_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    last_message_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id: Mapped[str] = mapped_column(String(36), ForeignKey("conversations.id"))
    sender_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    content: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ============================================================================
# USAGE TRACKING (Freemium)
# ============================================================================

class UsageRecord(Base):
    __tablename__ = "usage_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    feature: Mapped[str] = mapped_column(String(50), index=True)
    count: Mapped[int] = mapped_column(Integer, default=1)

    period_start: Mapped[datetime] = mapped_column(DateTime)
    period_end: Mapped[datetime] = mapped_column(DateTime)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
