#!/usr/bin/env python3
"""
测试Kimi Agent初始化
"""
import os
import sys

# 设置环境变量
os.environ['KIMI_API_KEY'] = 'sk-Gm1bxgkOYrDgvo4vShhaCNuj8Vg6jC45wSxULr1RuEbtQq5W'

# 添加路径
sys.path.append('.')

try:
    from mm_agents.agent import PromptAgent
    
    print("开始测试Kimi Agent初始化...")
    
    # 创建agent实例
    agent = PromptAgent(
        platform="ubuntu",
        model="kimi | moonshot-v1-8k",  # 使用kimi模型
        max_tokens=1500,
        top_p=0.9,
        temperature=0.5,
        action_space="pyautogui",
        observation_type="screenshot",
        max_trajectory_length=3
    )
    
    print("✅ Kimi Agent 初始化成功!")
    print(f"Provider: {agent.provider}")
    print(f"Model: {agent.model}")
    print(f"Client type: {type(agent.client)}")
    
except Exception as e:
    print(f"❌ 初始化失败: {e}")
    import traceback
    traceback.print_exc()
