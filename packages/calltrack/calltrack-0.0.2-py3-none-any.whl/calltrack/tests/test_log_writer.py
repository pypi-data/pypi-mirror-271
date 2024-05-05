import json
import os

import pytest

from ..src.log_writer import ConsoleLogWriter, JSONLogWriter


# Testing ConoleLogWriter class
def test_console_log_writer_append():
    log_writer = ConsoleLogWriter()
    log_writer.append("Test log")
    assert len(log_writer.queue) == 1
    assert log_writer.queue[0] == "Test log"


def test_console_log_writer_flush():
    log_writer = ConsoleLogWriter()
    log_writer.append("Test log 1")
    log_writer.append("Test log 2")
    assert len(log_writer.queue) == 2
    log_writer.flush()
    assert len(log_writer.queue) == 0


def test_console_log_writer_write(capfd):
    console_log_writer = ConsoleLogWriter()
    console_log_writer.write("Test log")
    captured = capfd.readouterr()
    assert captured.out == "Test log\n"


# Testing JSONLogWriter class
def test_json_log_writer_init(mocker):
    mocker.patch("os.makedirs")
    writer = JSONLogWriter("test_dir")
    assert writer.dir == "test_dir"
    os.makedirs.assert_called_once_with(
        os.path.join(os.getcwd(), "test_dir"), exist_ok=True
    )


def test_json_log_writer_flush(mocker):
    mocker.patch("os.path.join")
    mocker.patch("os.makedirs")
    writer = JSONLogWriter("test_dir")
    writer.append({"key": "value"})
    writer.append({"key2": "value2"})
    assert len(writer.queue) == 2
    writer.flush()
    os.path.join.assert_called()
    os.makedirs.assert_called_once_with(
        os.path.join(os.getcwd(), "test_dir"), exist_ok=True
    )
    assert len(writer.queue) == 0


def test_json_log_writer_write(mocker):
    mocker.patch("json.dump")
    mocker.patch("os.path.join")
    mocker.patch("os.makedirs")
    writer = JSONLogWriter("test_dir")
    writer.write({"key": "value"}, "test_file.json")
    json.dump.assert_called_once()
    os.path.join.assert_called()


def test_json_log_writer_check_log():
    writer = JSONLogWriter("test_dir")
    with pytest.raises(TypeError):
        writer._check_log("not a dict")


# Running the tests
if __name__ == "__main__":
    pytest.main()
