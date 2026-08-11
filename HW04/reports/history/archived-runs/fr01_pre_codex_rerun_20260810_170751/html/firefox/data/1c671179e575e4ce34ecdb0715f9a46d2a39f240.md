# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr01_account_registration\fr01.registration.spec.ts >> FR-01 Account registration >> FR01-TC-03 [negative] name key missing from the request body
- Location: automation\tests\fr01_account_registration\fr01.registration.spec.ts:123:5

# Error details

```
Error: http://localhost:3000/api/register status

expect(received).toBe(expected) // Object.is equality

Expected: 400
Received: 200
```

```
Error: the request was rejected, so fr01.fr01-tc-03.msn1f436ed4@example.com must not have been written

expect(received).toBeFalsy()

Received: true
```

# Test source

```ts
  89  |     `${tcId}: expect_signal "${field}" is not a known field - fix the data file`,
  90  |   ).toBeDefined();
  91  |   return keyword;
  92  | }
  93  | 
  94  | function resolveEmail(raw: string, tcId: string): string {
  95  |   if (raw === '{{UNIQUE}}') return `fr01.${tcId.toLowerCase()}.${RUN_ID}@example.com`;
  96  |   if (raw === '{{EXISTING}}') return SEED_EMAIL;
  97  |   // Same address, different case - the point of OQ-09 is whether that is the same account.
  98  |   if (raw === '{{EXISTING_UPPER}}') return SEED_EMAIL.toUpperCase();
  99  |   return raw.replace('{{RUN}}', RUN_ID);
  100 | }
  101 | 
  102 | /** Is this row aimed at the seeded account? Those rows must not assert "nothing exists". */
  103 | function targetsSeededAccount(row: RegistrationCase): boolean {
  104 |   return row.email === '{{EXISTING}}' || row.email === '{{EXISTING_UPPER}}';
  105 | }
  106 | 
  107 | test.describe('FR-01 Account registration', () => {
  108 |   // `playwright` is worker-scoped, so it is usable here; the `request` fixture is not.
  109 |   test.beforeAll(async ({ playwright }) => {
  110 |     const api = await playwright.request.newContext();
  111 |     const seeded = await api.post(`${API_URL}/api/register`, {
  112 |       data: { name: SEED_NAME, email: SEED_EMAIL, password: SEED_PASSWORD },
  113 |       failOnStatusCode: false,
  114 |     });
  115 |     expect(
  116 |       seeded.ok(),
  117 |       `could not seed the existing account ${SEED_EMAIL} - TC-09 and TC-21 have no baseline`,
  118 |     ).toBeTruthy();
  119 |     await api.dispose();
  120 |   });
  121 | 
  122 |   for (const row of cases) {
  123 |     test(caseTitle(row), async ({ page, request, registerPage }) => {
  124 |       const email = resolveEmail(row.email, row.tc_id);
  125 | 
  126 |       // Recorded in the report so a reader knows this row is not using the spec password.
  127 |       if (row.bypass === 'password-gate') {
  128 |         test.info().annotations.push({
  129 |           type: 'Data note',
  130 |           description:
  131 |             'carries a password that satisfies the client-side gate, so the case can ' +
  132 |             'reach the rule it was written for (see TC_Matrix_FR01.md, bypass column)',
  133 |         });
  134 |       }
  135 | 
  136 |       /* ---------- api rows: the form has no way to send these ---------- */
  137 |       if (row.level === 'api') {
  138 |         const payload: Record<string, string> = {
  139 |           name: row.name,
  140 |           email,
  141 |           password: row.password,
  142 |         };
  143 |         if (row.omit_field) delete payload[row.omit_field];
  144 | 
  145 |         const response = await request.post(`${API_URL}/api/register`, {
  146 |           data: payload,
  147 |           failOnStatusCode: false,
  148 |         });
  149 | 
  150 |         // Pattern 2 - contract assertion.
  151 |         if (row.expect_outcome === 'success') {
  152 |           await expectApiResponse(response, Number(row.expect_signal), (body) => {
  153 |             expect(body.id, 'a created account must come back with its identifier').toEqual(
  154 |               expect.any(Number),
  155 |             );
  156 |           });
  157 |         } else {
  158 |           // Soft, so a wrong status does not abort before the check below finds out
  159 |           // whether the account was created anyway. Both facts belong in the report.
  160 |           expect
  161 |             .soft(response.status(), `${response.url()} status`)
  162 |             .toBe(Number(row.expect_signal));
  163 |         }
  164 | 
  165 |         // Pattern 3 - the status code is a claim; whether the row was written is the fact.
  166 |         // A 400 that inserts anyway, or a 200 that inserts nothing, both pass on status alone.
  167 |         if (row.omit_field === 'email' || row.omit_field === 'password') {
  168 |           // No observable check available: /api/login is keyed on e-mail and verifies the
  169 |           // password, so a request that omitted either one cannot be looked up afterwards.
  170 |           // Deliberately left unverified rather than faked with a weaker check.
  171 |           test.info().annotations.push({
  172 |             type: 'Coverage gap',
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
> 189 |             ).toBeFalsy();
      |               ^ Error: the request was rejected, so fr01.fr01-tc-03.msn1f436ed4@example.com must not have been written
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
  273 |         await expect(page).toHaveURL(new RegExp(`${row.expect_signal}$`));
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
```