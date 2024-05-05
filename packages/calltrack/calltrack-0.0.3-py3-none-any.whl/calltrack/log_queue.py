import uuid
from collections import deque
from typing import Any, Deque


class LogQueue:
    def __init__(self, name: str | None = None):
        self.name = name if name else "default"
        self.id = uuid.uuid4()
        self.queue: Deque = deque([])

    def append(self, log: Any) -> None:
        """Add the log on top of a stack."""
        self.queue.append(log)

    def popleft(self):
        return self.queue.popleft()

    def __len__(self):
        return len(self.queue)
