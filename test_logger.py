import pytest
import json
import os
from logger import log_entry, load_logs, clear_logs

def test_log_creates_entry():
    clear_logs()
    log_entry("test message", "INFO")
    logs = load_logs()
    assert len(logs) == 1
    assert logs[0]["message"] == "test message"
    assert logs[0]["level"] == "INFO"

def test_log_level_warning():
    clear_logs()
    log_entry("something wrong", "WARNING")
    logs = load_logs()
    assert logs[0]["level"] == "WARNING"

def test_clear_logs():
    log_entry("to be cleared", "INFO")
    clear_logs()
    assert load_logs() == []

def test_corrupted_log_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with open("app.log.json", "w") as f:
        f.write("not valid json{{{{")
    log_entry("recovery test", "INFO")
    logs = load_logs()
    assert len(logs) == 1
