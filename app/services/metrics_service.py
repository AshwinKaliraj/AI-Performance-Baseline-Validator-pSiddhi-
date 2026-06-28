import time
import psutil

request_count=0
error_count=0
success_count=0

response_times=[]

application_start_time=time.time()


def increment_request_count():
    global request_count
    request_count+=1


def increment_error_count():
    global error_count
    error_count+=1


def increment_success_count():
    global success_count
    success_count+=1


def record_response_time(response_time):
    response_times.append(response_time)


def get_average_response_time():

    if not response_times:
        return 0

    return round(sum(response_times)/len(response_times),2)


def get_min_response_time():

    if not response_times:
        return 0

    return round(min(response_times),2)


def get_max_response_time():

    if not response_times:
        return 0

    return round(max(response_times),2)


def get_success_rate():

    if request_count==0:
        return 0

    return round((success_count/request_count)*100,2)


def get_throughput():

    uptime=time.time()-application_start_time

    if uptime==0:
        return 0

    return round(request_count/uptime,2)


def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)


def get_memory_usage():
    return psutil.virtual_memory().percent


def get_metrics():

    return{

        "request_count":request_count,

        "success_count":success_count,

        "error_count":error_count,

        "success_rate":get_success_rate(),

        "average_response_time_ms":get_average_response_time(),

        "min_response_time_ms":get_min_response_time(),

        "max_response_time_ms":get_max_response_time(),

        "throughput_requests_per_second":get_throughput(),

        "cpu_usage_percent":get_cpu_usage(),

        "memory_usage_percent":get_memory_usage()

    }