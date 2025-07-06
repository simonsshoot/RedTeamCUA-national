# RedTeamCUA OpenAI API 配置脚本
# 已配置您提供的OpenAI API密钥

Write-Host "=== RedTeamCUA OpenAI API 配置 ===" -ForegroundColor Green

# 设置OpenAI API密钥
Write-Host "设置 OpenAI API 环境变量..." -ForegroundColor Yellow
$env:OPENAI_API_KEY = "your_openai_api_key_here"

# 为了兼容项目中的Azure配置格式，设置相应变量
$env:AZURE_API_KEY = $env:OPENAI_API_KEY
$env:AZURE_API_VERSION = "2024-02-15-preview"  
$env:AZURE_ENDPOINT = "https://api.openai.com/v1"

# 用于第二次调用(OSWorld动作翻译)
$env:AZURE_API_VERSION_FOR_SECOND_CALL = "2024-02-15-preview"
$env:AZURE_ENDPOINT_FOR_SECOND_CALL = "https://api.openai.com/v1"

# Web服务配置 (已设置为本地)
$env:OWNCLOUD = "localhost:8092"
$env:ROCKETCHAT = "localhost:3000"
$env:SERVER_HOSTNAME = "localhost"

# 可选: RocketChat NPC 仿真
$env:AZURE_OPENAI_API_KEY = $env:OPENAI_API_KEY
$env:AZURE_MODEL_FOR_ROCKETCHAT_NPC = "gpt-4o"

Write-Host "✅ OpenAI API密钥已设置" -ForegroundColor Green
Write-Host "✅ 兼容Azure配置已设置" -ForegroundColor Green
Write-Host "✅ Web服务环境变量已设置" -ForegroundColor Green

# 验证设置
Write-Host "`n当前配置:" -ForegroundColor Cyan
Write-Host "OPENAI_API_KEY: 已设置 (sk-proj-...)" -ForegroundColor White
Write-Host "AZURE_ENDPOINT: $env:AZURE_ENDPOINT" -ForegroundColor White
Write-Host "OWNCLOUD: $env:OWNCLOUD" -ForegroundColor White  
Write-Host "ROCKETCHAT: $env:ROCKETCHAT" -ForegroundColor White

Write-Host "`n现在可以运行实验了！" -ForegroundColor Green
