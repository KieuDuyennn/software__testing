import type { Locator, Page } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * FR-11 Order history view, user side (Pool B).
 *
 * SCAFFOLD - verify locators against the live SUT before use.
 */
export class OrderHistoryPage extends BasePage {
  readonly path = '/orders';

  constructor(page: Page) { super(page); }

  get rows(): Locator { return this.page.getByRole('row').filter({ hasNot: this.page.getByRole('columnheader') }); }
  get emptyState(): Locator { return this.page.getByText(/no orders|chưa có đơn hàng/i); }
  get statusFilter(): Locator { return this.page.getByLabel(/status|trạng thái/i); }
  get pagination(): Locator { return this.page.getByRole('navigation', { name: /pagination|phân trang/i }); }

  /** All values in one column, for the sortedness / integrity assertions. */
  async columnValues(columnIndex: number): Promise<string[]> {
    return this.rows.locator('td').nth(columnIndex).allInnerTexts();
  }

  async openOrder(orderId: string): Promise<void> {
    await this.page.getByRole('link', { name: new RegExp(orderId) }).click();
  }
}
