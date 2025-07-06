# RedTeamCUA-National GitHub上传脚本 (PowerShell版本)
# Usage: .\upload_to_github.ps1

Write-Host "=== RedTeamCUA-National GitHub上传脚本 ===" -ForegroundColor Green
Write-Host

# 检查Git是否安装
try {
    $gitVersion = git --version
    Write-Host "✅ Git已安装: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git未安装，请先安装Git:" -ForegroundColor Red
    Write-Host "   下载地址: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "   或使用winget: winget install Git.Git" -ForegroundColor Yellow
    exit 1
}

# 设置项目目录
$PROJECT_DIR = $PSScriptRoot
Write-Host "📁 项目目录: $PROJECT_DIR" -ForegroundColor Cyan

# 切换到项目目录
Set-Location $PROJECT_DIR

# 检查是否在正确的目录
if (-not (Test-Path "run.py")) {
    Write-Host "❌ 错误：不在RedTeamCUA项目目录中" -ForegroundColor Red
    exit 1
}

# 初始化Git仓库（如果不存在）
if (-not (Test-Path ".git")) {
    Write-Host "🔧 初始化Git仓库..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git仓库初始化完成" -ForegroundColor Green
} else {
    Write-Host "📦 Git仓库已存在" -ForegroundColor Green
}

# 检查虚拟机目录是否被正确忽略
Write-Host "🔍 检查虚拟机目录排除情况..." -ForegroundColor Cyan
if (Test-Path "vmware_vm_data") {
    $gitIgnoreCheck = git check-ignore vmware_vm_data 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 虚拟机目录已被Git忽略" -ForegroundColor Green
    } else {
        Write-Host "⚠️  警告：虚拟机目录未被忽略，添加到.gitignore" -ForegroundColor Yellow
        Add-Content .gitignore "`nvmware_vm_data/"
    }
}

# 检查大文件
Write-Host "📊 检查大文件..." -ForegroundColor Cyan
$largeFiles = Get-ChildItem -Recurse -File | Where-Object { $_.Length -gt 100MB -and $_.FullName -notlike "*\.git\*" }
foreach ($file in $largeFiles) {
    $sizeGB = [math]::Round($file.Length / 1GB, 2)
    $sizeMB = [math]::Round($file.Length / 1MB, 2)
    if ($sizeGB -gt 1) {
        Write-Host "⚠️  大文件警告: $($file.Name) ($sizeGB GB)" -ForegroundColor Yellow
    } else {
        Write-Host "⚠️  大文件警告: $($file.Name) ($sizeMB MB)" -ForegroundColor Yellow
    }
}

# 显示将要上传的文件统计
Write-Host "📈 文件统计：" -ForegroundColor Cyan
$pythonFiles = (Get-ChildItem -Recurse -Include "*.py" | Where-Object { $_.FullName -notlike "*__pycache__*" }).Count
$configFiles = (Get-ChildItem -Recurse -Include "*.json", "*.yml", "*.yaml").Count
$docFiles = (Get-ChildItem -Recurse -Include "*.md", "*.txt").Count
Write-Host "   Python文件: $pythonFiles" -ForegroundColor White
Write-Host "   配置文件: $configFiles" -ForegroundColor White
Write-Host "   文档文件: $docFiles" -ForegroundColor White

# 设置Git用户信息（如果未设置）
try {
    $userName = git config user.name
    if (-not $userName) {
        Write-Host "🔧 设置Git用户信息..." -ForegroundColor Yellow
        $username = Read-Host "请输入Git用户名"
        $email = Read-Host "请输入Git邮箱"
        git config user.name "$username"
        git config user.email "$email"
        Write-Host "✅ Git用户信息设置完成" -ForegroundColor Green
    }
} catch {
    Write-Host "🔧 设置Git用户信息..." -ForegroundColor Yellow
    $username = Read-Host "请输入Git用户名"
    $email = Read-Host "请输入Git邮箱"
    git config user.name "$username"
    git config user.email "$email"
    Write-Host "✅ Git用户信息设置完成" -ForegroundColor Green
}

# 添加远程仓库
Write-Host "🔗 配置远程仓库..." -ForegroundColor Cyan
try {
    $existingRemote = git remote get-url origin 2>$null
    if ($existingRemote) {
        Write-Host "📡 远程仓库已存在: $existingRemote" -ForegroundColor Green
        $changeRemote = Read-Host "是否要更改远程仓库地址？(y/N)"
        if ($changeRemote -eq "y" -or $changeRemote -eq "Y") {
            git remote set-url origin git@github.com:simonsshoot/RedTeamCUA-national.git
            Write-Host "✅ 远程仓库地址已更新" -ForegroundColor Green
        }
    } else {
        throw "No remote found"
    }
} catch {
    git remote add origin git@github.com:simonsshoot/RedTeamCUA-national.git
    Write-Host "✅ 远程仓库已添加" -ForegroundColor Green
}

