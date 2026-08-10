# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr01_account_registration\fr01.registration.spec.ts >> FR-01 Account registration >> FR01-TC-01a [positive] all three fields valid so the account is created
- Location: automation\tests\fr01_account_registration\fr01.registration.spec.ts:123:5

# Error details

```
Error: browserContext.close: Protocol error (Browser.removeBrowserContext): can't access property "_maybeDontRestoreTabs", this._windows[aWindow.__SSi] is undefined
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - link "EShop" [ref=e5] [cursor=pointer]:
      - /url: /
    - navigation [ref=e6]:
      - link "Giỏ hàng" [ref=e7] [cursor=pointer]:
        - /url: /cart
      - link "Đăng nhập" [ref=e8] [cursor=pointer]:
        - /url: /login
      - link "Đăng ký" [ref=e9] [cursor=pointer]:
        - /url: /register
  - main [ref=e10]:
    - generic [ref=e11]:
      - heading "Đăng Ký" [level=2] [ref=e12]
      - generic [ref=e13]:
        - generic [ref=e14]:
          - generic [ref=e15]: Username
          - textbox [ref=e16]
        - generic [ref=e17]:
          - generic [ref=e18]: Mật khẩu
          - textbox [ref=e19]
        - link "Quên mật khẩu?" [ref=e21] [cursor=pointer]:
          - /url: /forgot-password
        - button "Sign In" [ref=e22] [cursor=pointer]
        - generic [ref=e23]:
          - text: Chưa có tài khoản?
          - link "Đăng ký ngay" [ref=e24] [cursor=pointer]:
            - /url: /register
  - contentinfo [ref=e25]: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```