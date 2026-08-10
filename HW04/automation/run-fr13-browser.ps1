param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('chromium', 'firefox', 'webkit')]
  [string]$Browser,

  [switch]$NewWave,

  [string]$Pattern,

  [string]$ReportTag
)

$ErrorActionPreference = 'Stop'
$backendDirectory = 'D:\Sem_9_25_26\Kiem_Thu_Phan_Mem\jmeter_demo\eshop\backend'
$existing = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
if ($existing) {
  Stop-Process -Id $existing.OwningProcess
}

$env:LOADTEST = '1'
$backendProcess = Start-Process `
  -FilePath 'C:\Program Files\nodejs\node.exe' `
  -ArgumentList 'server.js' `
  -WorkingDirectory $backendDirectory `
  -WindowStyle Hidden `
  -PassThru

try {
  $healthy = $false
  for ($attempt = 1; $attempt -le 20; $attempt += 1) {
    Start-Sleep -Milliseconds 250
    try {
      $probe = Invoke-WebRequest -Uri 'http://localhost:3000/api/products' -UseBasicParsing
      if ($probe.StatusCode -eq 200 -and -not $probe.Headers['RateLimit']) {
        $healthy = $true
        break
      }
    } catch {
      # The server may still be binding; retry until the bounded loop expires.
    }
  }
  if (-not $healthy) {
    throw 'FR-13 backend did not become healthy in LOADTEST=1 mode'
  }

  Write-Output "FR-13 backend PID $($backendProcess.Id): healthy, rate limiter bypassed"
  $env:FEATURE = 'fr13'
  $env:BROWSER = if ($ReportTag) {
    $ReportTag
  } elseif ($NewWave) {
    "$Browser-wave"
  } else {
    $Browser
  }
  $arguments = @(
    'playwright', 'test', 'automation/tests/fr13_dashboard', "--project=$Browser"
  )
  if ($Pattern) {
    $arguments += @('--grep', $Pattern)
  } elseif ($NewWave) {
    $arguments += @(
      '--grep', 'FR13-API-'
    )
  }
  & npx.cmd @arguments
  $testExitCode = $LASTEXITCODE
} finally {
  if ($backendProcess -and -not $backendProcess.HasExited) {
    Stop-Process -Id $backendProcess.Id
  }
}

exit $testExitCode
