#!/bin/bash
# RedTeamCUA-National GitHub上传脚本

echo "=== RedTeamCUA-National GitHub上传脚本 ==="
echo

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装，请先安装Git："
    echo "   Windows: https://git-scm.com/download/win"
    echo "   Ubuntu: sudo apt install git"
    echo "   CentOS: sudo yum install git"
    exit 1
fi

# 设置项目目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 项目目录: $PROJECT_DIR"

# 检查是否在正确的目录
if [ ! -f "$PROJECT_DIR/run.py" ]; then
    echo "❌ 错误：不在RedTeamCUA项目目录中"
    exit 1
fi

# 初始化Git仓库（如果不存在）
if [ ! -d "$PROJECT_DIR/.git" ]; then
    echo "🔧 初始化Git仓库..."
    cd "$PROJECT_DIR"
    git init
    echo "✅ Git仓库初始化完成"
else
    echo "📦 Git仓库已存在"
    cd "$PROJECT_DIR"
fi

# 检查虚拟机目录是否被正确忽略
echo "🔍 检查虚拟机目录排除情况..."
if [ -d "vmware_vm_data" ]; then
    if git check-ignore vmware_vm_data > /dev/null 2>&1; then
        echo "✅ 虚拟机目录已被Git忽略"
    else
        echo "⚠️  警告：虚拟机目录未被忽略，添加到.gitignore"
        echo "vmware_vm_data/" >> .gitignore
    fi
fi

# 检查文件大小
echo "📊 检查大文件..."
find . -type f -size +100M | grep -v '.git' | while read file; do
    echo "⚠️  大文件警告: $file ($(du -h "$file" | cut -f1))"
done

# 显示将要上传的文件统计
echo "📈 文件统计："
echo "   Python文件: $(find . -name "*.py" | grep -v __pycache__ | wc -l)"
echo "   配置文件: $(find . -name "*.json" -o -name "*.yml" -o -name "*.yaml" | wc -l)"
echo "   文档文件: $(find . -name "*.md" -o -name "*.txt" | wc -l)"
echo "   总文件数: $(git ls-files --others --exclude-standard 2>/dev/null | wc -l) (未跟踪)"

# 设置Git用户信息（如果未设置）
if [ -z "$(git config user.name)" ]; then
    echo "🔧 设置Git用户信息..."
    read -p "请输入Git用户名: " username
    read -p "请输入Git邮箱: " email
    git config user.name "$username"
    git config user.email "$email"
    echo "✅ Git用户信息设置完成"
fi

# 添加远程仓库
echo "🔗 配置远程仓库..."
if git remote get-url origin > /dev/null 2>&1; then
    echo "📡 远程仓库已存在: $(git remote get-url origin)"
    read -p "是否要更改远程仓库地址？(y/N): " change_remote
    if [[ $change_remote =~ ^[Yy]$ ]]; then
        git remote set-url origin git@github.com:simonsshoot/RedTeamCUA-national.git
        echo "✅ 远程仓库地址已更新"
    fi
else
    git remote add origin git@github.com:simonsshoot/RedTeamCUA-national.git
    echo "✅ 远程仓库已添加"
fi

# 创建主要的README文件
if [ -f "README_GITHUB.md" ]; then
    cp README_GITHUB.md README.md
    echo "✅ GitHub README已创建"
fi

# 添加所有文件到Git
echo "📦 添加文件到Git..."
git add .

# 显示状态
echo "📋 Git状态："
git status --short | head -20
if [ $(git status --short | wc -l) -gt 20 ]; then
    echo "   ... 还有 $(($(git status --short | wc -l) - 20)) 个文件"
fi

# 确认提交
echo
read -p "是否继续提交所有更改？(Y/n): " confirm
if [[ ! $confirm =~ ^[Nn]$ ]]; then
    # 提交更改
    echo "💾 提交更改..."
    commit_message="feat: RedTeamCUA-National项目初始化

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
- API密钥和敏感配置"

    git commit -m "$commit_message"
    echo "✅ 提交完成"

    # 推送到GitHub
    echo "🚀 推送到GitHub..."
    echo "⚠️  首次推送可能需要SSH密钥认证"
    
    if git push -u origin main 2>/dev/null; then
        echo "✅ 推送成功！"
    elif git push -u origin master 2>/dev/null; then
        echo "✅ 推送成功！"
    else
        echo "❌ 推送失败，尝试手动推送："
        echo "   git push -u origin main"
        echo "   或"
        echo "   git push -u origin master"
        echo
        echo "可能的原因："
        echo "1. SSH密钥未配置"
        echo "2. GitHub仓库不存在或无权限"
        echo "3. 网络连接问题"
        exit 1
    fi

    # 成功信息
    echo
    echo "🎉 上传完成！"
    echo "📍 仓库地址: https://github.com/simonsshoot/RedTeamCUA-national"
    echo "📝 建议下一步操作："
    echo "   1. 在GitHub上检查文件是否正确上传"
    echo "   2. 更新仓库描述和标签"
    echo "   3. 创建Release版本"
    echo "   4. 添加贡献者指南"
    
else
    echo "❌ 用户取消上传"
fi

echo
echo "=== 脚本执行完成 ==="
