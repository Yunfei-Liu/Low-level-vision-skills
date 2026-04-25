#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run batch low-level vision tasks from a JSON manifest.")
    parser.add_argument("--manifest", required=True, help="Path to tasks JSON list.")
    parser.add_argument("--python", default=sys.executable, help="Python executable for child runs.")
    parser.add_argument("--model", default=None, help="Optional model override.")
    parser.add_argument("--size", default=None, help="Optional size override.")
    parser.add_argument("--output-root", default="outputs", help="Output root directory.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    items = json.loads(manifest_path.read_text(encoding="utf-8"))

    runner = Path(__file__).resolve().parent / "run_task.py"
    for i, item in enumerate(items, start=1):
        input_path = item["input"]
        task = item["task"]
        cmd = [
            args.python,
            str(runner),
            "--input",
            input_path,
            "--task",
            task,
            "--output-root",
            args.output_root,
        ]
        if args.model:
            cmd.extend(["--model", args.model])
        if args.size:
            cmd.extend(["--size", args.size])

        print(f"[{i}/{len(items)}] Running task={task}, input={input_path}")
        subprocess.run(cmd, check=True)

    print("Batch completed.")


if __name__ == "__main__":
    main()
