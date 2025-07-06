# RedTeamCUA 多模型API支持指南

## 🌟 概述

RedTeamCUA现已扩展支持多种国内外LLM API服务，让您可以使用不同的模型进行对抗性测试实验。这不仅提供了更多选择，还能让您比较不同模型在安全任务上的表现。

## 🚀 支持的模型服务

### 🌍 国际模型
| 服务商 | 模型 | 配置格式 | 特点 |
|--------|------|----------|------|
| OpenAI | GPT-4o | `openai \| gpt-4o` | 最强性能 |
| OpenAI | GPT-3.5-turbo | `openai \| gpt-3.5-turbo` | 性价比高 |
| Azure OpenAI | GPT-4o | `azure \| gpt-4o` | 企业级 |
| AWS Bedrock | Claude 3.5 | `aws \| us.anthropic.claude-3-5-sonnet-20241022-v2:0` | 安全性强 |

### 🇨🇳 国内模型
| 服务商 | 模型 | 配置格式 | 特点 |
|--------|------|----------|------|
| 月之暗面 | Kimi 8K | `kimi \| moonshot-v1-8k` | 长上下文，推荐 |
| 月之暗面 | Kimi 32K | `kimi \| moonshot-v1-32k` | 超长上下文 |
| 深度求索 | DeepSeek Chat | `deepseek \| deepseek-chat` | 极高性价比 |
| 深度求索 | DeepSeek Coder | `deepseek \| deepseek-coder` | 代码专用 |
| 智谱AI | GLM-4 | `zhipu \| glm-4` | 中文优化 |
| 智谱AI | GLM-4V | `zhipu \| glm-4v` | 多模态支持 |
| 阿里云 | 通义千问Turbo | `qwen \| qwen-turbo` | 快速响应 |
| 阿里云 | 通义千问Plus | `qwen \| qwen-plus` | 高质量 |
| 百度 | 文心一言4.0 | `baidu \| ernie-4.0-8k` | 国产大模型 |
| 百度 | 文心一言3.5 | `baidu \| ernie-3.5` | 轻量级 |

## 📋 配置步骤

### 1. 获取API密钥

#### Kimi (月之暗面)
1. 访问 https://platform.moonshot.cn/console/api-keys
2. 注册/登录账户
3. 创建API密钥
4. 复制密钥 (格式: sk-...)

#### DeepSeek
1. 访问 https://platform.deepseek.com/api_keys
2. 注册/登录账户
3. 创建API密钥
4. 复制密钥 (格式: sk-...)

#### 智谱AI
1. 访问 https://open.bigmodel.cn/usercenter/apikeys
2. 注册/登录账户
3. 创建API密钥
4. 复制密钥

#### 通义千问 (阿里云)
1. 访问 https://dashscope.console.aliyun.com/
2. 开通DashScope服务
3. 获取API Key
4. 复制密钥 (格式: sk-...)

#### 文心一言 (百度)
1. 访问 https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application
2. 创建应用
3. 获取API Key和Secret Key
4. 记录两个密钥

### 2. 设置环境变量

#### 使用配置向导 (推荐)
```powershell
.\set_multi_model_api.ps1
```

#### 手动设置
```powershell
# Kimi
$env:KIMI_API_KEY = "sk-your-kimi-key"

# DeepSeek  
$env:DEEPSEEK_API_KEY = "sk-your-deepseek-key"

# 智谱AI
$env:ZHIPU_API_KEY = "your-zhipu-key"

# 通义千问
$env:QWEN_API_KEY = "sk-your-qwen-key"

# 文心一言
$env:BAIDU_API_KEY = "your-baidu-api-key"
$env:BAIDU_SECRET_KEY = "your-baidu-secret-key"
```

### 3. 测试连接
```powershell
python test_multi_model_api.py
```

## 🔬 实验示例

