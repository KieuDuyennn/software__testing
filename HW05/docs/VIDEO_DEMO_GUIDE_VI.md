# Kịch bản video demo HW05 (7-8 phút)

Video phải là bằng chứng thật: YouTube unlisted, có giọng thuyết minh tiếng Việt
của sinh viên và cho thấy JMeter cùng Task Manager trong một khung hình khi tải
đang chạy. Nếu không còn video ghi từ các lần chạy chính thức, cần chạy lại và
quay màn hình; không dựng video giả từ ảnh tĩnh.

## Chuẩn bị

- Hiện MSSV `23127184`, hostname `KIEUDUYEN` và URL repository.
- Mở JMeter/terminal ở bên trái, Task Manager ở bên phải.
- Dùng backend mới với `LOADTEST=1`, dữ liệu đã seed và PID backend đúng.
- Che thông tin nhạy cảm nếu có, nhưng giữ tên plan, thời gian và số liệu rõ.

## Timeline gợi ý

### 0:00-0:45 — Giới thiệu

Nói MSSV, SUT và workflow: đăng nhập, tìm kiếm, xem chi tiết, thêm giỏ hàng,
checkout. Giải thích ba nhóm endpoint auth-heavy, read-heavy và transactional.

### 0:45-1:35 — Thiết kế data-driven và human review

Mở một JMX và ba CSV. Chỉ ra JWT correlation, product ID động, content
assertions, think time 300-700 ms và ba listener khác nhau. Nói ngắn gọn các lỗi
AI đã được sửa: thread tròn tùy ý, Stress tuyến tính, đường dẫn CSV tuyệt đối,
assertion chỉ kiểm tra status và đếm nhầm controller rows.

### 1:35-2:35 — Load

Cho thấy plan `23127184_Load_20260817.jmx`, JMeter và Task Manager trong cùng
khung hình. Nêu 34 VU, ramp 68 giây, 64.16 request/s tổng, p95 10 ms, 0% lỗi và
8,547 journey hoàn chỉnh.

### 2:35-3:35 — Stress

Nêu bốn mức 33/66/99/132 VU. Ở mức cao nhất đạt khoảng 260.6 request/s, p95 13
ms, 0% lỗi. Kết luận đúng là chưa thấy knee trong phạm vi đo, không khẳng định
132 VU là capacity.

### 3:35-4:35 — Spike

Nêu baseline 17 VU và burst 168 VU. Burst đạt 361.6 request/s, p95 26 ms; bucket
recovery đầu tiên về 33.8 request/s và p95 12 ms, phục hồi trong tối đa 30 giây.

### 4:35-5:35 — Soak và endurance threshold

Nêu 27 VU giữ 15 phút, 52.8-54.5 request/s, p95 tối đa 12 ms trong các full
stable bucket, 0% lỗi và memory peak 172.0 MB. Giải thích memory giảm giữa run
nên chưa đủ bằng chứng gọi là leak.

### 5:35-6:35 — Agent Skill demo

Mở `.claude/skills/performance-testing/SKILL.md`, chỉ ra bốn phase skill và chạy
một bước thật trên một nhóm endpoint hoàn chỉnh, ví dụ validator/analyzer trên
raw JTL. Cho thấy output có đủ năm label và journey-completeness check.

### 6:35-7:30 — AI critique và continuous testing

Mở `docs/AI_CRITIQUE.md` và lưu đồ. Nêu hai lỗi diễn giải quan trọng: controller
row làm đếm dư journey và overall p95 che phase của Spike. Kết thúc bằng trigger
theo risky path, confirmation run và ngưỡng regression p95.

## Trước khi upload

- Nghe lại để chắc chắn giọng rõ và toàn bộ video dài ít nhất sáu phút.
- Kiểm tra tên plan, Task Manager và số liệu có đọc được ở 1080p.
- Upload YouTube ở chế độ Unlisted, mở link trong cửa sổ ẩn danh để xác nhận.
- Chạy script đóng gói với URL thật; không sửa URL thành ví dụ hoặc placeholder.