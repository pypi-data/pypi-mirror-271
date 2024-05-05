import os

from .calltrack import JSONCalltrack
from .log_queue import LogQueue

json_calltrack = JSONCalltrack(queue=LogQueue(), save_dir=os.getcwd(), autoflush=False)
