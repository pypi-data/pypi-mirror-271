import json
import os
import uuid
from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime
from typing import Any


class LogQueue:
    def __init__(self, name: str):
        self.name = name
        self.id = uuid.uuid4()
        self.queue = deque([])

    def append(self, log: Any) -> None:
        """Add the log on top of a stack."""
        self.queue.append(log)

    def popleft(self):
        return self.queue.popleft()


class LogWriter(ABC):
    """LogWriter Abstract Class"""

    def __init__(self, log_queue: LogQueue):
        self.log_queue = log_queue

    def flush(self) -> None:
        while self.log_queue.queue:
            self.write(self.log_queue.popleft())

    @abstractmethod
    def write(
        self,
        log: Any,
    ) -> None:
        """Write logs"""


class ConsoleLogWriter(LogWriter):
    def write(self, log: Any) -> None:
        print(log)


class JSONLogWriter(LogWriter):
    def __init__(
        self, log_queue: LogQueue, save_dir: str, autoflush: bool = False
    ) -> None:
        super().__init__(log_queue=log_queue)
        self.save_dir = save_dir
        self.autoflush = autoflush

        self._prepare_dir()

    def flush(self, filename: str | None = None):
        concat_log = {}
        while self.log_queue.queue:
            log = self.log_queue.queue.popleft()
            self._check_log(log)
            concat_log.update(log)
        self.write(concat_log, filename)

    def write(self, log: dict, filename: str | None = None) -> None:
        self._check_log(log)
        """Assuming the log is well formatted"""
        self._export_log(log, filename)

    def append(self, log: dict) -> None:
        self.log_queue.append(log)

    def _export_log(self, log: dict, filename: str | None = None) -> None:
        """Export the logs to a JSON file.

        Args:
        ----
            file_path (str, optional): The file path to save the logs. If not provided, a default file path will be used.

        """
        if not filename:
            filename = self._default_filename()
        if not filename.endswith(".json"):
            filename = filename + ".json"

        filepath = os.path.join(self.save_dir, filename)
        print(log, filepath)
        with open(filepath, "w") as file:
            json.dump(log, file, indent=4)

    def _default_filename(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"log_{timestamp}.json"

    def _prepare_dir(self) -> None:
        os.makedirs(os.path.join(os.getcwd(), self.save_dir), exist_ok=True)

    def _check_log(self, log: dict) -> None:
        if not isinstance(log, dict):
            raise TypeError(
                f"The log should be a dict. It is received as a {type(log)}. Value= {log}"
            )
