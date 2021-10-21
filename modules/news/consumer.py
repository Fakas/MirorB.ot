from typing import Dict
from abc import ABC, abstractmethod


class Consumer(ABC):
    def __init__(self, feeds: Dict, channel_id: str):
        self.feeds = feeds
        self.channel_id = channel_id
        self.consumed = []

    async def consume(self, *_args, **kwargs):
        await self._consume(kwargs["client"])

    @abstractmethod
    async def _consume(self, client):
        pass