### 基础对抗性测试
```powershell
# 使用Kimi进行OwnCloud平台测试
python run.py \
  --model "kimi | moonshot-v1-8k" \
  --headless \
  --path_to_vm ./vmware_vm_data/Ubuntu0/Ubuntu0.vmx \
  --observation_type screenshot \
  --test_all_meta_path ./evaluation_examples/test_all_owncloud.json \
  --domain owncloud \
  --max_steps 5
```

### 模型对比实验
```powershell
# 测试不同模型在相同任务上的表现
python run.py --model "kimi | moonshot-v1-8k" --result_dir ./results/kimi ...
python run.py --model "deepseek | deepseek-chat" --result_dir ./results/deepseek ...
python run.py --model "zhipu | glm-4" --result_dir ./results/zhipu ...
```

### 小规模快速测试
```powershell
# 使用DeepSeek进行快速测试（成本最低）
python run.py \
  --model "deepseek | deepseek-chat" \
  --headless \
  --path_to_vm ./vmware_vm_data/Ubuntu0/Ubuntu0.vmx \
  --observation_type screenshot \
  --test_all_meta_path ./evaluation_examples/test_all_owncloud.json \
  --domain owncloud \
  --max_steps 3
```

## 💰 成本对比

| 模型 | 相对成本 | 推荐场景 |
|------|----------|----------|
| DeepSeek Chat | ⭐ 极低 | 大规模测试、初步验证 |
| Kimi 8K | ⭐⭐ 低 | 日常实验、平衡性能和成本 |
| 通义千问Turbo | ⭐⭐ 低 | 中文任务优化 |
| 智谱GLM-4 | ⭐⭐⭐ 中 | 中文场景、多样化测试 |
| OpenAI GPT-3.5 | ⭐⭐⭐ 中 | 国际基准对比 |
| OpenAI GPT-4o | ⭐⭐⭐⭐⭐ 高 | 最终验证、高质量结果 |

## 🎯 使用建议

### 首次使用
1. **推荐模型**: `kimi | moonshot-v1-8k` 或 `deepseek | deepseek-chat`
2. **小规模测试**: 先运行3-5个任务验证配置
3. **逐步扩展**: 确认无误后运行完整测试集

### 研究场景
- **探索阶段**: 使用DeepSeek进行大量快速测试
- **验证阶段**: 使用Kimi或GPT-4o进行精确验证
- **对比研究**: 同时使用多个模型对比结果差异

### 成本优化
- **预算有限**: 优先使用国内模型
- **高质量需求**: 关键实验使用GPT-4o
- **批量测试**: DeepSeek + 抽样GPT-4o验证

## 🔧 故障排除

### 常见问题

#### API连接失败
```bash
❌ 认证失败: API密钥无效
```
**解决方案**: 检查API密钥是否正确设置，确认没有多余空格

#### 余额不足
```bash
❌ insufficient_quota 或余额不足
```
**解决方案**: 充值账户或切换到其他有余额的模型

#### 网络连接问题
```bash
❌ 连接错误: 无法连接到服务器
```
**解决方案**: 检查网络连接，某些服务可能需要特殊网络配置

### 调试技巧
1. **单独测试**: 使用 `test_multi_model_api.py` 单独测试每个API
2. **查看日志**: 检查 `./logs/` 目录下的详细日志
3. **降级模型**: 如果高级模型失败，尝试基础模型
4. **减少步数**: 设置较小的 `--max_steps` 进行调试

## 📈 性能监控

### 结果对比
不同模型的实验结果会保存在对应目录:
```
results/
├── kimi/
├── deepseek/
├── zhipu/
└── openai/
```

### 指标分析
- **成功率**: 任务完成比例
- **步骤效率**: 平均完成步数
- **安全性**: 对抗性攻击的识别能力
- **成本效益**: 成本与性能的平衡

---

🎉 **现在您可以使用多种模型进行RedTeamCUA实验了！选择最适合您需求的模型开始探索吧！**
