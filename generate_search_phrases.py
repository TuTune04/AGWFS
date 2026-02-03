#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


def parse_models(output: str) -> list[str]:
    models: list[str] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        if line.strip().lower().startswith("name"):
            continue
        models.append(line.split()[0])
    return models


def load_models() -> list[str]:
    if shutil.which("ollama") is None:
        raise FileNotFoundError("Không tìm thấy lệnh 'ollama' trong PATH.")
    result = subprocess.run(
        ["ollama", "list"],
        check=True,
        text=True,
        capture_output=True,
    )
    return parse_models(result.stdout)


def build_prompt(topic: str, count: int) -> str:
    return (
        f"Hãy tạo {count} cụm từ tìm kiếm ngắn gọn bằng tiếng Việt cho chủ đề: "
        f"\"{topic}\". Mỗi cụm từ trên một dòng, không đánh số."
    )


def clean_phrase(line: str) -> str:
    line = line.strip()
    if not line:
        return ""
    line = re.sub(r"^\s*[-*\d]+[.)-]?\s*", "", line)
    return line.strip()


def extract_phrases(output: str) -> list[str]:
    phrases: list[str] = []
    for line in output.splitlines():
        phrase = clean_phrase(line)
        if phrase:
            phrases.append(phrase)
    return phrases


def run_model(model: str, prompt: str) -> list[str]:
    result = subprocess.run(
        ["ollama", "run", model, "--prompt", prompt],
        check=True,
        text=True,
        capture_output=True,
    )
    return extract_phrases(result.stdout)


def write_phrases(path: Path, phrases: list[str]) -> None:
    path.write_text("\n".join(phrases) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tự động dùng Ollama để tạo cụm từ tìm kiếm và lưu ra file txt."
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Chủ đề cần tạo cụm từ tìm kiếm.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Số lượng cụm từ mỗi mô hình tạo ra.",
    )
    parser.add_argument(
        "--output",
        default="search_phrases.txt",
        help="Đường dẫn file txt đầu ra.",
    )
    parser.add_argument(
        "--models",
        nargs="*",
        help="Chỉ định danh sách mô hình cần dùng (bỏ trống để dùng tất cả).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chỉ in thông tin, không gọi Ollama.",
    )
    args = parser.parse_args()

    try:
        models = args.models or load_models()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"Lỗi khi lấy danh sách mô hình: {exc}", file=sys.stderr)
        return 1

    if not models:
        print("Không tìm thấy mô hình Ollama nào.", file=sys.stderr)
        return 1

    prompt = build_prompt(args.topic, args.count)

    if args.dry_run:
        print("Các mô hình sẽ dùng:", ", ".join(models))
        print("Prompt:\n", prompt)
        return 0

    phrases: list[str] = []
    seen: set[str] = set()
    for model in models:
        try:
            model_phrases = run_model(model, prompt)
        except subprocess.CalledProcessError as exc:
            print(f"Lỗi khi chạy mô hình {model}: {exc}", file=sys.stderr)
            continue
        for phrase in model_phrases:
            if phrase not in seen:
                seen.add(phrase)
                phrases.append(phrase)

    if not phrases:
        print("Không tạo được cụm từ nào.", file=sys.stderr)
        return 1

    output_path = Path(args.output)
    write_phrases(output_path, phrases)
    print(f"Đã ghi {len(phrases)} cụm từ vào {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
