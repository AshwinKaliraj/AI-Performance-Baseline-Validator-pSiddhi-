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


def calculate_baseline():

    current_value=104

    moving_average=round(statistics.mean(historical_response_times),2)

    standard_deviation=round(statistics.stdev(historical_response_times),2)

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