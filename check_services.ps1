#!/usr/bin/env powershell
# Service Status Check Script for RedTeamCUA

Write-Host "=== RedTeamCUA Service Status Check ===" -ForegroundColor Green

# Set Docker path
$env:PATH = $env:PATH + ";C:\Program Files\Docker\Docker\resources\bin"

Write-Host "`nChecking Docker containers..." -ForegroundColor Yellow
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host "`nChecking web service endpoints..." -ForegroundColor Yellow

# Check OwnCloud
try {
    $owncloud = Invoke-WebRequest -Uri "http://localhost:8092" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ OwnCloud (port 8092): Accessible" -ForegroundColor Green
} catch {
    Write-Host "❌ OwnCloud (port 8092): Not accessible - $($_.Exception.Message)" -ForegroundColor Red
}

# Check RocketChat
try {
    $rocketchat = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ RocketChat (port 3000): Accessible" -ForegroundColor Green
} catch {
    Write-Host "❌ RocketChat (port 3000): Not accessible - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== Service Check Complete ===" -ForegroundColor Green
Write-Host "If all services are running, you can proceed to the next step!" -ForegroundColor Cyan
