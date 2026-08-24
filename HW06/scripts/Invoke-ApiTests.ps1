<#
.SYNOPSIS
    Runs the HW06 API suite end to end against a freshly seeded EShop backend.

.DESCRIPTION
    1. Starts eshop/backend with LOADTEST=1 (bypasses the 200-req/15-min rate
       limiter, which a full suite would otherwise trip with HTTP 429).
       Starting the backend drops and re-seeds database.sqlite, so every run
       begins from identical state.
    2. Hands off to scripts/run-suite.js, which drives Newman and writes the
       HTML reports to reports/ and the JSON summaries alongside them.
    3. Stops the backend.

    Failing assertions in full mode are expected: they are the SUT's real
    defects. In gate mode a failure means the regression baseline broke.

.PARAMETER Api
    Run only one API (1-4). Omit to run all four.

.PARAMETER Mode
    full (default) runs every folder. gate runs only the folders listed in
    postman/config/ci-suite.json - the same set the CI pipeline gates on.

.PARAMETER KeepServer
    Leave the backend running after the suite finishes.

.EXAMPLE
    .\scripts\Invoke-ApiTests.ps1
    .\scripts\Invoke-ApiTests.ps1 -Api 3 -KeepServer
    .\scripts\Invoke-ApiTests.ps1 -Mode gate
#>
[CmdletBinding()]
param(
    [ValidateRange(1, 4)][int] $Api,
    [ValidateSet('full', 'gate')][string] $Mode = 'full',
    [switch] $KeepServer
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

New-Item -ItemType Directory -Force -Path "reports", "evidence/newman-console" | Out-Null

# --- 1. Start the SUT ------------------------------------------------------
Write-Host "Starting EShop backend (LOADTEST=1, database re-seeded)..." -ForegroundColor Cyan
$env:LOADTEST = "1"
$server = Start-Process -FilePath "node" -ArgumentList "eshop/backend/server.js" `
    -PassThru -NoNewWindow `
    -RedirectStandardOutput "evidence/newman-console/sut-stdout.log" `
    -RedirectStandardError  "evidence/newman-console/sut-stderr.log"

$ready = $false
foreach ($attempt in 1..40) {
    Start-Sleep -Milliseconds 400
    try {
        Invoke-WebRequest -Uri "http://localhost:3000/api/products" -UseBasicParsing -TimeoutSec 2 | Out-Null
        $ready = $true
        break
    } catch { }
}
if (-not $ready) {
    if (-not $server.HasExited) { Stop-Process -Id $server.Id -Force }
    throw "Backend did not become ready on http://localhost:3000. See evidence/newman-console/sut-stderr.log"
}
Write-Host "Backend ready (pid $($server.Id))." -ForegroundColor Green

# --- 2. Run the suite ------------------------------------------------------
# run-suite.js drives Newman as a library, so no npx resolution is involved.
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$log = "evidence/newman-console/suite_${Mode}_$stamp.log"
$suiteArgs = @("scripts/run-suite.js", "--mode", $Mode, "--env", "local")
if ($Api) { $suiteArgs += @("--only", "$Api") }

$exitCode = 0
try {
    # No `2>&1` here: in Windows PowerShell 5.1 redirecting a native command's
    # stderr wraps each line in an ErrorRecord, which -ErrorActionPreference
    # Stop then treats as terminating - a harmless Node deprecation warning
    # would abort the run. stderr still reaches the console as-is.
    $ErrorActionPreference = "Continue"
    & node $suiteArgs | Tee-Object -FilePath $log
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = "Stop"
}
finally {
    if (-not $KeepServer) {
        if (-not $server.HasExited) { Stop-Process -Id $server.Id -Force }
        Write-Host "`nBackend stopped." -ForegroundColor DarkGray
    } else {
        Write-Host "`nBackend left running on pid $($server.Id)." -ForegroundColor Yellow
    }
}

Write-Host "`nHTML reports : reports/"
Write-Host "Console log  : $log"
if ($Mode -eq 'full') {
    Write-Host "Failing assertions above are the SUT's real defects - triage them in docs/bugs/BUG_REPORT.md."
}

exit $exitCode
