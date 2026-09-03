from app.services import metrics_service


def reset_metrics():
    metrics_service.request_count = 0
    metrics_service.error_count = 0
    metrics_service.success_count = 0
    metrics_service.response_times = []


def test_increment_request_count():
    reset_metrics()

    metrics_service.increment_request_count()
    metrics_service.increment_request_count()

    assert metrics_service.request_count == 2


def test_increment_error_count():
    reset_metrics()

    metrics_service.increment_error_count()

    assert metrics_service.error_count == 1


def test_increment_success_count():
    reset_metrics()

    metrics_service.increment_success_count()
    metrics_service.increment_success_count()

    assert metrics_service.success_count == 2


def test_record_response_time():
    reset_metrics()

    metrics_service.record_response_time(100)
    metrics_service.record_response_time(150)

    assert metrics_service.response_times == [100, 150]


def test_average_response_time_empty():
    reset_metrics()

    assert metrics_service.get_average_response_time() == 0


def test_average_response_time():
    reset_metrics()

    metrics_service.record_response_time(100)
    metrics_service.record_response_time(150)
    metrics_service.record_response_time(125)

    assert metrics_service.get_average_response_time() == 125


def test_min_response_time_empty():
    reset_metrics()

    assert metrics_service.get_min_response_time() == 0


def test_min_response_time():
    reset_metrics()

    metrics_service.record_response_time(100)
    metrics_service.record_response_time(50)
    metrics_service.record_response_time(150)

    assert metrics_service.get_min_response_time() == 50


def test_max_response_time_empty():
    reset_metrics()

    assert metrics_service.get_max_response_time() == 0


def test_max_response_time():
    reset_metrics()

    metrics_service.record_response_time(100)
    metrics_service.record_response_time(50)
    metrics_service.record_response_time(150)

    assert metrics_service.get_max_response_time() == 150


def test_success_rate_zero_requests():
    reset_metrics()

    assert metrics_service.get_success_rate() == 0


def test_success_rate():
    reset_metrics()

    metrics_service.request_count = 10
    metrics_service.success_count = 8

    assert metrics_service.get_success_rate() == 80


def test_throughput_zero_uptime(monkeypatch):
    reset_metrics()

    monkeypatch.setattr(
        metrics_service.time,
        "time",
        lambda: metrics_service.application_start_time
    )

    assert metrics_service.get_throughput() == 0


def test_throughput():
    reset_metrics()

    metrics_service.request_count = 100

    monkeypatch_time = (
        metrics_service.application_start_time + 10
    )

    monkeypatch = None

    original_time = metrics_service.time.time

    try:
        metrics_service.time.time = lambda: monkeypatch_time
        assert metrics_service.get_throughput() == 10
    finally:
        metrics_service.time.time = original_time


def test_cpu_usage(monkeypatch):
    monkeypatch.setattr(
        metrics_service.psutil,
        "cpu_percent",
        lambda interval: 25.5
    )

    assert metrics_service.get_cpu_usage() == 25.5


def test_memory_usage(monkeypatch):
    class Memory:
        percent = 60.5

    monkeypatch.setattr(
        metrics_service.psutil,
        "virtual_memory",
        lambda: Memory()
    )

    assert metrics_service.get_memory_usage() == 60.5


def test_get_metrics(monkeypatch):
    reset_metrics()

    metrics_service.request_count = 10
    metrics_service.success_count = 8
    metrics_service.error_count = 2
    metrics_service.response_times = [
        100,
        150,
        200
    ]

    monkeypatch.setattr(
        metrics_service.psutil,
        "cpu_percent",
        lambda interval: 20
    )

    class Memory:
        percent = 50

    monkeypatch.setattr(
        metrics_service.psutil,
        "virtual_memory",
        lambda: Memory()
    )

    monkeypatch.setattr(
        metrics_service,
        "get_throughput",
        lambda: 2.5
    )

    result = metrics_service.get_metrics()

    assert result["request_count"] == 10
    assert result["success_count"] == 8
    assert result["error_count"] == 2
    assert result["success_rate"] == 80
    assert result["average_response_time_ms"] == 150
    assert result["min_response_time_ms"] == 100
    assert result["max_response_time_ms"] == 200
    assert result["throughput_requests_per_second"] == 2.5
    assert result["cpu_usage_percent"] == 20
    assert result["memory_usage_percent"] == 50