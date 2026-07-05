import statistics

from app.services import history_service


def detect_anomaly(current_value):

    historical_response_times=history_service.get_history()

    moving_average=statistics.mean(historical_response_times)

    standard_deviation=statistics.stdev(historical_response_times)

    if standard_deviation==0:
        z_score=0
    else:
        z_score=round((current_value-moving_average)/standard_deviation,2)

    if abs(z_score)<2:
        status="Normal"

    elif abs(z_score)<3:
        status="Warning"

    else:
        status="Anomaly"

    return{

        "current_value":current_value,

        "moving_average":round(moving_average,2),

        "standard_deviation":round(standard_deviation,2),

        "z_score":z_score,

        "status":status

    }