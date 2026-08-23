# HW05 – Kiểm thử Hiệu năng (Performance Testing)

> Bản dịch tiếng Việt của `ver2.md` (bản yêu cầu chính thức). Bản tiếng Anh là bản gốc có giá trị khi có tranh chấp về cách hiểu.

## 1. Thông tin chung

| **Mã bài tập** | **HW05-AI** |
| --- | --- |
| **Thời lượng** | 10 giờ |
| **Hạn nộp** | Xem link nộp bài trên Moodle |
| **Hình thức** | Bài tập cá nhân |
| **Nộp bài** | Moodle (báo cáo) |
| **Giảng viên & Trợ giảng** | TS. Lâm Quang Vũ / TS. Trần Duy Hoàng / ThS. Trần Thị Bích Hạnh / ThS. Trương Phước Lộc / ThS. Hồ Tuấn Thanh |
| **Liên hệ** | lqvu@fit.hcmus.edu.vn / tdhoang@fit.hcmus.edu.vn / ttbhanh@fit.hcmus.edu.vn / tploc@fit.hcmus.edu.vn / hthanh@fit.hcmus.edu.vn |
| **Chính sách AI** | Mở — **bắt buộc** phải có phần khai báo và đính kèm AI Audit Report |
| **Mức Bloom-AI yêu cầu** | G9.1 → G9.6, tùy theo bài tập (xem phần *CLO Mapping*) |

## 2. Nguyên tắc định hướng

Các nguyên tắc sau định nghĩa cách bạn được kỳ vọng làm việc xuyên suốt chuỗi bài tập của môn học. Hãy đọc kỹ trước khi bắt đầu, vì bài nộp của bạn sẽ được chấm dựa trên các nguyên tắc này.

- **Chiến lược AI-First.** Bạn bắt buộc phải áp dụng AI vào các kỹ thuật kiểm thử đã học trên lớp. Tuy nhiên, điều này **không** có nghĩa là đưa ra một prompt chung chung duy nhất kiểu *"chạy load test và cho tôi biết hiệu năng có tốt không."* Thay vào đó, bạn phải dẫn dắt AI qua **từng bước** của kỹ thuật đúng như cách đã được dạy, sử dụng AI như một trợ lý có kỷ luật chứ không phải một hộp đen.
- **Human review (Con người rà soát).** Mọi kết quả do AI tạo ra đều phải được chính bạn — sinh viên — rà soát cẩn thận. Bạn chịu trách nhiệm hoàn toàn về tính đúng đắn của các kết quả này. Bạn được kỳ vọng phải thực hiện mọi chỉnh sửa và tinh chỉnh cần thiết — nộp nguyên output thô của AI mà không rà soát là **không được chấp nhận**.
- **AI Audit Report.** Toàn bộ quá trình sử dụng AI phải được ghi lại trong một nhật ký đầy đủ. Bạn được khuyến khích xây dựng các Agent Skill có thể tự động thực hiện những hoạt động này cho các bài tập tương tự. Nếu bạn **không** dùng AI, bạn vẫn phải khai báo điều đó một cách tường minh.
- **Tài liệu hóa.** Toàn bộ quy trình làm việc phải được tài liệu hóa ở định dạng text như Markdown.
- **Chất lượng hơn là hoàn thành.** Bài của bạn được chấm không chỉ dựa trên việc có hoàn thành hay không, mà còn dựa trên **số lượng và chất lượng** của các sản phẩm bàn giao: test plan, file dữ liệu, log thô và các report view, bằng chứng về tài nguyên/phần cứng, video demo, phần phản biện phân tích của AI, và các link tham chiếu.

## 3. Chuẩn đầu ra

Sau khi hoàn thành bài tập này, bạn sẽ có thể:

