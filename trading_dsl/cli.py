"""Minimal offline validator command."""
import argparse, json
from pathlib import Path
from .validation import validate_backtest_config, validate_strategy

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("file", type=Path); parser.add_argument("--backtest-config", action="store_true")
    args = parser.parse_args(); data = json.loads(args.file.read_text())
    report = validate_backtest_config(data) if args.backtest_config else validate_strategy(data)
    print(json.dumps(report.to_dict(), indent=2)); return 0 if report.valid else 1

if __name__ == "__main__": raise SystemExit(main())
