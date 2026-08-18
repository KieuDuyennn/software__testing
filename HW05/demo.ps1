<#
    HW05 Agent Skill demo.

    Safe default (no new load is generated):
        powershell -ExecutionPolicy Bypass -File .\demo.ps1

    Live 60-second demonstration with genuine evidence capture:
        powershell -ExecutionPolicy Bypass -File .\demo.ps1 `
          -RunLive -BackendProcessId <PID>

    Keep JMeter and Task Manager visible in the same frame while -RunLive runs.
    Demo artifacts are separate from the official result sets.
#>

[CmdletBinding()]
param(
    [switch]$RunLive,

    [int]$BackendProcessId = 0,

    [ValidateRange(1, 20)]
    [int]$Threads = 2,

    [ValidateRange(1, 120)]
    [int]$RampSeconds = 4,

    [ValidateRange(20, 300)]
    [int]$DurationSeconds = 60,

    [string]$TargetHost = 'localhost',

    [ValidateRange(1, 65535)]
    [int]$Port = 3000
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$studentId = '23127184'
$dataDir = Join-Path $root 'data'
$officialPlan = Join-Path $root 'test-plans/23127184_Load_20260817.jmx'
$validator = Join-Path $root '.claude/skills/perf-implement-and-run/scripts/validate-test-data.ps1'
$generator = Join-Path $root '.claude/skills/perf-implement-and-run/scripts/new-plan.ps1'
$runner = Join-Path $root '.claude/skills/perf-implement-and-run/scripts/run-scenario.ps1'
$analyzer = Join-Path $root '.claude/skills/perf-analyze-and-retest/scripts/analyze-jtl.py'

function Write-Step([int]$Number, [string]$Text) {
    Write-Host "`n[$Number/5] $Text" -ForegroundColor Cyan
}

function Require-File([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Missing demo dependency: $Path"
    }
}

foreach ($path in @($officialPlan, $validator, $generator, $runner, $analyzer)) {
    Require-File $path
}

Push-Location $root
try {
    Write-Host 'HW05 Agent Skill demo - Student 23127184' -ForegroundColor Green
    Write-Host 'Workflow: login -> search -> product detail -> add to cart -> checkout'

    Write-Step 1 'Validate the three data-driven CSV pools'
    & $validator -DataDir $dataDir -ExpectedMaxThreads $Threads

    Write-Step 2 'Inspect the reviewed JMeter workflow and listener'
    [xml]$planXml = Get-Content -Raw -Encoding UTF8 $officialPlan
    $samplers = @($planXml.SelectNodes('//HTTPSamplerProxy') | ForEach-Object { $_.testname })
    $requiredSamplers = @('01 login', '02 search products', '03 product detail', '04 add to cart', '05 checkout')
    foreach ($label in $requiredSamplers) {
        if ($samplers -notcontains $label) { throw "Official plan is missing sampler '$label'." }
    }
    $listeners = @($planXml.SelectNodes('//ResultCollector') | ForEach-Object { $_.guiclass })
    Write-Host "JMX OK: $($requiredSamplers.Count) correlated endpoint steps"
    Write-Host "Listener: $($listeners -join ', ')"

    Write-Step 3 'Recompute the official Load result from raw JTL evidence'
    $loadRun = Get-ChildItem (Join-Path $root 'results') -Directory |
        Where-Object { $_.Name -like '23127184_Load_20260817_*' } |
        Sort-Object Name -Descending |
        Select-Object -First 1
    if (-not $loadRun) { throw 'Official Load result directory was not found.' }
    $jtl = Join-Path $loadRun.FullName 'result.jtl'
    $resources = Join-Path $loadRun.FullName 'resources.csv'
    Require-File $jtl
    Require-File $resources
    & python $analyzer $jtl `
        --resources $resources `
        --bucket 30 `
        --p95 300 `
        --error-rate 1 `
        --journey-label '01 login' `
        --journey-label '02 search products' `
        --journey-label '03 product detail' `
        --journey-label '04 add to cart' `
        --journey-label '05 checkout'
    if ($LASTEXITCODE -ne 0) { throw 'Raw JTL analysis failed.' }

    Write-Step 4 'Human-review checkpoint'
    Write-Host 'Verify that request rows are separated from controller rows.'
    Write-Host 'Confirm p95/error values against the report before accepting the conclusion.'
    Write-Host 'Capacity and leak claims remain student decisions based on measured evidence.'

    if (-not $RunLive) {
        Write-Step 5 'Preflight complete'
        Write-Host 'For the recorded live demo, start a fresh LOADTEST=1 backend and run:'
        Write-Host '  powershell -ExecutionPolicy Bypass -File .\demo.ps1 -RunLive -BackendProcessId <PID>' -ForegroundColor Yellow
        return
    }

    Write-Step 5 'Generate and execute a short live plan with evidence capture'
    if ($BackendProcessId -le 0) {
        throw '-BackendProcessId is required with -RunLive; do not guess the monitored process.'
    }
    $backend = Get-Process -Id $BackendProcessId -ErrorAction Stop
    $healthUrl = "http://${TargetHost}:$Port/api/products"
    $response = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -ne 200) { throw "Backend preflight failed: HTTP $($response.StatusCode)." }
    Write-Host "Backend OK: PID $($backend.Id), $healthUrl"

    if (-not (Get-Command jmeter -ErrorAction SilentlyContinue)) {
        throw 'jmeter is not on PATH.'
    }
    $demoPlanDir = Join-Path $root 'evidence/demo'
    $demoRunDir = Join-Path $root 'evidence/demo-runs'
    $demoStamp = (Get-Date -Format 'yyyyMMdd-HHmmss') + '-DEMO'
    & $generator `
        -Scenario Load `
        -StudentId $studentId `
        -Date $demoStamp `
        -TargetHost $TargetHost `
        -Port "$Port" `
        -DataDir 'data' `
        -OutDir $demoPlanDir `
        -Threads $Threads `
        -RampSeconds $RampSeconds `
        -DurationSeconds $DurationSeconds `
        -BaselineIterPerSec 32.9
    if ($LASTEXITCODE -ne 0) { throw 'Demo plan generation failed.' }

    $demoPlan = Join-Path $demoPlanDir "${studentId}_Load_${demoStamp}.jmx"
    Require-File $demoPlan
    & $runner `
        -Plan $demoPlan `
        -OutRoot $demoRunDir `
        -TargetProcessId $BackendProcessId `
        -DataDir $dataDir
    if ($LASTEXITCODE -ne 0) { throw 'Live demo run failed.' }

    Write-Host "`nLive demo complete. Evidence: $demoRunDir" -ForegroundColor Green
    Write-Host 'Review the JTL, HTML report and resources.csv before citing the demo.'
} finally {
    Pop-Location
}