# 创建主要的README文件
if (Test-Path "README_GITHUB.md") {
    Copy-Item "README_GITHUB.md" "README.md" -Force
    Write-Host "✅ GitHub README已创建" -ForegroundColor Green
}

# 添加所有文件到Git
Write-Host "📦 添加文件到Git..." -ForegroundColor Cyan
git add .

# 显示状态
Write-Host "📋 Git状态：" -ForegroundColor Cyan
$gitStatus = git status --short
$statusLines = $gitStatus | Select-Object -First 20
foreach ($line in $statusLines) {
    Write-Host "   $line" -ForegroundColor White
}
if ($gitStatus.Count -gt 20) {
    Write-Host "   ... 还有 $($gitStatus.Count - 20) 个文件" -ForegroundColor Gray
}

# 确认提交
Write-Host
$confirm = Read-Host "是否继续提交所有更改？(Y/n)"
if ($confirm -ne "n" -and $confirm -ne "N") {
    # 提交更改
    Write-Host "💾 提交更改..." -ForegroundColor Yellow
    $commitMessage = @"
feat: RedTeamCUA-National项目初始化

- 添加国内大模型支持 (Kimi, DeepSeek)
- 基于论文数据的ASR评估结果
- 完整的Docker + VMware环境配置
- CIA攻击类型分析和可视化
- 一键部署和测试脚本
- 详细的中文文档和使用指南
- 安全配置和最佳实践建议

排除内容:
- 虚拟机镜像文件 (vmware_vm_data/)
- 实验结果和缓存数据
- API密钥和敏感配置
"@

    git commit -m $commitMessage
    Write-Host "✅ 提交完成" -ForegroundColor Green

    # 推送到GitHub
    Write-Host "🚀 推送到GitHub..." -ForegroundColor Yellow
    Write-Host "⚠️  首次推送可能需要SSH密钥认证" -ForegroundColor Yellow
    
    try {
        git push -u origin main 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ 推送成功！" -ForegroundColor Green
        } else {
            git push -u origin master 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ 推送成功！" -ForegroundColor Green
            } else {
                throw "Push failed"
            }
        }
    } catch {
        Write-Host "❌ 推送失败，尝试手动推送：" -ForegroundColor Red
        Write-Host "   git push -u origin main" -ForegroundColor Yellow
        Write-Host "   或" -ForegroundColor Yellow
        Write-Host "   git push -u origin master" -ForegroundColor Yellow
        Write-Host
        Write-Host "可能的原因：" -ForegroundColor Yellow
        Write-Host "1. SSH密钥未配置" -ForegroundColor White
        Write-Host "2. GitHub仓库不存在或无权限" -ForegroundColor White
        Write-Host "3. 网络连接问题" -ForegroundColor White
        
        # 提供SSH密钥配置帮助
        Write-Host
        Write-Host "SSH密钥配置帮助：" -ForegroundColor Cyan
        Write-Host "1. 生成SSH密钥：ssh-keygen -t rsa -b 4096 -C `"your_email@example.com`"" -ForegroundColor White
        Write-Host "2. 复制公钥：Get-Content `"~\.ssh\id_rsa.pub`"" -ForegroundColor White
        Write-Host "3. 在GitHub设置中添加SSH密钥" -ForegroundColor White
        exit 1
    }

    # 成功信息
    Write-Host
    Write-Host "🎉 上传完成！" -ForegroundColor Green
    Write-Host "📍 仓库地址: https://github.com/simonsshoot/RedTeamCUA-national" -ForegroundColor Cyan
    Write-Host "📝 建议下一步操作：" -ForegroundColor Yellow
    Write-Host "   1. 在GitHub上检查文件是否正确上传" -ForegroundColor White
    Write-Host "   2. 更新仓库描述和标签" -ForegroundColor White
    Write-Host "   3. 创建Release版本" -ForegroundColor White
    Write-Host "   4. 添加贡献者指南" -ForegroundColor White
    
} else {
    Write-Host "❌ 用户取消上传" -ForegroundColor Red
}

Write-Host
Write-Host "=== 脚本执行完成 ===" -ForegroundColor Green
