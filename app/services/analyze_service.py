from app.services import gemini_service
from app.services import groq_service
from app.services import baseline_service
from app.services import anomaly_service
from app.services import risk_service
from app.services import validation_service
from app.services import ai_summary_service

from app.utils.prometheus_metrics import (
    BASELINE_MOVING_AVERAGE,
    BASELINE_STANDARD_DEVIATION,
    ANOMALY_Z_SCORE,
    RISK_SCORE,
    VALIDATION_STATUS
)


def analyze(current_value):

    # -----------------------------
    # Calculate AI Metrics
    # -----------------------------

    baseline = baseline_service.calculate_baseline()

    anomaly = anomaly_service.detect_anomaly(current_value)

    risk = risk_service.calculate_risk(current_value)

    validation = validation_service.validate_performance(current_value)

    # -----------------------------
    # Update Prometheus Metrics
    # -----------------------------

    BASELINE_MOVING_AVERAGE.set(
        baseline["moving_average"]
    )

    BASELINE_STANDARD_DEVIATION.set(
        baseline["standard_deviation"]
    )

    ANOMALY_Z_SCORE.set(
        anomaly["z_score"]
    )

    RISK_SCORE.set(
        risk["risk_score"]
    )

    VALIDATION_STATUS.set(
        1 if validation["validation_status"] == "Pass" else 0
    )

    # -----------------------------
    # Generate AI Explanations
    # -----------------------------

    try:
        gemini_explanation = gemini_service.generate_explanation(
            baseline,
            anomaly,
            risk,
            validation
        )
    except Exception as e:
        gemini_explanation = f"Gemini Error: {str(e)}"

    try:
        groq_explanation = groq_service.generate_explanation(
            baseline,
            anomaly,
            risk,
            validation
        )
    except Exception as e:
        groq_explanation = f"Groq Error: {str(e)}"

    # -----------------------------
    # Save Latest AI Analysis
    # -----------------------------

    ai_summary_service.update(
        gemini_explanation,
        groq_explanation
    )

    # -----------------------------
    # Recommendation
    # -----------------------------

    recommendation = generate_recommendation(
        risk["risk_level"]
    )

    return {

        "baseline": baseline,

        "anomaly": anomaly,

        "risk": risk,

        "validation": validation,

        "recommendation": recommendation,

        "gemini_explanation": gemini_explanation,

        "groq_explanation": groq_explanation

    }


def generate_recommendation(risk_level):

    if risk_level == "Low":

        return {

            "action": "System is healthy. Continue monitoring."

        }

    elif risk_level == "Medium":

        return {

            "action": "Monitor performance closely."

        }

    elif risk_level == "High":

        return {

            "action": "Investigate response time and resource utilization."

        }

    else:

        return {

            "action": "Immediate investigation required. Critical anomaly detected."

        }