- Thiết kế và chạy các bài kiểm thử hiệu năng **Load, Stress và Spike** nhắm vào backend API của SUT bằng JMeter (hoặc k6).
- Thu thập và trình bày các chỉ số hiệu năng kèm giám sát tài nguyên và nhiều loại report view, đồng thời xác định **ngưỡng chịu tải (endurance threshold)** trên chính phần cứng của bạn.
- Dùng AI để phân tích kết quả, sau đó phản biện phân tích đó một cách có phê phán — chỉ ra chỗ AI **diễn giải sai chỉ số** và những đề xuất tối ưu nào của nó là khả thi.
- Đề xuất một pipeline kiểm thử hiệu năng liên tục (continuous performance testing).
- Thể hiện năng lực Bloom-AI ở các mức **G9.2 (Apply)**, **G9.3 (Analyse)**, **G9.4 (Collaborate)** và **G9.6 (Disrupt)**.

## 4. Hệ thống được kiểm thử (SUT)

**SUT:** EShop — một ứng dụng demo thương mại điện tử tiếng Việt được thiết kế để thực hành kiểm thử.

**Repository:** https://github.com/ttbhanh/eshop-sut

Các tính năng của ứng dụng được tổ chức thành các nhóm (pool) sau:

- **Pool A — Xác thực, Danh mục và Sản phẩm**
    - FR-01: Đăng ký tài khoản
    - FR-02: Đăng nhập và khóa tài khoản
    - FR-03: Quên mật khẩu và đặt lại mật khẩu (hai bước)
    - FR-04: Quản lý hồ sơ cá nhân
    - FR-05: Danh sách và tìm kiếm sản phẩm
    - FR-06: Xem chi tiết sản phẩm
- **Pool B — Giỏ hàng và Thanh toán**
    - FR-07: Giỏ hàng
    - FR-08: Thanh toán (Checkout)
    - FR-09: Mã giảm giá (Coupon)
    - FR-10: Máy trạng thái đơn hàng (Order state machine)
    - FR-11: Xem lịch sử đơn hàng (người dùng)
- **Pool C — Web Admin**
    - FR-12: Kiểm soát truy cập
    - FR-13: Dashboard
    - FR-14: Quản lý danh mục (CRUD)
    - FR-15: Quản lý sản phẩm (CRUD)
    - FR-16: Nhập sản phẩm từ CSV
    - FR-17: Quản lý mã giảm giá (CRUD)
    - FR-18: Quản lý đơn hàng (admin)
    - FR-19: Quản lý người dùng (admin)
- **Pool D — Ứng dụng Mobile**

SUT cung cấp một REST backend API mà frontend web tiêu thụ; tra cứu repository để biết chính xác các endpoint và cổng.

## 5. Phạm vi — Lựa chọn Endpoint

Nhắm vào **ba nhóm endpoint** của backend API, ánh xạ mỗi nhóm vào API của SUT:

- **Read-heavy (nặng về đọc)** — ví dụ: danh sách/tìm kiếm sản phẩm và chi tiết sản phẩm.
- **Auth-heavy (nặng về xác thực)** — ví dụ: đăng nhập, có tính đến hành vi khóa tài khoản.
- **Transactional (giao dịch)** — ví dụ: thêm vào giỏ hàng và thanh toán / tạo đơn hàng.

Như các bài tập trước, phải đảm bảo lựa chọn của bạn **không trùng** với các thành viên khác trong nhóm: không hai thành viên nào được kiểm thử **cùng một workflow**.

## 6. Yêu cầu

Với mỗi task dưới đây, hãy tài liệu hóa quy trình của bạn trong báo cáo chính và đính kèm bằng chứng bắt buộc. Xem lại các bài giảng liên quan về kiểm thử hiệu năng trước khi bắt đầu.

### Task 1 — Thiết kế và thực thi test với sự hỗ trợ của AI

Theo chiến lược AI-first, dùng công cụ AI để thiết kế và sinh ra các test plan, sau đó rà soát, sửa chữa và chịu trách nhiệm hoàn toàn về chúng.

