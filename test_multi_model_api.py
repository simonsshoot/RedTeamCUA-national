#!/usr/bin/env python3
"""
RedTeamCUA 多模型API连接测试脚本
支持国内外主流LLM API服务
"""

import os
import json
import requests
import sys
from typing import Dict, Any, Optional

def test_openai_api():
    """测试标准OpenAI API"""
    print("🔍 测试标准OpenAI API...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY 环境变量未设置")
        return False
    
    print(f"✅ API密钥: {api_key[:20]}...{api_key[-4:]}")
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ OpenAI API 测试成功! 响应: {message[:50]}...")
            return True
        else:
            print(f"❌ OpenAI API 测试失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ OpenAI API 测试错误: {e}")
        return False

def test_kimi_api():
    """测试Kimi API"""
    print("🔍 测试Kimi (月之暗面) API...")
    
    api_key = os.getenv("KIMI_API_KEY")
    if not api_key:
        print("❌ KIMI_API_KEY 环境变量未设置")
        return False
    
    print(f"✅ API密钥: {api_key[:20]}...{api_key[-4:]}")
    
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "moonshot-v1-8k",
        "messages": [{"role": "user", "content": "Hello"}],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ Kimi API 测试成功! 响应: {message[:50]}...")
            return True
        else:
            print(f"❌ Kimi API 测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Kimi API 测试错误: {e}")
        return False

def test_deepseek_api():
    """测试DeepSeek API"""
    print("🔍 测试DeepSeek API...")
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ DEEPSEEK_API_KEY 环境变量未设置")
        return False
    
    print(f"✅ API密钥: {api_key[:20]}...{api_key[-4:]}")
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 50,
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ DeepSeek API 测试成功! 响应: {message[:50]}...")
            return True
        else:
            print(f"❌ DeepSeek API 测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ DeepSeek API 测试错误: {e}")
        return False

def test_zhipu_api():
    """测试智谱AI API"""
    print("🔍 测试智谱AI (GLM) API...")
    
    api_key = os.getenv("ZHIPU_API_KEY")
    if not api_key:
        print("❌ ZHIPU_API_KEY 环境变量未设置")
        return False
    
    print(f"✅ API密钥: {api_key[:20]}...{api_key[-4:]}")
    
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "glm-4",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 50,
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ 智谱AI API 测试成功! 响应: {message[:50]}...")
            return True
        else:
            print(f"❌ 智谱AI API 测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 智谱AI API 测试错误: {e}")
        return False

def test_qwen_api():
    """测试阿里云通义千问API"""
    print("🔍 测试阿里云通义千问 API...")
    
    api_key = os.getenv("QWEN_API_KEY")
    if not api_key:
        print("❌ QWEN_API_KEY 环境变量未设置")
        return False
    
    print(f"✅ API密钥: {api_key[:20]}...{api_key[-4:]}")
    
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "qwen-turbo",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 50,
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ 通义千问 API 测试成功! 响应: {message[:50]}...")
            return True
        else:
            print(f"❌ 通义千问 API 测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 通义千问 API 测试错误: {e}")
        return False

