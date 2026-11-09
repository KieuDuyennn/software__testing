<#
    monitor-resources.ps1 — Step 4/6: sample the target process while a test runs.

    CPU utilisation and memory utilisation are two of the ten metrics the course
    requires, and neither can be recovered afterwards: the load tool only sees
    the responses, not what the server was doing to produce them. If nobody
    samples during the run, those rows in the report are simply empty.

    Writes a CSV: timestamp, cpu_percent, working_set_mb, private_mb, threads, handles.
    Reading the first and last rows of that file answers "did memory come back
    down", which is the whole point of a soak test.

    Usage:
        powershell -File monitor-resources.ps1 -ProcessName node -OutFile results/run/resources.csv
        powershell -File monitor-resources.ps1 -ProcessId 1234 -IntervalSeconds 5 -DurationSeconds 900

    Stops on -DurationSeconds, or when the process exits, or on Ctrl+C.
#>

[CmdletBinding()]
param(
    [string]$ProcessName = "node",
    [int]$ProcessId = 0,
    [string]$OutFile = "resources.csv",
    [int]$IntervalSeconds = 2,
    [int]$DurationSeconds = 0
)

$ErrorActionPreference = "Stop"

function Resolve-Target {
    <#
        Picks the process to watch. When several candidates share a name — common
        with node, where an editor or a tool may also be running — the largest
        working set is the best guess at "the server", because a seeded backend
        holds far more memory than a helper process.
    #>
    param([string]$Name, [int]$Id)

    if ($Id -gt 0) {
        $p = Get-Process -Id $Id -ErrorAction SilentlyContinue
        if (-not $p) { throw "no process with PID $Id" }
        return $p
    }

    $candidates = @(Get-Process -Name $Name -ErrorAction SilentlyContinue)
    if ($candidates.Count -eq 0) { throw "no process named '$Name' is running" }
    if ($candidates.Count -gt 1) {
        $candidateList = ($candidates | ForEach-Object { "$($_.Id):$($_.ProcessName)" }) -join ", "
        throw "multiple processes named '$Name' found ($candidateList); pass -ProcessId to select the backend explicitly"
    }
    return $candidates[0]
}

$target = Resolve-Target -Name $ProcessName -Id $ProcessId
$logicalCores = (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors

$dir = Split-Path -Parent $OutFile
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }

# Written without a byte-order mark. Out-File -Encoding utf8 in Windows
# PowerShell 5.1 emits one, and a BOM in front of a CSV header turns the first
# column name into "﻿timestamp" for every standard parser downstream.
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$resolvedOut = $OutFile
if (-not [System.IO.Path]::IsPathRooted($resolvedOut)) {
    $resolvedOut = Join-Path (Get-Location).Path $OutFile
}
[System.IO.File]::WriteAllText(
    $resolvedOut,
    "timestamp,elapsed_s,cpu_percent,working_set_mb,private_mb,threads,handles" + [Environment]::NewLine,
    $utf8NoBom)

Write-Output "watching PID $($target.Id) ($($target.ProcessName)), $logicalCores logical cores"
Write-Output "writing  $OutFile every ${IntervalSeconds}s"

$startedAt = Get-Date
$previousCpu = $target.TotalProcessorTime
$previousAt = $startedAt
$samples = 0

while ($true) {
    Start-Sleep -Seconds $IntervalSeconds

    try {
        $target.Refresh()
    } catch {
        Write-Output "process exited after $samples samples"
        break
    }
    if ($target.HasExited) {
        Write-Output "process exited after $samples samples"
        break
    }

    $now = Get-Date
    $currentCpu = $target.TotalProcessorTime

    # CPU percent = processor time consumed in the window, divided by the wall
    # time available across all cores. Dividing by core count keeps the figure on
    # a 0-100 scale, so a single saturated core on an 8-thread machine reads as
    # 12.5% rather than 100% - state that convention in the report, because the
    # other common convention (per-core) makes the same run look eight times busier.
    $cpuDeltaMs = ($currentCpu - $previousCpu).TotalMilliseconds
    $wallMs = ($now - $previousAt).TotalMilliseconds
    $cpuPercent = 0
    if ($wallMs -gt 0) {
        $cpuPercent = [math]::Round($cpuDeltaMs / ($wallMs * $logicalCores) * 100, 2)
    }

    $row = "{0},{1},{2},{3},{4},{5},{6}" -f `
        $now.ToString("yyyy-MM-ddTHH:mm:ss"),
        [math]::Round(($now - $startedAt).TotalSeconds, 1),
        $cpuPercent,
        [math]::Round($target.WorkingSet64 / 1MB, 1),
        [math]::Round($target.PrivateMemorySize64 / 1MB, 1),
        $target.Threads.Count,
        $target.HandleCount

    [System.IO.File]::AppendAllText($resolvedOut, $row + [Environment]::NewLine, $utf8NoBom)

    $previousCpu = $currentCpu
    $previousAt = $now
    $samples++

    if ($DurationSeconds -gt 0 -and ($now - $startedAt).TotalSeconds -ge $DurationSeconds) {
        Write-Output "duration reached, $samples samples"
        break
    }
}

Write-Output "done: $OutFile"
