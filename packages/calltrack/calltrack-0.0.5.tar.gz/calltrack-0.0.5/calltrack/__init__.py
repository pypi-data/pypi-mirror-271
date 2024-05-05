import atexit
import functools
import inspect
import json
import time
import uuid
from datetime import datetime
from typing import Callable

from .calltrack import ConsoleCalltrack, JSONCalltrack
from .dependencies import json_calltrack
from .utils import CustomJSONEncoder

atexit.register(lambda: json_calltrack.flush() if json_calltrack.queue.queue else None)


def consolelog(func: Callable):
    @functools.wraps(func)
    def consolelog_wrapper(*args, **kwargs):
        calltrack = ConsoleCalltrack()

        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        timestamp = datetime.now()
        start_time = time.perf_counter()

        output = func(*args, **kwargs)

        end_time = time.perf_counter()
        run_time = end_time - start_time

        calltrack.append(f"Calling {func.__name__}({signature})")
        calltrack.append(f"{func.__name__}() returned {repr(output)}")
        calltrack.append(f"Computation time: {run_time}")
        calltrack.append(f"Timestamp: {timestamp}")

        calltrack.flush()

        return output

    return consolelog_wrapper


def jsonlog(
    _func=None,
    *,
    calltrack: JSONCalltrack | None = None,
):
    if not calltrack:
        calltrack = json_calltrack

    def jsonlog_decorator(func: Callable, calltrack: JSONCalltrack):
        @functools.wraps(func)
        def jsonlog_wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]

            uuidv1 = uuid.uuid1()

            timestamp = datetime.now()
            start_time = time.perf_counter()

            output = func(*args, **kwargs)

            end_time = time.perf_counter()
            run_time = end_time - start_time

            calltrack.append(
                log={
                    str(uuidv1): {
                        "call": f"{func.__name__}( {', '.join([f'{arg}={val}' for arg, val in zip(inspect.signature(func).parameters, args)])}, {kwargs_repr} )",
                        "name": func.__name__,
                        "args": args_repr,
                        "kwargs": kwargs_repr,
                        "annotations": json.dumps(
                            func.__annotations__, cls=CustomJSONEncoder
                        ),
                        "output": repr(output),
                        "run_time": run_time,
                        "timestamp": str(timestamp),
                    }
                }
            )
            if calltrack.autoflush:
                calltrack.write(calltrack.log_queue.popleft())

            return output

        return jsonlog_wrapper

    if _func is None:
        return lambda func: jsonlog_decorator(func, calltrack=calltrack)
    else:
        return jsonlog_decorator(_func, calltrack=calltrack)
