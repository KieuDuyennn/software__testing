[CmdletBinding()]
param(
    [int]$DurationSeconds = 300,
    [string]$OutputPath = 'output/demo/23127184_HW06_live_demo_5min.mp4'
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$output = Join-Path $root $OutputPath
$presenter = Join-Path $PSScriptRoot 'run-recorded-demo-hw06.ps1'

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    throw 'ffmpeg is not available on PATH.'
}
New-Item -ItemType Directory -Force -Path (Split-Path $output -Parent) | Out-Null

$font = 'C\:/Windows/Fonts/arialbd.ttf'
$filter = "drawbox=x=0:y=0:w=iw:h=48:color=black@0.58:t=fill," +
          "drawtext=fontfile='$font':text='HW06 LIVE DEMO | LE PHAM KIEU DUYEN | 23127184':" +
          'fontcolor=white:fontsize=22:x=w-tw-16:y=12'

$ffmpegArgs = @(
    '-y',
    '-f', 'gdigrab',
    '-framerate', '15',
    '-draw_mouse', '1',
    '-i', 'desktop',
    '-f', 'lavfi',
    '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
    '-vf', $filter,
    '-t', $DurationSeconds,
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-crf', '23',
    '-pix_fmt', 'yuv420p',
    '-c:a', 'aac',
    '-b:a', '96k',
    '-shortest',
    $output
)

Write-Host "Recording a $DurationSeconds-second live demo to $output" -ForegroundColor Green
$ffmpegProcess = Start-Process ffmpeg -ArgumentList $ffmpegArgs -NoNewWindow -PassThru
Start-Sleep -Seconds 2
# Run presenter in this same visible terminal so the desktop capture contains
# the live skill pipeline, rather than a hidden child console.
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $presenter -TargetSeconds ($DurationSeconds - 8)
Wait-Process -Id $ffmpegProcess.Id -Timeout 30 -ErrorAction SilentlyContinue
if (-not $ffmpegProcess.HasExited) { Stop-Process -Id $ffmpegProcess.Id -Force }
if (-not (Test-Path -LiteralPath $output)) { throw 'ffmpeg did not produce the MP4.' }

Get-Item -LiteralPath $output | Select-Object FullName, Length, LastWriteTime
