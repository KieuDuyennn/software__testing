<#
    new-plan.ps1 — Step 5: implement the test design as a JMeter test plan.

    Composes assets/plan-skeleton.jmx with assets/workflow-fragment.xml, wrapping
    the workflow in the thread-group shape for the requested scenario, and writes
    a file named {StudentId}_{Scenario}_{yyyyMMdd}.jmx.

    Why generate instead of hand-editing: load, stress and spike differ only in
    the shape of concurrency over time. Keeping one workflow definition means a
    fix to an assertion or a header lands in all three plans at once, instead of
    in whichever file someone remembered to update.

    THE DEFAULT PROFILES ARE A FROZEN EXAMPLE, NOT A MEASUREMENT OF YOUR TARGET.
    They were derived once, from one baseline run: the EShop workflow at ~26 ms of
    server time per iteration (~38 iterations/s on a single-threaded target), on a
    4-core laptop, against a catalogue of 5000 products. Change any of those and
    the numbers stop describing anything real — the same endpoints against a
    5-product catalogue have a completely different ceiling.

    The failure mode this warns about is specific and easy to walk into: a plan
    generated with these defaults looks derived, cites "~38 iterations/s", and
    reads like evidence — while nothing was measured. Pass -BaselineIterPerSec
    with a figure you measured (perf-env-and-criteria/scripts/baseline.js prints
    it) and the profiles scale to your target. Omit it and the script says out
    loud, in its output, that the sizing is inherited rather than measured, so
    that admission travels with the plan instead of getting lost.

    Usage:
        powershell -File new-plan.ps1 -Scenario Load   -StudentId 23127184
        powershell -File new-plan.ps1 -Scenario Stress -StudentId 23127184 -OutDir test-plans
        powershell -File new-plan.ps1 -Scenario Spike  -StudentId 23127184 -Threads 240
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("Load", "Stress", "Spike", "Soak")]
    [string]$Scenario,

    [Parameter(Mandatory = $true)]
    [string]$StudentId,

    [string]$Date = (Get-Date -Format "yyyyMMdd"),
    [string]$TargetHost = "localhost",
    [string]$Port = "3000",
    [string]$DataDir = "data",
    [string]$OutDir = "test-plans",

    # Overrides. Left at 0 the scenario default applies.
    [int]$Threads = 0,
    [int]$RampSeconds = 0,
    [int]$DurationSeconds = 0,

    # Measured capacity of YOUR target, in complete workflow iterations per second.
    # baseline.js prints this. Supplying it rescales every thread count from the
    # frozen 38 iter/s example to something that describes the system you are
    # about to test. Left at 0, the example numbers are used and the output says so.
    [double]$BaselineIterPerSec = 0
)

$ErrorActionPreference = "Stop"

$assetDir = Join-Path $PSScriptRoot "..\assets"
$skeletonPath = Join-Path $assetDir "plan-skeleton.jmx"
$fragmentPath = Join-Path $assetDir "workflow-fragment.xml"

foreach ($p in @($skeletonPath, $fragmentPath)) {
    if (-not (Test-Path $p)) { throw "missing asset: $p" }
}

<#
    Scenario profiles.

    think_base/think_range are the Uniform Random Timer settings in milliseconds,
    and the timer fires before EACH of the five samplers — so one iteration takes
    roughly 5 x mean_think plus service time. That multiplier is easy to forget
    and it is what decides how many threads a target rate needs.

    Think time is deliberately compressed to sub-second. A human browsing a shop
    pauses far longer, but reaching the same request rate with realistic pauses
    would need several hundred threads, and past roughly 250 threads this class of
    machine measures JMeter rather than the target. The compression is recorded in
    the plan document as a stated deviation.
#>
$profiles = @{
    Load = @{
        Threads = 50; Ramp = 100; Duration = 600; ThinkBase = 300; ThinkRange = 400
        Listener = "Summary Report"
        Comment  = "~20 iterations/s, about half of measured capacity: anticipated peak."
    }
    Stress = @{
        Threads = 200; Ramp = 600; Duration = 780; ThinkBase = 300; ThinkRange = 400
        Listener = "Aggregate Report"
        Comment  = "Four-stage staircase to roughly 2x capacity; each stage is held before the next increment."
    }
    Spike = @{
        Threads = 200; Ramp = 5; Duration = 60; ThinkBase = 300; ThinkRange = 400
        Listener = "View Results Tree"
        Comment  = "20 VU baseline, abrupt jump to 200 VU for 60s, then recovery."
    }
    Soak = @{
        Threads = 40; Ramp = 80; Duration = 900; ThinkBase = 300; ThinkRange = 400
        Listener = "Summary Report"
        Comment  = "~16 iterations/s held 15 minutes; read for trend, not level."
    }
}

