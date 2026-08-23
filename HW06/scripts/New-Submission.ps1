<#
.SYNOPSIS
    Preflight-checks and packages the HW06 Moodle submission.

.DESCRIPTION
    Verifies every artefact Section 14 requires, refuses to package while any
    of them is missing or still a placeholder, then builds
    output/23127184_HW06_AI_API_<Grade>.zip and verifies the archive. The
    curated, reviewable folder remains in output/submission-ready/.

    Run with -PreflightOnly at any time to see what is still outstanding.

.PARAMETER Grade
    Three-digit self-assessed grade for the filename, e.g. 095.

.PARAMETER VideoUrl
    YouTube link to the Agent Skill demo. Required unless -PreflightOnly.

.EXAMPLE
    .\scripts\New-Submission.ps1 -PreflightOnly
    .\scripts\New-Submission.ps1 -Grade 095 -VideoUrl https://youtu.be/xxxxxxxxxxx
#>
[CmdletBinding()]
param(
    [ValidatePattern('^https://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_-]+')]
    [string] $VideoUrl,

    [ValidatePattern('^[0-9]{3}$')]
    [string] $Grade = '100',

    [switch] $PreflightOnly
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$studentId = '23127184'
$problems = @()

function Test-Required([string] $Relative, [string] $Why) {
    if (-not (Test-Path -LiteralPath (Join-Path $root $Relative))) {
        $script:problems += "MISSING  $Relative  ($Why)"
    }
}

# --- Artefacts required by Section 14 --------------------------------------
Test-Required 'README.md'                                   'self-assessment table + test summary'
Test-Required 'SUBMISSION_CHECKLIST.md'                     'final handoff checklist'
Test-Required '23127184_HW06_REPORT.md'                     'main report (Markdown)'
Test-Required 'output/pdf/23127184_HW06_AI_API_Report.pdf'  'main report (PDF)'
Test-Required 'output/pdf/23127184_HW06_AI_Audit_Report.pdf' 'AI audit (PDF)'
Test-Required 'docs/ai-audit/AI_AUDIT.md'                   'AI audit report'
Test-Required 'docs/AI_CRITIQUE.md'                         'AI critique, 200-300 words'
Test-Required 'docs/bugs/BUG_REPORT.md'                     'bug report'
Test-Required 'docs/cicd/CI_CD_REPORT.md'                   'CI/CD report'
Test-Required 'docs/postman/POSTMAN_FEATURES.md'            'list of Postman features used'
Test-Required 'docs/design/GENERATOR_DESIGN.md'             'generator design'
Test-Required 'docs/design/generator_pseudocode.py'         'generator pseudocode'
Test-Required 'testcases/23127184_HW06_TestCases.xlsx'      'Excel test cases + summary'
Test-Required 'evidence/git-commit-log.txt'                 'git commit log'

foreach ($c in @('API1_FR01_Register', 'API2_FR06_ProductDetail',
                 'API3_FR11_OrderHistory', 'API4_FR13_AdminOrders')) {
    Test-Required "collections/$c.postman_collection.json" "Postman collection for $c"
    Test-Required "reports/$c.html"                        "Newman HTML report for $c"
}

# --- The self-drawn diagram ------------------------------------------------
$diagramFiles = @(Get-ChildItem -Path (Join-Path $root 'docs/design/diagram') -File -ErrorAction SilentlyContinue)
$diagramImages = @($diagramFiles | Where-Object { $_.Extension -in '.png', '.jpg', '.jpeg', '.svg', '.pdf' })
$diagramSources = @($diagramFiles | Where-Object { $_.Extension -in '.drawio', '.excalidraw', '.pptx', '.fig', '.mermaid', '.mmd' })
if ($diagramImages.Count -eq 0) {
    $problems += "MISSING  docs/design/diagram/*.(png|svg|pdf)  (self-drawn generator diagram)"
}
if ($diagramSources.Count -eq 0) {
    $problems += "MISSING  docs/design/diagram/*.(drawio|excalidraw|pptx|mmd)  (editable source for the self-drawn diagram)"
}

# --- Screenshot evidence ---------------------------------------------------
foreach ($shot in @(
    'evidence/screenshots/postman-console-x-student-id.png',
    'evidence/screenshots/github-actions-green-summary.png',
    'evidence/screenshots/github-actions-red-summary.png',
    'evidence/postman-cloud/workspace.png',
    'evidence/postman-cloud/environment.png',
    'evidence/postman-cloud/runner.png',
    'evidence/postman-cloud/monitor.png',
    'evidence/postman-cloud/mock-server.png'
)) {
    Test-Required $shot 'authentic execution evidence'
}
foreach ($issue in 66..70) {
    $matching = @(Get-ChildItem -Path (Join-Path $root 'evidence/screenshots') -File -ErrorAction SilentlyContinue |
                  Where-Object { $_.Name -like "github-issue-$issue-*.png" })
    if ($matching.Count -eq 0) {
        $problems += "MISSING  evidence/screenshots/github-issue-$issue-*.png  (GitHub Issue evidence)"
    }
}

# --- Placeholders that must be resolved ------------------------------------
foreach ($doc in @('README.md', '23127184_HW06_REPORT.md')) {
    $path = Join-Path $root $doc
    if (Test-Path -LiteralPath $path) {
        $text = Get-Content -Raw -Encoding UTF8 $path
        if ($text -match '_?TODO_?') { $problems += "PLACEHOLDER  $doc still contains TODO markers" }
    }
}

$readmeText = Get-Content -Raw -Encoding UTF8 (Join-Path $root 'README.md')
$reportText = Get-Content -Raw -Encoding UTF8 (Join-Path $root '23127184_HW06_REPORT.md')
if ($readmeText -match 'Pending authentic evidence|_Finalize after evidence_') {
    $problems += 'PLACEHOLDER  README.md self-assessment is not finalized'
}
if ($reportText -match 'Group uniqueness:\*\*\s*pending') {
    $problems += 'PLACEHOLDER  main report still needs dated group uniqueness confirmation'
}
if (($readmeText -match 'VIDEO_ID') -or
    ($readmeText -notmatch 'https://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_-]{6,}')) {
    $problems += 'PLACEHOLDER  README.md still needs the real YouTube demo URL'
}
if ($reportText -notmatch 'https://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_-]{6,}') {
    $problems += 'PLACEHOLDER  main report still needs the real YouTube demo URL'
}

# --- AI critique word count (200-300, mandatory) ---------------------------
$critiquePath = Join-Path $root 'docs/AI_CRITIQUE.md'
if (Test-Path -LiteralPath $critiquePath) {
    $raw = Get-Content -Raw -Encoding UTF8 $critiquePath
    $marker = '## Final critique'
    $idx = $raw.IndexOf($marker)
    if ($idx -lt 0) {
        $problems += "AI critique: '## Final critique' section not found"
    } else {
        $body = $raw.Substring($idx + $marker.Length)
        $body = ($body -split '\r?\n' | Where-Object { $_ -notmatch '^\s*[#>*|-]|^\s*$' }) -join ' '
        $words = ([regex]::Matches($body, "\b[\w'-]+\b")).Count
        if ($words -lt 200 -or $words -gt 300) {
            $problems += "AI critique must be 200-300 words; found $words"
        }
    }
}

# --- Report ----------------------------------------------------------------
if ($problems.Count -gt 0) {
    Write-Host "`nPreflight found $($problems.Count) outstanding item(s):`n" -ForegroundColor Yellow
    $problems | ForEach-Object { Write-Host "  $_" -ForegroundColor Yellow }
    if (-not $PreflightOnly) { throw "Refusing to package an incomplete submission." }
    Write-Host "`n(Preflight only - nothing packaged.)`n" -ForegroundColor DarkGray
    exit 1
}

Write-Host "`nPreflight passed: every machine-checkable artefact is present." -ForegroundColor Green
if ($PreflightOnly) {
    Write-Host "Remaining human gates: the diagram really is self-drawn, the critique is yours, the video link works."
    exit 0
}

if ([string]::IsNullOrWhiteSpace($VideoUrl)) {
    throw "VideoUrl is required to package. Do not submit with a pending link."
}

# --- Stage -----------------------------------------------------------------
$output  = Join-Path $root 'output'
$staging = Join-Path $output 'submission-ready'
$zipPath = Join-Path $output "${studentId}_HW06_AI_API_${Grade}.zip"

if (Test-Path -LiteralPath $staging) { Remove-Item -LiteralPath $staging -Recurse -Force }
New-Item -ItemType Directory -Path $staging | Out-Null

foreach ($dir in @('.claude', 'collections', 'config', 'data', 'docs', 'evidence',
                   'refs', 'reports', 'scripts', 'testcases')) {
    $src = Join-Path $root $dir
    if (Test-Path -LiteralPath $src) {
        Copy-Item -LiteralPath $src -Destination (Join-Path $staging $dir) -Recurse -Force
    }
}
Copy-Item -LiteralPath (Join-Path $root 'README.md'),
                       (Join-Path $root 'SUBMISSION_CHECKLIST.md'),
                       (Join-Path $root '23127184_HW06_REPORT.md'),
                       (Join-Path $root 'package.json') -Destination $staging

$pdfDest = Join-Path $staging 'output/pdf'
New-Item -ItemType Directory -Path $pdfDest -Force | Out-Null
Get-ChildItem -LiteralPath (Join-Path $root 'output/pdf') -File | Copy-Item -Destination $pdfDest -Force

# Ship the pipeline definition, which lives at the repository root.
$wfDest = Join-Path $staging 'cicd-workflow'
New-Item -ItemType Directory -Path $wfDest -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $root '../.github/workflows/hw06-api-tests.yml') -Destination $wfDest -Force

