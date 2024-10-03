from lecture_1.hw.helper.helper import is_int, send_answer
import json

async def fibonacci(scope, recieve, send) -> None:
    if scope["method"] != "GET":
        await send_answer(send, 404, "404 Not Found")
        return

    path = scope["path"]
    path = path.lstrip("/fibonacci")
    path = path.lstrip("/")

    if not is_int(path):
        await send_answer(send, 422, "422 Unprocessable Entity")
        return

    n = int(path)

    if n < 0:
        await send_answer(send, 400, "400 Bad Request")
        return

    n1, n2 = 1, 1
    for i in range(2, n):
        n1, n2 = n2, n1 + n2

    if n == 0:
        n2 = 0

    result = json.dumps({"result": n2})
    await send_answer(send, 200, result, content_type="application/json")