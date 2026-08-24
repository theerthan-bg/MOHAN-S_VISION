"""Portfolio data — sample multi-asset portfolio for Mohan's Vision."""

# ── User profile ────────────────────────────────────────────────────────────

user_profile = {
    "name": "Mohan Gowda",
    "age": 28,
    "risk_profile": "Moderate",
    "pan": "ABCPG1234D",
    "total_invested": 1_850_000,
    "annual_income": 1_200_000,
}

# ── Asset classes ────────────────────────────────────────────────────────────

equities = [
    {"name": "Reliance Industries", "ticker": "RELIANCE", "qty": 20, "avg_price": 2400, "ltp": 2980, "sector": "Energy"},
    {"name": "HDFC Bank", "ticker": "HDFCBANK", "qty": 30, "avg_price": 1550, "ltp": 1720, "sector": "Banking"},
    {"name": "Infosys", "ticker": "INFY", "qty": 25, "avg_price": 1380, "ltp": 1510, "sector": "IT"},
    {"name": "TCS", "ticker": "TCS", "qty": 10, "avg_price": 3600, "ltp": 4100, "sector": "IT"},
    {"name": "ITC Ltd", "ticker": "ITC", "qty": 100, "avg_price": 380, "ltp": 460, "sector": "FMCG"},
    {"name": "Maruti Suzuki", "ticker": "MARUTI", "qty": 5, "avg_price": 9800, "ltp": 11200, "sector": "Auto"},
]

mutual_funds = [
    {"name": "Axis Bluechip Fund", "folio": "AXB12345", "units": 500, "nav": 62.40, "invested": 25_000, "type": "Equity"},
    {"name": "HDFC Mid-Cap Opportunities", "folio": "HDM67890", "units": 300, "nav": 128.75, "invested": 30_000, "type": "Equity"},
    {"name": "SBI Debt Fund", "folio": "SBD11223", "units": 1000, "nav": 34.20, "invested": 30_000, "type": "Debt"},
    {"name": "Mirae Asset Emerging Bluechip", "folio": "MAE44556", "units": 200, "nav": 105.60, "invested": 18_000, "type": "Equity"},
    {"name": "ICICI Pru Balanced Advantage", "folio": "ICB77889", "units": 800, "nav": 52.30, "invested": 35_000, "type": "Hybrid"},
]

bonds = [
    {"name": "GOI 2030 Bond", "isin": "IN0020230015", "face_value": 100_000, "coupon": 7.26, "maturity": "2030-06-15", "units": 2},
    {"name": "HDFC Bank NCD", "isin": "INE001A0801", "face_value": 10_000, "coupon": 8.10, "maturity": "2027-03-31", "units": 5},
    {"name": "REC Ltd Bond", "isin": "INE020B0152", "face_value": 10_000, "coupon": 7.74, "maturity": "2028-09-20", "units": 10},
]

gold = [
    {"name": "Sovereign Gold Bond 2023-I", "type": "SGB", "units": 10, "issue_price": 5923, "ltp": 7100, "exclude_from_total": False},
    {"name": "Digital Gold (Groww)", "type": "Digital", "grams": 15.5, "buy_price_per_gram": 5600, "ltp_per_gram": 7050, "exclude_from_total": False},
    {"name": "Gold ETF — NIPPON", "type": "ETF", "units": 20, "avg_price": 52.30, "ltp": 64.80, "exclude_from_total": False},
]

nps = [
    {"name": "NPS — Tier I (SBI Pension Fund)", "account": "PRAN1234567890", "balance": 95_000, "monthly_contribution": 3_000, "scheme": "Moderate LC-50"},
]

reits_invits = [
    {"name": "Embassy Office Parks REIT", "ticker": "EMBASSY", "units": 50, "avg_price": 320, "ltp": 380, "type": "REIT"},
    {"name": "IndiGrid InvIT", "ticker": "INDIGRID", "units": 100, "avg_price": 135, "ltp": 158, "type": "InvIT"},
]


# ── Compute totals ────────────────────────────────────────────────────────────

def compute_holdings() -> dict:
    """Compute current market value totals across all asset classes."""

    equities_total = sum(s["qty"] * s["ltp"] for s in equities)

    mf_total = sum(f["units"] * f["nav"] for f in mutual_funds)

    # Bond value ≈ face value × units (simplified; no mark-to-market)
    bonds_total = sum(b["face_value"] * b["units"] for b in bonds)

    gold_total = 0
    for g in gold:
        if g.get("exclude_from_total"):
            continue
        if g["type"] == "SGB":
            gold_total += g["units"] * g["ltp"]
        elif g["type"] == "Digital":
            gold_total += g["grams"] * g["ltp_per_gram"]
        elif g["type"] == "ETF":
            gold_total += g["units"] * g["ltp"]

    nps_total = sum(n["balance"] for n in nps)

    reits_invits_total = sum(r["units"] * r["ltp"] for r in reits_invits)

    total = equities_total + mf_total + bonds_total + gold_total + nps_total + reits_invits_total

    return {
        "equities_total": round(equities_total, 2),
        "mutual_funds_total": round(mf_total, 2),
        "bonds_total": round(bonds_total, 2),
        "gold_total": round(gold_total, 2),
        "nps_total": round(nps_total, 2),
        "reits_invits_total": round(reits_invits_total, 2),
        "total": round(total, 2),
    }
