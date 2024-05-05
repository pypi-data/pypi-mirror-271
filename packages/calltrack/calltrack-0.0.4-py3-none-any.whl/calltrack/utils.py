import json
import os
from typing import Any, Dict, Union


def is_path_creatable(pathname: str) -> bool:
    """
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    """
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Union[str, Dict[str, Any]]:
        if isinstance(obj, type):
            return str(obj.__name__)
        return super().default(obj)
