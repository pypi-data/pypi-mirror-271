import asyncio
from asyncio import Event
from dataclasses import dataclass, field

import pampy


@dataclass
class Subscriber:
    src_handle: "Messages"

    def __post_init__(self):
        self.value_set = Event()
        self.value_empty = Event()
        self.message = None

    async def tell(self, message):
        assert not self.value_set.is_set()
        self.message = message
        self.value_empty.clear()
        self.value_set.set()
        await self.value_empty.wait()

    async def get(self):
        await self.value_set.wait()
        message = self.message
        self.message = None
        self.value_set.clear()
        self.value_empty.set()
        return message

    def unsubscribe(self):
        self.src_handle.unsubscribe(self)

    def __aiter__(self):
        return self

    async def __anext__(self):
        item = await self.get()
        if item is None:
            raise StopAsyncIteration
        return item

    async def wait(self, pattern):
        from pampy import _
        matched = False
        while not matched:
            message = await self.get()

            def on_match(*args):
                nonlocal matched
                matched = True

            pampy.match(message,
                        pattern, on_match,
                        _, lambda *args: None
                        )
        return message


@dataclass
class Messages:
    subscribers: list[Subscriber] = field(default_factory=list)

    def subscribe(self) -> Subscriber:
        subscriber = Subscriber(self)
        self.subscribers.append(subscriber)
        return subscriber

    async def publish(self, message):
        for subscriber in self.subscribers:
            await subscriber.tell(message)

    def unsubscribe(self, subscriber: Subscriber):
        self.subscribers.remove(subscriber)

    async def close(self):
        await self.publish(None)
