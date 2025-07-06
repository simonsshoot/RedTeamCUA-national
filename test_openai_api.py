#!/usr/bin/env python3
"""
OpenAI API 连接测试脚本
支持标准 OpenAI API 和 Azure OpenAI
"""

import os
import json
import requests
import sys

def test_standard_openai_connection():
    """测试标准OpenAI API连接"""
    print("🔍 测试标准 OpenAI API 连接...")
    
    # 检查环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY 环境变量未设置")
        return False
    
    print(f"✅ API密钥: {api_key[:20]}...{api_key[-4:]}")
    print(f"✅ 终结点: https://api.openai.com/v1")
    
    # 测试模型列表API
    url = "https://api.openai.com/v1/models"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            models = response.json()
            model_list = models.get('data', [])
            print(f"✅ 连接成功！找到 {len(model_list)} 个可用模型")
            
            # 显示一些主要的GPT模型
            gpt_models = [m for m in model_list if 'gpt' in m.get('id', '').lower()]
            if gpt_models:
                print("\n📋 可用的GPT模型 (部分):")
                for model in gpt_models[:10]:  # 只显示前10个
                    model_id = model.get('id', 'Unknown')
                    print(f"  - {model_id}")
                if len(gpt_models) > 10:
                    print(f"  ... 以及其他 {len(gpt_models) - 10} 个GPT模型")
                    
            return True
                
        elif response.status_code == 401:
            print("❌ 认证失败: API密钥无效")
            return False
        elif response.status_code == 429:
            print("❌ 请求过于频繁，请稍后再试")
            return False
        else:
            print(f"❌ 连接失败: HTTP {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 连接超时")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误: 无法连接到服务器")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def test_azure_openai_connection():
    """测试Azure OpenAI连接"""
    print("🔍 测试 Azure OpenAI 连接...")
    
    # 检查环境变量
    api_key = os.getenv("AZURE_API_KEY")
    endpoint = os.getenv("AZURE_ENDPOINT")
    api_version = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")
    
    if not api_key:
        print("❌ AZURE_API_KEY 环境变量未设置")
        return False
        
    if not endpoint:
        print("❌ AZURE_ENDPOINT 环境变量未设置") 
        return False
    
    print(f"✅ API密钥: {api_key[:10]}...{api_key[-4:]}")
    print(f"✅ 终结点: {endpoint}")
    print(f"✅ API版本: {api_version}")
    
    # 构建请求URL (列出部署)
    url = f"{endpoint.rstrip('/')}/openai/deployments?api-version={api_version}"
    
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            deployments = response.json()
            print(f"✅ 连接成功！找到 {len(deployments.get('data', []))} 个部署")
            
            if deployments.get('data'):
                print("\n📋 可用的模型部署:")
                for deployment in deployments['data']:
                    model = deployment.get('model', 'Unknown')
                    name = deployment.get('id', 'Unknown')
                    status = deployment.get('status', 'Unknown')
                    print(f"  - {name} ({model}) - 状态: {status}")
                    
                return True
            else:
                print("⚠️ 连接成功但没有找到部署，请确保已部署模型")
                return False
                
        elif response.status_code == 401:
            print("❌ 认证失败: API密钥无效")
            return False
        elif response.status_code == 404:
            print("❌ 终结点无效或资源不存在")
            return False
        else:
            print(f"❌ 连接失败: HTTP {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 连接超时")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误: 无法连接到服务器")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def test_standard_chat_completion():
    """测试标准OpenAI聊天完成API"""
    print("\n🤖 测试标准OpenAI聊天完成API...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY 环境变量未设置")
        return False
    
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",  # 使用较便宜的模型进行测试
        "messages": [
            {"role": "user", "content": "Hello! Please respond with 'API test successful' if you can see this message."}
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ 聊天API测试成功!")
            print(f"📝 模型响应: {message}")
            return True
        else:
            print(f"❌ 聊天API测试失败: HTTP {response.status_code}")
            error_info = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"错误信息: {error_info}")
            return False
            
    except Exception as e:
        print(f"❌ 聊天API测试错误: {e}")
        return False