def test_baidu_api():
    """测试百度文心一言API"""
    print("🔍 测试百度文心一言 API...")
    
    api_key = os.getenv("BAIDU_API_KEY")
    secret_key = os.getenv("BAIDU_SECRET_KEY")
    
    if not api_key or not secret_key:
        print("❌ BAIDU_API_KEY 和 BAIDU_SECRET_KEY 环境变量未设置")
        return False
    
    print(f"✅ API Key: {api_key[:20]}...")
    print(f"✅ Secret Key: {secret_key[:20]}...")
    
    try:
        # 获取access token
        token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
        token_response = requests.post(token_url, timeout=30)
        access_token = token_response.json().get("access_token")
        
        if not access_token:
            print(f"❌ 获取百度access token失败: {token_response.text}")
            return False
        
        print("✅ 成功获取access token")
        
        # 调用文心一言API
        api_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-8k?access_token={access_token}"
        
        data = {
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.3,
            "max_output_tokens": 50
        }
        
        response = requests.post(api_url, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                message = result["result"]
                print(f"✅ 文心一言 API 测试成功! 响应: {message[:50]}...")
                return True
            else:
                print(f"❌ 文心一言 API 响应异常: {result}")
                return False
        else:
            print(f"❌ 文心一言 API 测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 文心一言 API 测试错误: {e}")
        return False

def show_usage_examples():
    """显示使用示例"""
    print(f"\n{'='*60}")
    print("🚀 使用示例 - 如何在RedTeamCUA中使用这些模型:")
    print(f"{'='*60}")
    
    examples = [
        ("OpenAI GPT-4o", "openai | gpt-4o"),
        ("OpenAI GPT-3.5", "openai | gpt-3.5-turbo"),
        ("Kimi 8k", "kimi | moonshot-v1-8k"),
        ("Kimi 32k", "kimi | moonshot-v1-32k"),
        ("DeepSeek Chat", "deepseek | deepseek-chat"),
        ("DeepSeek Coder", "deepseek | deepseek-coder"),
        ("智谱GLM-4", "zhipu | glm-4"),
        ("智谱GLM-4V", "zhipu | glm-4v"),
        ("通义千问Turbo", "qwen | qwen-turbo"),
        ("通义千问Plus", "qwen | qwen-plus"),
        ("文心一言4.0", "baidu | ernie-4.0-8k"),
        ("文心一言3.5", "baidu | ernie-3.5"),
    ]
    
    for name, model_param in examples:
        print(f"📌 {name}:")
        print(f"   python run.py --model \"{model_param}\" --headless \\")
        print(f"     --path_to_vm ./vmware_vm_data/Ubuntu0/Ubuntu0.vmx \\")
        print(f"     --observation_type screenshot \\")
        print(f"     --test_all_meta_path ./evaluation_examples/test_all_owncloud.json \\")
        print(f"     --domain owncloud --max_steps 5")
        print()

def show_env_setup_guide():
    """显示环境变量设置指南"""
    print(f"\n{'='*60}")
    print("🔧 环境变量设置指南:")
    print(f"{'='*60}")
    
    env_vars = [
        ("OpenAI", "OPENAI_API_KEY", "从 https://platform.openai.com/api-keys 获取"),
        ("Kimi", "KIMI_API_KEY", "从 https://platform.moonshot.cn/console/api-keys 获取"),
        ("DeepSeek", "DEEPSEEK_API_KEY", "从 https://platform.deepseek.com/api_keys 获取"),
        ("智谱AI", "ZHIPU_API_KEY", "从 https://open.bigmodel.cn/usercenter/apikeys 获取"),
        ("通义千问", "QWEN_API_KEY", "从阿里云DashScope控制台获取"),
        ("文心一言", "BAIDU_API_KEY + BAIDU_SECRET_KEY", "从百度云千帆大模型平台获取"),
    ]
    
    print("在PowerShell中设置环境变量:")
    for service, var_name, source in env_vars:
        if "+" in var_name:
            print(f"\n📌 {service}:")
            print(f"   $env:BAIDU_API_KEY = \"your-api-key\"")
            print(f"   $env:BAIDU_SECRET_KEY = \"your-secret-key\"")
        else:
            print(f"\n📌 {service}:")
            print(f"   $env:{var_name} = \"your-api-key\"")
        print(f"   # {source}")

def main():
    """主函数"""
    print("=== RedTeamCUA 多模型API连接测试 ===\n")
    
    # 检测并测试所有可用的API
    test_results = {}
    
    tests = [
        ("OpenAI", test_openai_api),
        ("Kimi", test_kimi_api),
        ("DeepSeek", test_deepseek_api),
        ("智谱AI", test_zhipu_api),
        ("通义千问", test_qwen_api),
        ("文心一言", test_baidu_api),
    ]
    
    for name, test_func in tests:
        print(f"\n{'-'*50}")
        try:
            result = test_func()
            test_results[name] = result
        except Exception as e:
            print(f"❌ {name} 测试出现异常: {e}")
            test_results[name] = False
    
    # 显示测试结果汇总
    print(f"\n{'='*60}")
    print("📊 测试结果汇总:")
    print(f"{'='*60}")
    
    successful_apis = []
    failed_apis = []
    
    for name, result in test_results.items():
        if result:
            print(f"✅ {name}: 连接成功")
            successful_apis.append(name)
        else:
            print(f"❌ {name}: 连接失败")
            failed_apis.append(name)
    
    print(f"\n📈 成功: {len(successful_apis)}/{len(test_results)} 个API服务")
    
    if successful_apis:
        print(f"✅ 可用服务: {', '.join(successful_apis)}")
        show_usage_examples()
    
    if failed_apis:
        print(f"❌ 失败服务: {', '.join(failed_apis)}")
        show_env_setup_guide()
    
    print(f"\n{'='*60}")
    if successful_apis:
        print("🎉 检测到可用的API服务！现在可以运行RedTeamCUA实验了！")
        print("📖 使用说明请参考上方的示例命令")
    else:
        print("⚠️ 未检测到任何可用的API服务")
        print("📖 请按照上方指南设置API密钥")

if __name__ == "__main__":
    main()
