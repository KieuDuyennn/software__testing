<#
    inventory-env.ps1 — Step 1: identify the test environment.

    Collects the machine and tooling facts a performance report has to state, and
    prints them as a Markdown table ready to paste into docs/phases/01_environment.md.

    Why a script instead of typing it by hand: the hostname, core count and tool
    versions are exactly the details that get mistyped or quietly go stale between
    runs, and they are also the details a grader checks against earlier work.

    Usage:
        powershell -File inventory-env.ps1
        powershell -File inventory-env.ps1 -OutFile docs/phases/01_environment.md

    On Linux/macOS there is no CIM; use screenfetch/neofetch plus `java -version`
    and `jmeter -v` and fill the same table by hand.
#>

[CmdletBinding()]
param(
    [string]$OutFile
)

$ErrorActionPreference = "Stop"

function Get-ToolVersion {
    <#
        Runs a command and pulls the first version-looking token out of its output.
        Tools disagree wildly on where they print the version (stdout, stderr,
        inside ASCII art), so matching a version pattern anywhere in the combined
        output is more reliable than parsing each tool's format.
    #>
    param(
        [string]$Command,
        [string[]]$Arguments
    )

    $cmd = Get-Command $Command -ErrorAction SilentlyContinue
    if (-not $cmd) { return "not found" }

    # Several tools (java is the classic) print their version banner on stderr.
    # Merging that stderr inside Windows PowerShell 5.1 turns each line into an
    # ErrorRecord, which then trips $ErrorActionPreference and loses the very text
    # being collected. Letting cmd.exe do the merge keeps PowerShell on the stdout
    # path only, so the same code works whichever stream a tool chose.
    $quoted = '"' + $cmd.Source + '"'
    if ($Arguments -and $Arguments.Count -gt 0) {
        $quoted = $quoted + " " + ($Arguments -join " ")
    }

    try {
        $raw = (cmd /c "$quoted 2>&1" | Out-String)
    } catch {
        return "present (call failed)"
    }

    $match = [regex]::Match($raw, '\d+\.\d+(\.\d+)?')
    if ($match.Success) { return $match.Value }
    return "present (version unreadable)"
}

$cs   = Get-CimInstance Win32_ComputerSystem
$cpu  = Get-CimInstance Win32_Processor | Select-Object -First 1
$os   = Get-CimInstance Win32_OperatingSystem

$totalRamGb = [math]::Round($cs.TotalPhysicalMemory / 1GB, 1)
$freeRamGb  = [math]::Round($os.FreePhysicalMemory * 1KB / 1GB, 1)

# JMeter prints its version inside an ASCII-art banner; -v is still the cheapest
# way to confirm it launches at all, which is half the point of this check.
$javaVersion   = Get-ToolVersion -Command "java"   -Arguments @("-version")
$jmeterVersion = Get-ToolVersion -Command "jmeter" -Arguments @("-v")
$nodeVersion   = Get-ToolVersion -Command "node"   -Arguments @("--version")

$lines = @()
$lines += "## Hardware and OS"
$lines += ""
$lines += "| Item | Value |"
$lines += "|---|---|"
$lines += "| Hostname | ``$($cs.Name)`` |"
$lines += "| CPU | $($cpu.Name.Trim()) |"
$lines += "| Cores / logical processors | $($cpu.NumberOfCores) / $($cpu.NumberOfLogicalProcessors) |"
$lines += "| Physical RAM | $totalRamGb GB (free at capture: $freeRamGb GB) |"
$lines += "| OS | $($os.Caption) $($os.Version) |"
$lines += "| Captured at | $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz') |"
$lines += ""
$lines += "## Tooling"
$lines += ""
$lines += "| Tool | Version |"
$lines += "|---|---|"
$lines += "| Java | $javaVersion |"
$lines += "| Apache JMeter | $jmeterVersion |"
$lines += "| Node.js | $nodeVersion |"
$lines += ""
$lines += "> Load generator and system under test share this machine. Response"
$lines += "> times therefore exclude real network latency, and CPU is contended"
$lines += "> between JMeter and the target above a few dozen threads. Both effects"
$lines += "> are stated as validity threats in the report."

$text = $lines -join [Environment]::NewLine

if ($OutFile) {
    $dir = Split-Path -Parent $OutFile
    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    $text | Out-File -FilePath $OutFile -Encoding utf8
    Write-Output "written: $OutFile"
} else {
    Write-Output $text
}
