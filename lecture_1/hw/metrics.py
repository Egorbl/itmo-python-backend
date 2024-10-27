from prometheus_client import Counter, Histogram

# Счётчик для количества вызовов по статус-кодам
REQUEST_COUNT = Counter(
    'http_requests_total_by_status',
    'Count of HTTP requests by status code',
    ['status_code', "endpoint"]
)