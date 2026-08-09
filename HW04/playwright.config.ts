import { defineConfig, devices } from '@playwright/test';
import { STUDENT_ID, STUDENT_NAME, RUN_STAMP, FEATURE, BROWSER_TAG } from './automation/utils/student';

/**
 * HW04 - Automation Testing on the EShop SUT.
 *
 * Report layout is driven by two env vars so that the 9 required runs
 * (3 features x 3 browsers) each land in their own folder:
 *
 *   FEATURE=fr01 BROWSER=chromium npx playwright test automation/tests/fr01_account_registration --project=chromium
 *     -> reports/html/fr01/chromium/index.html
 *
 * automation/run-all-browsers.ps1 loops all 9 combinations for you.
 *
 * The "Run by: {StudentID}" evidence required by the brief (section 6, Task 1
 * and section 11) is stamped in three places so it survives any reporter change:
 *   1. the HTML report title,
 *   2. config `metadata`, rendered in the report header,
 *   3. a per-test annotation added in automation/fixtures/test-fixtures.ts.
 */

const reportFolder = `reports/html/${FEATURE}/${BROWSER_TAG}`;

export default defineConfig({
  testDir: './automation/tests',
  outputDir: './test-results',

  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  timeout: 60_000,
  expect: { timeout: 10_000 },

  metadata: {
    'Run by': STUDENT_ID,
    'Student name': STUDENT_NAME,
    'Feature under test': FEATURE,
    'Browser': BROWSER_TAG,
    'Run started (ISO)': RUN_STAMP,
    'Assignment': 'HW04-AI - Automation Testing',
    'SUT': 'EShop (https://github.com/ttbhanh/eshop-sut)',
  },

  reporter: [
    ['list'],
    ['html', {
      open: 'never',
      outputFolder: reportFolder,
      title: `HW04 EShop Automation - ${FEATURE.toUpperCase()} - ${BROWSER_TAG} - Run by: ${STUDENT_ID} - ${RUN_STAMP}`,
    }],
    ['json', { outputFile: `reports/json/${FEATURE}-${BROWSER_TAG}.json` }],
  ],

  use: {
    // The web front-end is the Vite dev server on 5173; :3000 is the backend API
    // (frontend-web posts to http://localhost:3000/api/...), so it must not be the
    // baseURL for page.goto(). Verified against the running SUT.
    baseURL: process.env.BASE_URL ?? 'http://localhost:5173',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 15_000,
    navigationTimeout: 30_000,
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
