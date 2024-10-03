from lecture_1.hw.helper.helper import send_answer
from lecture_1.hw.src.factorial import factorial
from lecture_1.hw.src.fibonacci import fibonacci
from lecture_1.hw.src.mean import mean

async def app(scope, receive, send) -> None:
    if scope["type"] == "http":
        path = scope['path']

        if path == "/factorial":
            await factorial(scope, receive, send)
            return
        if path.startswith("/fibonacci"):
            await fibonacci(scope, receive, send)
            return
        if path == "/mean":
            await mean(scope, receive, send)
            return

        await send_answer(send, 404, "404 Not Found")
    elif scope["type"] == "lifespan":
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return
