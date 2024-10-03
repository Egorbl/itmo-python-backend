import json
from lecture_1.hw.helper.helper import send_answer

async def mean(scope, recieve, send) -> None:
    if scope["method"] != "GET":
        await send_answer(send, 404, "404 Not Found")
        return
    request = await recieve()
    body = request["body"]

    if len(body) == 0:
        await send_answer(send, 422, "422 Unprocessable Entity")
        return

    body = json.loads(body)

    if body is None:
        await send_answer(send, 422, "422 Unprocessable Entity")
        return

    if len(body) == 0:
        await send_answer(send, 400, "400 Bad Request")
        return

    float_sum = 0

    for el in body:
        if not (isinstance(el, int) or isinstance(el, float)):
            await send_answer(send, 422, "422 Unprocessable Entity")
            return
        float_sum += el

    result = json.dumps({"result": float_sum / len(body)})
    await send_answer(send, 200, result, content_type="application/json")

