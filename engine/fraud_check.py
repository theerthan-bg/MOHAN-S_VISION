"""Fraud / Scam Shield Engine — entity verification and scam alerts."""

import re
from datetime import datetime, timedelta

# ── Hardcoded known-scam / known-safe entity database ──────────────────────

KNOWN_SCAMS = [
    {
        "name": "Growfast Investments",
        "type": "Fake Investment Scheme",
        "risk": "HIGH",
        "description": "Promises 40% monthly returns. Unregistered with SEBI.",
        "reported_date": "2024-11-15",
        "victims": 3200,
    },
    {
        "name": "CryptoWealth Pro",
        "type": "Crypto Ponzi",
        "risk": "HIGH",
        "description": "Fake crypto trading platform collecting deposits and vanishing.",
        "reported_date": "2024-12-02",
        "victims": 8700,
    },
    {
        "name": "Sure Returns Ltd",
        "type": "Chit Fund Fraud",
        "risk": "HIGH",
        "description": "Unregistered chit fund collecting money with no returns.",
        "reported_date": "2025-01-10",
        "victims": 1500,
    },
    {
        "name": "QuickLoan Express",
        "type": "Loan App Scam",
        "risk": "HIGH",
        "description": "Charges upfront 'processing fees' then blocks the user.",
        "reported_date": "2025-02-20",
        "victims": 5600,
    },
    {
        "name": "NRI Investment Club",
        "type": "Impersonation Fraud",
        "risk": "HIGH",
        "description": "Impersonates SEBI-registered advisors to collect funds.",
        "reported_date": "2025-03-05",
        "victims": 900,
    },
    {
        "name": "FD Doubler Scheme",
        "type": "Fake FD Scheme",
        "risk": "HIGH",
        "description": "Advertises guaranteed FD doubling in 12 months.",
        "reported_date": "2025-03-18",
        "victims": 2100,
    },
]

KNOWN_SAFE = [
    {"name": "SBI", "full_name": "State Bank of India", "sebi_reg": "INB010002437", "type": "Bank"},
    {"name": "HDFC Bank", "full_name": "HDFC Bank Limited", "sebi_reg": "INB040002412", "type": "Bank"},
    {"name": "ICICI Bank", "full_name": "ICICI Bank Limited", "sebi_reg": "INB010002434", "type": "Bank"},
    {"name": "Zerodha", "full_name": "Zerodha Broking Limited", "sebi_reg": "INZ000031633", "type": "Broker"},
    {"name": "Groww", "full_name": "Groww (Nextbillion Technology)", "sebi_reg": "INZ000208032", "type": "Broker"},
    {"name": "ICICI Prudential", "full_name": "ICICI Prudential AMC", "sebi_reg": "INP000000327", "type": "AMC"},
    {"name": "HDFC Mutual Fund", "full_name": "HDFC AMC Limited", "sebi_reg": "INP000001289", "type": "AMC"},
    {"name": "Axis Bank", "full_name": "Axis Bank Limited", "sebi_reg": "INB010002427", "type": "Bank"},
    {"name": "NSE", "full_name": "National Stock Exchange of India", "sebi_reg": "INB230339133", "type": "Exchange"},
    {"name": "BSE", "full_name": "Bombay Stock Exchange", "sebi_reg": "INB011072918", "type": "Exchange"},
]

RECENT_SCAM_ALERTS = [
    {
        "title": "Fake SEBI SMS Scam",
        "description": "Fraudsters are sending SMS claiming to be SEBI and asking users to click links to 'update KYC'.",
        "risk_level": "HIGH",
        "date": "2025-06-10",
        "category": "Phishing",
    },
    {
        "title": "WhatsApp Investment Group Scam",
        "description": "Fake investment WhatsApp groups promising daily returns on stock tips. Never join unsolicited groups.",
        "risk_level": "HIGH",
        "date": "2025-06-05",
        "category": "Social Media Fraud",
    },
    {
        "title": "Telegram 'Trading Bot' Fraud",
        "description": "Bots on Telegram claiming to automate trading with 'guaranteed' 20% weekly returns.",
        "risk_level": "HIGH",
        "date": "2025-05-28",
        "category": "Crypto / Bot Scam",
    },
    {
        "title": "Fake IPO Application Scam",
        "description": "Fraudulent websites mimicking real IPO portals to collect bank credentials.",
        "risk_level": "MEDIUM",
        "date": "2025-05-20",
        "category": "IPO Fraud",
    },
    {
        "title": "Loan App Harassment",
        "description": "Illegal loan apps charging 3x interest and harassing contacts. Only use RBI-registered lenders.",
        "risk_level": "HIGH",
        "date": "2025-05-15",
        "category": "Loan Fraud",
    },
    {
        "title": "Fake Mutual Fund Advisor",
        "description": "Individuals claiming to be AMFI-registered advisors without valid ARN numbers.",
        "risk_level": "MEDIUM",
        "date": "2025-05-08",
        "category": "Investment Fraud",
    },
]


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


def check_entity(query: str) -> dict:
    """Check if an entity is a known scam or a verified safe entity."""
    if not query or not query.strip():
        return {"status": "error", "message": "Please enter an entity name to check."}

    q = _normalize(query)

    # Check against scams
    for scam in KNOWN_SCAMS:
        if q in _normalize(scam["name"]) or _normalize(scam["name"]) in q:
            return {
                "status": "danger",
                "verdict": "⚠️ SCAM DETECTED",
                "entity": scam["name"],
                "risk": scam["risk"],
                "type": scam["type"],
                "description": scam["description"],
                "reported_date": scam["reported_date"],
                "victims": scam["victims"],
                "message": f"'{query}' is a known scam. Do NOT invest or share personal details.",
            }

    # Check against safe entities
    for safe in KNOWN_SAFE:
        if q in _normalize(safe["name"]) or _normalize(safe["name"]) in q:
            return {
                "status": "safe",
                "verdict": "✅ VERIFIED & SAFE",
                "entity": safe["full_name"],
                "sebi_reg": safe["sebi_reg"],
                "type": safe["type"],
                "message": f"'{safe['full_name']}' is a SEBI/RBI-registered entity. Safe to proceed.",
            }

    # Unknown entity
    return {
        "status": "unknown",
        "verdict": "🔍 NOT FOUND IN DATABASE",
        "entity": query,
        "message": (
            f"'{query}' was not found in our database. "
            "Always verify on SEBI's official website (sebi.gov.in) before investing."
        ),
        "tips": [
            "Check SEBI registration at sebi.gov.in",
            "Verify broker on NSE/BSE website",
            "Never invest based on unsolicited tips",
            "Check RBI approved lender list for loan apps",
        ],
    }


def get_recent_scam_alerts(limit: int = 6) -> list:
    """Return the most recent scam alerts."""
    return RECENT_SCAM_ALERTS[:limit]


def get_search_suggestions(query: str) -> list:
    """Return autocomplete suggestions for entity names."""
    if not query or len(query) < 2:
        return []
    q = _normalize(query)
    suggestions = []
    for entity in KNOWN_SAFE:
        if q in _normalize(entity["name"]):
            suggestions.append({"name": entity["full_name"], "type": entity["type"], "status": "safe"})
    for scam in KNOWN_SCAMS:
        if q in _normalize(scam["name"]):
            suggestions.append({"name": scam["name"], "type": scam["type"], "status": "danger"})
    return suggestions[:8]
