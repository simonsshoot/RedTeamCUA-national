#!/usr/bin/env python3
"""
测试Kimi API初始化
"""

import os
from openai import OpenAI

# 检查环境变量
kimi_api_key = os.getenv("KIMI_API_KEY")
print(f"KIMI_API_KEY: {kimi_api_key[:20]}..." if kimi_api_key else "Not set")

if not kimi_api_key:
    print("❌ KIMI_API_KEY environment variable is not set")
    exit(1)

try:
    # 尝试初始化Kimi客户端
    client = OpenAI(
        api_key=kimi_api_key,
        base_url="https://api.moonshot.cn/v1"
    )
    print("✅ Kimi OpenAI client initialized successfully")
    
    # 测试简单调用
    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    print(f"✅ Kimi API call successful: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
