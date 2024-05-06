import asyncio
from pydantic import BaseModel
from typing import Optional


class NullConfig(BaseModel):
    """
    todo...
    """

    pass


class Worker:
    """
    Async worker backing `Producer`, `ConsumerGroup` & `ProducerConsumerGroup`. It provides:
    - config model inititialization
    - main worker loop
    - connection lease acquisition
    - topic storage and consumption
    """

    config: BaseModel

    def __init__(self, config: Optional[BaseModel]):
        if config:
            self.config = config
        else:
            self.config = NullConfig()

    async def start(self):
        while True:
            await asyncio.gather(
                asyncio.sleep(5),
                self.work(),
            )

    async def work(self):
        raise NotImplementedError
