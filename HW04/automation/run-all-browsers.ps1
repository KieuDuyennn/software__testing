# Runs the 9 browser runs required by the brief (3 features x 3 browsers).
# Each run writes its own HTML report under reports/html/<feature>/<browser>/.
#
# Usage:  npm run runs:all
#    or:  powershell -ExecutionPolicy Bypass -File ./automation/run-all-browsers.ps1
#
# Run it from the HW04 root, not from automation/ - the report paths are
# relative to the folder holding playwright.config.ts.
#
# A feature that FAILS is still a completed run - the HTML report is the
# deliverable, and a failing assertion that reveals a real defect is a Task 1
# outcome, not a reason to stop the loop. That is why $ErrorActionPreference is
# left at Continue and each run's exit code is only recorded, never fatal.

$features = @(
    @{ Tag = 'fr01'; Path = 'automation/tests/fr01_account_registration' },
    @{ Tag = 'fr11'; Path = 'automation/tests/fr11_order_history' },
    @{ Tag = 'fr13'; Path = 'automation/tests/fr13_dashboard' }
)
$browsers = @('chromium', 'firefox', 'webkit')

$summary = @()

foreach ($feature in $features) {
    foreach ($browser in $browsers) {
        $env:FEATURE = $feature.Tag
        $env:BROWSER = $browser

        Write-Host ""
        Write-Host "=== $($feature.Tag) / $browser ===" -ForegroundColor Cyan
        $started = (Get-Date).ToString('o')

        npx playwright test $feature.Path --project=$browser
        $code = $LASTEXITCODE

        $summary += [pscustomobject]@{
            Feature  = $feature.Tag
            Browser  = $browser
            Started  = $started
            ExitCode = $code
            Report   = "reports/html/$($feature.Tag)/$browser/index.html"
        }
    }
}

$env:FEATURE = $null
$env:BROWSER = $null

Write-Host ""
Write-Host "=== 9-run summary ===" -ForegroundColor Cyan
$summary | Format-Table -AutoSize

$logPath = "reports/run-summary.txt"
$summary | Format-Table -AutoSize | Out-File -FilePath $logPath -Encoding utf8
Write-Host "Summary written to $logPath"
Write-Host "Paste these counts into README.md before submitting."