$profile = $profiles[$Scenario]

# The example the defaults were frozen from. Everything below is expressed as a
# ratio to it, so a measured figure rescales the whole profile coherently instead
# of leaving one number updated and the rest stale.
$exampleIterPerSec = 38.0
$sizingProvenance = ""
if ($BaselineIterPerSec -gt 0) {
    $scale = $BaselineIterPerSec / $exampleIterPerSec
    $profile.Threads = [Math]::Max(1, [int][Math]::Round($profile.Threads * $scale))
    $sizingProvenance = ("measured: {0:N1} iterations/s, scaled x{1:N2} from the {2} example" `
        -f $BaselineIterPerSec, $scale, $exampleIterPerSec)
} else {
    # -f binds tighter than +, so the concatenation has to be parenthesised as a
    # whole or the format only applies to the final fragment.
    $sizingProvenance = (("INHERITED, NOT MEASURED: thread counts assume ~{0} iterations/s " +
        "measured on a different machine against 5000 products. Re-measure with baseline.js " +
        "and pass -BaselineIterPerSec, or state in the report that the sizing is unverified.") `
        -f $exampleIterPerSec)
}

if ($Threads -gt 0)         { $profile.Threads = $Threads }
if ($RampSeconds -gt 0)     { $profile.Ramp = $RampSeconds }
if ($DurationSeconds -gt 0) { $profile.Duration = $DurationSeconds }

# Recompute the human-readable sizing note after applying overrides. Frozen
# comments that still say "200 VU" beside a 168-thread plan undermine both the
# audit trail and human review even when the executable XML is correct.
$capacityForComment = if ($BaselineIterPerSec -gt 0) { $BaselineIterPerSec } else { $exampleIterPerSec }
$serviceSeconds = 1.0 / $capacityForComment
$meanThinkPerSamplerSeconds = ($profile.ThinkBase + ($profile.ThinkRange / 2.0)) / 1000.0
$iterationSeconds = $serviceSeconds + (5 * $meanThinkPerSamplerSeconds)
$estimatedRate = $profile.Threads / $iterationSeconds
switch ($Scenario) {
    "Load" {
        $profile.Comment = ("{0} VU; estimated {1:N1} iterations/s ({2:N0}% of sizing capacity)." -f `
            $profile.Threads, $estimatedRate, ($estimatedRate / $capacityForComment * 100))
    }
    "Stress" {
        $profile.Comment = ("Four-stage staircase to {0} VU; estimated peak {1:N1} iterations/s ({2:N0}% of sizing capacity)." -f `
            $profile.Threads, $estimatedRate, ($estimatedRate / $capacityForComment * 100))
    }
    "Spike" {
        $baselineForComment = [math]::Max(10, [int]($profile.Threads / 10))
        $combinedRate = ($profile.Threads + $baselineForComment) / $iterationSeconds
        $profile.Comment = ("{0} VU baseline plus {1} VU burst; estimated combined peak {2:N1} iterations/s ({3:N0}% of sizing capacity)." -f `
            $baselineForComment, $profile.Threads, $combinedRate, ($combinedRate / $capacityForComment * 100))
    }
    "Soak" {
        $profile.Comment = ("{0} VU; estimated {1:N1} iterations/s ({2:N0}% of sizing capacity) for endurance observation." -f `
            $profile.Threads, $estimatedRate, ($estimatedRate / $capacityForComment * 100))
    }
}

<#
    Read and write UTF-8 explicitly.

    Get-Content/Out-File in Windows PowerShell 5.1 default to the ANSI codepage
    on read and to UTF-8 *with BOM* on write. Either one alone corrupts a .jmx:
    the ANSI read mangles non-ASCII characters, and the BOM sits in front of the
    XML declaration where JMeter's parser refuses it.
