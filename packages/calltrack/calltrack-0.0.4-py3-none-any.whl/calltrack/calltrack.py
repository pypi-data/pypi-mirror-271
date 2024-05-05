import json
import os
import warnings
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from .log_queue import LogQueue
from .utils import is_path_creatable


class Calltrack(ABC):
    """Calltrack Abstract Class"""

    def __init__(self, queue: LogQueue = LogQueue()):
        self.queue = queue

    def flush(self) -> None:
        while self.queue.queue:
            self.write(self.queue.popleft())

    def append(self, log: dict) -> None:
        self.queue.append(log)

    @abstractmethod
    def write(
        self,
        log: Any,
    ) -> None:
        """Write logs"""


class ConsoleCalltrack(Calltrack):
    def write(self, log: Any) -> None:
        print(log)


class JSONCalltrack(Calltrack):
    def __init__(
        self, save_dir: str, queue: LogQueue = LogQueue(), autoflush: bool = False
    ) -> None:
        super().__init__(queue=queue)
        self._save_dir = save_dir
        self.autoflush = autoflush

        self._prepare_dir()

    @property
    def save_dir(self):
        return self._save_dir

    @save_dir.setter
    def save_dir(self, path: str) -> None:
        if is_path_creatable(path):
            self._save_dir = path
            self._prepare_dir()
        else:
            warnings.warn("The provided path is ill-formed.")

    def flush(self, filename: str | None = None):
        concat_log = {}
        while self.queue.queue:
            log = self.queue.queue.popleft()
            self._check_log(log)
            concat_log.update(log)
        self.write(concat_log, filename)

    def write(self, log: dict, filename: str | None = None) -> None:
        self._check_log(log)
        """Assuming the log is well formatted"""
        self._export_log(log, filename)

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
