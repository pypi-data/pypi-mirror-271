import json
import os
from datetime import datetime
from tkinter import Tk, filedialog

import streamlit as st


def read_json_file(file):
    with open(file) as f:
        return json.load(f)


def select_directory():
    root = Tk()
    root.withdraw()  #
    directory = filedialog.askdirectory()
    root.destroy()
    return directory


def view():
    st.set_page_config(layout="wide")
    st.title("Calltrack View")

    process_directory()


def process_directory():
    st.sidebar.header("Select Logs Directory")
    logs_path_input = st.sidebar.text_input("Enter logs directory path:", "")
    logs_path = logs_path_input

    if logs_path:
        json_files = [f for f in os.listdir(logs_path) if f.endswith(".json")]
        json_files.sort(
            key=lambda x: datetime.strptime(
                x.split("_", 1)[1].split(".")[0], "%Y%m%d_%H%M%S_%f"
            ),
            reverse=True,
        )

        selected_files = st.sidebar.multiselect("Select JSON files", json_files)

        if len(selected_files) > 0:
            cols = st.columns(len(selected_files))
            for i, file in enumerate(selected_files):
                file_path = os.path.join(logs_path, file)
                data = read_json_file(file_path)
                with cols[i]:
                    st.subheader(f"File: {file}")
                    for idx, obj in enumerate(data):
                        with st.expander(f"### Step {idx+1}"):
                            for key, value in data[obj].items():
                                st.markdown(f"**{key}:** {value}".replace("\n", ""))
        else:
            st.write("Please select files to compare.")
    else:
        st.write("Please provide a valid logs directory path.")


if __name__ == "__main__":
    view()
