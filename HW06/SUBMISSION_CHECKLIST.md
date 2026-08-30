# HW06 - Hướng dẫn gom và nộp bài

MSSV: **23127184**

## 1. Bộ file nộp chính

Không chọn từng file thủ công. Chạy:

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
| Postman | `postman/collections/`, `postman/config/`, `postman/data/` | Collection, environment và data-driven files |
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
- [x] Sơ đồ generator trong `docs/design/diagram/generator-design.png` là bản
  sinh viên tự vẽ lại bằng draw.io.
- [x] Đã render 15 ảnh minh chứng Newman cho các Issue #47-#55, #59-#64 bằng
  `scripts/build-issue-evidence.py`, lấy trường verbatim từ transcript tiền-fix.
- [x] Sinh viên đã tự bố cục lại sơ đồ trong draw.io và export đè lên
  `docs/design/diagram/generator-design.png` (ngày 2026-08-30). Ảnh có MSSV
  23127184 ở box input và ở khối renderer. Hai file nháp do máy sinh
  (`generator-design.mmd`, `generator-design.svg`) đã xoá khỏi repo, và đoạn tự
  khai "draft" ở mục 12 báo cáo chính đã được thay bằng phần giải thích các
  quyết định thiết kế. Đề mục 11 liệt kê sơ đồ là một trong ba thứ TA kiểm tra
  là không do AI sinh ra.
- [x] Repository đã ở trạng thái public (kiểm tra ngày 2026-08-30 bằng
  `gh repo view KieuDuyennn/software__testing --json visibility`, kết quả
  `PUBLIC`), nên link repo, GitHub Actions và GitHub Issues trong bài nộp đều
  mở được với người chấm.
- [x] Đã chụp `evidence/screenshots/github-actions-red-one-case.png` từ run
  <https://github.com/KieuDuyennn/software__testing/actions/runs/32700593817>:
  bảng job summary thấy rõ API2 có 1 failed assertion, ba API còn lại 0,
  tổng 1.801/1/1.802.
- [x] Đã quay video demo Agent Skill sinh test cho `POST /api/register`, tải
  lên YouTube tại <https://youtu.be/zgGwFg2e8UE> và chèn link vào README cùng
  mục 12 báo cáo chính. Bản ghi màn hình gốc không lưu trong repo; `output/demo/`
  đã được đưa vào `.gitignore` để không đẩy file 18 MB lên Git.
- [x] Xác nhận bộ ba API không trùng với thành viên nhóm ngày 2026-08-24.
- [x] Điền điểm tự đánh giá 100/100 trong README.
- [x] Excel đã được đồng bộ từ nguồn 386 case, gồm audit, 20 case tự thêm và
  kết quả full run; vẫn nên mở một lần bằng Excel trước khi nộp để kiểm tra font.

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
- [ ] Thử lại các link GitHub Actions, GitHub Issues, repository và YouTube.
- [ ] Bảo đảm ảnh là ảnh thật, rõ MSSV/tài khoản/trạng thái khi rubric yêu cầu.
- [ ] Không nộp `node_modules`, `tmp`, database SQLite hay log chạy thử dư.

## 6. Việc còn lại của sinh viên cho phần data-driven

Phần chạy data-driven đã hoàn tất bằng Newman (27 iteration, 128 assertion,
không có assertion nào fail, xem `reports/*_ddt.html`). Còn đúng một ảnh cần
tự chụp để chứng minh đã dùng **Collection Runner với data file**:

1. Mở Postman, import `postman/collections/API1_FR01_Register_ddt.postman_collection.json`.
2. Chọn **Run collection** → mục **Data**, chọn file `postman/data/api1_fr01_register.csv`.
3. Kiểm tra Postman báo `10 iterations` và bấm **Preview** để thấy 10 dòng dữ liệu.
4. Bảo đảm SUT đang chạy (`npm run sut:start`), rồi bấm **Run**.
5. Chụp màn hình kết quả (thấy rõ tên file CSV và số iteration) và lưu vào
   `evidence/postman-cloud/runner-data-driven.png`.
