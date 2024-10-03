async def send_answer(send, status: int, response_body: str, content_type:str="text/plain") -> None:
    response_body = response_body.encode('utf-8')
    content_type = content_type.encode('utf-8')

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
