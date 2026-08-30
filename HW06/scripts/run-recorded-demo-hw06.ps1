[CmdletBinding()]
param([int]$TargetSeconds = 292)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$host.UI.RawUI.WindowTitle = 'HW06 SKILL-BASED TEST GENERATION DEMO - 23127184'
$started = Get-Date

function Show-Section([string]$Title, [string]$Subtitle = '') {
    Clear-Host
    Write-Host 'LE PHAM KIEU DUYEN | MSSV 23127184 | HW06' -ForegroundColor Green
    Write-Host 'LIVE DEMO: DUNG AGENT SKILL TAO TEST CASE API' -ForegroundColor Green
    Write-Host ('=' * 78) -ForegroundColor DarkCyan
    Write-Host $Title -ForegroundColor Yellow
    if ($Subtitle) { Write-Host $Subtitle -ForegroundColor Cyan }
    Write-Host ('=' * 78) -ForegroundColor DarkCyan
    Write-Host
}

function Pause-Demo([int]$Seconds) { Start-Sleep -Seconds $Seconds }

function Open-Report([string]$Path, [int]$Seconds = 35) {
    Write-Host ('Report file: ' + (Resolve-Path -LiteralPath $Path).Path) -ForegroundColor White
    Write-Host 'Day la report Newman vua tao, xem truc tiep tren man hinh console.' -ForegroundColor Cyan
    Pause-Demo $Seconds
}

Set-Location $root

Show-Section '1/7  KICH HOAT AGENT SKILL' '.claude/skills/api-test-generator/SKILL.md'
Write-Host 'Yeu cau cho Agent:' -ForegroundColor White
Write-Host '  Dung skill api-test-generator tao test cho POST /api/register.'
Write-Host
Write-Host 'Skill bat buoc pipeline 8 buoc:' -ForegroundColor Yellow
Write-Host '  0 Parse contract        1 Domain partitions'
Write-Host '  2 State transitions     3 Security SEC-01..SEC-07'
Write-Host '  4 Schema validation     5 Validate case quality'
Write-Host '  6 Human review          7 Emit Postman + Excel'
Write-Host
Write-Host 'NGUYEN TAC ORACLE:' -ForegroundColor Red
Write-Host 'Expected result lay tu API spec + FR/SEC, KHONG lay tu response cua SUT.'
Write-Host 'Moi case phai co Rule ID va header X-Student-Id=23127184.'
Write-Host 'Skill bat buoc dung lai de sinh vien review truoc khi publish.'
Pause-Demo 30

Show-Section '2/7  STAGE 0 - PARSE CONTRACT' 'Doc truc tiep API specification va FR-01'
Write-Host 'API SPEC:' -ForegroundColor Yellow
Get-Content -Encoding UTF8 'refs\spec\api_specification.md' -TotalCount 21 | Select-Object -Skip 10
Write-Host
Write-Host 'FR-01 ORACLE:' -ForegroundColor Yellow
$requirements = Get-Content -Encoding UTF8 'refs\spec\eshop_requirements_README.md'
foreach ($i in 30..35) { Write-Host $requirements[$i] }
Write-Host
Write-Host 'Restatement: POST /api/register, JSON body, no auth, success 200.' -ForegroundColor Cyan
Write-Host 'Parameters: name, email, password, confirmPassword; rules FR-01, SEC-01/05/06.'
Pause-Demo 30

Show-Section '3/7  STAGE 1-4 - TAO CAC NHOM TEST' 'Domain partitions + Security + Schema, moi case co oracle'
$cases = Get-Content -Raw -Encoding UTF8 'testcases\api1-fr01-register_cases.json' | ConvertFrom-Json
$cases | Group-Object dim | Sort-Object Name | Select-Object Name, Count | Format-Table -AutoSize
Write-Host 'Vi du test case do Skill tao:' -ForegroundColor Yellow
$cases | Where-Object { $_.id -match '^A1-(DP-001|DP-002|DP-031|SEC-001)$' } |
    Select-Object id, dim, rule, partition, expected | Format-Table -Wrap -AutoSize
Write-Host 'Boundary/invalid: missing, null, empty, whitespace, wrong type, 1000+ chars.'
Write-Host 'Security: SQL injection, role injection, password leak; schema strict.'
Pause-Demo 36

