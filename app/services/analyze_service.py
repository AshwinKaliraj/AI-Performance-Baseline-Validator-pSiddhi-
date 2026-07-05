from app.services import baseline_service
from app.services import anomaly_service
from app.services import risk_service
from app.services import validation_service


def analyze(current_value):

    baseline=baseline_service.calculate_baseline()

    anomaly=anomaly_service.detect_anomaly(current_value)

    risk=risk_service.calculate_risk(current_value)

    validation=validation_service.validate_performance(current_value)

    recommendation=generate_recommendation(risk["risk_level"])


    return{

        "baseline":baseline,

        "anomaly":anomaly,

        "risk":risk,

        "validation":validation,

        "recommendation":recommendation

    }


def generate_recommendation(risk_level):

    if risk_level=="Low":

        return{

            "action":"System is healthy. Continue monitoring."

        }

    elif risk_level=="Medium":

        return{

            "action":"Monitor performance closely."

        }

    elif risk_level=="High":

        return{

            "action":"Investigate response time and resource utilization."

        }

    else:

        return{

            "action":"Immediate investigation required. Critical anomaly detected."

        }