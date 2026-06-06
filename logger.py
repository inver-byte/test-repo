import argparse
import json
import os
from datetime import datetime

LOG_FILE = "app.log.json"

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def log_entry(message, level="INFO"):
    logs = load_logs()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message
    }
    logs.append(entry)
    save_logs(logs)
    print(f"[{entry['level']}] {entry['message']}")

def view_logs(level=None, limit=10):
    logs = load_logs()
    if level:
        logs = [l for l in logs if l["level"] == level]
    for entry in logs[-limit:]:
        print(f"{entry['timestamp']} [{entry['level']}] {entry['message']}")

def clear_logs():
    save_logs([])
    print("Log cleared.")

def main():
    parser = argparse.ArgumentParser(description="Simple JSON logger")
    sub = parser.add_subparsers(dest="command")

    log_cmd = sub.add_parser("log", help="Add a log entry")
    log_cmd.add_argument("message")
    log_cmd.add_argument("--level", choices=["INFO", "WARNING", "ERROR"], default="INFO")

    view_cmd = sub.add_parser("view", help="View log entries")
    view_cmd.add_argument("--level", choices=["INFO", "WARNING", "ERROR"])
    view_cmd.add_argument("--limit", type=int, default=10)

    sub.add_parser("clear", help="Clear all logs")

    args = parser.parse_args()

    if args.command == "log":
        log_entry(args.message, args.level)
    elif args.command == "view":
        view_logs(args.level, args.limit)
    elif args.command == "clear":
        clear_logs()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
