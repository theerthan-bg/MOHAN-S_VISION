"""Mohan's Vision Authentication Module — SQLite-backed user management."""

import sqlite3
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect, url_for, request

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def get_db():
    """Get a database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            pan TEXT,
            password_hash TEXT NOT NULL,
            risk_profile TEXT DEFAULT 'Moderate',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS linked_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_type TEXT NOT NULL,
            details TEXT NOT NULL,
            linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def register_user(name, email, phone, pan, password):
    """Register a new user. Returns (success, message)."""
    conn = get_db()
    cursor = conn.cursor()

    try:
        # Check if email already exists
        existing = cursor.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            conn.close()
            return False, "An account with this email already exists."

        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, email, phone, pan, password_hash) VALUES (?, ?, ?, ?, ?)",
            (name, email, phone, pan, password_hash),
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id
    except Exception as e:
        conn.close()
        return False, str(e)


def authenticate_user(email, password):
    """Authenticate a user. Returns (success, user_dict or error_message)."""
    conn = get_db()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if not user:
        return False, "No account found with this email."

    if not check_password_hash(user["password_hash"], password):
        return False, "Incorrect password."

    return True, dict(user)


def get_current_user():
    """Get the current logged-in user from session."""
    user_id = session.get("user_id")
    if not user_id:
        return None

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    return dict(user) if user else None


def login_required(f):
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function
def update_user(user_id, name, phone, risk_profile, pan=None):
    """Update a user's profile details. Returns (success, message)."""
    conn = get_db()
    cursor = conn.cursor()

    try:
        if pan is not None:
            cursor.execute(
                "UPDATE users SET name = ?, phone = ?, risk_profile = ?, pan = ? WHERE id = ?",
                (name, phone, risk_profile, pan, user_id),
            )
        else:
            cursor.execute(
                "UPDATE users SET name = ?, phone = ?, risk_profile = ? WHERE id = ?",
                (name, phone, risk_profile, user_id),
            )
        conn.commit()
        conn.close()
        return True, "Profile updated successfully."
    except Exception as e:
        conn.close()
        return False, str(e)


def link_account(user_id, account_type, details_json):
    """Link a financial account to a user. Returns (success, message)."""
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO linked_accounts (user_id, account_type, details) VALUES (?, ?, ?)",
            (user_id, account_type, details_json),
        )
        conn.commit()
        conn.close()
        return True, "Account linked successfully."
    except Exception as e:
        conn.close()
        return False, str(e)


def get_linked_accounts(user_id):
    """Get all linked accounts for a user."""
    conn = get_db()
    accounts = conn.execute(
        "SELECT * FROM linked_accounts WHERE user_id = ? ORDER BY linked_at DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(a) for a in accounts]
