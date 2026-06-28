import time
from app.services import metrics_service

users=[
    {
        "id":1,
        "name":"Ashwin",
        "role":"Admin"
    },
    {
        "id":2,
        "name":"Virat",
        "role":"User"
    },
    {
        "id":3,
        "name":"Dhoni",
        "role":"Manager"
    }
]


def get_all_users():

    start_time=time.perf_counter()

    metrics_service.increment_request_count()
    time.sleep(0.2)
    metrics_service.increment_success_count()

    result=users

    response_time=(time.perf_counter()-start_time)*1000

    metrics_service.record_response_time(response_time)

    return result


def get_user_by_id(user_id:int):

    start_time=time.perf_counter()

    metrics_service.increment_request_count()
    time.sleep(0.2)

    for user in users:

        if user["id"]==user_id:

            response_time=(time.perf_counter()-start_time)*1000

            metrics_service.record_response_time(response_time)
            metrics_service.increment_success_count()

            return user

    metrics_service.increment_error_count()

    response_time=(time.perf_counter()-start_time)*1000

    metrics_service.record_response_time(response_time)

    return {"message":"User not found"}