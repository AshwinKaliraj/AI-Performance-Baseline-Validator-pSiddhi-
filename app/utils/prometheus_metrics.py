from prometheus_client import Counter, Histogram, Gauge

# -----------------------------
# HTTP Metrics
# -----------------------------

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ["method", "endpoint"]
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP Errors",
    ["method", "endpoint"]
)

# -----------------------------
# AI Performance Metrics
# -----------------------------

BASELINE_MOVING_AVERAGE = Gauge(
    "baseline_moving_average",
    "Current Moving Average Baseline"
)

BASELINE_STANDARD_DEVIATION = Gauge(
    "baseline_standard_deviation",
    "Current Baseline Standard Deviation"
)

ANOMALY_Z_SCORE = Gauge(
    "anomaly_z_score",
    "Current Z Score"
)

RISK_SCORE = Gauge(
    "risk_score",
    "Current Risk Score"
)

VALIDATION_STATUS = Gauge(
    "validation_status",
    "Validation Status (1=Pass, 0=Fail)"
)