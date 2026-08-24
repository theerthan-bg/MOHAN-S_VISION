"""Health Score Engine — computes a portfolio health score (0–100)."""

from data.portfolio import (
    user_profile, equities, mutual_funds, bonds, gold, nps,
    reits_invits, compute_holdings,
)

# Ideal allocation percentages by asset class (for a Moderate risk profile)
IDEAL_ALLOCATIONS = {
    "equities": 40,
    "mutual_funds": 25,
    "bonds": 15,
    "gold": 10,
    "nps": 5,
    "reits_invits": 5,
}


def _deviation_score(actual_pct: float, ideal_pct: float) -> float:
    """Return a 0–100 score based on deviation from ideal allocation."""
    deviation = abs(actual_pct - ideal_pct)
    # Every 1% deviation costs 2 points, floored at 0
    return max(0.0, 100.0 - deviation * 2)


def compute_health_score() -> dict:
    """Compute the overall portfolio health score and per-asset breakdown."""
    holdings = compute_holdings()
    total = holdings.get("total", 1) or 1  # avoid division by zero

    breakdown = []
    weighted_score = 0.0
    total_ideal_weight = sum(IDEAL_ALLOCATIONS.values())

    asset_map = {
        "equities": holdings.get("equities_total", 0),
        "mutual_funds": holdings.get("mutual_funds_total", 0),
        "bonds": holdings.get("bonds_total", 0),
        "gold": holdings.get("gold_total", 0),
        "nps": holdings.get("nps_total", 0),
        "reits_invits": holdings.get("reits_invits_total", 0),
    }

    label_map = {
        "equities": "Equities",
        "mutual_funds": "Mutual Funds",
        "bonds": "Bonds / Debt",
        "gold": "Gold",
        "nps": "NPS",
        "reits_invits": "REITs / InvITs",
    }

    for key, ideal_pct in IDEAL_ALLOCATIONS.items():
        value = asset_map.get(key, 0)
        actual_pct = round((value / total) * 100, 1)
        score = _deviation_score(actual_pct, ideal_pct)
        weighted_score += score * (ideal_pct / total_ideal_weight)
        breakdown.append(
            {
                "asset": label_map[key],
                "key": key,
                "value": value,
                "actual_pct": actual_pct,
                "ideal_pct": ideal_pct,
                "score": round(score, 1),
            }
        )

    overall = round(weighted_score, 1)

    # Grade
    if overall >= 85:
        grade, grade_label = "A", "Excellent"
    elif overall >= 70:
        grade, grade_label = "B", "Good"
    elif overall >= 55:
        grade, grade_label = "C", "Average"
    elif overall >= 40:
        grade, grade_label = "D", "Below Average"
    else:
        grade, grade_label = "F", "Poor"

    return {
        "score": overall,
        "grade": grade,
        "grade_label": grade_label,
        "total_value": total,
        "breakdown": breakdown,
    }
