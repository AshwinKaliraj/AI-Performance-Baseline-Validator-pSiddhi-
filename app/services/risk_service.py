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


def calculate_risk(current_value):

    moving_average=statistics.mean(historical_response_times)

    standard_deviation=statistics.stdev(historical_response_times)

    z_score=round((current_value-moving_average)/standard_deviation,2)

    if abs(z_score)<2:
        risk_score=20
        risk_level="Low"

    elif abs(z_score)<3:
        risk_score=60
        risk_level="Medium"

    elif abs(z_score)<4:
        risk_score=85
        risk_level="High"

    else:
        risk_score=100
        risk_level="Critical"

    return{
        "current_value":current_value,
        "moving_average":round(moving_average,2),
        "standard_deviation":round(standard_deviation,2),
        "z_score":z_score,
        "risk_score":risk_score,
        "risk_level":risk_level
    }