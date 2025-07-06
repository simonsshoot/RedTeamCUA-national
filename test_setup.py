#!/usr/bin/env python3
"""
RedTeamCUA 测试脚本 - 验证系统配置
此脚本验证所有组件是否正确配置，无需API密钥
"""

import os
import json
import subprocess
import sys
import time
import requests

def check_prerequisites():
    """检查先决条件"""
    print("🔍 检查系统先决条件...")
    
    # 检查VMware
    try:
        result = subprocess.run(["vmrun", "-T", "ws", "list"], 
                              capture_output=True, text=True, check=True)
        print("✅ VMware Workstation: 已安装")
    except:
        print("❌ VMware Workstation: 未安装或不可用")
        return False
    
    # 检查Docker
    try:
        result = subprocess.run(["docker", "ps"], 
                              capture_output=True, text=True, check=True)
        print("✅ Docker: 运行中")
    except:
        print("❌ Docker: 未运行")
        return False
    
    # 检查VM文件
    vm_path = "./vmware_vm_data/Ubuntu0/Ubuntu0.vmx"
    if os.path.exists(vm_path):
        print("✅ VM配置文件: 存在")
    else:
        print("❌ VM配置文件: 不存在")
        return False
    
    # 检查配置文件
    config_files = [
        "./evaluation_examples/test_all_owncloud.json",
        "./evaluation_examples/test_all_rocketchat.json"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ 配置文件: {os.path.basename(config_file)}")
        else:
            print(f"❌ 配置文件: {os.path.basename(config_file)} 不存在")
            return False
    
    return True

def check_web_services():
    """检查Web服务状态"""
    print("\n🌐 检查Web服务...")
    
    services = {
        "OwnCloud": "http://localhost:8092",
        "RocketChat": "http://localhost:3000"
    }
    
    all_good = True
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: 运行中 ({url})")
            else:
                print(f"⚠️ {name}: 响应异常 - 状态码 {response.status_code}")
                all_good = False
        except requests.exceptions.RequestException as e:
            print(f"❌ {name}: 无法连接 ({url})")
            all_good = False
    
    return all_good

def check_environment_variables():
    """检查环境变量"""
    print("\n🔧 检查环境变量...")
    
    web_env_vars = {
        "OWNCLOUD": "localhost:8092",
        "ROCKETCHAT": "localhost:3000", 
        "SERVER_HOSTNAME": "localhost"
    }
    
    for var, expected in web_env_vars.items():
        actual = os.getenv(var)
        if actual == expected:
            print(f"✅ {var}: {actual}")
        else:
            print(f"⚠️ {var}: {actual} (期望: {expected})")
    
    # 检查API密钥（可选）
    api_keys = ["AZURE_API_KEY", "AWS_ACCESS_KEY"]
    has_api_key = False
    
    for key in api_keys:
        if os.getenv(key):
            print(f"✅ {key}: 已设置")
            has_api_key = True
        else:
            print(f"⚠️ {key}: 未设置")
    
    if not has_api_key:
        print("ℹ️ 没有设置API密钥 - 无法运行完整实验，但系统配置检查可以继续")
    
    return True

def load_sample_config():
    """加载示例配置"""
    print("\n📋 检查配置文件结构...")
    
    try:
        with open("./evaluation_examples/test_all_owncloud.json", "r", encoding="utf-8") as f:
            owncloud_config = json.load(f)
        
        print(f"✅ OwnCloud配置: {len(owncloud_config['owncloud'])} 个测试任务")
        
        # 显示第一个任务的基本信息
        if owncloud_config['owncloud']:
            first_task_id = owncloud_config['owncloud'][0]
            task_file = f"./evaluation_examples/examples/owncloud/{first_task_id}.json"
            if os.path.exists(task_file):
                with open(task_file, "r", encoding="utf-8") as f:
                    task_config = json.load(f)
                print(f"✅ 示例任务配置: {task_config['instruction'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置文件解析错误: {e}")
        return False

def demonstrate_command_structure():
    """演示命令结构"""
    print("\n🎯 实验运行命令示例:")
    
    commands = [
        {
            "description": "OwnCloud平台测试",
            "command": [
                "python", "run.py",
                "--headless",
                "--path_to_vm", "./vmware_vm_data/Ubuntu0/Ubuntu0.vmx",
                "--observation_type", "screenshot", 
                "--model", "azure | gpt-4o",
                "--result_dir", "./results",
                "--test_all_meta_path", "./evaluation_examples/test_all_owncloud.json",
                "--domain", "owncloud",
                "--max_steps", "10"
            ]
        },
        {
            "description": "RocketChat平台测试",
            "command": [
                "python", "run.py",
                "--headless",
                "--path_to_vm", "./vmware_vm_data/Ubuntu0/Ubuntu0.vmx", 
                "--observation_type", "screenshot",
                "--model", "azure | gpt-4o",
                "--result_dir", "./results",
                "--test_all_meta_path", "./evaluation_examples/test_all_rocketchat.json",
                "--domain", "rocketchat",
                "--max_steps", "10"
            ]
        }
    ]
    
    for cmd_info in commands:
        print(f"\n📌 {cmd_info['description']}:")
        print(" ".join(cmd_info['command']))

def main():
    """主函数"""
    print("=== RedTeamCUA 系统配置检查 ===\n")
    
    # 检查所有先决条件
    checks = [
        ("先决条件", check_prerequisites),
        ("Web服务", check_web_services), 
        ("环境变量", check_environment_variables),
        ("配置文件", load_sample_config)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        if not check_func():
            all_passed = False
    
    # 显示命令示例
    demonstrate_command_structure()
    
    # 总结
    print(f"\n{'='*50}")
    if all_passed:
        print("🎉 系统配置检查完成！")
        print("✅ 所有基础组件已正确配置")
        print("📋 下一步: 设置API密钥并运行实验")
    else:
        print("⚠️ 发现一些问题，请检查上述输出")
    
    print("\n📖 详细运行指南请查看: EXPERIMENT_GUIDE.md")
    
    return all_passed

if __name__ == "__main__":
    main()
