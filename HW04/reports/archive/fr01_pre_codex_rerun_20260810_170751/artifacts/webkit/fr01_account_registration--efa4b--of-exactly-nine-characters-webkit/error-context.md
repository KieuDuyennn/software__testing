# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr01_account_registration\fr01.registration.spec.ts >> FR-01 Account registration >> FR01-BVA-03 [edge] password of exactly nine characters
- Location: automation\tests\fr01_account_registration\fr01.registration.spec.ts:123:5

# Error details

```
Error: expect(page).toHaveURL(expected) failed

Expected pattern: /\/login$/
Received string:  "http://localhost:5173/register"
Timeout: 10000ms

Call log:
  - Expect "toHaveURL" with timeout 10000ms
    23 × locator resolved to <html lang="en">…</html>
       - unexpected value "http://localhost:5173/register"

```

```yaml
- banner:
  - link "EShop":
    - /url: /
  - navigation:
    - link "Giỏ hàng":
      - /url: /cart
    - link "Đăng nhập":
      - /url: /login
    - link "Đăng ký":
      - /url: /register
- main:
  - heading "Đăng Ký Tài Khoản" [level=2]
  - text: Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT. Họ Tên
  - textbox: Nguyen Van A
  - text: Email
  - textbox: fr01.fr01-bva-03.msn1tz6ggi8@example.com
  - text: Mật khẩu
  - textbox: Pa1!abcde
  - paragraph: "Yêu cầu: Tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt."
  - button "Đăng Ký"
  - text: Đã có tài khoản?
  - link "Đăng nhập":
    - /url: /login
- contentinfo: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  173 |             description: `omitting ${row.omit_field} leaves no way to observe whether a row was created`,
  174 |           });
  175 |         } else {
  176 |           const login = await request.post(`${API_URL}/api/login`, {
  177 |             data: { email, password: row.password },
  178 |             failOnStatusCode: false,
  179 |           });
  180 |           if (row.expect_outcome === 'success') {
  181 |             expect(login.status(), `${email} was reported created, so it must be usable`).toBe(200);
  182 |             const body = await login.json();
  183 |             expect(body.user?.email, 'the stored e-mail must be the one that was sent').toBe(email);
  184 |             expect(body.user?.name, 'the stored name must be the one that was sent').toBe(row.name);
  185 |           } else {
  186 |             expect(
  187 |               login.ok(),
  188 |               `the request was rejected, so ${email} must not have been written`,
  189 |             ).toBeFalsy();
  190 |           }
  191 |         }
  192 |         return;
  193 |       }
  194 | 
  195 |       /* ---------- ui rows ---------- */
  196 |       await registerPage.goto();
  197 |       await expect(registerPage.heading).toBeVisible();
  198 |       await registerPage.register({ name: row.name, email, password: row.password });
  199 | 
  200 |       switch (row.expect_channel) {
  201 |       case 'native': {
  202 |         // Pattern 1 - the browser's own constraint validation, not an app message.
  203 |         const empty = (['name', 'email', 'password'] as const).filter(
  204 |           (field) => (field === 'email' ? email : row[field]) === '',
  205 |         );
  206 |         expect(
  207 |           empty.length,
  208 |           'a native-validation row must leave at least one required field empty',
  209 |         ).toBeGreaterThan(0);
  210 | 
  211 |         const inputOf = {
  212 |           name: registerPage.nameInput,
  213 |           email: registerPage.emailInput,
  214 |           password: registerPage.passwordInput,
  215 |         };
  216 |         for (const field of empty) {
  217 |           const valid = await registerPage.isValid(inputOf[field]);
  218 |           // The message is browser-supplied and differs per engine, so it is never an
  219 |           // expected value - it is fetched only when the case is about to fail, purely
  220 |           // so the report says what the browser actually did.
  221 |           const reported = valid
  222 |             ? ` (browser reported: "${await registerPage.validationMessageOf(inputOf[field])}")`
  223 |             : '';
  224 |           expect(
  225 |             valid,
  226 |             `${field} is required, so the browser must refuse to submit the form${reported}`,
  227 |           ).toBe(false);
  228 |         }
  229 |         await expect(page).toHaveURL(/\/register$/);
  230 |         await expect(
  231 |           registerPage.errorBanner,
  232 |           'the form never reached the app, so it must not have rendered an app error',
  233 |         ).toBeHidden();
  234 |         return;
  235 |       }
  236 | 
  237 |       case 'banner': {
  238 |         // Pattern 1 - the user must be told what is wrong, and about which field.
  239 |         // Soft on purpose: when the app shows no banner at all, the interesting question
  240 |         // is what it did instead, and a hard failure here would abort before the check
  241 |         // below answers it. Soft failures still fail the test at the end.
  242 |         await expect
  243 |           .soft(
  244 |             registerPage.errorBanner,
  245 |             'registration was refused, so the reason must be shown to the user',
  246 |           )
  247 |           .toBeVisible();
  248 |         await expect
  249 |           .soft(
  250 |             registerPage.errorBanner,
  251 |             `the message must name the ${row.expect_signal} field, otherwise the user cannot act on it`,
  252 |           )
  253 |           .toHaveText(keywordFor(row.expect_signal, row.tc_id));
  254 |         await expect.soft(page).toHaveURL(/\/register$/);
  255 | 
  256 |         // Pattern 3 - a refused registration must not have written an account anyway.
  257 |         // Skipped for the two rows aimed at the seeded account, which exists by design.
  258 |         if (!targetsSeededAccount(row)) {
  259 |           const login = await request.post(`${API_URL}/api/login`, {
  260 |             data: { email, password: row.password },
  261 |             failOnStatusCode: false,
  262 |           });
  263 |           expect(
  264 |             login.ok(),
  265 |             `registration was refused, so ${email} must not be a usable account`,
  266 |           ).toBeFalsy();
  267 |         }
  268 |         return;
  269 |       }
  270 | 
  271 |       case 'redirect': {
  272 |         // Pattern 1 - the app's own success signal.
> 273 |         await expect(page).toHaveURL(new RegExp(`${row.expect_signal}$`));
      |                            ^ Error: expect(page).toHaveURL(expected) failed
  274 |         // Not "the error banner is hidden": that element belongs to /register and cannot
  275 |         // exist here, so such a check could never fail. The falsifiable statement is that
  276 |         // the registration form itself is gone - if the app had stayed put and rendered an
  277 |         // error, its submit button would still be on screen.
  278 |         await expect(
  279 |           registerPage.submitButton,
  280 |           'the app claims the account was created, so the registration form must be gone',
  281 |         ).toBeHidden();
  282 | 
  283 |         // Pattern 3 - and the account must actually exist, with the data that was typed.
  284 |         // A redirect on its own proves navigation, not persistence.
  285 |         const login = await request.post(`${API_URL}/api/login`, {
  286 |           data: { email, password: row.password },
  287 |           failOnStatusCode: false,
  288 |         });
  289 |         expect(
  290 |           login.status(),
  291 |           `the UI reported success, so ${email} must be able to log in`,
  292 |         ).toBe(200);
  293 |         const body = await login.json();
  294 |         expect(body.user?.email, 'the stored email must be the one that was submitted').toBe(email);
  295 |         expect(body.user?.name, 'the stored name must be the one that was submitted').toBe(row.name);
  296 |         return;
  297 |       }
  298 | 
  299 |       default:
  300 |         // Reached only if the data file carries a channel this spec does not implement.
  301 |         // Failing here is the point: silently treating it as one of the known branches
  302 |         // could pass a case that was written to be refused.
  303 |         throw new Error(
  304 |           `${row.tc_id}: unknown expect_channel "${row.expect_channel}" - ` +
  305 |             'expected native, banner, redirect or api',
  306 |         );
  307 |       }
  308 |     });
  309 |   }
  310 | });
  311 | 
```