# SANA Health Platform

**A comprehensive AI/ML-powered healthcare platform for evidence-based Complementary and Alternative Medicine (CAM).**

---

## Prototype Status

> **This is a demonstration prototype with simulated data.**
>
> All features use realistic dummy data to illustrate the platform's vision. This prototype is designed to demonstrate SANA's complete vision to investors, stakeholders, and partners. It does not connect to real APIs, databases, or external services.

---

## What is SANA?

SANA bridges the gap between alternative medicine and evidence-based healthcare by:

1. **Creating Accountability**: Practitioners can't just claim effectiveness - their outcomes are measured
2. **Building Evidence**: Automatically collecting research-grade data to prove CAM works
3. **Integrating with Healthcare**: NHS referrals, insurance integration, corporate wellness
4. **Empowering Patients**: Giving people data about their health and tools to improve it

## Platform Overview

### For Patients/Clients
- **Health Graph**: 360-degree wellness visualization across 6 dimensions
- **AI Journal (SIRM)**: Therapeutic journaling with 4 AI personas
- **Practitioner Matching**: Find verified practitioners with proven outcomes
- **Wearable Integration**: Connect Apple Health, Oura Ring, and more

### For Practitioners
- **SANA Index**: Outcome-weighted quality score (0-100)
- **Evidence Dashboard**: Track outcomes, benchmark against peers
- **Practice Management**: Appointments, client management, analytics

### For Institutions & Enterprises
- **NHS Social Prescribing**: Bi-directional referrals with ROI tracking
- **Corporate Wellness**: Employee wellbeing programs with business impact metrics
- **Research Portal**: FHIR/REDCap export, GDPR-compliant data access

---

## Repository Structure

```
sana-proto/
├── backend/                    # FastAPI Python backend
│   ├── api/routes/            # 23 API route modules (350+ endpoints)
│   ├── database/              # SQLAlchemy ORM models
│   └── main.py                # Application entry point
│
├── sana_vision_prototype/      # Flutter mobile app
│   ├── lib/screens/           # 9 UI screens
│   ├── lib/widgets/           # Reusable components
│   ├── lib/services/          # API services
│   └── lib/models/            # Data models & mock data
│
└── docs/                       # Documentation
    ├── ALGORITHMS.md          # Algorithm specifications
    └── DEMO_GUIDE.md          # Investor demo walkthrough
```

---

## Core Algorithms

| Algorithm | Purpose |
|-----------|---------|
| **SISM** | Holistic health scoring across 6 wellness domains |
| **SANA Index** | Outcome-weighted practitioner credibility (Credentials 20%, Volume 20%, Outcomes 40%, Data Quality 10%, Satisfaction 10%) |
| **SIRM** | AI therapeutic journaling with 4 personas |
| **SPRM** | Intelligent practitioner-patient matching |
| **SOU** | Thompson Sampling for treatment optimization |
| **SST** | Crisis detection and safety monitoring |

See [docs/ALGORITHMS.md](docs/ALGORITHMS.md) for detailed specifications.

---

## Quick Start

### Prerequisites
- Flutter 3.0+ (for mobile app)
- Python 3.9+ (for backend)

### Running the Flutter App

```bash
cd sana_vision_prototype
flutter pub get
flutter run
```

### Running the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

API documentation available at: `http://localhost:8000/docs`

---

## Technology Stack

### Frontend
- **Flutter** - Cross-platform mobile framework
- **Material Design 3** - Modern UI components
- **fl_chart** - Data visualization

### Backend
- **FastAPI** - Modern async Python framework
- **SQLAlchemy 2.0** - ORM with async support
- **Pydantic v2** - Data validation

### Infrastructure (Production)
- PostgreSQL database
- JWT authentication
- Stripe payments integration

---

## Demo Data

All data is simulated to demonstrate the platform's potential:

| Metric | Demo Value | Purpose |
|--------|------------|---------|
| Client health score journey | 50 → 78 | Shows 12-month improvement |
| Average improvement rate | 44% | Across treatment conditions |
| Practitioner SANA Index | 87/100 | Demonstrates top performer |
| NHS cost savings | £124,000 | Shows enterprise ROI |
| Research data points | 12,450+ | Illustrates evidence generation |

---

## Documentation

- [Algorithm Specifications](docs/ALGORITHMS.md) - Technical details of all algorithms
- [Demo Guide](docs/DEMO_GUIDE.md) - Step-by-step investor demo walkthrough
- [Flutter App README](sana_vision_prototype/README.md) - Feature documentation
- [Getting Started](sana_vision_prototype/GETTING_STARTED.md) - Setup instructions

---

## License

Proprietary - SANA Health Platform

---

*Built to showcase the future of integrated, evidence-based healthcare*
