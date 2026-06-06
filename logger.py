import argparse
import json
import os
from datetime import datetime

def log_entry(message, level="INFO"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message
    }
    log_file = "app.log.json"
    logs = []
    if os.path.exists(log_file):
        with open(log_file) as f:
            logs = json.load(f)
    logs.append(entry)
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)
    print(f"[{entry['level']}] {entry['message']}")

def main():
    parser = argparse.ArgumentParser(description="Simple JSON logger")
    parser.add_argument("message", help="Message to log")
    parser.add_argument("--level", choices=["INFO", "WARNING", "ERROR"], default="INFO")
    args = parser.parse_args()
    log_entry(args.message, args.level)

if __name__ == "__main__":
    main()
