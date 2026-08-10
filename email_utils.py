"""Email utility — sends OTP via Gmail SMTP."""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load from environment (set in .env or system environment variables)
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_otp_email(recipient_email: str, otp_code: str, user_name: str = "User") -> tuple[bool, str]:
    """Send an OTP email to the recipient.

    Args:
        recipient_email: The destination email address.
        otp_code: The 6-digit OTP string to send.
        user_name: The recipient's display name.

    Returns:
        (success: bool, message: str)
    """
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        return False, (
            "Email credentials not configured. "
            "Set MAIL_USERNAME and MAIL_PASSWORD in your .env file."
        )

    subject = "Your Mohan's Vision OTP Code"

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #0f172a; color: #e2e8f0; padding: 40px;">
      <div style="max-width: 480px; margin: 0 auto; background: #1e293b;
                  border-radius: 16px; padding: 36px; border: 1px solid #334155;">
        <h2 style="color: #6366f1; margin-top: 0;">Mohan's Vision 🔐</h2>
        <p>Hello <strong>{user_name}</strong>,</p>
        <p>Your one-time password (OTP) for account verification is:</p>
        <div style="text-align: center; margin: 28px 0;">
          <span style="font-size: 40px; font-weight: bold; letter-spacing: 12px;
                       color: #6366f1; background: #0f172a; padding: 16px 24px;
                       border-radius: 12px; display: inline-block;">{otp_code}</span>
        </div>
        <p style="color: #94a3b8; font-size: 14px;">
          ⏱️ This OTP is valid for <strong>10 minutes</strong>.<br>
          Do not share this code with anyone.
        </p>
        <hr style="border-color: #334155; margin: 24px 0;">
        <p style="color: #64748b; font-size: 12px; margin: 0;">
          If you did not request this OTP, please ignore this email.
        </p>
      </div>
    </body>
    </html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Mohan's Vision <{MAIL_USERNAME}>"
        msg["To"] = recipient_email

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_USERNAME, recipient_email, msg.as_string())

        return True, f"OTP sent successfully to {recipient_email}"

    except smtplib.SMTPAuthenticationError:
        return False, (
            "Gmail authentication failed. "
            "Make sure you're using an App Password, not your regular Gmail password. "
            "Generate one at: https://myaccount.google.com/apppasswords"
        )
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {e}"
    except Exception as e:
        return False, f"Failed to send email: {e}"
