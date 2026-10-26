# Mã nguồn website Thakorn

Gói xuất ngày 25/10/2026 từ mã nguồn của website:
https://thakorn-tangphadungrutch.ngaikho.chatgpt.site

- Phiên bản đã lưu: 16.
- Source commit: `98ab1f2da7d34bee640252e51e23258841045e28`.
- Toàn bộ file được theo dõi trong mã nguồn được giữ nguyên. File hướng dẫn này được bổ sung riêng cho gói tải xuống.

## Mở trong Visual Studio Code

1. Giải nén ZIP.
2. Trong VS Code, chọn **File > Open Folder** và mở thư mục `Thakorn_Portfolio`.
3. Mở Terminal tại thư mục đó và chạy:

```powershell
py -m http.server 8000 --directory dist
```

Nếu máy dùng lệnh `python` thay vì `py`, chạy:

```sh
python -m http.server 8000 --directory dist
```

4. Mở http://localhost:8000 trong trình duyệt.
5. Dừng server bằng Ctrl+C.

Website là HTML/CSS/JavaScript tĩnh; để xem bản hiện có chỉ cần Python 3 hoặc một HTTP server tĩnh tương đương. Hãy phục vụ `dist` làm thư mục gốc để các liên kết `/assets/`, trang con và tài liệu hoạt động đúng.

## Cấu trúc

- `dist/`: toàn bộ website sẵn chạy, gồm trang chủ, các trang nội dung, dự án và game drone.
- `dist/assets/`: hình ảnh, logo, CSS và JavaScript, gồm mã game Drone Simulator.
- `dist/documents/`: résumé PDF, báo cáo dự án, poster và chứng nhận được website sử dụng.
- `content/projects.json`: dữ liệu dự án và hoạt động.
- `content/drone-simulator.html`: nội dung trang game.
- `tools/write_pages.py`: công cụ tạo lại các trang HTML.
- `tools/test_drone_mission.mjs`: kiểm tra logic game.
- `tools/prepare_*.py`: các script xử lý ảnh trong quá trình xây website ban đầu.
- `SOURCES.md`: ghi chú nguồn nội dung và hình ảnh.
- `README.md`: hướng dẫn gốc của dự án.

## Chỉnh sửa bằng Codex

- Giao diện: xem các file CSS và JavaScript trong `dist/assets/`.
- Nội dung có cấu trúc: sửa `content/projects.json` và các mẫu trong `tools/write_pages.py`.
- Game: xem `content/drone-simulator.html`, `dist/assets/drone-mission.js`, `dist/assets/drone-simulator.js` và `dist/assets/drone-simulator.css`.

Nếu muốn tạo lại HTML sau khi sửa dữ liệu/mẫu, cài Pillow rồi chạy:

```powershell
py -m pip install Pillow
py tools/write_pages.py
```

Nếu chỉnh trực tiếp HTML trong `dist`, lần chạy tiếp theo của `tools/write_pages.py` sẽ tạo lại HTML theo dữ liệu/mẫu. Hãy cập nhật cùng nguồn tạo trang nếu muốn giữ thay đổi đó.

Các ảnh dùng trên website đã có sẵn trong `dist/assets/`. Các script `prepare_*` ghi lại quy trình xử lý ảnh ban đầu và có thể cần ảnh gốc cùng đường dẫn nguồn tương ứng; không cần chạy các script này để xem hoặc chỉnh giao diện hiện tại.

Font DM Sans và Manrope được tải qua Google Fonts khi có Internet.

## Phạm vi gói xuất

Gói này chứa toàn bộ mã nguồn hiện tại và tài nguyên đã được đưa vào website. Gói không bao gồm lịch sử Git, thông tin đăng nhập hay những ảnh gốc trên Google Drive chưa được đưa vào website. Việc xuất gói không thay đổi website đang công khai.
