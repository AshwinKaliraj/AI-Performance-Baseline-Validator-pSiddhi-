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


def validate_performance(current_value):

    moving_average=statistics.mean(historical_response_times)

    standard_deviation=statistics.stdev(historical_response_times)

    z_score=round((current_value-moving_average)/standard_deviation,2)

    if abs(z_score)<2:
        risk_level="Low"
        validation_status="Pass"
        message="Performance is within the acceptable baseline."

    elif abs(z_score)<3:
        risk_level="Medium"
        validation_status="Warning"
        message="Performance is slightly deviating from the baseline."

    elif abs(z_score)<4:
        risk_level="High"
        validation_status="Fail"
        message="Performance exceeds the acceptable threshold."

    else:
        risk_level="Critical"
        validation_status="Fail"
        message="Critical performance anomaly detected."

    return{
        "current_value":current_value,
        "z_score":z_score,
        "risk_level":risk_level,
        "validation_status":validation_status,
        "message":message
    }