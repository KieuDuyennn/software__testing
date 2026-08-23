<#
.SYNOPSIS
    Writes the HW06 commit log required by Section 12 of the brief.

.DESCRIPTION
    Exports every commit that touched HW06/ on the current branch to
    evidence/git-commit-log.txt, in a plain-text format a TA can read without
    running git. Run it again right before packaging the submission.
#>
[CmdletBinding()]
param(
    [string] $OutFile = "evidence/git-commit-log.txt"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$repoRoot = (git rev-parse --show-toplevel).Trim()
$branch   = (git rev-parse --abbrev-ref HEAD).Trim()
$header = @(
    "HW06 - API Testing | Git commit log",
    "Student ID : 23127184",
    "Repository : $((git remote get-url origin).Trim())",
    "Branch     : $branch",
    "Generated  : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss K')",
    "Scope      : commits touching HW06/",
    ("=" * 78),
    ""
)

Push-Location $repoRoot
try {
    $log = git log --date=iso --pretty=format:"%h  %ad  %an%n    %s%n" -- HW06
}
finally { Pop-Location }

$header + $log | Set-Content -Path $OutFile -Encoding utf8
$count = (git log --oneline -- HW06 | Measure-Object -Line).Lines
Write-Host "Wrote $OutFile ($count commits touching HW06/)." -ForegroundColor Green
