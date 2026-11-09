<#
    Validate the CSV contract used by the shared E2E workflow before generating
    or running a plan. This prevents missing columns, empty pools and accidental
    account sharing from becoming fake performance failures.
#>

[CmdletBinding()]
param(
    [string]$DataDir = "data",
    [int]$ExpectedMaxThreads = 0
)

$ErrorActionPreference = "Stop"

$contracts = @(
    @{ File = "credentials.csv";    Columns = @("email", "password"); StatePerUser = $true },
    @{ File = "search_keywords.csv"; Columns = @("keyword", "product_id"); StatePerUser = $false },
    @{ File = "order_payloads.csv"; Columns = @("total_amount", "shipping_address"); StatePerUser = $false }
)

if (-not (Test-Path -LiteralPath $DataDir -PathType Container)) {
    throw "data directory not found: $DataDir"
}

foreach ($contract in $contracts) {
    $path = Join-Path $DataDir $contract.File
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "missing required CSV: $path"
    }

    $header = Get-Content -LiteralPath $path -Encoding UTF8 -TotalCount 1
    if ([string]::IsNullOrWhiteSpace($header)) { throw "empty CSV: $path" }
    $columns = @($header -split ',' | ForEach-Object { $_.Trim().Trim('"') })
    foreach ($required in $contract.Columns) {
        if ($columns -notcontains $required) {
            throw "$($contract.File) is missing column '$required' (found: $($columns -join ', '))"
        }
    }

    $rows = @(Import-Csv -LiteralPath $path -Encoding UTF8)
    if ($rows.Count -eq 0) { throw "$($contract.File) has a header but no data rows" }

    for ($i = 0; $i -lt $rows.Count; $i++) {
        foreach ($required in $contract.Columns) {
            if ([string]::IsNullOrWhiteSpace("$($rows[$i].$required)")) {
                throw "$($contract.File) row $($i + 2) has an empty '$required' value"
            }
        }
    }

    if ($contract.File -eq "credentials.csv") {
        $duplicates = @($rows | Group-Object email | Where-Object Count -gt 1)
        if ($duplicates.Count -gt 0) {
            throw "credentials.csv contains duplicate emails: $($duplicates.Name -join ', ')"
        }
    }

    if ($ExpectedMaxThreads -gt 0 -and $contract.StatePerUser -and $rows.Count -lt $ExpectedMaxThreads) {
        Write-Warning "$($contract.File) has $($rows.Count) rows for $ExpectedMaxThreads VU; credentials will recycle and users will share state"
    }

    Write-Output "CSV OK: $($contract.File) ($($rows.Count) rows)"
}

Write-Output "test-data contract valid: $DataDir"
