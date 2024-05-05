import os
import subprocess
import sys


def start(args=sys.argv):
    path = args[1] if len(args) > 1 else None
    script_dir = os.path.dirname(os.path.realpath(__file__))
    target_file_path = os.path.join(script_dir, "view.py")

    command = ["streamlit", "run", target_file_path]

    if path:
        command.extend(["--", "--path", path])

    subprocess.run(command)
