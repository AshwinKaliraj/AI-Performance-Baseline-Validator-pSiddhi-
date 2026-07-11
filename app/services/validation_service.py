import statistics

from app.services import history_service

from app.utils.prometheus_metrics import VALIDATION_STATUS


def validate_performance(current_value):

    historical_response_times = history_service.get_history()

    moving_average = statistics.mean(historical_response_times)

    standard_deviation = statistics.stdev(historical_response_times)

    if standard_deviation == 0:
        z_score = 0
    else:
        z_score = round((current_value - moving_average) / standard_deviation, 2)

    if abs(z_score) < 2:
        risk_level = "Low"
        validation_status = "Pass"
        message = "Performance is within the acceptable baseline."

    elif abs(z_score) < 3:
        risk_level = "Medium"
        validation_status = "Warning"
        message = "Performance is slightly deviating from the baseline."

    elif abs(z_score) < 4:
        risk_level = "High"
        validation_status = "Fail"
        message = "Performance exceeds the acceptable threshold."

    else:
        risk_level = "Critical"
        validation_status = "Fail"
        message = "Critical performance anomaly detected."

    # Update Prometheus Metric
    if validation_status == "Pass":
        VALIDATION_STATUS.set(1)
    else:
        VALIDATION_STATUS.set(0)

    return {

        "current_value": current_value,

        "z_score": z_score,

        "risk_level": risk_level,

        "validation_status": validation_status,

        "message": message

    }