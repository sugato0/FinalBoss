from asyncio import sleep

async def background_loop():
    while True:
        await sleep(60)
