# RiskLens (OneVest)

**A unified multi-asset investment super-app for the Indian retail investor** — combining portfolio health scoring, fraud detection, financial goal tracking, and verified financial content, all in a bilingual (English + Hindi) interface.

> 🏆 Built for the **SEBI Securities Market TechSprint**

---

## 📌 Overview

Indian retail investors typically have their money scattered across demat, mutual fund, NPS, gold, and REIT accounts with no single score to measure portfolio health or risk alignment. At the same time, investment fraud through unregistered advisors and Ponzi schemes is rising, fueled by FOMO-driven, social-media-influenced trading behaviour — with no structured, goal-based investing to counter it.

**RiskLens** is the SEBI-aware "health check" for your investments — combining portfolio analytics, fraud protection, and goal planning in one bilingual app.

| Metric | Value |
|---|---|
| Asset Classes Tracked | 6 |
| Max Health Score | 900 |
| Health Score Signals | 4 |
| Fraud Check Sources | 3 |
| Risk Profiles | 3 |
| Languages Supported | 2 (English & Hindi) |

---

## ✨ Core Features

### 🏠 Dashboard (`/dashboard`)
- Personalised greeting with time-of-day awareness (morning/afternoon/evening), in English & Hindi
- Portfolio total value with Indian number formatting (Lakhs/Crores)
- Financial Health Score at a glance
- Goal progress summary cards
- Quick-access navigation to all modules

### 📊 Portfolio (`/portfolio`)
Multi-asset portfolio view covering **6 asset classes**:

| Asset Class | Examples | Key Data Fields |
|---|---|---|
| Equities | RELIANCE, INFY, TCS | symbol, quantity, avg_buy_price, current_price, sector |
| Mutual Funds | Mirae, Parag Parikh | name, invested, current_value, units, nav |
| Bonds | SGB, Govt Securities | name, type, face_value, coupon_rate, maturity |
| Gold | SGB, Digital Gold | name, grams, buy_price, current_price |
| NPS | NPS Tier I & II | tier, corpus, equity_pct, debt_pct |
| REITs/InvITs | Embassy, PowerGrid InvIT | name, units, buy_price, current_price |

### 🛡️ Fraud Shield (`/shield`)
- Real-time autocomplete search
- Checks against SEBI-registered intermediaries, scam alerts, and known finfluencers
- Colour-coded results: ✅ Verified / ⚠️ Warning / 🚨 Critical Scam
- Recent Scam Alerts feed (sorted by date)
- Pre-populated "try searching" chips for demos

### 🎯 Goals (`/goals`)
- Multiple financial goals (retirement, education, home, travel, etc.)
- SIP-based projection to determine if each goal is on-track
- Required SIP calculator for off-track goals
- Intelligent nudges in English & Hindi
- Summary stats: total target, total saved, overall % funded, on-track count

### 📰 Verified Voices (`/voices`)
Curated content from SEBI-registered advisors and trusted financial educators, filterable by category.

### 👤 Auth & Settings (`/login`, `/settings`)
- Register with name, email, phone, PAN, and password
- Password hashing via Werkzeug's PBKDF2
- Profile updates (name, phone, risk profile)
- Link external financial accounts (broker, bank, etc.)

---

## 🧮 Financial Health Score Engine

`engine/health_score.py` computes a composite **0–900 score** from four independently weighted signals:

| Signal | Weight | Description |
|---|---|---|
| Diversification | 30% | Portfolio allocation vs. ideal allocation for risk profile |
| Concentration Risk | 25% | Stock/sector over-exposure |
| Advisor Trust | 20% | Use of SEBI-registered advisors |
| Behavioural Risk | 25% | Churn, panic-selling, FOMO trades |

```python
composite = (
    diversification_score * 0.30 +
    concentration_score   * 0.25 +
    advisor_trust_score   * 0.20 +
    behavioural_score     * 0.25
) * 9   # Scale 0-100 → 0-900
```

**Score Bands**

| Range | Band | Meaning |
|---|---|---|
| 750–900 | Excellent | Well-managed, diversified, disciplined investor |
| 550–749 | Good | Generally sound, minor areas to improve |
| 350–549 | Needs Attention | Noticeable risks — review recommended |
| 0–349 | At Risk | Significant issues — immediate action needed |

---

## 🛡️ Fraud Shield Engine

`engine/fraud_check.py` checks any name, firm, or registration number against three data sources using a custom fuzzy-matching algorithm.

