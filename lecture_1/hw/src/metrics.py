from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


async def metrics_endpoint(scope, receive, send):
    if scope["type"] == "http":
        # Преобразование заголовка CONTENT_TYPE_LATEST в формат bytes
        headers = [(b"content-type", CONTENT_TYPE_LATEST.encode("utf-8"))]

        # Отправка заголовка HTTP-ответа
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": headers,
        })

        # Отправка тела ответа в виде байтов, как ожидается для Prometheus
        await send({
            "type": "http.response.body",
            "body": generate_latest(),
        })
