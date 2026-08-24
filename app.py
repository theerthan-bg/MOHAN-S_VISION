"""RiskLens — Flask Application.
Super App for Unified Multi-Asset Investing and Awareness."""

import json
import random
import time
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from datetime import datetime

from engine.health_score import compute_health_score, IDEAL_ALLOCATIONS
from engine.fraud_check import check_entity, get_recent_scam_alerts, get_search_suggestions
from engine.goal_tracker import compute_all_goals
from data.portfolio import (
    user_profile, equities, mutual_funds, bonds, gold, nps,
    reits_invits, compute_holdings,
)
from data.goals import financial_goals
from data.verified_content import verified_content, content_categories
from auth import (
    init_db, register_user, authenticate_user, get_current_user,
    login_required, link_account, get_linked_accounts,
)

app = Flask(__name__)
app.secret_key = "risklens-super-secret-key-change-in-production-2024"

# Initialize the database on startup
init_db()


def format_inr(val):
    """Format a number as Indian Rupee string."""
    if val >= 10_000_000:
        return f"₹{val / 10_000_000:.2f} Cr"
    if val >= 100_000:
        return f"₹{val / 100_000:.2f} L"
    return f"₹{val:,.0f}"


def get_time_of_day():
    hour = datetime.now().hour
    if hour < 12:
        return "morning", "सुबह"
    elif hour < 17:
        return "afternoon", "दोपहर"
    return "evening", "शाम"


# ── Jinja2 filters ──
app.jinja_env.filters["format_inr"] = format_inr
app.jinja_env.globals["now"] = datetime.now


# ── Auth routes ──

@app.route("/login", methods=["GET", "POST"])
def login():
    mode = request.args.get("mode", "login")
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        mode = request.form.get("mode", "login")
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if mode == "signup":
            name = request.form.get("name", "").strip()
            phone = request.form.get("phone", "").strip()

            if not name or not email or not password:
                flash("Please fill in all required fields.", "error")
                return redirect(url_for("login"))

            # Register immediately — no email verification
            success, result = register_user(name, email, phone, None, password)
            if success:
                session["user_id"] = result
                session["user_name"] = name
                flash(f"Welcome to Mohan's Vision, {name}! 🎉", "success")
                return redirect(url_for("dashboard"))
            else:
                flash(result, "error")
                return redirect(url_for("login"))
        else:
            # Login mode
            if not email or not password:
                flash("Please enter your email and password.", "error")
                return redirect(url_for("login"))

            success, result = authenticate_user(email, password)
            if success:
                session["user_id"] = result["id"]
                session["user_name"] = result["name"]
                return redirect(url_for("dashboard"))
            else:
                flash(result, "error")
                return redirect(url_for("login"))

    return render_template("login.html",mode=mode)


@app.route("/logout")
def logout():
    session.clear()
    flash("You've been logged out.", "success")
    return redirect(url_for("login"))




# ── Page routes ──

@app.route("/")
def onboarding():
    return render_template("onboarding.html")


@app.route("/dashboard")
@login_required
def dashboard():
    health_data = compute_health_score()
    goal_data = compute_all_goals(financial_goals)
    tod_en, tod_hi = get_time_of_day()
    user = get_current_user()
    display_name = user["name"].split()[0] if user else "User"
    return render_template(
        "dashboard.html",
        health=health_data,
        goals=goal_data,
        user=user_profile,
        tod_en=tod_en,
        tod_hi=tod_hi,
        format_inr=format_inr,
        display_name=display_name,
    )


@app.route("/portfolio")
@login_required
def portfolio():
    holdings = compute_holdings()
    return render_template(
        "portfolio.html",
        holdings=holdings,
        equities=equities,
        mutual_funds=mutual_funds,
        bonds=bonds,
        gold=[g for g in gold if not g["exclude_from_total"]],
        nps=nps,
        reits_invits=reits_invits,
        format_inr=format_inr,
    )


@app.route("/score")
@login_required
def health_score():
    health_data = compute_health_score()
    return render_template(
        "health_score.html",
        health=health_data,
        format_inr=format_inr,
    )


@app.route("/shield")
@login_required
def fraud_shield():
    recent_alerts = get_recent_scam_alerts(6)
    return render_template(
        "fraud_shield.html",
        recent_alerts=recent_alerts,
    )


@app.route("/voices")
@login_required
def verified_voices():
    return render_template(
        "verified_voices.html",
        content=verified_content,
        categories=content_categories,
    )


@app.route("/goals")
@login_required
def goals():
    goal_data = compute_all_goals(financial_goals)
    total_target = sum(g["target_amount"] for g in goal_data)
    total_current = sum(g["current_amount"] for g in goal_data)
    on_track_count = sum(1 for g in goal_data if g["on_track"])
    return render_template(
        "goals.html",
        goals=goal_data,
        total_target=total_target,
        total_current=total_current,
        overall_pct=round((total_current / total_target) * 100, 1) if total_target else 0,
        on_track_count=on_track_count,
        format_inr=format_inr,
    )


@app.route("/settings")
@login_required
def settings():
    user = get_current_user()
    linked_accounts = get_linked_accounts(user["id"])
    return render_template("settings.html", user=user, linked_accounts=linked_accounts)

@app.route("/settings/update", methods=["POST"])
@login_required
def settings_update():
    user = get_current_user()
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    risk_profile = request.form.get("risk_profile", "Moderate").strip()
    
    if not name:
        flash("Name is required.", "error")
        return redirect(url_for("settings"))
        
    from auth import update_user
    success, message = update_user(user["id"], name, phone, risk_profile)
    if success:
        flash(message, "success")
        # Update session name just in case
        session["user_name"] = name
    else:
        flash(message, "error")
        
    return redirect(url_for("settings"))


# ── API endpoints ──

@app.route("/api/fraud-check", methods=["POST"])
def api_fraud_check():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "")
    result = check_entity(query)
    return jsonify(result)


@app.route("/api/suggestions")
def api_suggestions():
    query = request.args.get("q", "")
    suggestions = get_search_suggestions(query)
    return jsonify(suggestions)


@app.route("/api/health-score")
def api_health_score():
    return jsonify(compute_health_score())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
