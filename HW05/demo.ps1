<#
    HW05 Agent Skill demo.

    Safe default (no new load is generated):
        powershell -ExecutionPolicy Bypass -File .\demo.ps1

    Show the recording script without running checks:
        powershell -ExecutionPolicy Bypass -File .\demo.ps1 -GuideOnly

    Live 60-second demonstration with genuine evidence capture:
        powershell -ExecutionPolicy Bypass -File .\demo.ps1 `
          -RunLive -BackendProcessId <PID> -PauseBetweenSteps

    Keep JMeter and Task Manager visible in the same frame while -RunLive runs.
    Demo artifacts are separate from the official result sets.
#>

[CmdletBinding()]
param(
    [switch]$RunLive,

    [switch]$GuideOnly,

    [switch]$PauseBetweenSteps,

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

function Write-Cue([string]$Text) {
    Write-Host "PRESENTER: $Text" -ForegroundColor Yellow
    if ($PauseBetweenSteps) {
        Read-Host 'Press Enter when this explanation is complete' | Out-Null
    }
}

function Show-DemoGuide {
    Write-Host @'

==================== HUONG DAN QUAY DEMO 6-7 PHUT ====================

Truoc khi quay:
  1. Start backend moi voi LOADTEST=1 va ghi lai PID chinh xac.
  2. Dat terminal/JMeter ben trai, Task Manager ben phai trong cung khung hinh.
  3. Hien MSSV 23127184, hostname KIEUDUYEN va nhanh Git hw5.
  4. Khong goi demo run la official run; evidence demo nam rieng.

0:00-0:40 - Gioi thieu
  Noi: "Em la sinh vien 23127184. Workflow gom login, search, product
  detail, add to cart va checkout; no phu auth-heavy, read-heavy va
  transactional endpoints."

0:40-1:20 - Agent Skill
  Mo .claude/skills/performance-testing/SKILL.md. Chi ra 4 phase skill:
  environment/criteria, plan/design, implement/run, analyze/retest.

1:20-2:20 - Data-driven plan
  Chay script safe mode. Khi buoc 1-2 hien ra, noi ve 3 CSV 240 dong,
  JWT correlation, 5 endpoint labels, content assertions va listener.

2:20-3:35 - Phan tich raw evidence
  O buoc 3, chi ra 42,810 request rows, p95 10 ms, error 0%, va 8,547
  complete journeys. Giai thich controller rows khong duoc cong vao request
  samples va partial tail khong duoc tinh la journey hoan chinh.

3:35-4:20 - Human review
  O buoc 4, noi: "AI output chi la gia thuyet. Em doi chieu raw JTL,
  tach request/controller, kiem tra phase va source code truoc khi ket luan."

4:20-5:45 - Live run co monitor
  Chay -RunLive voi backend PID that. Giu terminal/JMeter va Task Manager
  cung khung hinh. Noi ro day la demo 2 VU ngan, khong thay the official run.

5:45-6:30 - Evidence va ket luan
  Mo evidence/demo-runs/<run>/ va chi ra result.jtl, report/, resources.csv,
  jmeter.log, run.md. Xac nhan student tu review ket qua truoc khi trich dan.

Lenh:
  Xem huong dan:
    powershell -ExecutionPolicy Bypass -File .\demo.ps1 -GuideOnly

  Preflight + recompute official Load:
    powershell -ExecutionPolicy Bypass -File .\demo.ps1 -PauseBetweenSteps

  Live demo:
    powershell -ExecutionPolicy Bypass -File .\demo.ps1 -RunLive `
      -BackendProcessId <PID> -PauseBetweenSteps

======================================================================
'@ -ForegroundColor Green
}

function Require-File([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Missing demo dependency: $Path"
    }
}

Show-DemoGuide
if ($GuideOnly) { return }

foreach ($path in @($officialPlan, $validator, $generator, $runner, $analyzer)) {
    Require-File $path
}

Push-Location $root
try {
    Write-Host 'HW05 Agent Skill demo - Student 23127184' -ForegroundColor Green
    Write-Host 'Workflow: login -> search -> product detail -> add to cart -> checkout'

    Write-Step 1 'Validate the three data-driven CSV pools'
    Write-Cue 'Explain why 240 unique credentials avoid shared-user state and why every CSV is validated before execution.'
    & $validator -DataDir $dataDir -ExpectedMaxThreads $Threads

    Write-Step 2 'Inspect the reviewed JMeter workflow and listener'
    Write-Cue 'Show JWT extraction, five endpoint labels, content assertions and the distinct listener assigned to Load.'
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
    Write-Cue 'State that raw JTL is ground truth; request samples and Transaction Controller rows must be counted separately.'
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
    Write-Cue 'Explain one AI mistake, the corrected raw value, and why the student owns the final interpretation.'
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
    Write-Cue 'Put JMeter or this terminal beside Task Manager in the same frame and say that this short run is demo evidence only.'
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
