import os
import smtplib
from email.message import EmailMessage


def send_validation_failure_email(result):
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_to = os.getenv("EMAIL_TO", smtp_user)

    if not smtp_user or not smtp_password or not email_to:
        print("Email notification skipped: SMTP configuration is missing")
        return False

    msg = EmailMessage()

    msg["Subject"] = "AI Performance Validation Failed"
    msg["From"] = smtp_user
    msg["To"] = email_to

    msg.set_content(
        f"""AI Performance Validation Alert

Validation Status: {result["validation_status"]}
Risk Level: {result["risk_level"]}

Current Value: {result["current_value"]}
Z-Score: {result["z_score"]}

Message:
{result["message"]}

The performance validation has detected a deviation from the established baseline.
"""
    )

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print("Validation failure email sent successfully")
        return True

    except Exception as e:
        print(f"Failed to send validation failure email: {e}")
        return False