Show-Section '4/7  STAGE 5-6 - VALIDATE VA HUMAN REVIEW' 'AI output khong publish thang; sinh vien audit tung case'
$cases | Group-Object audit_label | Sort-Object Name | Select-Object Name, Count | Format-Table -AutoSize
Write-Host 'Mot case INCOMPLETE thuc te:' -ForegroundColor Yellow
$cases | Where-Object audit_label -eq 'INCOMPLETE' | Select-Object -First 1 |
    Select-Object id, rule, partition, audit_label, audit_reason, correction | Format-List
Write-Host 'VALID: oracle du can cu. INCOMPLETE: chi giu safety invariant co can cu.'
Write-Host 'Moi quyet dinh review deu co reason va correction de truy vet.'
Pause-Demo 34

Show-Section '5/7  STAGE 7 - EMIT ARTIFACTS' 'Render source da review thanh Postman collection va JSON export'
Write-Host '> python scripts/render-cases.py --api 1 --skip-workbook' -ForegroundColor White
Write-Host
& python 'scripts\render-cases.py' --api 1 --skip-workbook
if ($LASTEXITCODE -ne 0) { throw "Renderer failed with exit code $LASTEXITCODE." }
Write-Host
Get-Item 'postman\collections\API1_FR01_Register.postman_collection.json', 'testcases\api1-fr01-register_cases.json' |
    Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
Write-Host 'Da emit X-Student-Id, request body va executable pm.test assertions.' -ForegroundColor Green
Pause-Demo 24

Show-Section '6/7  CHAY LIVE COLLECTION VUA SINH' 'Khoi dong EShop, seed lai DB, chay Newman regression gate'
Write-Host '> .\scripts\Invoke-ApiTests.ps1 -Mode gate' -ForegroundColor White
Write-Host
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root 'scripts\Invoke-ApiTests.ps1') -Mode gate
if ($LASTEXITCODE -ne 0) { throw "Regression gate failed with exit code $LASTEXITCODE." }
Write-Host
Write-Host 'REGRESSION GATE PASSED - collection vua emit da duoc thuc thi.' -ForegroundColor Green
Pause-Demo 10

Show-Section '7/7  KIEM TRA BAO CAO NEWMAN' 'Mo report HTML vua tao, khong dung slide'
$reportFiles = @('reports\API1_FR01_Register.json','reports\API2_FR06_ProductDetail.json','reports\API3_FR11_OrderHistory.json','reports\API4_FR13_AdminOrders.json')
$totalRequests = 0; $totalAssertions = 0; $failedAssertions = 0
foreach ($file in $reportFiles) {
    $report = Get-Content -Raw -Encoding UTF8 $file | ConvertFrom-Json
    $requests = [int]$report.run.stats.requests.total
    $assertions = [int]$report.run.stats.assertions.total
    $failed = [int]$report.run.stats.assertions.failed
    $totalRequests += $requests; $totalAssertions += $assertions; $failedAssertions += $failed
    '{0,-37} req={1,4} assert={2,4} failed={3}' -f (Split-Path $file -Leaf), $requests, $assertions, $failed
}
Write-Host
Write-Host ("LIVE TOTAL: requests={0}; assertions={1}; failed={2}" -f $totalRequests, $totalAssertions, $failedAssertions) -ForegroundColor Green
Write-Host 'Dang mo reports/API1_FR01_Register.html ...' -ForegroundColor Cyan
Pause-Demo 5
Open-Report -Path 'reports\API1_FR01_Register.html' -Seconds 35

Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class DemoForeground {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
}
'@
[DemoForeground]::SetForegroundWindow((Get-Process -Id $PID).MainWindowHandle) | Out-Null
Pause-Demo 2

Show-Section 'HOAN THANH LIVE DEMO' 'Skill -> Spec/FR/SEC -> Review -> Postman -> Newman report'
Write-Host 'API 1: 126 cases (121 AI-generated + 5 student-added).' -ForegroundColor White
Write-Host 'Toan bo suite: 386 cases; ket qua va log luu trong reports/ va evidence/.'
Write-Host 'Khong lay response SUT lam expected result; moi oracle truy vet ve requirement.'
Write-Host
Write-Host 'LE PHAM KIEU DUYEN - 23127184' -ForegroundColor Green
Write-Host 'END OF LIVE HW06 DEMONSTRATION' -ForegroundColor Green

$remaining = $TargetSeconds - [int]((Get-Date) - $started).TotalSeconds
if ($remaining -gt 0) { Pause-Demo $remaining }
