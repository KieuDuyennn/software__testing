<#
    run-scenario.ps1 — Step 6: execute a test plan and capture the evidence.

    Runs JMeter in non-GUI mode, samples the target process throughout, and
    collects everything one run produces into a single timestamped folder:

        results/<PlanName>_<yyyyMMdd-HHmmss>/
            result.jtl      raw samples - the evidence, never edited
            report/         JMeter HTML dashboard
            resources.csv   CPU and memory of the target during the run
            jmeter.log      tool log, where a failed run explains itself
            run.md          what was run, when, and against what

    Keeping the four together matters because a .jtl on its own cannot answer
    "was the machine already busy" or "which build was this" - and those are the
    first questions asked when two runs disagree.

    Non-GUI mode is not a convenience here. The GUI's own rendering competes with
    the test for CPU on the same machine, so a GUI run measures a slower system
    than a headless one.

    Usage:
        powershell -File run-scenario.ps1 -Plan test-plans/23127184_Load_20260815.jmx
        powershell -File run-scenario.ps1 -Plan test-plans/23127184_Spike_20260815.jmx -TargetProcessName node
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Plan,

    [string]$OutRoot = "results",
    [string]$TargetProcessName = "node",
    [int]$TargetProcessId = 0,
    [int]$SampleIntervalSeconds = 2,
    [string]$DataDir = "data",
    [switch]$SkipHtmlReport
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Plan)) { throw "test plan not found: $Plan" }
if (-not (Get-Command jmeter -ErrorAction SilentlyContinue)) {
    throw "jmeter is not on PATH. Install it, or open a new shell if it was just installed."
}

# Finish every preflight check before creating a run folder or background job.
# A malformed CSV must fail cleanly rather than leave a monitor process behind.
$resolvedDataDir = (Resolve-Path -LiteralPath $DataDir -ErrorAction Stop).Path
$validator = Join-Path $PSScriptRoot "validate-test-data.ps1"
& $validator -DataDir $resolvedDataDir

$before = $null
if ($TargetProcessId -gt 0) {
    $before = Get-Process -Id $TargetProcessId -ErrorAction Stop
} else {
    $candidates = @(Get-Process -Name $TargetProcessName -ErrorAction SilentlyContinue)
    if ($candidates.Count -eq 0) {
        throw "target process '$TargetProcessName' not found; start the backend or pass -TargetProcessId"
    }
    if ($candidates.Count -gt 1) {
        $candidateList = ($candidates | ForEach-Object { "$($_.Id):$($_.ProcessName)" }) -join ", "
        throw "multiple '$TargetProcessName' processes found ($candidateList); pass -TargetProcessId for the backend"
    }
    $before = $candidates[0]
}

$planName = [System.IO.Path]::GetFileNameWithoutExtension($Plan)
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$runDir = Join-Path $OutRoot "${planName}_${stamp}"
New-Item -ItemType Directory -Force -Path $runDir | Out-Null

$jtl = Join-Path $runDir "result.jtl"
$log = Join-Path $runDir "jmeter.log"
$resources = Join-Path $runDir "resources.csv"
$reportDir = Join-Path $runDir "report"

# Record the target's state before the run. A backend that is already at 300 MB
# and 40% CPU will produce different numbers than one just started, and that
# difference is invisible later unless it is written down now.
$monitorJob = $null
if ($before) {
    $monitorScript = Join-Path $PSScriptRoot "monitor-resources.ps1"
    # A background job starts in its own working directory, so every path handed
    # to it has to be absolute or the CSV lands somewhere nobody looks.
    $resourcesAbsolute = Join-Path (Resolve-Path $runDir).Path "resources.csv"

    $monitorJob = Start-Job -ScriptBlock {
        param($ScriptPath, $TargetPid, $OutPath, $Interval)
        & powershell -NoProfile -File $ScriptPath -ProcessId $TargetPid -OutFile $OutPath -IntervalSeconds $Interval
    } -ArgumentList $monitorScript, $before.Id, $resourcesAbsolute, $SampleIntervalSeconds

    Write-Output "monitor : started for PID $($before.Id)"
}

Write-Output "plan    : $Plan"
Write-Output "output  : $runDir"
Write-Output "running JMeter (non-GUI)..."

$jmeterArgs = @("-n", "-t", $Plan, "-l", $jtl, "-j", $log)
$jmeterArgs += "-Jdata.dir=$($resolvedDataDir -replace '\\', '/')"
if (-not $SkipHtmlReport) {
    $jmeterArgs += @("-e", "-o", $reportDir)
}

$startedAt = Get-Date
$finishedAt = $null
$exitCode = -1
try {
    & jmeter @jmeterArgs
    $exitCode = $LASTEXITCODE
} finally {
    $finishedAt = Get-Date
    if ($monitorJob) {
        Stop-Job $monitorJob -ErrorAction SilentlyContinue
        Receive-Job $monitorJob -ErrorAction SilentlyContinue | Out-Null
        Remove-Job $monitorJob -Force -ErrorAction SilentlyContinue
    }
}

$after = $null
if ($before) {
    try {
        $after = Get-Process -Id $before.Id -ErrorAction Stop
    } catch {
        Write-Warning "target process exited during the run - that is itself a finding"
    }
}

$durationSeconds = [math]::Round(($finishedAt - $startedAt).TotalSeconds, 1)

$notes = @()
$notes += "# Run record"
$notes += ""
$notes += "| Field | Value |"
$notes += "|---|---|"
$notes += "| Test plan | ``$Plan`` |"
$notes += "| Started | $($startedAt.ToString('yyyy-MM-dd HH:mm:ss zzz')) |"
$notes += "| Finished | $($finishedAt.ToString('yyyy-MM-dd HH:mm:ss zzz')) |"
$notes += "| Wall duration | $durationSeconds s |"
$notes += "| JMeter exit code | $exitCode |"
$notes += "| Host | $env:COMPUTERNAME |"
if ($before) {
    $notes += "| Target PID | $($before.Id) |"
    $notes += "| Target memory before | $([math]::Round($before.WorkingSet64 / 1MB, 1)) MB |"
}
if ($after) {
    $notes += "| Target memory after | $([math]::Round($after.WorkingSet64 / 1MB, 1)) MB |"
}
$notes += ""
$notes += "Raw samples in ``result.jtl``. Resource samples in ``resources.csv``."
$notes += "Analyse with perf-analyze-and-retest; do not edit the raw files."

$notes -join [Environment]::NewLine | Out-File -FilePath (Join-Path $runDir "run.md") -Encoding utf8

Write-Output ""
if ($exitCode -ne 0) {
    Write-Warning "JMeter exited with code $exitCode - check $log before trusting these results"
} else {
    Write-Output "run complete in ${durationSeconds}s"
}
if ($before -and $after) {
    $delta = [math]::Round(($after.WorkingSet64 - $before.WorkingSet64) / 1MB, 1)
    Write-Output "target memory: $([math]::Round($before.WorkingSet64/1MB,1)) MB -> $([math]::Round($after.WorkingSet64/1MB,1)) MB (delta $delta MB)"
}
Write-Output "results: $runDir"
