"""
SANA Health Platform - Main FastAPI Application
Complete AI/ML platform for personalized health and wellness
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import route modules
from api.routes import (
    auth, scoring, evidence, planning, verification, matching,
    safety, learning, herbs, index, practice, marketplace,
    payments, messaging, analytics, wearables, enterprise,
    widget, outcomes, scanner, ai_assistant, marketplace_products,
    freemium
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🌿 SANA Health Platform starting up...")
    yield
    # Shutdown
    print("🌿 SANA Health Platform shutting down...")


# Create FastAPI application
app = FastAPI(
    title="SANA Health Platform",
    description="""
    ## Comprehensive AI/ML Platform for Personalized Health and Wellness

    ### Core Algorithms (12)
    - **SISM** - Integrative Scoring Model
    - **Health Graph** - Evidence Engine
    - **SHAM** - Habit & Activity Model
    - **SCVM** - Credential Vetting
    - **SPRM** - Practitioner Matching
    - **SST** - Safety & Triage
    - **SOU** - Outcome Uplift (Thompson Sampling)
    - **SHI** - SANA Herb Index
    - **SANA Index** - Practitioner Credibility Scoring
    - **SIRM** - Journal AI (8 Personas)
    - **Product Scanner** - Supplement Analysis
    - **Clinical AI** - SOAP Notes & Diagnosis

    ### Platform Services (14)
    Auth, Practice, Marketplace, Payments, Messaging, Analytics,
    Wearables, Enterprise, Widget, Outcomes, Scanner, AI Assistant,
    Marketplace Products, Freemium
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# REGISTER API ROUTES
# ============================================================================

# Core Algorithms
app.include_router(scoring.router, prefix="/api/v1/scoring", tags=["Scoring (SISM)"])
app.include_router(evidence.router, prefix="/api/v1/evidence", tags=["Evidence (Health Graph)"])
app.include_router(planning.router, prefix="/api/v1/planning", tags=["Planning (SHAM)"])
app.include_router(verification.router, prefix="/api/v1/verification", tags=["Verification (SCVM)"])
app.include_router(matching.router, prefix="/api/v1/matching", tags=["Matching (SPRM)"])
app.include_router(safety.router, prefix="/api/v1/safety", tags=["Safety (SST)"])
app.include_router(learning.router, prefix="/api/v1/learning", tags=["Learning (SOU)"])
app.include_router(herbs.router, prefix="/api/v1/herbs", tags=["Herbs (SHI)"])
app.include_router(index.router, prefix="/api/v1/index", tags=["Index (SANA Index)"])

# Platform Services
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(practice.router, prefix="/api/v1/practice", tags=["Practice Management"])
app.include_router(marketplace.router, prefix="/api/v1/marketplace", tags=["Marketplace"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])
app.include_router(messaging.router, prefix="/api/v1/messaging", tags=["Messaging"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(wearables.router, prefix="/api/v1/wearables", tags=["Wearables"])
app.include_router(enterprise.router, prefix="/api/v1/enterprise", tags=["Enterprise"])
app.include_router(widget.router, prefix="/api/v1/widget", tags=["Widget"])
app.include_router(outcomes.router, prefix="/api/v1/outcomes", tags=["Outcomes (PROMs)"])
app.include_router(scanner.router, prefix="/api/v1/scanner", tags=["Product Scanner"])
app.include_router(ai_assistant.router, prefix="/api/v1/ai", tags=["AI Assistant"])
app.include_router(marketplace_products.router, prefix="/api/v1/marketplace-products", tags=["Marketplace Products"])
app.include_router(freemium.router, prefix="/api/v1/freemium", tags=["Freemium"])


# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": "SANA Health Platform",
        "version": "1.0.0",
        "status": "operational",
        "products": {
            "market": "Practice management and marketplace",
            "evidence": "AI research infrastructure",
            "enterprise": "B2B solutions for NHS, corporate, clinics"
        },
        "algorithms": 12,
        "services": 14,
        "endpoints": "350+",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "sana-api"}


@app.get("/api/v1", tags=["Health"])
async def api_info():
    """API version information"""
    return {
        "version": "1.0.0",
        "base_url": "/api/v1",
        "algorithms": [
            "scoring", "evidence", "planning", "verification",
            "matching", "safety", "learning", "herbs", "index"
        ],
        "services": [
            "auth", "practice", "marketplace", "payments", "messaging",
            "analytics", "wearables", "enterprise", "widget", "outcomes",
            "scanner", "ai", "marketplace-products", "freemium"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
