[CmdletBinding()]
param(
    [Parameter()]
    [ValidatePattern('^https://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_-]+')]
    [string]$VideoUrl,

    [Parameter()]
    [ValidatePattern('^[0-9]{3}$')]
    [string]$Grade = '090',

    [switch]$PreflightOnly
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$studentId = '23127184'
$readmePath = Join-Path $root 'README.md'
$reportPath = Join-Path $root '23127184_HW05_REPORT.md'

function Require-Path([string]$RelativePath) {
    $path = Join-Path $root $RelativePath
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Missing required artifact: $RelativePath"
    }
}

$required = @(
    'README.md',
    '23127184_HW05_REPORT.md',
    'docs/AI_CRITIQUE.md',
    'docs/ai-audit/AI_AUDIT.md',
    'docs/phases/05_continuous_performance.md',
    'docs/assets/continuous-performance-flow.png',
    'test-plans/23127184_Load_20260817.jmx',
    'test-plans/23127184_Stress_20260817.jmx',
    'test-plans/23127184_Spike_20260817.jmx',
    'test-plans/23127184_Soak_20260817.jmx',
    'data/credentials.csv',
    'data/search_keywords.csv',
    'data/order_payloads.csv',
    'evidence/hardware/dxdiag.txt',
    'evidence/screenshots/23127184_hardware_dxdiag_20260817.png'
)
$required | ForEach-Object { Require-Path $_ }

$runs = @(
    'results/23127184_Load_20260817_20260817-222415',
    'results/23127184_Stress_20260817_20260817-223704',
    'results/23127184_Spike_20260817_20260817-224818',
    'results/23127184_Soak_20260817_20260817-225434'
)
foreach ($run in $runs) {
    foreach ($artifact in @('result.jtl', 'resources.csv', 'jmeter.log', 'run.md', 'report/index.html')) {
        Require-Path (Join-Path $run $artifact)
    }
}

$critique = Get-Content -Raw -Encoding UTF8 (Join-Path $root 'docs/AI_CRITIQUE.md')
$critiqueBody = ($critique -split '\r?\n' | Where-Object { $_ -notmatch '^#|^>|^\s*$' }) -join ' '
$wordCount = ([regex]::Matches($critiqueBody, "\b[\w'-]+\b")).Count
if ($wordCount -lt 200 -or $wordCount -gt 300) {
    throw "AI Critique must contain 200-300 words; found $wordCount."
}

if ($PreflightOnly) {
    Write-Host 'Preflight passed for all machine-checkable artifacts.'
    Write-Host 'Remaining human gate: genuine video URL and critique approval.'
    exit 0
}

if ([string]::IsNullOrWhiteSpace($VideoUrl)) {
    throw 'VideoUrl is required. Do not package with VIDEO_URL_PENDING.'
}

foreach ($path in @($readmePath, $reportPath)) {
    $content = Get-Content -Raw -Encoding UTF8 $path
    if ($content -notmatch 'VIDEO_URL_PENDING') {
        if ($content -notmatch [regex]::Escape($VideoUrl)) {
            throw "No pending video marker or matching URL in $path"
        }
    } else {
        $content = $content.Replace('VIDEO_URL_PENDING', $VideoUrl)
        Set-Content -LiteralPath $path -Value $content -Encoding UTF8
    }
}

& python (Join-Path $root 'scripts/build-pdfs.py')
if ($LASTEXITCODE -ne 0) { throw 'PDF build or validation failed.' }

$gitLogPath = Join-Path $root 'evidence/git-commit-log.txt'
$gitLog = & git -C $root log --date=iso-strict --pretty=format:'%h %ad %s'
Set-Content -LiteralPath $gitLogPath -Value $gitLog -Encoding UTF8

$output = Join-Path $root 'output'
$staging = Join-Path $output 'submission-staging'
$zipName = $studentId + '_HW05_AI_Performance_' + $Grade + '.zip'
$zipPath = Join-Path $output $zipName
if (-not $staging.StartsWith($output + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'Refusing to clean staging outside output.'
}
if (Test-Path -LiteralPath $staging) { Remove-Item -LiteralPath $staging -Recurse -Force }
New-Item -ItemType Directory -Path $staging | Out-Null

$directories = @('.claude/skills', 'config', 'data', 'docs', 'evidence', 'refs', 'results', 'scripts', 'test-plans')
foreach ($directory in $directories) {
    $source = Join-Path $root $directory
    $destination = Join-Path $staging $directory
    New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force
}
Copy-Item -LiteralPath $readmePath,$reportPath -Destination $staging
$pdfDestination = Join-Path $staging 'output/pdf'
New-Item -ItemType Directory -Path $pdfDestination -Force | Out-Null
Get-ChildItem -LiteralPath (Join-Path $root 'output/pdf') -File | Copy-Item -Destination $pdfDestination -Force

if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory(
    $staging,
    $zipPath,
    [System.IO.Compression.CompressionLevel]::Optimal,
    $false
)

$archive = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    $entries = $archive.Entries.FullName
    foreach ($entry in @(
        'README.md',
        '23127184_HW05_REPORT.md',
        'output/pdf/23127184_HW05_AI_Performance_Report.pdf',
        'output/pdf/23127184_HW05_AI_Audit_Report.pdf',
        'evidence/git-commit-log.txt'
    )) {
        if ($entries -notcontains $entry) { throw "ZIP verification failed: $entry" }
    }
    foreach ($entryName in @('README.md', '23127184_HW05_REPORT.md')) {
        $entry = $archive.GetEntry($entryName)
        $reader = [System.IO.StreamReader]::new($entry.Open())
        try {
            if ($reader.ReadToEnd().Contains('VIDEO_URL_PENDING')) {
                throw "ZIP still contains a pending video marker in $entryName"
            }
        } finally {
            $reader.Dispose()
        }
    }
} finally {
    $archive.Dispose()
}

Write-Host "Created and verified: $zipPath"
Write-Host 'Open the ZIP manually once, then upload it to Moodle.'