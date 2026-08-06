import type { Locator, Page } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * FR-13 Dashboard, admin side (Pool C).
 *
 * HW02 recorded a confirmed defect here (dashboard revenue counted twice) - the
 * data-integrity assertion in `automation/utils/assertions.ts` exists mainly for this page.
 * Do not soften an assertion just because it fails; a failing assertion that
 * reveals a genuine defect is a Task 1 deliverable, not a broken test.
 *
 * SCAFFOLD - verify locators against the live SUT before use.
 */
export class AdminDashboardPage extends BasePage {
  readonly path = '/admin/dashboard';

  constructor(page: Page) { super(page); }

  kpiCard(name: string | RegExp): Locator {
    return this.page.getByRole('region', { name }).or(this.page.getByTestId(`kpi-${name}`)).first();
  }

  get revenueValue(): Locator { return this.kpiCard(/revenue|doanh thu/i).getByTestId('kpi-value'); }
  get orderCountValue(): Locator { return this.kpiCard(/orders|đơn hàng/i).getByTestId('kpi-value'); }
  get userCountValue(): Locator { return this.kpiCard(/users|người dùng/i).getByTestId('kpi-value'); }
  get dateRangeFilter(): Locator { return this.page.getByLabel(/date range|khoảng thời gian/i); }
  get recentOrdersTable(): Locator { return this.page.getByRole('table', { name: /recent orders|đơn hàng gần đây/i }); }
}
