performance_history=[
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


def add_history(response_time):

    performance_history.append(response_time)

    return{
        "message":"Performance sample stored successfully."
    }


def get_history():

    return performance_history