from lecture_1.hw.metrics import REQUEST_COUNT
async def send_answer(send, status: int, response_body: str, content_type:str="text/plain", endpoint="/") -> None:
    response_body = response_body.encode('utf-8')
    content_type = content_type.encode('utf-8')

    REQUEST_COUNT.labels(status_code=status, endpoint=endpoint).inc()

    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': [
            (b'content-type', content_type),
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': response_body,
        'more_body': False,
    })


def is_int(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True
