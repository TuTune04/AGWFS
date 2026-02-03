#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime
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


def choose_models(models: list[str]) -> list[str]:
    print("Các mô hình Ollama đang có:")
    for idx, model in enumerate(models, start=1):
        print(f"{idx}. {model}")
    print("Nhập số thứ tự mô hình muốn dùng (cách nhau bởi dấu phẩy),")
    print("hoặc nhấn Enter để dùng tất cả:")
    raw = input("> ").strip()
    if not raw:
        return models
    selected: list[str] = []
    for part in raw.split(","):
        part = part.strip()
        if not part.isdigit():
            continue
        idx = int(part)
        if 1 <= idx <= len(models):
            model = models[idx - 1]
            if model not in selected:
                selected.append(model)
    return selected


DEFAULT_LANGUAGES: dict[str, str] = {
    "VI": "Tiếng Việt",
    "EN": "Tiếng Anh",
    "JA": "Tiếng Nhật",
}


START_MARKER = "===BEGIN_QUERIES==="


def build_prompt(topic: str, count: int) -> str:
    return (
        f"Hãy tạo một danh sách gồm {count} cụm từ tìm kiếm (search queries) "
        f"độc lập, mỗi dòng chỉ chứa 1 cụm từ, cho chủ đề: \"{topic}\".\n"
        "Yêu cầu chi tiết:\n"
        "Ngôn ngữ: Sử dụng ngẫu nhiên một trong ba thứ tiếng: Tiếng Việt, "
        "Tiếng Anh và Tiếng Nhật cho mỗi dòng (ví dụ: dòng 1 tiếng Việt, "
        "dòng 2 tiếng Nhật, dòng 3 tiếng Anh...).\n"
        "Nội dung: Mỗi dòng phải mang một ý nghĩa hoàn toàn khác nhau, "
        "không được là bản dịch của nhau. Các chủ đề cần trải rộng từ: "
        "Công nghệ (AI, lập trình), Thể thao (UFC, bóng đá), Đời sống "
        "(nấu ăn, decor), Khoa học, du lịch và giải trí.\n"
        "Định dạng: mỗi dòng một cụm từ, không đánh số thứ tự, "
        "không có thêm ký tự đặc biệt hay lời giải thích. "
        "Mỗi cụm từ 1 dòng, không viết liền nhau.\n"
        f"Hãy in đúng một dòng chứa ký hiệu bắt đầu: {START_MARKER}\n"
        "Tất cả cụm từ phải được in sau dòng ký hiệu bắt đầu này."
    )


def clean_phrase(line: str) -> str:
    line = line.strip()
    if not line:
        return ""
    line = re.sub(r"^\s*[-*\d]+[.)-]?\s*", "", line)
    return line.strip()


def strip_language_tag(line: str) -> tuple[str, str]:
    match = re.match(r"^\s*\[([A-Za-z]{2})\]\s*(.+)$", line)
    if match:
        return match.group(1).upper(), match.group(2).strip()
    match = re.match(r"^\s*([A-Za-z]{2})\s*[:\-]\s*(.+)$", line)
    if match:
        return match.group(1).upper(), match.group(2).strip()
    return "", line.strip()


def extract_phrases(output: str) -> list[tuple[str, str]]:
    phrases: list[tuple[str, str]] = []
    started = False
    for line in output.splitlines():
        if not started:
            if line.strip() == START_MARKER:
                started = True
            continue
        raw = clean_phrase(line)
        if not raw:
            continue
        lang, phrase = strip_language_tag(raw)
        if phrase:
            phrases.append((lang, phrase))
    return phrases


def run_model(model: str, prompt: str) -> list[tuple[str, str]]:
    result = subprocess.run(
        ["ollama", "run", model],
        check=True,
        text=True,
        encoding="utf-8",
        capture_output=True,
        input=prompt + "\n",
    )
    return extract_phrases(result.stdout)


def write_phrases(path: Path, phrases: list[str]) -> None:
    path.write_text("\n".join(phrases) + "\n", encoding="utf-8")


def next_output_path(project_dir: Path) -> Path:
    today = datetime.date.today().strftime("%Y%m%d")
    output_dir = project_dir / "text" / today
    output_dir.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(rf"^{today}_(\d{{3}})\.txt$")
    max_seq = 0
    for item in output_dir.iterdir():
        if not item.is_file():
            continue
        match = pattern.match(item.name)
        if match:
            seq = int(match.group(1))
            if seq > max_seq:
                max_seq = seq
    next_seq = max_seq + 1
    filename = f"{today}_{next_seq:03d}.txt"
    return output_dir / filename


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        description="Tự động dùng Ollama để tạo cụm từ tìm kiếm và lưu ra file txt."
    )
    parser.add_argument(
        "--topic",
        default="random",
        help="Chủ đề cần tạo cụm từ tìm kiếm (mặc định: random).",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=50,
        help="Số cụm từ mỗi lượt (sẽ tạo thêm cùng số lượng).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Đường dẫn file txt đầu ra (bỏ trống để tự tạo trong thư mục text/YYYYMMDD).",
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
    if not args.models and not args.dry_run:
        models = choose_models(models)
        if not models:
            print("Không có mô hình nào được chọn.", file=sys.stderr)
            return 1

    total_needed = args.count
    prompt = build_prompt(args.topic, total_needed)

    if args.dry_run:
        print("Các mô hình sẽ dùng:", ", ".join(models))
        print("Prompt:\n", prompt)
        return 0

    phrases: list[str] = []
    seen: set[str] = set()
    languages_seen: set[str] = set()
    for model in models:
        try:
            remaining = max(total_needed - len(phrases), 0)
            if remaining == 0:
                break
            prompt = build_prompt(args.topic, total_needed)
            model_phrases = run_model(model, prompt)
        except subprocess.CalledProcessError as exc:
            print(f"Lỗi khi chạy mô hình {model}: {exc}", file=sys.stderr)
            continue
        for lang, phrase in model_phrases:
            if lang and lang not in DEFAULT_LANGUAGES:
                continue
            if phrase not in seen:
                seen.add(phrase)
                if lang:
                    languages_seen.add(lang)
                phrases.append(phrase)
                if len(phrases) >= total_needed:
                    break

    if not phrases:
        print("Không tạo được cụm từ nào.", file=sys.stderr)
        return 1
    if len(languages_seen) < len(DEFAULT_LANGUAGES):
        print(
            "Cảnh báo: số ngôn ngữ thu được chưa đủ tối thiểu.",
            file=sys.stderr,
        )
    if len(phrases) < total_needed:
        print(
            "Cảnh báo: số cụm từ thu được ít hơn yêu cầu.",
            file=sys.stderr,
        )

    project_dir = Path(__file__).resolve().parent
    output_path = Path(args.output) if args.output else next_output_path(project_dir)
    write_phrases(output_path, phrases)
    print(f"Đã ghi {len(phrases)} cụm từ vào {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
