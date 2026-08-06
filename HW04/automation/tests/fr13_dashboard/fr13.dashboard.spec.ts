import { test, expect } from '../../fixtures/test-fixtures';
import { loadJson, caseTitle, type TestCaseRow } from '../../utils/data-loader';
import { expectFigureMatches, expectApiResponse } from '../../utils/assertions';

/**
 * FR-13 Dashboard, admin (Pool C) - HW04 Task 1.
 *
 * SCAFFOLD - see the checklist in the FR-01 spec; the same five items apply here.
 *
 * HW02 recorded a confirmed revenue-doubling defect on this page. At least one
 * case here must recompute the KPI from an independent source and compare, so a
 * wrong-but-present number cannot pass. If that assertion fails, that is a bug
 * to file (GitHub Issue + screenshot + docs/02_Bug_Report.md), not a test to relax.
 */

interface DashboardCase extends TestCaseRow {
  account: 'admin' | 'user' | 'anonymous';
  date_range: string | null;
  kpi: string;
  expect_outcome: 'rendered' | 'forbidden' | 'zero_state';
  cross_check: 'api' | 'orders_table' | 'none';
}

const { cases } = loadJson<{ cases: DashboardCase[] }>('fr13_dashboard.json');

test.describe('FR-13 Dashboard', () => {
  for (const row of cases) {
    test(caseTitle(row), async ({ page, request, loginPage, adminDashboardPage }) => {
      if (row.account === 'admin') {
        await loginPage.login(process.env.ADMIN_EMAIL ?? '', process.env.ADMIN_PASSWORD ?? '');
      } else if (row.account === 'user') {
        await loginPage.login(process.env.USER_EMAIL ?? '', process.env.USER_PASSWORD ?? '');
      }

      await adminDashboardPage.goto();

      if (row.expect_outcome === 'forbidden') {
        // Pattern 1: UI state - access control must be enforced, not just hidden.
        await expect(page).toHaveURL(/login|403|unauthorized/);
        await expect(adminDashboardPage.revenueValue).toBeHidden();
        return;
      }

      await expect(adminDashboardPage.revenueValue).toBeVisible();

      if (row.cross_check === 'api') {
        // Pattern 2: API assertion - what the server says the total is.
        const response = await request.get(`${process.env.API_URL}/api/admin/orders`);
        let expectedRevenue = 0;
        await expectApiResponse(response, 200, (body) => {
          expectedRevenue = (body.data ?? body).reduce(
            (sum: number, order: any) => sum + Number(order.total ?? 0),
            0,
          );
        });
        // Pattern 3: data integrity - the rendered figure must equal that total.
        expectFigureMatches(
          await adminDashboardPage.revenueValue.innerText(),
          expectedRevenue,
          'dashboard revenue',
        );
      }
    });
  }
});
