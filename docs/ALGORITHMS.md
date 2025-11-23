# SANA Platform Algorithms

This document provides an overview of the core algorithms powering the SANA Health Platform.

## Algorithm Summary

| Algorithm | Name | Purpose | Status |
|-----------|------|---------|--------|
| **SISM** | SANA Integrative Scoring Model | Holistic health scoring across 6 wellness domains | Prototype |
| **SANA Index** | Practitioner Quality Score | Outcome-weighted practitioner credibility scoring | Prototype |
| **SIRM** | SANA Insight & Reflection Model | AI-powered therapeutic journaling with 4 personas | Prototype |
| **SPRM** | SANA Practitioner Recommendation Model | Intelligent practitioner-patient matching | Prototype |
| **SOU** | SANA Outcome Uplift | Thompson Sampling for treatment optimization | Prototype |
| **SST** | SANA Safety & Triage | Crisis detection and safety monitoring | Prototype |
| **Health Graph** | Evidence Engine | CAM intervention knowledge base | Prototype |

---

## 1. SISM - SANA Integrative Scoring Model

**Purpose:** Calculate holistic health scores across multiple wellness dimensions.

### Domains & Weights

| Domain | Weight | Description | Data Sources |
|--------|--------|-------------|--------------|
| Physical Health | 20% | Body function, fitness, nutrition | Wearables, questionnaire |
| Mental Wellbeing | 20% | Cognitive function, clarity, focus | Questionnaire, journal |
| Emotional Balance | 20% | Mood regulation, stress response | Journal, questionnaire |
| Social Connection | 15% | Relationships, community, support | Questionnaire |
| Sleep Quality | 15% | Rest, recovery, circadian rhythm | Wearables, questionnaire |
| Energy Levels | 10% | Vitality, stamina, motivation | Wearables, journal |

### Score Calculation

```
Overall Score = SUM(Domain Score * Domain Weight)
```

### Status Classification

| Score Range | Status |
|-------------|--------|
| 80-100 | Thriving |
| 65-79 | Good |
| 50-64 | Fair |
| 0-49 | Needs Attention |

### Features
- Biological age estimation based on biomarkers
- Top 3 improvement levers identification
- 12-month historical tracking
- Multi-source data integration

**Implementation:** `backend/api/routes/scoring.py`

---

## 2. SANA Index - Practitioner Quality Score

**Purpose:** Provide an outcome-weighted credibility score for CAM practitioners.

### Components & Weights

| Component | Weight | Max Points | Description |
|-----------|--------|------------|-------------|
| Credentials | 20% | 20 | Education, licenses, certifications |
| Volume | 20% | 20 | Treatment volume and experience |
| **Outcomes** | **40%** | **40** | Measured client health improvements |
| Data Completeness | 10% | 10 | Profile and data quality |
| Client Satisfaction | 10% | 10 | Ratings and reviews |

### Key Innovation

The SANA Index is **outcome-weighted**, meaning 40% of a practitioner's score comes from actual measured health improvements in their clients. This differentiates it from typical review-based ratings.

### Outcome Measurement
- Uses validated PROMs: WHO-5, DASS-21, VAS
- Condition-specific benchmarks
- Minimum sample size requirements for reliability
- Comparison to platform averages

### Badges
- **Top 10%**: Practitioners in 90th percentile
- **Rising Star**: Upward trending practitioners above 70th percentile
- **New Practitioner**: Recently onboarded, building track record

**Implementation:** `backend/api/routes/index.py`

---

## 3. SIRM - SANA Insight & Reflection Model

**Purpose:** AI-powered therapeutic journaling with multiple therapeutic personas.

### Available Personas

| Persona | Style | Approach |
|---------|-------|----------|
| Compassionate Therapist | Empathetic, supportive | Validation and grounding techniques |
| Wise Philosopher | Thought-provoking, profound | Stoic wisdom and perspective shifts |
| Creative Poet | Metaphorical, artistic | Creative reframing and expression |
| Evidence-Based Coach | Practical, research-backed | Data-driven recommendations |

### Features
- Context-aware responses connected to wellness data
- Mood tracking and sentiment analysis
- Tag-based journal organization
- Historical pattern recognition

**Implementation:** `sana_vision_prototype/lib/screens/journal_screen.dart`, `sana_vision_prototype/lib/models/dummy_data.dart`

---

## 4. SPRM - SANA Practitioner Recommendation Model

**Purpose:** Match users with the most suitable practitioners based on needs and preferences.

### Match Score Components

| Factor | Weight | Description |
|--------|--------|-------------|
| Specialty Alignment | 30% | Condition-practitioner specialty match |
| SANA Index | 25% | Practitioner quality score |
| User Reviews | 20% | Client satisfaction ratings |
| Availability | 15% | Scheduling convenience |
| Price Fit | 10% | Budget alignment |

### Matching Process
1. Filter by user conditions and preferences
2. Calculate composite match score
3. Generate personalized match reasons
4. Rank and return top matches

**Implementation:** `backend/api/routes/matching.py`

---

## 5. SOU - SANA Outcome Uplift

**Purpose:** Use reinforcement learning to optimize treatment recommendations over time.

### Algorithm: Thompson Sampling with Beta-Bernoulli

```
For each intervention-condition pair:
- Track successes (alpha) and failures (beta)
- Sample from Beta(alpha, beta) distribution
- Select intervention with highest sample
- Update posteriors based on outcomes
```

### Features
- Balances exploration vs exploitation
- Continuous learning from treatment outcomes
- UCB-style exploration bonus for under-explored interventions
- Condition-specific intervention rankings

**Implementation:** `backend/api/routes/learning.py`

---

## 6. SST - SANA Safety & Triage

**Purpose:** Detect health crises and provide appropriate safety responses.

### Risk Levels

| Level | Trigger | Action |
|-------|---------|--------|
| Critical | Self-harm risk, medical emergency | Escalate to emergency services |
| High | Mental health crisis, severe symptoms | Connect to crisis support |
| Moderate | Concerning patterns | Suggest professional help |
| Low | Minor concerns | Provide resources |
| Safe | No concerns detected | Continue normal operation |

### Detection Methods
- NLP analysis for crisis indicators
- Keyword and pattern matching
- Wearable data anomaly detection
- Herb-drug interaction checking

**Implementation:** `backend/api/routes/safety.py`

---

## 7. Health Graph - Evidence Engine

**Purpose:** Knowledge base of evidence-based CAM interventions.

### Evidence Levels

| Level | Criteria |
|-------|----------|
| Strong | Multiple RCTs, meta-analysis available |
| Moderate | Some RCTs, consistent findings |
| Limited | Few studies, preliminary evidence |
| Emerging | Case studies, traditional use |

### Data Points
- Effect sizes (Cohen's d)
- Study counts
- Safety ratings
- ICD-10 condition mapping
- Contraindications

**Implementation:** `backend/api/routes/evidence.py`

---

## Prototype Notes

**All algorithms in this prototype use simulated data and simplified implementations.**

In production, these would include:
- Real machine learning models trained on outcome data
- Integration with validated assessment instruments
- HIPAA/GDPR-compliant data pipelines
- External data source integrations (wearables, EHRs)
- Continuous model retraining and validation

---

*Last updated: November 2024*
