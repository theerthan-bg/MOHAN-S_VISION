"""Goal Tracker Engine — computes progress for each financial goal."""

from datetime import date


def _months_between(start: date, end: date) -> float:
    """Return approximate months between two dates."""
    return max(1, (end.year - start.year) * 12 + (end.month - start.month))


def compute_goal(goal: dict) -> dict:
    """Enrich a single goal dict with computed progress fields."""
    today = date.today()
    target_date = goal.get("target_date")
    target_amount = goal.get("target_amount", 0)
    current_amount = goal.get("current_amount", 0)
    monthly_sip = goal.get("monthly_sip", 0)

    # Progress percentage
    progress_pct = round((current_amount / target_amount) * 100, 1) if target_amount else 0
    progress_pct = min(progress_pct, 100.0)

    # Months remaining
    if isinstance(target_date, date):
        months_left = _months_between(today, target_date)
        days_left = (target_date - today).days
    else:
        months_left = 0
        days_left = 0

    # Amount still needed
    amount_needed = max(0, target_amount - current_amount)

    # Required monthly SIP to reach goal (simple linear projection)
    required_sip = round(amount_needed / months_left, 0) if months_left > 0 else 0

    # On track check: will current SIP cover the shortfall?
    projected_total = current_amount + (monthly_sip * months_left)
    on_track = projected_total >= target_amount

    return {
        **goal,
        "progress_pct": progress_pct,
        "amount_needed": amount_needed,
        "months_left": int(months_left),
        "days_left": days_left,
        "required_sip": required_sip,
        "projected_total": round(projected_total, 0),
        "on_track": on_track,
    }


def compute_all_goals(goals: list) -> list:
    """Compute progress for all goals and return enriched list."""
    return [compute_goal(g) for g in goals]