#>
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Read-Utf8 {
    param([string]$Path)
    return [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
}

$fragment = Read-Utf8 $fragmentPath

# Drop the asset's own documentation header. It explains the file to whoever
# maintains it, and it would otherwise be copied into every thread group of
# every generated plan.
$fragment = [regex]::Replace($fragment, "^\s*<!--.*?-->\s*", "", "Singleline")

$fragment = $fragment -replace "\{\{THINK_BASE\}\}", $profile.ThinkBase
$fragment = $fragment -replace "\{\{THINK_RANGE\}\}", $profile.ThinkRange

function New-ThreadGroup {
    <#
        One ThreadGroup carrying its own copy of the workflow.

        loops = -1 with continue_forever = false means "iterate until the
        scheduler stops you", which is what makes duration the controlling
        parameter rather than a loop count nobody can convert into a time.
    #>
    param(
        [string]$Name,
        [int]$ThreadCount,
        [int]$Ramp,
        [int]$Duration,
        [int]$Delay,
        [string]$Workflow
    )

    $sb = New-Object System.Text.StringBuilder
    [void]$sb.AppendLine("      <ThreadGroup guiclass=`"ThreadGroupGui`" testclass=`"ThreadGroup`" testname=`"$Name`" enabled=`"true`">")
    [void]$sb.AppendLine("        <stringProp name=`"ThreadGroup.on_sample_error`">continue</stringProp>")
    [void]$sb.AppendLine("        <elementProp name=`"ThreadGroup.main_controller`" elementType=`"LoopController`" guiclass=`"LoopControlPanel`" testclass=`"LoopController`" testname=`"Loop Controller`" enabled=`"true`">")
    [void]$sb.AppendLine("          <boolProp name=`"LoopController.continue_forever`">false</boolProp>")
    [void]$sb.AppendLine("          <intProp name=`"LoopController.loops`">-1</intProp>")
    [void]$sb.AppendLine("        </elementProp>")
    [void]$sb.AppendLine("        <stringProp name=`"ThreadGroup.num_threads`">$ThreadCount</stringProp>")
    [void]$sb.AppendLine("        <stringProp name=`"ThreadGroup.ramp_time`">$Ramp</stringProp>")
    [void]$sb.AppendLine("        <boolProp name=`"ThreadGroup.scheduler`">true</boolProp>")
    [void]$sb.AppendLine("        <stringProp name=`"ThreadGroup.duration`">$Duration</stringProp>")
    [void]$sb.AppendLine("        <stringProp name=`"ThreadGroup.delay`">$Delay</stringProp>")
    [void]$sb.AppendLine("        <boolProp name=`"ThreadGroup.same_user_on_next_iteration`">false</boolProp>")
    [void]$sb.AppendLine("      </ThreadGroup>")
    [void]$sb.AppendLine("      <hashTree>")
    [void]$sb.AppendLine($Workflow)
    [void]$sb.AppendLine("      </hashTree>")
    return $sb.ToString()
}

# A spike needs two thread groups: a steady baseline that runs for the whole test
# and a burst that starts partway through. Reading recovery afterwards is the
# point of the scenario, so the baseline outlives the burst on purpose.
if ($Scenario -eq "Spike") {
    $baselineThreads = [math]::Max(10, [int]($profile.Threads / 10))
    $spikeDelay = 90
    $recovery = 120
    $totalDuration = $spikeDelay + $profile.Duration + $recovery

    $threadGroups =
        (New-ThreadGroup -Name "TG baseline ($baselineThreads VU, whole run)" `
            -ThreadCount $baselineThreads -Ramp 20 -Duration $totalDuration -Delay 0 -Workflow $fragment) +
        [Environment]::NewLine +
        (New-ThreadGroup -Name "TG spike ($($profile.Threads) VU burst)" `
            -ThreadCount $profile.Threads -Ramp $profile.Ramp -Duration $profile.Duration -Delay $spikeDelay -Workflow $fragment)
} elseif ($Scenario -eq "Stress") {
    # Build a real staircase rather than a single linear ramp. Each group adds
    # its share of users and remains active until the common end time, so total
    # concurrency rises in four measurable stages. This makes the first stage
    # that violates a threshold attributable; a single ramp only says that the
    # system failed somewhere on the way up.
    $stageCount = 4
    $stageGap = [math]::Max(1, [int][math]::Floor($profile.Ramp / $stageCount))
    $stageRamp = [math]::Max(5, [int][math]::Min(30, [math]::Floor($stageGap / 5)))
    $baseStageThreads = [int][math]::Floor($profile.Threads / $stageCount)
    $remainder = $profile.Threads % $stageCount
    $groups = @()

    for ($i = 0; $i -lt $stageCount; $i++) {
        $increment = $baseStageThreads
        if ($i -lt $remainder) { $increment++ }
        if ($increment -le 0) { continue }

        $delay = $i * $stageGap
        $duration = $profile.Duration - $delay
        if ($duration -le $stageRamp) {
            throw "stress duration is too short for $stageCount stages; increase -DurationSeconds"
        }
        $cumulative = [math]::Min($profile.Threads, ($baseStageThreads * ($i + 1)) + [math]::Min($remainder, $i + 1))
        $groups += New-ThreadGroup -Name "TG Stress stage $($i + 1) (+$increment VU, total $cumulative)" `
            -ThreadCount $increment -Ramp $stageRamp -Duration $duration -Delay $delay -Workflow $fragment
    }
    $threadGroups = $groups -join [Environment]::NewLine
} else {
    $threadGroups = New-ThreadGroup -Name "TG $Scenario ($($profile.Threads) VU)" `
        -ThreadCount $profile.Threads -Ramp $profile.Ramp -Duration $profile.Duration -Delay 0 -Workflow $fragment
}

<#
    Listener per scenario. Three scenarios, three distinct views, because each
    answers a different question:
      Summary Report     compact per-label overview - is the steady state healthy?
      Aggregate Report   percentiles per label      - where does the tail go?
      View Results Tree  individual responses       - what did the failures say?

    The results tree logs errors only. Storing every sample of a 200-thread burst
    would cost more memory than the burst itself.
#>
$listenerGui = @{
    "Summary Report"    = "SummaryReport"
    "Aggregate Report"  = "StatVisualizer"
    "View Results Tree" = "ViewResultsFullVisualizer"
}[$profile.Listener]

$errorLoggingOnly = "false"
if ($profile.Listener -eq "View Results Tree") { $errorLoggingOnly = "true" }

$listener = @"
      <ResultCollector guiclass="$listenerGui" testclass="ResultCollector" testname="$($profile.Listener)" enabled="true">
        <boolProp name="ResultCollector.error_logging">$errorLoggingOnly</boolProp>
        <stringProp name="filename"></stringProp>
      </ResultCollector>
      <hashTree/>
"@

$planName = "${StudentId}_${Scenario}_${Date}"
if ([System.IO.Path]::IsPathRooted($DataDir)) {
    throw "-DataDir must be relative so the submitted .jmx stays portable; use -Jdata.dir or run-scenario.ps1 -DataDir to override it at runtime"
}
$resolvedDataDir = (Resolve-Path $DataDir -ErrorAction SilentlyContinue)
if (-not $resolvedDataDir) { throw "data directory not found: $DataDir" }

# Refuse to generate a plan whose variables are absent or malformed. A plan can
# be valid XML and still send literal ${email} strings for ten minutes.
$validator = Join-Path $PSScriptRoot "validate-test-data.ps1"
if (-not (Test-Path $validator)) { throw "missing validator: $validator" }
& $validator -DataDir $resolvedDataDir.Path -ExpectedMaxThreads $profile.Threads

# Keep the submitted plan portable. The default remains the caller-provided
# relative directory, while -Jdata.dir=... can override it at execution time on
# another machine. Never freeze the current machine's absolute path into .jmx.
$dataDirForXml = $DataDir -replace "\\", "/"
$dataDirForXml = [System.Security.SecurityElement]::Escape($dataDirForXml)
$dataProperty = '${__P(data.dir,' + $dataDirForXml + ')}'

$plan = Read-Utf8 $skeletonPath
$plan = $plan -replace "\{\{PLAN_NAME\}\}", $planName
# XML-escape: the provenance string is prose and may contain & or angle brackets.
$sizingXml = [System.Security.SecurityElement]::Escape("$($profile.Comment) $sizingProvenance")
$plan = $plan.Replace("{{SIZING}}", $sizingXml)
$plan = $plan -replace "\{\{HOST\}\}", $TargetHost
$plan = $plan -replace "\{\{PORT\}\}", $Port
$plan = $plan.Replace("{{DATA_DIR}}", $dataProperty)
$plan = $plan.Replace("{{THREAD_GROUPS}}", $threadGroups)
$plan = $plan.Replace("{{LISTENER}}", $listener)

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }
$outPath = Join-Path $OutDir "$planName.jmx"
[System.IO.File]::WriteAllText((Join-Path (Resolve-Path $OutDir).Path "$planName.jmx"), $plan, $utf8NoBom)

Write-Output "written : $outPath"
Write-Output "scenario: $Scenario - $($profile.Comment)"
Write-Output "threads : $($profile.Threads)  ramp: $($profile.Ramp)s  duration: $($profile.Duration)s"
Write-Output "think   : $($profile.ThinkBase)-$($profile.ThinkBase + $profile.ThinkRange) ms per sampler"
Write-Output "listener: $($profile.Listener)"
Write-Output "data    : portable default '$DataDir' (override with -Jdata.dir=PATH)"
if ($Scenario -eq "Stress") {
    Write-Output "shape   : 4-stage staircase, one increment every ${stageGap}s"
}
if ($BaselineIterPerSec -gt 0) {
    Write-Output "sizing  : $sizingProvenance"
} else {
    Write-Warning $sizingProvenance
}
