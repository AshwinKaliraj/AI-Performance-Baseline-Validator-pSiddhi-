import statistics

historical_response_times=[
    100,
    110,
    98,
    95,
    102,
    105,
    108,
    97,
    99,
    101
]


def detect_anomaly(current_value):

    moving_average=statistics.mean(historical_response_times)

    standard_deviation=statistics.stdev(historical_response_times)

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