# RedTeamCUA 多模型API密钥配置脚本
# 支持国内外主流LLM API服务

Write-Host "=== RedTeamCUA 多模型API配置向导 ===" -ForegroundColor Green

Write-Host "`n选择您要配置的API服务:" -ForegroundColor Cyan
Write-Host "1. OpenAI (GPT-4o, GPT-3.5-turbo)" -ForegroundColor White
Write-Host "2. Kimi (月之暗面 - moonshot)" -ForegroundColor White  
Write-Host "3. DeepSeek (深度求索)" -ForegroundColor White
Write-Host "4. 智谱AI (GLM-4)" -ForegroundColor White
Write-Host "5. 通义千问 (阿里云)" -ForegroundColor White
Write-Host "6. 文心一言 (百度)" -ForegroundColor White
Write-Host "7. 配置所有 (跳过空值)" -ForegroundColor Yellow

$choice = Read-Host "`n请输入选择 (1-7)"

function Set-OpenAI-Config {
    Write-Host "`n配置OpenAI API..." -ForegroundColor Yellow
    $apiKey = Read-Host "请输入OpenAI API Key (sk-...)"
    if ($apiKey) {
        $env:OPENAI_API_KEY = $apiKey
        Write-Host "✅ OpenAI API Key 已设置" -ForegroundColor Green
    }
}

function Set-Kimi-Config {
    Write-Host "`n配置Kimi API..." -ForegroundColor Yellow
    $apiKey = Read-Host "请输入Kimi API Key (sk-...)"
    if ($apiKey) {
        $env:KIMI_API_KEY = $apiKey
        Write-Host "✅ Kimi API Key 已设置" -ForegroundColor Green
    }
}

function Set-DeepSeek-Config {
    Write-Host "`n配置DeepSeek API..." -ForegroundColor Yellow
    $apiKey = Read-Host "请输入DeepSeek API Key (sk-...)"
    if ($apiKey) {
        $env:DEEPSEEK_API_KEY = $apiKey
        Write-Host "✅ DeepSeek API Key 已设置" -ForegroundColor Green
    }
}

function Set-Zhipu-Config {
    Write-Host "`n配置智谱AI API..." -ForegroundColor Yellow
    $apiKey = Read-Host "请输入智谱AI API Key"
    if ($apiKey) {
        $env:ZHIPU_API_KEY = $apiKey
        Write-Host "✅ 智谱AI API Key 已设置" -ForegroundColor Green
    }
}

function Set-Qwen-Config {
    Write-Host "`n配置通义千问 API..." -ForegroundColor Yellow
    $apiKey = Read-Host "请输入通义千问 API Key (sk-...)"
    if ($apiKey) {
        $env:QWEN_API_KEY = $apiKey
        Write-Host "✅ 通义千问 API Key 已设置" -ForegroundColor Green
    }
}

function Set-Baidu-Config {
    Write-Host "`n配置文心一言 API..." -ForegroundColor Yellow
    $apiKey = Read-Host "请输入百度API Key"
    $secretKey = Read-Host "请输入百度Secret Key"
    if ($apiKey -and $secretKey) {
        $env:BAIDU_API_KEY = $apiKey
        $env:BAIDU_SECRET_KEY = $secretKey
        Write-Host "✅ 文心一言 API Keys 已设置" -ForegroundColor Green
    }
}

# 根据用户选择执行配置
switch ($choice) {
    "1" { Set-OpenAI-Config }
    "2" { Set-Kimi-Config }
    "3" { Set-DeepSeek-Config }
    "4" { Set-Zhipu-Config }
    "5" { Set-Qwen-Config }
    "6" { Set-Baidu-Config }
    "7" {
        Write-Host "`n配置所有API..." -ForegroundColor Yellow
        Set-OpenAI-Config
        Set-Kimi-Config
        Set-DeepSeek-Config
        Set-Zhipu-Config
        Set-Qwen-Config
        Set-Baidu-Config
    }
    default {
        Write-Host "无效选择，退出配置" -ForegroundColor Red
        exit
    }
}

# 设置Web服务环境变量 (兼容现有配置)
$env:OWNCLOUD = "localhost:8092"
$env:ROCKETCHAT = "localhost:3000"
$env:SERVER_HOSTNAME = "localhost"

Write-Host "`n=== 配置完成 ===" -ForegroundColor Green
Write-Host "现在可以运行API测试:" -ForegroundColor Cyan
Write-Host "python test_multi_model_api.py" -ForegroundColor White

Write-Host "`n示例运行命令:" -ForegroundColor Cyan
Write-Host "# 使用Kimi模型运行实验" -ForegroundColor Gray
Write-Host "python run.py --model `"kimi | moonshot-v1-8k`" --headless \\" -ForegroundColor White
Write-Host "  --path_to_vm ./vmware_vm_data/Ubuntu0/Ubuntu0.vmx \\" -ForegroundColor White
Write-Host "  --observation_type screenshot \\" -ForegroundColor White
Write-Host "  --test_all_meta_path ./evaluation_examples/test_all_owncloud.json \\" -ForegroundColor White
Write-Host "  --domain owncloud --max_steps 5" -ForegroundColor White

Write-Host "`n# 使用DeepSeek模型运行实验" -ForegroundColor Gray
Write-Host "python run.py --model `"deepseek | deepseek-chat`" --headless \\" -ForegroundColor White
Write-Host "  --path_to_vm ./vmware_vm_data/Ubuntu0/Ubuntu0.vmx \\" -ForegroundColor White
Write-Host "  --observation_type screenshot \\" -ForegroundColor White
Write-Host "  --test_all_meta_path ./evaluation_examples/test_all_owncloud.json \\" -ForegroundColor White
Write-Host "  --domain owncloud --max_steps 5" -ForegroundColor White

Write-Host "`n📋 API密钥获取地址:" -ForegroundColor Yellow
Write-Host "• OpenAI: https://platform.openai.com/api-keys" -ForegroundColor White
Write-Host "• Kimi: https://platform.moonshot.cn/console/api-keys" -ForegroundColor White  
Write-Host "• DeepSeek: https://platform.deepseek.com/api_keys" -ForegroundColor White
Write-Host "• 智谱AI: https://open.bigmodel.cn/usercenter/apikeys" -ForegroundColor White
Write-Host "• 通义千问: https://dashscope.console.aliyun.com/" -ForegroundColor White
Write-Host "• 文心一言: https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application" -ForegroundColor White
