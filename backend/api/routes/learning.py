"""
SANA Learning Routes - SOU (SANA Outcome Uplift)
Reinforcement learning with Thompson Sampling for outcome optimization
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import random
import math

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class OutcomeMetrics(BaseModel):
    total_treatments: int
    positive_outcomes: int
    negative_outcomes: int
    average_improvement: float
    confidence_interval: tuple


class InterventionPerformance(BaseModel):
    intervention_id: str
    intervention_name: str
    condition: str
    alpha: float  # Beta distribution parameter (successes + 1)
    beta: float   # Beta distribution parameter (failures + 1)
    expected_success_rate: float
    sample_count: int
    thompson_sample: float
    rank: int


class PredictionResponse(BaseModel):
    user_id: str
    condition: str
    top_recommendations: List[Dict]
    confidence: float
    model_version: str


# ============================================================================
# MOCK DATA - Thompson Sampling Parameters
# ============================================================================

# Beta distribution parameters for each intervention-condition pair
# alpha = successes + 1, beta = failures + 1
INTERVENTION_PRIORS = {
    ("acupuncture", "anxiety"): {"alpha": 156, "beta": 44, "name": "Acupuncture"},
    ("acupuncture", "chronic_pain"): {"alpha": 189, "beta": 56, "name": "Acupuncture"},
    ("mbsr", "anxiety"): {"alpha": 178, "beta": 52, "name": "MBSR"},
    ("mbsr", "stress"): {"alpha": 201, "beta": 49, "name": "MBSR"},
    ("cbt", "anxiety"): {"alpha": 234, "beta": 41, "name": "CBT"},
    ("cbt", "depression"): {"alpha": 198, "beta": 52, "name": "CBT"},
    ("ashwagandha", "anxiety"): {"alpha": 89, "beta": 36, "name": "Ashwagandha"},
    ("ashwagandha", "stress"): {"alpha": 95, "beta": 30, "name": "Ashwagandha"},
    ("yoga", "anxiety"): {"alpha": 145, "beta": 55, "name": "Yoga"},
    ("yoga", "chronic_pain"): {"alpha": 112, "beta": 48, "name": "Yoga"},
    ("massage", "chronic_pain"): {"alpha": 167, "beta": 58, "name": "Massage Therapy"},
    ("massage", "stress"): {"alpha": 134, "beta": 46, "name": "Massage Therapy"},
    ("valerian", "insomnia"): {"alpha": 78, "beta": 42, "name": "Valerian Root"},
    ("melatonin", "insomnia"): {"alpha": 123, "beta": 47, "name": "Melatonin"},
}


def thompson_sample(alpha: float, beta: float) -> float:
    """Sample from Beta distribution for Thompson Sampling"""
    return random.betavariate(alpha, beta)


def expected_value(alpha: float, beta: float) -> float:
    """Calculate expected success rate from Beta distribution"""
    return alpha / (alpha + beta)


# ============================================================================
# ROUTES
# ============================================================================

@router.get("/metrics")
async def get_learning_metrics():
    """
    Get overall learning system metrics

    **SOU (SANA Outcome Uplift) System:**
    - Uses Thompson Sampling for intervention selection
    - Continuously learns from treatment outcomes
    - Balances exploration vs exploitation
    - Updates posteriors with each outcome
    """
    total_treatments = sum(p["alpha"] + p["beta"] - 2 for p in INTERVENTION_PRIORS.values())
    total_successes = sum(p["alpha"] - 1 for p in INTERVENTION_PRIORS.values())

    return {
        "model_version": "SOU-2.1",
        "algorithm": "Thompson Sampling with Beta-Bernoulli",
        "total_outcomes_recorded": total_treatments,
        "overall_success_rate": round(total_successes / total_treatments, 3),
        "interventions_tracked": len(set(k[0] for k in INTERVENTION_PRIORS.keys())),
        "conditions_tracked": len(set(k[1] for k in INTERVENTION_PRIORS.keys())),
        "last_model_update": datetime.utcnow().isoformat(),
        "exploration_rate": 0.15  # Epsilon for exploration
    }


@router.get("/predict-outcome")
async def predict_outcome(
    condition: str,
    intervention: Optional[str] = None,
    user_id: Optional[str] = None
):
    """
    Predict outcome probability for intervention-condition pair

    Uses posterior Beta distributions to estimate success probability
    with confidence intervals
    """
    if intervention:
        key = (intervention.lower(), condition.lower())
        if key not in INTERVENTION_PRIORS:
            raise HTTPException(status_code=404, detail="Intervention-condition pair not found")

        params = INTERVENTION_PRIORS[key]
        alpha, beta = params["alpha"], params["beta"]
        expected = expected_value(alpha, beta)

        # Calculate 95% credible interval (simplified)
        ci_lower = expected - 0.1
        ci_upper = min(expected + 0.1, 1.0)

        return {
            "intervention": intervention,
            "condition": condition,
            "predicted_success_rate": round(expected, 3),
            "confidence_interval": [round(ci_lower, 3), round(ci_upper, 3)],
            "sample_size": alpha + beta - 2,
            "confidence": "high" if alpha + beta > 100 else "medium"
        }
    else:
        # Return top interventions for condition
        matching = {k: v for k, v in INTERVENTION_PRIORS.items() if k[1] == condition.lower()}
        if not matching:
            raise HTTPException(status_code=404, detail=f"No data for condition: {condition}")

        results = []
        for (interv, cond), params in matching.items():
            expected = expected_value(params["alpha"], params["beta"])
            results.append({
                "intervention": params["name"],
                "predicted_success_rate": round(expected, 3),
                "sample_size": params["alpha"] + params["beta"] - 2
            })

        results.sort(key=lambda x: x["predicted_success_rate"], reverse=True)

        return {
            "condition": condition,
            "top_interventions": results[:5]
        }


@router.get("/top-performers")
async def get_top_performers(
    condition: Optional[str] = None,
    limit: int = Query(default=10, le=50)
):
    """
    Get top performing interventions using Thompson Sampling

    Ranks interventions by sampling from posterior distributions,
    balancing exploitation of known good options with exploration
    """
    results = []

    for (intervention, cond), params in INTERVENTION_PRIORS.items():
        if condition and cond != condition.lower():
            continue

        sample = thompson_sample(params["alpha"], params["beta"])
        expected = expected_value(params["alpha"], params["beta"])

        results.append(InterventionPerformance(
            intervention_id=intervention,
            intervention_name=params["name"],
            condition=cond,
            alpha=params["alpha"],
            beta=params["beta"],
            expected_success_rate=round(expected, 3),
            sample_count=params["alpha"] + params["beta"] - 2,
            thompson_sample=round(sample, 3),
            rank=0
        ))

    # Rank by Thompson sample (for exploration-exploitation balance)
    results.sort(key=lambda x: x.thompson_sample, reverse=True)
    for i, r in enumerate(results):
        r.rank = i + 1

    return {
        "algorithm": "Thompson Sampling",
        "condition_filter": condition,
        "results": results[:limit],
        "note": "Rankings use Thompson Sampling for exploration-exploitation balance"
    }


@router.post("/record-outcome")
async def record_outcome(
    intervention: str,
    condition: str,
    outcome: str,  # success, failure, partial
    user_id: str,
    practitioner_id: Optional[str] = None,
    outcome_score: Optional[float] = None
):
    """
    Record treatment outcome to update learning model

    Updates Beta distribution parameters:
    - Success: alpha += 1
    - Failure: beta += 1

    This enables continuous learning from real-world outcomes
    """
    key = (intervention.lower(), condition.lower())

    if key in INTERVENTION_PRIORS:
        if outcome == "success":
            INTERVENTION_PRIORS[key]["alpha"] += 1
        elif outcome == "failure":
            INTERVENTION_PRIORS[key]["beta"] += 1
        # Partial outcomes could increment both slightly

    return {
        "recorded": True,
        "intervention": intervention,
        "condition": condition,
        "outcome": outcome,
        "new_expected_rate": round(expected_value(
            INTERVENTION_PRIORS.get(key, {"alpha": 1, "beta": 1})["alpha"],
            INTERVENTION_PRIORS.get(key, {"alpha": 1, "beta": 1})["beta"]
        ), 3),
        "message": "Outcome recorded and model updated"
    }


@router.get("/exploration-recommendations")
async def get_exploration_recommendations(
    user_id: str,
    condition: str
):
    """
    Get recommendations that balance exploration and exploitation

    Uses Upper Confidence Bound (UCB) style bonus for under-explored
    interventions to encourage data collection
    """
    matching = {k: v for k, v in INTERVENTION_PRIORS.items() if k[1] == condition.lower()}

    recommendations = []
    for (interv, cond), params in matching.items():
        expected = expected_value(params["alpha"], params["beta"])
        sample_count = params["alpha"] + params["beta"] - 2

        # UCB-style exploration bonus
        exploration_bonus = math.sqrt(2 * math.log(1000) / max(sample_count, 1))
        ucb_score = expected + 0.1 * exploration_bonus

        recommendations.append({
            "intervention": params["name"],
            "expected_success": round(expected, 3),
            "exploration_score": round(ucb_score, 3),
            "data_confidence": "high" if sample_count > 100 else "needs_more_data",
            "reason": "Under-explored but promising" if exploration_bonus > 0.1 else "Well-established efficacy"
        })

    recommendations.sort(key=lambda x: x["exploration_score"], reverse=True)

    return {
        "user_id": user_id,
        "condition": condition,
        "recommendations": recommendations[:5],
        "strategy": "UCB-Thompson hybrid for optimal learning"
    }
