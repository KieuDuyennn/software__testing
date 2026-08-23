# HW06 - Hướng dẫn gom và nộp bài

MSSV: **23127184**

## 1. Bộ file nộp chính

Không chọn từng file thủ công. Sau khi hoàn tất các mục còn thiếu ở phần 3,
chạy:

```powershell
.\scripts\New-Submission.ps1 -Grade 100 -VideoUrl https://youtu.be/VIDEO_ID
```

Script sẽ kiểm tra, tạo thư mục để xem lại tại `output/submission-ready/`, sau
đó tạo file duy nhất cần tải lên Moodle:

`output/23127184_HW06_AI_API_100.zip`

## 2. Bản đồ thư mục

| Nhóm | Vị trí | Mục đích |
|---|---|---|
| Báo cáo chính | `23127184_HW06_REPORT.md`, `output/pdf/` | Bản Markdown và PDF để chấm |
| Test case | `testcases/` | Excel tổng hợp và JSON nguồn |
| Postman | `collections/`, `config/`, `data/` | Collection, environment và data-driven files |
| Kết quả chạy | `reports/` | Newman HTML/JSON và summary |
| Minh chứng | `evidence/` | Ảnh thật, console log và Git commit log |
| Tài liệu chi tiết | `docs/` | Phase, bug, CI/CD, audit, critique và generator |
| Mã tái tạo | `scripts/`, `.claude/` | Runner và Agent Skill |
| Tài liệu tham khảo | `refs/`, `eshop/` | Chỉ để đối chiếu; không cần gom thủ công |

## 3. Việc bắt buộc còn thiếu trước khi đóng gói

- [x] Chụp `evidence/screenshots/postman-console-x-student-id.png` có dòng
  `[HW06] X-Student-Id=23127184` từ một request chạy thật.
- [ ] Chụp kết quả Runner, Monitor và Mock Server vào
  `evidence/postman-cloud/runner.png`, `monitor.png`, `mock-server.png`.
- [x] Đã có ảnh generator và file Mermaid chỉnh sửa được trong
  `docs/design/diagram/`.
- [ ] Sinh viên mở source trong draw.io, tự rà soát/chỉnh và bảo đảm giải thích
  được toàn bộ sơ đồ trong video (điều kiện tác quyền của đề).
- [ ] Chèn link video YouTube demo vào README và báo cáo chính.
- [x] Xác nhận bộ ba API không trùng với thành viên nhóm ngày 2026-08-24.
- [x] Điền điểm tự đánh giá 100/100 trong README.
- [ ] Mở Excel kiểm tra hình thức và lưu bản cuối.

Chi tiết cách chụp minh chứng nằm tại `evidence/REQUIRED_USER_EVIDENCE.md`.

## 4. Kiểm tra nhanh

```powershell
.\scripts\New-Submission.ps1 -PreflightOnly
git status --short
```

Kết quả đúng là preflight không báo thiếu file, file ZIP mở được, và branch
`hw6` không có thay đổi cần commit (ngoài các file cá nhân có chủ ý).

## 5. Trước khi tải lên Moodle

- [ ] Tên ZIP đúng mẫu `23127184_HW06_AI_API_<000-100>.zip`.
- [ ] Mở ZIP và đọc thử README, hai PDF, Excel và một Newman HTML report.
- [ ] Thử các link GitHub Actions, GitHub Issues, repository và YouTube.
- [ ] Bảo đảm ảnh là ảnh thật, rõ MSSV/tài khoản/trạng thái khi rubric yêu cầu.
- [ ] Không nộp `node_modules`, `tmp`, database SQLite hay log chạy thử dư.