**Data Sources**
1. SEBI Registered Intermediaries — brokers, RIAs, RAs, stock exchanges
2. Scam Alerts — SEBI-issued warnings and known Ponzi/fraudulent schemes
3. Known Finfluencers — unregistered social media financial advice givers

**Decision Priority:** `Scam Match? → SEBI Registered? → Finfluencer? → Not Found`
Scam matches are always surfaced first, regardless of other matches.

| Status | Risk Level | Meaning |
|---|---|---|
| VERIFIED | Safe | SEBI-registered and active |
| SUSPENDED | Warning | Registered, but suspended/expired |
| FINFLUENCER | Warning | Known social media personality, not SEBI-registered |
| SCAM_ALERT | Critical | Matches a known SEBI scam advisory |
| NOT_FOUND | Unknown | Not found in any database — exercise caution |

---

## 🎯 Goal Tracker Engine

`engine/goal_tracker.py` projects whether each financial goal will be met, using SIP future-value math with compound interest, and generates bilingual nudges (`SUCCESS`, `ON_TRACK`, `INCREASE_SIP`, `AT_RISK`).

---

## 🏗️ System Architecture

MVC-like architecture with clear layer separation:

```
Browser Request → Flask Route (app.py) → Engine / Auth Module →
Data Layer → Jinja2 Template → HTML Response
```

| Layer | Components |
|---|---|
| Presentation | Jinja2 templates, CSS design system, Vanilla JS, Lucide Icons |
| Business Logic | `app.py`, `engine/health_score.py`, `engine/fraud_check.py`, `engine/goal_tracker.py`, `auth.py` |
| Data | `data/portfolio.py`, `data/goals.py`, `data/sebi_registry.py`, `data/verified_content.py`, `users.db` |

**Key Design Decisions**
- **No ORM** — direct `sqlite3` queries for simplicity and minimal dependencies
- **Static data files** — portfolio, SEBI registry, and goals data live in Python files (simulating a DB); easily swappable for a real DB
- **Custom Jinja2 filter** — `format_inr` for Indian number formatting (Lakhs/Crores)
- **Bilingual** — `.lang-en` / `.lang-hi` CSS classes toggled via JS
- **Session-based auth** — Flask's signed cookie sessions, no JWT

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python / Flask 3.0 | Web framework, routing, business logic |
| Templating | Jinja2 | Server-side HTML rendering |
| Frontend | Vanilla JS + CSS Variables | Dynamic UI, dark mode, bilingual toggle |
| Icons | Lucide Icons | SVG icon library |
| Database | SQLite3 | User accounts & linked financial accounts |
| Auth | Werkzeug + Flask sessions | Password hashing & cookie-based auth |
| Deployment | Render + Gunicorn | Production WSGI server |
| Env Secrets | python-dotenv | Load environment variables from `.env` |

---

## 📂 File Structure

```
onevest/
├── app.py                  # Main Flask app — routes & app factory
├── auth.py                 # Authentication: register, login, sessions
├── email_utils.py          # Email helper (OTP / transactional)
├── generate_docs.py        # Auto-generates documentation
├── requirements.txt        # flask, gunicorn, python-dotenv
├── render.yaml              # Render.com deployment config
├── users.db                 # SQLite database (auto-created)
├── .env                      # Secret keys & environment variables
│
├── engine/                  # Core business logic engines
│   ├── __init__.py
│   ├── health_score.py     # Financial Health Score (0-900)
│   ├── fraud_check.py      # SEBI registry fraud/scam checker
│   └── goal_tracker.py     # SIP-based goal projection & nudges
│
├── data/                     # Static data (simulates database tables)
│   ├── portfolio.py         # Equities, MFs, bonds, gold, NPS, REITs
│   ├── goals.py              # Financial goals definitions
│   ├── sebi_registry.py     # SEBI intermediaries, scam alerts, finfluencers
│   └── verified_content.py  # Curated verified financial content
│
├── templates/                # Jinja2 HTML templates
│   ├── app_shell.html       # Base shell — nav, bottom-bar, JS imports
│   ├── base.html             # Minimal base for login/onboarding
│   ├── login.html            # Login + Register page
│   ├── onboarding.html      # First-time user onboarding
│   ├── dashboard.html       # Main dashboard
│   ├── portfolio.html       # Multi-asset portfolio view
│   ├── health_score.html    # Health score breakdown
│   ├── fraud_shield.html    # Fraud check tool
│   ├── goals.html            # Goal tracker
│   ├── verified_voices.html # Educational content
│   ├── settings.html        # User profile settings
│   ├── connect_accounts.html# Link broker/bank accounts
│   ├── verify_otp.html      # OTP verification
│   └── partials/             # Reusable template fragments
│
└── static/                   # CSS, JS, and image assets
```