# --- Zip with portable entry names -----------------------------------------
# .NET Framework's CreateFromDirectory writes backslash entry names, which are
# not ZIP-spec conformant and unpack as one literal filename on Linux/macOS.
# Entries are therefore added explicitly with forward slashes.
if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$prefix = $staging.TrimEnd('\') + '\'
$writer = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($file in Get-ChildItem -LiteralPath $staging -Recurse -File -Force) {
        $entry = $file.FullName.Substring($prefix.Length).Replace('\', '/')
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
            $writer, $file.FullName, $entry,
            [System.IO.Compression.CompressionLevel]::Optimal) | Out-Null
    }
} finally { $writer.Dispose() }

# --- Verify the archive ----------------------------------------------------
$archive = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    $entries = @($archive.Entries.FullName | ForEach-Object { $_.Replace('\', '/') })
    foreach ($required in @(
        'README.md',
        '23127184_HW06_REPORT.md',
        'output/pdf/23127184_HW06_AI_API_Report.pdf',
        'output/pdf/23127184_HW06_AI_Audit_Report.pdf',
        'docs/bugs/BUG_REPORT.md',
        'docs/cicd/CI_CD_REPORT.md',
        'testcases/23127184_HW06_TestCases.xlsx',
        'evidence/git-commit-log.txt',
        'cicd-workflow/hw06-api-tests.yml'
    )) {
        if ($entries -notcontains $required) { throw "ZIP verification failed: $required" }
    }
    if (($entries | Where-Object { $_ -like '*\*' }).Count -gt 0) {
        throw "ZIP contains backslash entry names - it will not unpack correctly on Linux/macOS."
    }
} finally { $archive.Dispose() }

Write-Host "`nCreated and verified: $zipPath" -ForegroundColor Green
Write-Host "$($entries.Count) entries. Open the ZIP once by hand, then upload it to Moodle."
