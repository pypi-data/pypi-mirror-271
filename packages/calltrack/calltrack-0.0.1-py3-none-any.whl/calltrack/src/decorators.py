import functools
import os
import time
import uuid
from datetime import datetime
from typing import Callable

from log_writer import ConsoleLogWriter, JSONLogWriter


def consolelog(func: Callable):
    @functools.wraps(func)
    def consolelog_wrapper(*args, **kwargs):
        writer = ConsoleLogWriter()

        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        timestamp = datetime.now()
        start_time = time.perf_counter()

        output = func(*args, **kwargs)

        end_time = time.perf_counter()
        run_time = end_time - start_time

        writer.append(f"Calling {func.__name__}({signature})")
        writer.append(f"{func.__name__}() returned {repr(output)}")
        writer.append(f"Computation time: {run_time}")
        writer.append(f"Timestamp: {timestamp}")

        writer.flush()

        return output

    return consolelog_wrapper


def jsonlog(
    _func=None,
    *,
    writer: JSONLogWriter = None,
):
    if not writer:
        writer = JSONLogWriter(save_dir=os.getcwd())

    def jsonlog_decorator(func: Callable, writer: JSONLogWriter):
        @functools.wraps(func)
        def jsonlog_wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)

            uuidv1 = uuid.uuid1()

            timestamp = datetime.now()
            start_time = time.perf_counter()

            output = func(*args, **kwargs)

            end_time = time.perf_counter()
            run_time = end_time - start_time

            writer.append(
                log={
                    str(uuidv1): {
                        "name": func.__name__,
                        "args": args_repr,
                        "kwargs": kwargs_repr,
                        "signature": signature,
                        "output": repr(output),
                        "run_time": run_time,
                        "timestamp": str(timestamp),
                    }
                }
            )
            if writer.autoflush:
                writer.write(writer.log_queue.popleft())

            return output

        return jsonlog_wrapper

    if _func is None:
        return lambda func: jsonlog_decorator(func, writer=writer)
    else:
        return jsonlog_decorator(_func, writer=writer)
