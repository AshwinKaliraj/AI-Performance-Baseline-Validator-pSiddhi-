import statistics

from app.services import history_service


def calculate_baseline():

    historical_response_times=history_service.get_history()

    current_value=historical_response_times[-1]

    moving_average=round(statistics.mean(historical_response_times),2)

    standard_deviation=round(statistics.stdev(historical_response_times),2)

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

        "moving_average":moving_average,

        "standard_deviation":standard_deviation,

        "current_value":current_value,

        "z_score":z_score,

        "status":status

    }