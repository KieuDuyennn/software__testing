import { test, expect } from '../../fixtures/test-fixtures';
import { loadJson, caseTitle, type TestCaseRow } from '../../utils/data-loader';
import { expectSortedDescByDate } from '../../utils/assertions';

/**
 * FR-11 Order history view, user (Pool B) - HW04 Task 1.
 *
 * SCAFFOLD - see the checklist in the FR-01 spec; the same five items apply here.
 *
 * Data setup note: FR-11 needs seeded accounts (one with orders, one without).
 * Seed them by hand in the SUT and record the account names in .env - do NOT let
 * the suite create orders as a side effect, or the 9 runs will drift apart.
 */

interface OrderHistoryCase extends TestCaseRow {
  account: string;
  filter: string | null;
  page: number | null;
  expect_row_count: number | null;
  expect_outcome: 'rendered' | 'empty_state' | 'forbidden' | 'not_found';
  expect_sorted_desc_by: string | null;
}

const { cases } = loadJson<{ cases: OrderHistoryCase[] }>('fr11_order_history.json');

test.describe('FR-11 Order history view', () => {
  for (const row of cases) {
    test(caseTitle(row), async ({ page, loginPage, orderHistoryPage }) => {
      if (row.account !== 'anonymous') {
        await loginPage.login(
          process.env.USER_EMAIL ?? '',
          process.env.USER_PASSWORD ?? '',
        );
      }

      await orderHistoryPage.goto();
      await orderHistoryPage.waitForReady();

      switch (row.expect_outcome) {
        case 'rendered': {
          // Pattern 1: UI state.
          await expect(orderHistoryPage.rows.first()).toBeVisible();
          if (row.expect_row_count !== null) {
            await expect(orderHistoryPage.rows).toHaveCount(row.expect_row_count);
          }
          // Pattern 3: data integrity - the list means what it claims to mean.
          if (row.expect_sorted_desc_by) {
            await expectSortedDescByDate(await orderHistoryPage.columnValues(1));
          }
          break;
        }
        case 'empty_state':
          await expect(orderHistoryPage.emptyState).toBeVisible();
          await expect(orderHistoryPage.rows).toHaveCount(0);
          break;
        case 'forbidden':
        case 'not_found':
          await expect(page).toHaveURL(/login|403|404/);
          break;
      }
    });
  }
});
