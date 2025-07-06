# RedTeamCUA Web Services Setup Script for Windows
# This script sets up all required web services for RedTeamCUA

Write-Host "🚀 Starting RedTeamCUA Web Services Setup..." -ForegroundColor Green

# Create downloads directory
if (!(Test-Path "downloads")) {
    New-Item -ItemType Directory -Path "downloads"
}
Set-Location "downloads"

# Function to check if command exists
function Test-CommandExists {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# Check if Docker is installed
if (!(Test-CommandExists "docker")) {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
if (!(Test-CommandExists "docker-compose")) {
    Write-Host "❌ Docker Compose is not available. Please ensure Docker Desktop is running." -ForegroundColor Red
    exit 1
}

Write-Host "📥 Downloading Reddit Forum image..." -ForegroundColor Yellow

# Download Reddit Forum image
if (!(Test-Path "postmill-populated-exposed-withimg.tar")) {
    Write-Host "Downloading Reddit Forum Docker image..."
    try {
        Invoke-WebRequest -Uri "http://metis.lti.cs.cmu.edu/webarena-images/postmill-populated-exposed-withimg.tar" -OutFile "postmill-populated-exposed-withimg.tar"
        Write-Host "✅ Reddit Forum image downloaded" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to download Reddit Forum image. Error: $_" -ForegroundColor Red
        Write-Host "💡 Trying alternative download method..." -ForegroundColor Yellow
        
        # Try using curl if available
        if (Test-CommandExists "curl") {
            curl -L -o postmill-populated-exposed-withimg.tar "http://metis.lti.cs.cmu.edu/webarena-images/postmill-populated-exposed-withimg.tar"
        }
        else {
            Write-Host "❌ Download failed. Please download manually from:" -ForegroundColor Red
            Write-Host "   http://metis.lti.cs.cmu.edu/webarena-images/postmill-populated-exposed-withimg.tar" -ForegroundColor Cyan
            exit 1
        }
    }
}
else {
    Write-Host "✅ Reddit Forum image already exists" -ForegroundColor Green
}

# Load Reddit image
Write-Host "📦 Loading Reddit Forum Docker image..." -ForegroundColor Yellow
docker load --input postmill-populated-exposed-withimg.tar

# Go back to main directory
Set-Location ".."

Write-Host "🐳 Starting all web services..." -ForegroundColor Yellow
# Start all services using Docker Compose
docker-compose up -d

Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep 30

# Wait for services to be ready
Write-Host "🚀 Waiting for services to initialize..." -ForegroundColor Yellow

$maxAttempts = 60
$attempt = 0

# Wait for RocketChat
Write-Host "Checking RocketChat..." -ForegroundColor Cyan
while ($attempt -lt $maxAttempts) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ RocketChat is ready!" -ForegroundColor Green
            break
        }
    }
    catch {
        Write-Host "." -NoNewline -ForegroundColor Yellow
        Start-Sleep 2
        $attempt++
    }
}

# Wait for OwnCloud
Write-Host "`nChecking OwnCloud..." -ForegroundColor Cyan
$attempt = 0
while ($attempt -lt $maxAttempts) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8092" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ OwnCloud is ready!" -ForegroundColor Green
            break
        }
    }
    catch {
        Write-Host "." -NoNewline -ForegroundColor Yellow
        Start-Sleep 2
        $attempt++
    }
}

# Wait for Reddit Forum
Write-Host "`nChecking Reddit Forum..." -ForegroundColor Cyan
$attempt = 0
while ($attempt -lt $maxAttempts) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:9999" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Reddit Forum is ready!" -ForegroundColor Green
            break
        }
    }
    catch {
        Write-Host "." -NoNewline -ForegroundColor Yellow
        Start-Sleep 2
        $attempt++
    }
}

Write-Host "`n🎉 All services are now running!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Service URLs:" -ForegroundColor Cyan
Write-Host "   🔹 Reddit Forum: http://localhost:9999" -ForegroundColor White
Write-Host "   🔹 OwnCloud: http://localhost:8092" -ForegroundColor White
Write-Host "   🔹 RocketChat: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Default credentials:" -ForegroundColor Cyan
Write-Host "   🔹 OwnCloud: theagentcompany / theagentcompany" -ForegroundColor White
Write-Host "   🔹 RocketChat: theagentcompany / theagentcompany" -ForegroundColor White
Write-Host ""
Write-Host "✅ Web services setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Note: If you encounter any SSL/security errors in browser," -ForegroundColor Yellow
Write-Host "   try using incognito mode or disable 'Always use secure connections' in Chrome settings." -ForegroundColor Yellow
