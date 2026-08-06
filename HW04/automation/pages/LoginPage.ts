import type { Locator, Page } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * Login - not a feature under test here, but FR-11 and FR-13 both need an
 * authenticated session, so it lives in the shared page objects.
 *
 * SCAFFOLD - verify locators against the live SUT before use.
 */
export class LoginPage extends BasePage {
  readonly path = '/login';

  constructor(page: Page) { super(page); }

  get emailInput(): Locator { return this.page.getByLabel(/email/i); }
  get passwordInput(): Locator { return this.page.getByLabel(/password|mật khẩu/i); }
  get submitButton(): Locator { return this.page.getByRole('button', { name: /login|đăng nhập/i }); }

  async login(email: string, password: string): Promise<void> {
    await this.goto();
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
    await this.page.waitForURL((url) => !url.pathname.includes('/login'));
  }
}
