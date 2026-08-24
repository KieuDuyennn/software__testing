# HW06 - Hướng dẫn gom và nộp bài

MSSV: **23127184**

## 1. Bộ file nộp chính

Không chọn từng file thủ công. Sau khi hoàn tất các mục còn thiếu ở phần 3,
chạy:

```powershell
.\scripts\New-Submission.ps1 -Grade 100
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
- [x] Đã chụp Collection Runner thật tại `evidence/postman-cloud/runner.png`:
  API2 chạy local, 433 assertions, 390 pass và 43 defect-revealing failures.
- [x] Đã tạo/chạy Monitor thật tại `evidence/postman-cloud/monitor.png`. Monitor
  hoàn thành ở trạng thái Unhealthy vì Postman Cloud không truy cập được
  `localhost`; ảnh ghi rõ 129 requests, 238 failed tests và 11 errors.
- [x] Đã chụp Mock Server đang chạy và request log tại
  `evidence/postman-cloud/mock-server.png`.
- [x] Đã có ảnh generator và file Mermaid chỉnh sửa được trong
  `docs/design/diagram/`.
- [ ] Sinh viên mở source trong draw.io, tự rà soát/chỉnh và bảo đảm giải thích
  được toàn bộ sơ đồ trong video (điều kiện tác quyền của đề).
- [ ] (Tùy chọn) Chèn link video YouTube demo vào README và báo cáo chính.
- [x] Xác nhận bộ ba API không trùng với thành viên nhóm ngày 2026-08-24.
- [x] Điền điểm tự đánh giá 100/100 trong README.
- [x] Excel đã được đồng bộ từ nguồn 386 case, gồm audit, 20 case tự thêm và
  kết quả full run; vẫn nên mở một lần bằng Excel trước khi nộp để kiểm tra font.

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

## 6. Việc còn lại của sinh viên cho phần data-driven

Phần chạy data-driven đã hoàn tất bằng Newman (27 iteration, 128 assertion,
không có assertion nào fail — xem `reports/*_ddt.html`). Còn đúng một ảnh cần
tự chụp để chứng minh đã dùng **Collection Runner với data file**:

1. Mở Postman, import `collections/API1_FR01_Register_ddt.postman_collection.json`.
2. Chọn **Run collection** → mục **Data**, chọn file `data/api1_fr01_register.csv`.
3. Kiểm tra Postman báo `10 iterations` và bấm **Preview** để thấy 10 dòng dữ liệu.
4. Bảo đảm SUT đang chạy (`npm run sut:start`), rồi bấm **Run**.
5. Chụp màn hình kết quả (thấy rõ tên file CSV và số iteration) và lưu vào
   `evidence/postman-cloud/runner-data-driven.png`.
