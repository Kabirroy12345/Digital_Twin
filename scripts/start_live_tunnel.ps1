# ==============================================================================
# PulmoTwin: Persistent Live Tunnel Launcher
# Automatically manages and keeps an active HTTPS tunnel alive
# ==============================================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " PulmoTwin: Live HTTPS Tunnel Manager" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

$port = 7860

# Ensure Flask server is up
$test = Test-NetConnection -ComputerName 127.0.0.1 -Port $port -InformationLevel Quiet
if (-not $test) {
    Write-Host "[!] Starting local PulmoTwin Flask server on port $port..." -ForegroundColor Yellow
    Start-Process -FilePath "C:\Users\HP\AppData\Local\Programs\Python\Python311\python.exe" -ArgumentList "app.py" -WindowStyle Minimized
    Start-Sleep -Seconds 3
}

Write-Host "[+] Local PulmoTwin Server active on http://127.0.0.1:$port" -ForegroundColor Green
Write-Host "[+] Starting persistent HTTPS reverse tunnel..." -ForegroundColor Cyan
Write-Host "    Press Ctrl+C at any time to terminate the tunnel." -ForegroundColor DarkGray

while ($true) {
    Write-Host "`n[*] Establishing connection to tunnel gateway..." -ForegroundColor Yellow
    ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -R 80:127.0.0.1:$port nokey@localhost.run
    Write-Host "[!] Connection dropped. Re-establishing in 5 seconds..." -ForegroundColor Red
    Start-Sleep -Seconds 5
}
