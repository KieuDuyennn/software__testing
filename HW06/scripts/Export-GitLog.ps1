<#
.SYNOPSIS
    Writes the HW06 commit log required by Section 12 of the brief.

.DESCRIPTION
    Exports every commit that touched HW06/ or the HW06 GitHub Actions workflow
    on the current branch to evidence/git-commit-log.txt, in a plain-text format
    a TA can read without running git. Run it again right before packaging the
    submission.

    The workflow file lives at the repository root, so it needs its own
    pathspec: without it the green CI sample commit, which changed nothing else,
    would be missing from the log the CI/CD report cites.
#>
[CmdletBinding()]
param(
    [string] $OutFile = "evidence/git-commit-log.txt"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

# git writes UTF-8; without this PowerShell decodes it as the console codepage
# and the author name comes out as mojibake.
$previousEncoding = [Console]::OutputEncoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$scope = @("HW06", ".github/workflows/hw06-api-tests.yml")

try {
    $repoRoot = (git rev-parse --show-toplevel).Trim()
    $branch   = (git rev-parse --abbrev-ref HEAD).Trim()
    $header = @(
        "HW06 - API Testing | Git commit log",
        "Student ID : 23127184",
        "Repository : $((git remote get-url origin).Trim())",
        "Branch     : $branch",
        "Generated  : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss K')",
        "Scope      : commits touching HW06/ or the HW06 Actions workflow",
        ("=" * 78),
        ""
    )

    # The pathspecs are relative to the current directory, so both git calls must
    # run from the repository root - not from HW06/, where they match nothing.
    Push-Location $repoRoot
    try {
        $log   = git log --date=iso --pretty=format:"%h  %ad  %an%n    %s%n" -- $scope
        $count = (git log --oneline -- $scope | Measure-Object -Line).Lines
    }
    finally { Pop-Location }
}
finally { [Console]::OutputEncoding = $previousEncoding }

$header + $log | Set-Content -Path $OutFile -Encoding utf8
Write-Host "Wrote $OutFile ($count commits in scope)." -ForegroundColor Green
