# AGWFS
Automatically generate words for searching.

## Ollama local script

Script dùng Ollama local để tạo cụm từ tìm kiếm và lưu mỗi dòng một cụm từ.

```bash
python3 generate_search_phrases.py --topic "du lịch Đà Nẵng" --count 10 --output search_phrases.txt
```

Tùy chọn:
- `--models` chỉ định danh sách mô hình (mặc định dùng tất cả mô hình có sẵn).
- `--dry-run` xem prompt và danh sách mô hình mà không chạy Ollama.
