from prometheus_client import Counter, Histogram

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

users_registered_total = Counter(
    'users_registered_total',
    'Total users registered',
    ['role'],
)

vacantes_llenas_total = Counter(
    'vacantes_llenas_total',
    'Total vacantes that reached full capacity',
)
