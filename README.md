# AGWFS
Automatically generate words for searching.

## Ollama local script

Script dùng Ollama local để tạo cụm từ tìm kiếm. Kết quả chỉ gồm các cụm từ, mỗi dòng một cụm.
Mặc định tạo 50 cụm từ và lưu vào thư mục `text/YYYYMMDD` theo tên `YYYYMMDD_###.txt`.
Khi chạy sẽ hiển thị danh sách model local để bạn chọn (nhập số thứ tự), hoặc Enter để dùng tất cả.

```bash
python generate_search_phrases.py
```

Ví dụ chỉ định chủ đề và số lượng:
```bash
python generate_search_phrases.py --topic "du lịch Đà Nẵng" --count 50
```

Ngôn ngữ: ngẫu nhiên trong 3 ngôn ngữ (Tiếng Việt, Tiếng Anh, Tiếng Nhật).

Tùy chọn:
- `--topic` chủ đề (mặc định: `random`).
- `--count` số cụm từ cần tạo (mặc định: `50`).
- `--output` đường dẫn file txt đầu ra (bỏ trống để tự tạo trong `text/YYYYMMDD`).
- `--models` chỉ định danh sách mô hình (bỏ qua bước chọn model).
- `--dry-run` xem prompt và danh sách mô hình mà không chạy Ollama.

## Batch chạy nhiều lần

Chạy tự động nhiều lần và ghi file vào thư mục theo ngày:

```bash
python run_batch_generate.py --times 3
```

Ví dụ chỉ định chủ đề, số lượng và mô hình:
```bash
python run_batch_generate.py --times 5 --topic "random" --count 50 --models llama3:8b
```
