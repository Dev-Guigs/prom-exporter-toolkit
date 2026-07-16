from exporter.custom_metrics import (
    HTTP_REQUESTS_TOTAL,
    JOB_QUEUE_SIZE,
    record_request,
    set_queue_size,
)


def test_record_request_increments_counter():
    before = HTTP_REQUESTS_TOTAL.labels(
        method="GET", endpoint="/health", status="200"
    )._value.get()

    record_request("GET", "/health", 200, 0.012)

    after = HTTP_REQUESTS_TOTAL.labels(
        method="GET", endpoint="/health", status="200"
    )._value.get()
    assert after == before + 1


def test_set_queue_size_updates_gauge():
    set_queue_size(42)
    assert JOB_QUEUE_SIZE._value.get() == 42
