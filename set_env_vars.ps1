# RedTeamCUA Environment Variables Configuration
# Please fill in your actual API keys and credentials

# ===========================================
# API Keys for CUA Models
# ===========================================

# For Claude models (AWS Bedrock)
# $env:AWS_REGION = "us-east-1"              # Your AWS region
# $env:AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
# $env:AWS_SECRET_KEY = "YOUR_AWS_SECRET_KEY"

# For OpenAI models (Azure)
# $env:AZURE_API_KEY = "YOUR_AZURE_API_KEY"
# $env:AZURE_API_VERSION = "2024-02-15-preview"
# $env:AZURE_ENDPOINT = "https://your-resource.openai.azure.com/"

# For second call (OSWorld action translation)
# $env:AZURE_API_VERSION_FOR_SECOND_CALL = "2024-02-15-preview"
# $env:AZURE_ENDPOINT_FOR_SECOND_CALL = "https://your-resource.openai.azure.com/"

# ===========================================
# Web Platform Domains (Local Setup)
# ===========================================

# For local VMware setup with Docker services
$env:REDDIT = "localhost:9999"         # Reddit forum (if available)
$env:OWNCLOUD = "localhost:8092"       # OwnCloud server
$env:ROCKETCHAT = "localhost:3000"     # RocketChat server

$env:SERVER_HOSTNAME = "localhost"     # Base hostname

# ===========================================
# Optional: SSH Key for Remote Web Platform
# ===========================================
# Only needed if using separate instance for web services
# $env:KEY_FILENAME = "path/to/your/ssh/key.pem"

# ===========================================
# RocketChat NPC Simulation (Optional)
# ===========================================
# For RocketChat agent communication simulation
# $env:AZURE_OPENAI_API_KEY = "YOUR_AZURE_API_KEY"
# $env:AZURE_MODEL_FOR_ROCKETCHAT_NPC = "resource_name/deployment_name/version"

Write-Host "Environment variables template loaded." -ForegroundColor Green
Write-Host "Please uncomment and fill in your actual API keys above." -ForegroundColor Yellow
Write-Host "Web platform domains are set for local Docker services." -ForegroundColor Cyan
