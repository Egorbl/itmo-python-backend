from lecture_1.hw.helper.helper import is_int, send_answer
import json

async def factorial(scope, recieve, send) -> None:
    if scope["method"] != "GET":
        await send_answer(send, 404, "404 Not Found")
        return

    n = scope.get("query_string")

    if n is None:
        await send_answer(send, 422, "422 Unprocessable Entity")
        return

    n = n.decode("utf-8").lstrip("n=")

    if not is_int(n):
        await send_answer(send, 422, "422 Unprocessable Entity")
        return

    n = int(n)
    if n < 0:
        await send_answer(send, 400, "400 Bad Request")
        return
    result = 1
    for i in range(2, n + 1):
        result *= i

    result = json.dumps({"result": result})
    await send_answer(send, 200, result, content_type="application/json")