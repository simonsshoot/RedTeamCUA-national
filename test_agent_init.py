#!/usr/bin/env python3
"""
测试PromptAgent初始化
"""

import os
import sys
sys.path.append('.')

# 设置环境变量
os.environ["KIMI_API_KEY"] = "sk-Gm1bxgkOYrDgvo4vShhaCNuj8Vg6jC45wSxULr1RuEbtQq5W"

try:
    from mm_agents.agent import PromptAgent
    
    # 尝试创建agent
    agent = PromptAgent(
        platform="ubuntu",
        model="kimi|moonshot-v1-8k",
        max_tokens=1500,
        top_p=0.9,
        temperature=0.5,
        action_space="pyautogui",
        observation_type="screenshot",
        max_trajectory_length=3
    )
    
    print("✅ PromptAgent initialized successfully with Kimi")
    print(f"Model: {agent.model}")
    print(f"Provider: {agent.provider}")
    
except Exception as e:
    print(f"❌ Error creating PromptAgent: {e}")
    import traceback
    traceback.print_exc()
