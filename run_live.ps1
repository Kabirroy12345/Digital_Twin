# PulmoTwin Digital Twin Live Launcher
# Digital Twin Challenge 2026 - Happiest Health Summit
Write-Host '==========================================================' -ForegroundColor Cyan
Write-Host '   Starting PulmoTwin: Live Cardiopulmonary Digital Twin  ' -ForegroundColor Yellow
Write-Host '   Happiest Health Challenge 2026 • Bengaluru Summit      ' -ForegroundColor Cyan
Write-Host '==========================================================' -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $scriptDir) { $scriptDir = Get-Location }

# Locate python
$pythonCandidates = @(
    "C:\Users\HP\AppData\Local\Programs\Python\Python311\python.exe",
    (Join-Path $scriptDir '.venv\Scripts\python.exe'),
    (Join-Path $scriptDir 'venv\Scripts\python.exe'),
    "python"
)

$pythonExe = "python"
foreach ($cand in $pythonCandidates) {
    if (Test-Path $cand) {
        $pythonExe = $cand
        break
    }
}

$appPy = Join-Path $scriptDir 'app.py'

$portCheck = Get-NetTCPConnection -LocalPort 7860 -ErrorAction SilentlyContinue
if (-not $portCheck) {
    Write-Host "[1/2] Starting PulmoTwin Flask Backend ($pythonExe)..." -ForegroundColor Green
    Start-Process -FilePath $pythonExe -ArgumentList $appPy -WorkingDirectory $scriptDir
    Start-Sleep -Seconds 4
} else {
    Write-Host '[1/2] PulmoTwin Backend is already running on port 7860.' -ForegroundColor Green
}

Write-Host '[2/2] Launching Public HTTPS Live Tunnel (localtunnel)...' -ForegroundColor Green
Write-Host 'Open http://127.0.0.1:7860 locally or use the public URL displayed below:' -ForegroundColor Yellow
npx -y localtunnel --port 7860
