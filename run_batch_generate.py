#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from generate_search_phrases import choose_models, load_models


def prompt_times() -> int:
    while True:
        raw = input("Nhập số lần chạy: ").strip()
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        print("Giá trị không hợp lệ. Vui lòng nhập số nguyên > 0.")


def resolve_models(args: argparse.Namespace) -> list[str]:
    if args.models:
        return args.models
    if args.dry_run:
        return []
    models = load_models()
    if not models:
        return []
    return choose_models(models)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Chạy generate_search_phrases.py tự động nhiều lần."
    )
    parser.add_argument(
        "--times",
        type=int,
        default=None,
        help="Số lần chạy (bỏ trống để nhập thủ công).",
    )
    parser.add_argument(
        "--topic",
        default="random",
        help="Chủ đề (mặc định: random).",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=50,
        help="Số cụm từ mỗi lần chạy (mặc định: 50).",
    )
    parser.add_argument(
        "--models",
        nargs="*",
        help="Danh sách mô hình muốn dùng.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chỉ in thông tin, không chạy Ollama.",
    )
    args = parser.parse_args()

    times = args.times if args.times is not None else prompt_times()
    if times <= 0:
        print("Số lần chạy phải > 0.", file=sys.stderr)
        return 1

    models = resolve_models(args)
    if not models and not args.dry_run:
        print("Không có mô hình nào được chọn.", file=sys.stderr)
        return 1

    script_path = Path(__file__).resolve().parent / "generate_search_phrases.py"
    for idx in range(1, times + 1):
        cmd = [
            sys.executable,
            str(script_path),
            "--topic",
            args.topic,
            "--count",
            str(args.count),
        ]
        if models:
            cmd.extend(["--models", *models])
        if args.dry_run:
            cmd.append("--dry-run")

        print(f"Chạy lần {idx}/{times}...")
        if args.dry_run:
            print("Lệnh:", " ".join(cmd))
            continue
        subprocess.run(cmd, check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
