import os
import subprocess


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    target_file_path = os.path.join(script_dir, "view.py")

    command = ["streamlit", "run", target_file_path]
    subprocess.run(command)


if __name__ == "__main__":
    main()