---

## 🔌 Routes & API Endpoints

### Page Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | Landing / onboarding screen |
| GET | `/login` | Login + register page |
| GET | `/logout` | Clears session and redirects to login |
| GET | `/dashboard` | Main dashboard with health & goals |
| GET | `/portfolio` | Multi-asset portfolio detail |
| GET | `/score` | Detailed health score breakdown |
| GET | `/shield` | Fraud check tool |
| GET | `/voices` | Verified content feed |
| GET | `/goals` | Goal tracker |
| GET | `/settings` | User profile & linked accounts |
| POST | `/settings/update` | Update user profile |

### API Endpoints (JSON)

| Method | Endpoint | Request | Response |
|---|---|---|---|
| POST | `/api/fraud-check` | `{"query": "name"}` | Fraud check result: status, risk_level, message, matches |
| GET | `/api/suggestions?q=` | URL param `q` | Array of up to 8 suggestion objects |
| GET | `/api/health-score` | None | Full health score object with all signals |

---

## 🗄️ Database Design

**Table: `users`**

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique user identifier |
| name | TEXT | NOT NULL | Full name |
| email | TEXT | UNIQUE NOT NULL | Login identifier |
| phone | TEXT | — | Mobile number (optional) |
| pan | TEXT | — | PAN card number (optional) |
| password_hash | TEXT | NOT NULL | PBKDF2 hashed password |
| risk_profile | TEXT | DEFAULT 'Moderate' | Conservative / Moderate / Aggressive |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation time |

**Table: `linked_accounts`**

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Record ID |
| user_id | INTEGER | NOT NULL, FK → users(id) | Owner user |
| account_type | TEXT | NOT NULL | e.g., "Zerodha", "HDFC Bank" |
| details | TEXT | NOT NULL | JSON string with account details |
| linked_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When account was linked |

> Portfolio data, financial goals, the SEBI registry, and verified content are stored as Python data structures in `data/`. These serve as a mock database and can be replaced with real database calls or API integration in production.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# Install dependencies
pip install -r requirements.txt

# Run the Flask development server
python app.py
```

The app will be available at `http://localhost:5000`.

> 💡 `init_db()` runs on every startup and creates SQLite tables automatically — no separate migration step needed.

### Dependencies

| Package | Purpose |
|---|---|
| flask==3.0 | Web framework |
| gunicorn | Production WSGI server |
| python-dotenv | Loads `.env` file for local development secrets |

---

## ☁️ Deployment

Deployed on **Render** using Gunicorn.

`render.yaml`:
```yaml
services:
  - type: web
    name: risklens
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: FLASK_ENV
        value: production
```

> ⚠️ **Production Note:** `app.secret_key` in `app.py` uses a placeholder value for local development. In production this must be replaced with a strong random key stored as an environment variable.

---

## 🌐 Bilingual Support

```html
<span class="lang-en">Financial Health Score</span>
<span class="lang-hi" style="display:none">वित्तीय स्वास्थ्य स्कोर</span>
```

A JS toggle switches visibility between `.lang-en` / `.lang-hi` classes across the entire app.

---

## 📖 Glossary

| Term | Definition |
|---|---|
| SEBI | Securities and Exchange Board of India — capital markets regulator |
| RIA | Registered Investment Adviser |
| RA | Research Analyst — SEBI-registered publisher of research reports |
| SIP | Systematic Investment Plan |
| NPS | National Pension System |
| REIT | Real Estate Investment Trust |
| InvIT | Infrastructure Investment Trust |
| SGB | Sovereign Gold Bond |
| PAN | Permanent Account Number |
| Churn Rate | Proportion of portfolio replaced through buying/selling |
| FOMO | Fear Of Missing Out — impulsive buying driven by hype |
| Finfluencer | Social media financial influencer without SEBI registration |

---

## 👥 Team

| Role | Name |
|---|---|
| Team Leader | *Mohan Gowda BR* |
| Team Managed  | *Theerthan BG* |

---

## 📄 License

This project was built for the **SEBI Securities Market TechSprint** hackathon. *(Add a license, e.g. MIT, if applicable.)*