def test_chat_completion():
    """测试聊天完成API"""
    print("\n🤖 测试聊天完成API...")
    
    api_key = os.getenv("AZURE_API_KEY")
    endpoint = os.getenv("AZURE_ENDPOINT")
    api_version = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")
    
    # 需要用户提供部署名称
    deployment_name = input("请输入您的GPT部署名称 (例如: gpt-4o-deployment): ").strip()
    
    if not deployment_name:
        print("⚠️ 跳过聊天测试: 未提供部署名称")
        return False
    
    url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
    
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {"role": "user", "content": "Hello! Please respond with 'API test successful' if you can see this message."}
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ 聊天API测试成功!")
            print(f"📝 模型响应: {message}")
            return True
        else:
            print(f"❌ 聊天API测试失败: HTTP {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 聊天API测试错误: {e}")
        return False

def main():
    """主函数"""
    print("=== OpenAI API 连接测试 ===\n")
    
    # 检查是否为标准OpenAI API还是Azure OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    azure_key = os.getenv("AZURE_API_KEY")
    azure_endpoint = os.getenv("AZURE_ENDPOINT")
    
    # 优先测试标准OpenAI API
    if openai_key:
        print("检测到标准OpenAI API配置，开始测试...")
        connection_ok = test_standard_openai_connection()
        
        if connection_ok:
            # 测试聊天API
            chat_ok = test_standard_chat_completion()
            
            if chat_ok:
                print(f"\n{'='*50}")
                print("🎉 所有测试通过！")
                print("✅ 标准OpenAI API 配置正确")
                print("🚀 现在可以运行 RedTeamCUA 实验了!")
                
                print(f"\n📋 下一步运行实验:")
                print("python run.py --headless --path_to_vm ./vmware_vm_data/Ubuntu0/Ubuntu0.vmx --observation_type screenshot --model \"gpt-4o\" --result_dir ./results --test_all_meta_path ./evaluation_examples/test_all_owncloud.json --domain owncloud --max_steps 5")
                return
            else:
                print(f"\n{'='*50}")
                print("⚠️ 基本连接成功，但聊天API测试失败")
                print("请检查API密钥的权限和余额")
        else:
            print(f"\n{'='*50}")
            print("❌ 标准OpenAI API连接测试失败")
            print("请检查OPENAI_API_KEY环境变量")
    
    # 如果标准API不可用，尝试Azure OpenAI
    elif azure_key and azure_endpoint:
        print("检测到Azure OpenAI配置，开始测试...")
        connection_ok = test_azure_openai_connection()
        
        if connection_ok:
            # 测试聊天API
            chat_ok = test_chat_completion()
            
            if chat_ok:
                print(f"\n{'='*50}")
                print("🎉 所有测试通过！")
                print("✅ Azure OpenAI 配置正确")
                print("🚀 现在可以运行 RedTeamCUA 实验了!")
                
                print(f"\n📋 下一步运行实验:")
                print("python run.py --headless --path_to_vm ./vmware_vm_data/Ubuntu0/Ubuntu0.vmx --observation_type screenshot --model \"azure | gpt-4o\" --result_dir ./results --test_all_meta_path ./evaluation_examples/test_all_owncloud.json --domain owncloud --max_steps 5")
            else:
                print(f"\n{'='*50}")
                print("⚠️ 基本连接成功，但聊天API测试失败")
                print("请检查部署名称是否正确")
        else:
            print(f"\n{'='*50}")
            print("❌ Azure OpenAI连接测试失败")
            print("请检查API密钥和终结点配置")
            print("参考文档: AZURE_OPENAI_SETUP.md")
    
    else:
        print("❌ 未检测到有效的API配置")
        print("请设置以下环境变量之一:")
        print("  标准OpenAI API: OPENAI_API_KEY")
        print("  Azure OpenAI: AZURE_API_KEY + AZURE_ENDPOINT")

if __name__ == "__main__":
    main()