- **Thiết kế và sinh bằng AI.** Dẫn dắt công cụ AI — **từng bước một**, không phải bằng một prompt chung chung duy nhất — để thiết kế và sinh ra ba test plan: **Load**, **Stress** và **Spike**. **Cả ba test plan đều phải thực thi cùng một workflow end-to-end, bao phủ cả ba nhóm endpoint: auth-heavy, read-heavy và transactional.** Ví dụ: một virtual user có thể đăng nhập, duyệt hoặc tìm kiếm sản phẩm, rồi thêm một món vào giỏ hàng và hoàn tất thanh toán. Để AI hỗ trợ chọn các tham số thực tế (think-time, ramp-up, số thread / virtual user) **cho từng kịch bản**, và giải thích ngắn gọn **workflow đó bao phủ từng nhóm endpoint như thế nào**.
- **Làm workflow hướng dữ liệu (data-driven).** Dùng dữ liệu đầu vào CSV trong workflow end-to-end để tham số hóa các request (ví dụ: thông tin đăng nhập, product ID, hoặc payload đơn hàng). Bạn **có thể dùng một hoặc nhiều file CSV**, tùy theo workflow của bạn cho phù hợp.
- **Dùng ba loại report view khác nhau.** Xuyên suốt ba test plan, hãy dùng ba loại listener/report **khác biệt** (ví dụ: View Results Tree, Summary Report, Aggregate Report); không được lặp lại cùng một loại. *(Thuật ngữ JMeter; người dùng k6 cung cấp các output tương đương và khác biệt.)*
- **Đặt tên mỗi test plan** theo mẫu `{StudentID}_{ScenarioType}_{YYYYMMDD}`.
- **Rà soát và sửa (human review).** Phản biện có phê phán các test plan do AI sinh ra và sửa chúng. Báo cáo những gì AI làm sai hoặc bỏ sót — ví dụ: ramp-up hoặc think-time phi thực tế, số thread sai, assertion yếu, hoặc thiếu xử lý khóa tài khoản — và giải thích **vì sao** nó bỏ sót (chất lượng prompt, giới hạn của mô hình, hay đặc thù của endpoint). Bạn chịu trách nhiệm hoàn toàn về các test plan cuối cùng.
- **Chạy càng đầy đủ càng tốt, kèm bằng chứng.** Thực thi **cả ba** kịch bản và với mỗi lần chạy, chụp lại ảnh màn hình công cụ **cùng với** mức sử dụng tài nguyên của tiến trình backend (htop / Task Manager / Activity Monitor), cộng thêm một báo cáo phần cứng (ảnh chụp dxdiag / screenfetch và một bảng thông số). Khi các lần chạy Stress/Spike kích hoạt cơ chế khóa đăng nhập sau 3 lần thất bại, hãy reset nó giữa các lần chạy và tài liệu hóa các bước. Xuất ra các file log `.jtl` thô và các thư mục HTML report.
- **Xác định ngưỡng chịu tải (endurance threshold).** Chạy một bài endurance/soak test ngắn (khoảng **10–15 phút** ở mức tải duy trì) để tìm ra ngưỡng của phần cứng bạn một cách thực nghiệm, báo cáo bằng **con số cụ thể** (ví dụ: RPS ổn định tối đa, trần bộ nhớ).
- **Quay video demo.** Video YouTube dạng unlisted, tổng thời lượng **tối thiểu 6 phút** (có thể tách thành một clip cho mỗi kịch bản), cho thấy công cụ và trình giám sát tài nguyên **trong cùng một khung hình**, kèm lời thuyết minh tiếng Việt do chính bạn thực hiện.
- **Báo cáo lỗi.** Ghi nhận mọi bug thật hoặc vấn đề hiệu năng (response lỗi, crash, hồi quy chức năng) lên trang GitHub Issues của bạn kèm ảnh chụp màn hình. Việc ghi nhận các vấn đề hiệu năng như độ trễ cao hay tỷ lệ lỗi tăng được **khuyến khích** nhưng không bị trừ điểm nếu thiếu.

### Task 2 — Phân tích bằng AI và săn lỗi diễn giải sai

Theo chiến lược AI-first, dùng AI để phân tích kết quả của bạn, sau đó phản biện có phê phán những gì nó tạo ra — phần phân tích là output của AI, còn phần rà soát là của bạn.

