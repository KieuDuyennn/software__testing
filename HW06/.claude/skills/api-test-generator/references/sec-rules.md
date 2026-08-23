# SEC-01..SEC-07 — attack patterns

Source: `refs/spec/eshop_requirements_README.md`. These are the security
requirements the SUT is *supposed* to satisfy; each is an oracle.

| ID | Requirement (VN) | What it means for an API test |
|---|---|---|
| SEC-01 | Mật khẩu **không** được lưu dưới dạng plaintext | Registering then reading the account back must never reveal the submitted password. Check login responses, admin user lists, and profile reads. |
| SEC-02 | Các API có tính bảo mật phải yêu cầu JWT Token hợp lệ | Every protected route must reject: no header, empty Bearer, malformed token, token signed with another key, token for a deleted user. |
| SEC-03 | API Admin phải kiểm tra `role = 'admin'` trong Token, không chỉ kiểm tra sự tồn tại của Token | A valid **non-admin** token on any `/api/admin/*` route must be refused. Existence of a token is not authorisation. |
| SEC-04 | Mọi dữ liệu user nhập vào khi hiển thị trên UI phải được escape đúng cách | Primarily a UI rule. At API level: store an XSS payload and confirm it comes back as data, not as executable markup, and that the API does not pre-render HTML. |
| SEC-05 | Truy vấn CSDL phải dùng Parameterized Query | Injection in every string parameter and path segment: `' OR 1=1--`, `'); DROP TABLE users;--`, UNION probes. Refused or neutralised — never a 500, never a leaked SQL error, never extra rows. |
| SEC-06 | API cập nhật hồ sơ không được cho phép thay đổi trường `role` từ client | Send `role: "admin"` in registration and profile-update bodies; the stored role must not change. Verify by reading the account back, not by trusting the response message. |
| SEC-07 | OTP đặt lại mật khẩu phải đủ entropy (tối thiểu 6 chữ số), có thời hạn và vô hiệu hóa sau khi dùng | Three separate assertions: length/entropy of the issued token, expiry after its window, and rejection on second use. |

## Actor matrix

Most of these need more than one actor. Set up all four before generating
security cases:

| Actor | How to obtain |
|---|---|
| Anonymous | send no `Authorization` header |
| User A | log in as `test@eshop.com` / `Test1234!` |
| User B (victim) | register a fresh account, log in, create data owned by it |
| Admin | log in as `admin@eshop.com` / `Admin123!` |

Cross every boundary deliberately: A reading B's data, A calling admin routes,
anonymous calling anything protected.

## Forged-token recipes

| Case | How |
|---|---|
| Missing | omit the header |
| Empty | `Authorization: Bearer ` |
| Malformed | `Authorization: Bearer not.a.real.token` |
| Wrong signature | sign a valid payload with a different secret |
| Tampered claim | take a real token, flip `role` to `admin`, re-encode without re-signing |
| Deleted user | log in, delete the account via admin, reuse the token |
