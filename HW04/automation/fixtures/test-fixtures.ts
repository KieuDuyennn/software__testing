import { test as base, expect } from '@playwright/test';
import { RUN_BY_LABEL, RUN_STAMP, STUDENT_NAME } from '../utils/student';
import { RegisterPage } from '../pages/RegisterPage';
import { LoginPage } from '../pages/LoginPage';
import { OrderHistoryPage } from '../pages/OrderHistoryPage';
import { AdminDashboardPage } from '../pages/AdminDashboardPage';

/**
 * Shared fixtures for the whole suite.
 *
 * Import `test` from here, never from '@playwright/test' directly - that is what
 * guarantees the "Run by" annotation lands on every single test in the HTML
 * report, which is the section 11 evidence requirement.
 */

type Pages = {
  registerPage: RegisterPage;
  loginPage: LoginPage;
  orderHistoryPage: OrderHistoryPage;
  adminDashboardPage: AdminDashboardPage;
};

export const test = base.extend<Pages>({
  // Runs before every test: stamp authorship onto the test's report entry.
  page: async ({ page }, use, testInfo) => {
    testInfo.annotations.push({ type: 'Run by', description: RUN_BY_LABEL });
    testInfo.annotations.push({ type: 'Student', description: STUDENT_NAME });
    testInfo.annotations.push({ type: 'Run started', description: RUN_STAMP });
    await use(page);
  },

  registerPage: async ({ page }, use) => { await use(new RegisterPage(page)); },
  loginPage: async ({ page }, use) => { await use(new LoginPage(page)); },
  orderHistoryPage: async ({ page }, use) => { await use(new OrderHistoryPage(page)); },
  adminDashboardPage: async ({ page }, use) => { await use(new AdminDashboardPage(page)); },
});

export { expect };
