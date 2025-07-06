# 🎉 RedTeamCUA 多模型API扩展完成

## ✨ 新增功能

### 支持的模型服务
RedTeamCUA现已支持以下模型API：

#### 🌍 国际模型
- **OpenAI**: GPT-4o, GPT-3.5-turbo
- **Azure OpenAI**: GPT-4o, Computer Use Preview
- **AWS Bedrock**: Claude 3.5 Sonnet

#### 🇨🇳 国内模型
- **Kimi (月之暗面)**: moonshot-v1-8k, moonshot-v1-32k
- **DeepSeek (深度求索)**: deepseek-chat, deepseek-coder
- **智谱AI**: GLM-4, GLM-4V
- **通义千问 (阿里云)**: qwen-turbo, qwen-plus
- **文心一言 (百度)**: ernie-4.0-8k, ernie-3.5

## 🔧 新增工具

### 1. 多模型API测试工具
```bash
python test_multi_model_api.py
```
- 自动检测和测试所有配置的API
- 显示连接状态和可用模型
- 提供详细的错误诊断

### 2. API配置向导
```bash
.\set_multi_model_api.ps1
```
- 交互式API密钥配置
- 支持单个或批量配置
- 包含获取密钥的指导链接

### 3. 详细使用指南
- `MULTI_MODEL_GUIDE.md` - 完整的多模型使用指南
- 包含成本对比、使用建议、故障排除

## 🚀 快速开始

### 1. 配置API密钥
```powershell
# 使用配置向导
.\set_multi_model_api.ps1

# 或手动设置（以Kimi为例）
$env:KIMI_API_KEY = "your-api-key"
```

### 2. 测试连接
```powershell
python test_multi_model_api.py
```

### 3. 运行实验
```powershell
# 使用Kimi模型
python run.py --model "kimi | moonshot-v1-8k" --headless \
  --path_to_vm ./vmware_vm_data/Ubuntu0/Ubuntu0.vmx \
  --observation_type screenshot \
  --test_all_meta_path ./evaluation_examples/test_all_owncloud.json \
  --domain owncloud --max_steps 5

# 使用DeepSeek模型（性价比最高）
python run.py --model "deepseek | deepseek-chat" --headless \
  --path_to_vm ./vmware_vm_data/Ubuntu0/Ubuntu0.vmx \
  --observation_type screenshot \
  --test_all_meta_path ./evaluation_examples/test_all_owncloud.json \
  --domain owncloud --max_steps 5
```

## 💡 优势特性

### 🔄 统一接口
所有模型使用相同的 `provider | model` 格式，便于切换和对比

### 💰 成本优化
国内模型通常比OpenAI便宜很多，特别适合大规模实验

### 🌐 访问稳定
国内模型无需特殊网络配置，访问更稳定

### 📊 对比研究
可以轻松在不同模型间进行对比实验

## 📋 推荐使用顺序

1. **首次测试**: `kimi | moonshot-v1-8k` (平衡性能和成本)
2. **大规模实验**: `deepseek | deepseek-chat` (极高性价比)
3. **精确验证**: `openai | gpt-4o` (最高质量，需充值)
4. **中文优化**: `zhipu | glm-4` (中文任务表现好)

## 🎯 下一步

现在您可以：
1. 选择合适的模型API进行实验
2. 对比不同模型在安全任务上的表现
3. 根据预算和需求选择最佳模型
4. 进行大规模的对抗性安全测试

---

🎊 **恭喜！您的RedTeamCUA环境现在支持多种模型API，可以进行更加丰富和经济的实验了！**
