import asyncio
from asyncio import TaskGroup

from proboscis_async_events import Messages


def test_run_messages():
    messages = Messages()

    async def test_pub_sub():
        await messages.publish("hello")
        sub = messages.subscribe()

        async def subber1():
            async for message in sub:
                print(f"got message:{message}")
                if message == 'end':
                    return

        async with TaskGroup() as tg:
            tg.create_task(subber1())
            print('publishing world')
            await messages.publish("world")
            print('publishing end')
            await messages.publish('end')
    asyncio.run(test_pub_sub())


