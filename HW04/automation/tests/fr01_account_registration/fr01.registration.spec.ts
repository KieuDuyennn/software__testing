import { test, expect } from '../../fixtures/test-fixtures';
import { loadCsv, caseTitle, type TestCaseRow } from '../../utils/data-loader';
import { expectFieldError, expectUiAndApiAgree } from '../../utils/assertions';

/**
 * FR-01 Account registration (Pool A) - HW04 Task 1.
 *
 * SCAFFOLD. This file shows the required shape; the >= 12 cases themselves are
 * what you drive the AI to produce, step by step (brief section 6: "not with a
 * single generic prompt"), then review and fix yourself.
 *
 * Checklist this file must satisfy before you call FR-01 done:
 *   [ ] >= 12 test cases, any mix of positive / negative / edge
 *   [ ] every case comes from automation/data/fr01_registration.csv - no inline arrays
 *   [ ] >= 3 distinct assertion patterns used across the suite
 *   [ ] runs green (or fails for a real, reported defect) on chromium, firefox, webkit
 *   [ ] every locator verified against the live SUT, not left as a scaffold guess
 */

interface RegistrationCase extends TestCaseRow {
  name: string;
  email: string;
  password: string;
  phone: string;
  expect_outcome: 'success' | 'rejected';
  expect_message: string;
  http_status: string;
}

const cases = loadCsv<RegistrationCase>('fr01_registration.csv');

test.describe('FR-01 Account registration', () => {
  test.beforeEach(async ({ registerPage }) => {
    await registerPage.goto();
    await registerPage.waitForReady();
  });

  for (const row of cases) {
    test(caseTitle(row), async ({ page, registerPage }) => {
      // Unique-email cases must not collide across the 9 runs - derive, don't hardcode.
      const email = row.email.includes('@')
        ? row.email.replace('@', `+${Date.now()}@`)
        : row.email;

      // Pattern 2: assert the UI action and the server response agree.
      await expectUiAndApiAgree(
        page,
        /\/api\/.*(register|auth)/,
        () => registerPage.register({ ...row, email }),
        Number(row.http_status),
      );

      if (row.expect_outcome === 'success') {
        // Pattern 1: UI state assertion.
        await expect(page).toHaveURL(/login|verify|home|\//);
      } else {
        // Pattern 1 variant: the specific field must carry the error.
        await expectFieldError(page, row.expect_message, /.+/);
      }
    });
  }
});
