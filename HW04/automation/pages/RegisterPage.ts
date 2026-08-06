import type { Locator, Page } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * FR-01 Account registration (Pool A).
 *
 * SCAFFOLD - every locator below is a guess until you open the SUT and check it.
 * Verify each one with `npx playwright codegen $BASE_URL/register` before you
 * trust a single test result, and record any correction you make in
 * `docs/test-plan/AI_Review_Gap_Analysis.md` (that is Task 1's "review and fix" evidence).
 */
export class RegisterPage extends BasePage {
  readonly path = '/register';

  constructor(page: Page) { super(page); }

  get nameInput(): Locator { return this.page.getByLabel(/name|họ tên/i); }
  get emailInput(): Locator { return this.page.getByLabel(/email/i); }
  get passwordInput(): Locator { return this.page.getByLabel(/^password|mật khẩu$/i); }
  get phoneInput(): Locator { return this.page.getByLabel(/phone|điện thoại/i); }
  get submitButton(): Locator { return this.page.getByRole('button', { name: /register|đăng ký/i }); }

  async register(data: { name?: string; email?: string; password?: string; phone?: string }): Promise<void> {
    if (data.name !== undefined) await this.nameInput.fill(data.name);
    if (data.email !== undefined) await this.emailInput.fill(data.email);
    if (data.password !== undefined) await this.passwordInput.fill(data.password);
    if (data.phone !== undefined) await this.phoneInput.fill(data.phone);
    await this.submitButton.click();
  }
}