- **Phân tích bằng AI.** Sau khi thu thập kết quả thô, prompt một công cụ AI để phân tích các file log `.jtl` và đề xuất các ngưỡng hiệu năng.
- **Rà soát và sửa (human review).** Phản biện có phê phán phân tích của AI và chỉ ra chỗ nó **diễn giải sai hoặc đọc sai** các chỉ số. Với mỗi chỗ diễn giải sai, hãy trích dẫn **giá trị đúng từ file log `.jtl` thô** của bạn và giải thích lỗi sai đó.
- **Đánh giá các đề xuất của AI.** Cho AI đề xuất các phương án tối ưu (ví dụ: thêm database index, connection pool, hoặc bật SQLite WAL) và phân loại từng đề xuất là **khả thi (feasible)** hay **ảo giác (hallucinated)**, kèm lập luận.

### Task 3 — Đề xuất Kiểm thử Hiệu năng Liên tục (Disrupt)

- Trong phần kết luận, hãy đề xuất một **mô hình kiểm thử hiệu năng liên tục** có khả năng theo dõi các commit của SUT, quyết định xem có nên chạy test hiệu năng hay không, và cảnh báo các hồi quy về p95. Bao gồm một **lưu đồ (flow chart)** và phần thảo luận về các **đánh đổi (trade-off)** (chi phí, cảnh báo giả).

## 7. Agent Skill

- Bạn được khuyến khích xây dựng một Agent Skill áp dụng quy trình kiểm thử hiệu năng và phân tích log này, để có thể tái sử dụng cho các endpoint khác trong những bài kiểm thử tương lai.
- Nộp kèm skill cùng một video demo (link YouTube) cho thấy đầy đủ từ đầu đến cuối cách bạn dùng skill đó trên một nhóm endpoint hoàn chỉnh.

## 8. Công cụ được phép và mức Bloom-AI

Bạn có thể dùng các công cụ sau, và phải khai báo chúng trong AI Audit Report:

- JMeter (mặc định) hoặc k6 (điểm thưởng).
- Bất kỳ công cụ AI nào bạn chọn (ví dụ: ChatGPT, Claude, Gemini) — để phân tích log.
- Một trình giám sát tài nguyên (htop / Task Manager / Activity Monitor).

Mức Bloom-AI yêu cầu cho bài tập này là **G9.2 (Apply)**, **G9.3 (Analyse)**, **G9.4 (Collaborate)** và **G9.6 (Disrupt)**.

## 9. AI Audit Report (Phụ lục bắt buộc)

Đính kèm AI Audit Report như một phụ lục. Sử dụng nội dung của các AI Template được cung cấp nếu cần.

- Nếu bạn **không** dùng AI, hãy khai báo: *"I do not use any AI help in this exercise."*
- Nếu bạn **có** dùng AI, hãy khai báo: *"I use AI tools for the following tasks,"* và bao gồm các thông tin sau cho **mỗi lượt tương tác**:
    - Tên công cụ AI
    - Ngày và giờ
    - Prompt của bạn
    - Output của AI

Để đơn giản hóa quy trình này, bạn được khuyến khích tạo một skill hoặc rule tự động trích xuất các thông tin trên sau mỗi phiên làm việc với AI.

## 10. AI Critique (200–300 từ, bắt buộc)

Viết một đoạn văn **200–300 từ** phản biện AI. Trả lời các câu hỏi sau: AI đã sai, thiên lệch, hoặc thiếu sót ở chỗ nào? Vì sao nó không phát hiện ra vấn đề đó? Bạn đã rút ra nguyên tắc gì về việc cộng tác với AI qua bài tập này?

Sử dụng nội dung của các AI Template được cung cấp nếu cần.

## 11. Ràng buộc chống gian lận bằng AI

Bài tập này dựa trên bằng chứng thực thi **thật và truy vết được**. Những mục sau **không được** do AI sinh ra hoặc bịa đặt, và TA sẽ kiểm chứng chúng khi chấm bài:

