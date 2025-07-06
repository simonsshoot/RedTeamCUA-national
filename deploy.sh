#!/bin/bash
# RedTeamCUA 一键部署脚本

echo "RedTeamCUA 环境自动化部署"
echo "=========================="

# 检查系统环境
check_system() {
    echo "检查系统环境..."
    
    # 检查Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker未安装，请先安装Docker"
        exit 1
    fi
    
    # 检查VMware (Windows)
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        if ! command -v vmrun &> /dev/null; then
            echo "⚠️  VMware未检测到，某些功能可能不可用"
        fi
    fi
    
    echo "✅ 系统环境检查完成"
}

# 配置网络
setup_network() {
    echo "配置网络环境..."
    
    # 检测IP地址
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        HOST_IP=$(ip route get 1 | awk '{print $NF;exit}')
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        HOST_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
    else
        # Windows
        HOST_IP=$(ipconfig | grep "IPv4" | head -1 | awk '{print $NF}')
    fi
    
    echo "检测到主机IP: $HOST_IP"
    
    # 更新Docker Compose配置
    sed -i "s/192.168.229.1/$HOST_IP/g" docker-compose.yml
    
    echo "✅ 网络配置完成"
}

# 启动服务
start_services() {
    echo "启动RedTeamCUA服务..."
    
    # 拉取镜像
    docker-compose pull
    
    # 启动服务
    docker-compose up -d
    
    # 等待服务启动
    echo "等待服务启动..."
    sleep 30
    
    # 验证服务
    echo "验证服务状态..."
    curl -s http://localhost:8092 > /dev/null && echo "✅ OwnCloud服务正常" || echo "❌ OwnCloud服务异常"
    curl -s http://localhost:3000 > /dev/null && echo "✅ RocketChat服务正常" || echo "❌ RocketChat服务异常"
}

# 配置API密钥
setup_api_keys() {
    echo "配置API密钥..."
    
    read -p "请输入OpenAI API Key (可选): " OPENAI_KEY
    read -p "请输入Kimi API Key (可选): " KIMI_KEY
    
    # 设置环境变量
    if [[ -n "$OPENAI_KEY" ]]; then
        export OPENAI_API_KEY="$OPENAI_KEY"
        echo "✅ OpenAI API Key已设置"
    fi
    
    if [[ -n "$KIMI_KEY" ]]; then
        export KIMI_API_KEY="$KIMI_KEY"
        echo "✅ Kimi API Key已设置"
    fi
}

# 运行测试
run_test() {
    echo "运行测试实验..."
    
    if [[ -n "$KIMI_API_KEY" ]]; then
        python run.py --test_all_meta_path evaluation_examples/test_all_owncloud.json --model "kimi|moonshot-v1-8k" --provider_name vmware
    elif [[ -n "$OPENAI_API_KEY" ]]; then
        python run.py --test_all_meta_path evaluation_examples/test_all_owncloud.json --model "openai|gpt-4o" --provider_name vmware
    else
        echo "⚠️  未配置API密钥，跳过测试运行"
    fi
}

# 主函数
main() {
    check_system
    setup_network
    start_services
    setup_api_keys
    
    echo ""
    echo "🎉 RedTeamCUA环境部署完成！"
    echo ""
    echo "服务访问地址："
    echo "  - OwnCloud: http://localhost:8092"
    echo "  - RocketChat: http://localhost:3000"
    echo "  - 监控面板: http://localhost:3001"
    echo ""
    echo "账户信息："
    echo "  - 用户名: theagentcompany"
    echo "  - 密码: theagentcompany"
    echo ""
    
    read -p "是否运行测试实验？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_test
    fi
}

# 执行主函数
main "$@"