- Tên file test plan, phải khớp mẫu `{StudentID}_{ScenarioType}_{YYYYMMDD}`.
- Các file log `.jtl` thô, đính kèm **đầy đủ** — không chỉ phần tóm tắt.
- Video demo, phải cho thấy công cụ và trình giám sát tài nguyên trong **cùng một khung hình** kèm giọng thuyết minh của chính bạn.
- Báo cáo phần cứng, có **hostname trùng khớp** với các lần triển khai ở các bài tập trước.

## 12. Git Commit Log

- Tạo một Git commit mới cho **mỗi bước** của quy trình (ví dụ: test plan của từng kịch bản, phần phân tích AI, và đề xuất kiểm thử liên tục).
- Cung cấp Git commit log ở định dạng file text.

## 13. Bảo vệ vấn đáp

**30% sinh viên** được chọn ngẫu nhiên có thể được mời tham gia buổi bảo vệ vấn đáp 5–7 phút trong tuần sau hạn nộp, để giải thích cách bạn đã hoàn thành bài tập này.

## 14. Quy định nộp bài

- **Định dạng tên file:** `<StudentID>_HW05_AI_Performance_<SelfAssessedGrade>.zip`
    - *SelfAssessedGrade:* một số 3 chữ số trong khoảng [000, 100].
    - *Ví dụ:* `25127001_HW05_AI_Performance_090.zip`
- **Nội dung bắt buộc trong file `.zip`:**
    - Báo cáo chính (Markdown + PDF), bao gồm báo cáo kiểm thử hiệu năng và phần phản biện phân tích AI của bạn.
    - Link repository GitHub công khai (chứa test plan và file dữ liệu).
    - Ba test plan (Load / Stress / Spike) theo đúng quy ước đặt tên.
    - Ba file log `.jtl` thô và ba thư mục HTML report.
    - Ảnh chụp màn hình trình giám sát tài nguyên và thông số phần cứng.
    - Link video demo YouTube dạng unlisted.
    - AI Critique và AI Audit Report (Markdown + PDF).
    - Git commit log (file text).
    - Báo cáo bug, kèm ảnh chụp màn hình các issue trên GitHub Issues (nếu có).
    - Một file `README.md` chứa bảng tự đánh giá (bên dưới) và một báo cáo tóm tắt kiểm thử: các kịch bản đã chạy; các nhóm endpoint đã phủ; ngưỡng chịu tải (kèm số liệu); số lượng bug / vấn đề hiệu năng; và link video demo.
    - Mọi tài liệu hỗ trợ khác.
- Nộp lên Moodle. Về hạn nộp, xem link nộp bài.

## 15. Bảng đánh giá

| **STT** | **Tiêu chí** | **Điểm** | **Điểm tự đánh giá** |
| --- | --- | --- | --- |
| **1** | Task 1 — Load testing | 20 |  |
| **2** | Task 1 — Stress testing | 20 |  |
| **3** | Task 1 — Spike testing | 20 |  |
| **4** | Task 2 — Phân tích AI + săn lỗi diễn giải sai (kèm giá trị đúng từ log thô) | 10 |  |
| **5** | Task 3 — Đề xuất Kiểm thử Hiệu năng Liên tục (G9.6) | 10 |  |
| **6** | Agent Skills | 10 |  |
|  | **Tổng** | **100** |  |

## 16. Tài liệu tham khảo

- ISTQB Foundation Level Syllabus (phiên bản mới nhất).
- Hardman, P. (2025). *A Post-AI Learning Taxonomy.*
- Fuster Rabella, M. (2025). *OECD Education Working Paper No. 338.*
- Anthropic (2025). *Building Reliable AI Test Agents* — engineering blog.
- Tài liệu DeepEval & Promptfoo — các framework kiểm thử LLM.

## 17. Quy định khác

- **Không** chấp nhận nộp trễ.
- Thiếu bất kỳ tài liệu bắt buộc nào sẽ bị **0 điểm**.
- Sao chép giữa các sinh viên — **bao gồm cả prompt** — sẽ bị **0 điểm cho cả hai bên**.
