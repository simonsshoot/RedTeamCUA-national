# RedTeamCUA实验运行指南

## 🔧 第三步：实验设置和运行

### 1. 设置API密钥环境变量

在运行实验之前，您需要设置相应的API密钥。根据您要使用的模型类型，请设置以下环境变量：

#### 对于Azure OpenAI (推荐用于演示)
```powershell
# 设置Azure OpenAI API密钥
$env:AZURE_API_KEY = "your-azure-api-key-here"
$env:AZURE_API_VERSION = "2024-02-15-preview"
$env:AZURE_ENDPOINT = "https://your-resource.openai.azure.com/"

# 用于第二次调用(OSWorld动作翻译)
$env:AZURE_API_VERSION_FOR_SECOND_CALL = "2024-02-15-preview"
$env:AZURE_ENDPOINT_FOR_SECOND_CALL = "https://your-resource.openai.azure.com/"
```

#### 对于AWS Claude模型
```powershell
$env:AWS_REGION = "us-east-1"
$env:AWS_ACCESS_KEY = "your-aws-access-key"
$env:AWS_SECRET_KEY = "your-aws-secret-key"
```

#### 对于RocketChat NPC仿真 (可选)
```powershell
$env:AZURE_OPENAI_API_KEY = "your-azure-api-key"
$env:AZURE_MODEL_FOR_ROCKETCHAT_NPC = "resource_name/deployment_name/version"
```

### 2. 本地Web服务环境变量(已设置)
```powershell
$env:REDDIT = "localhost:9999"
$env:OWNCLOUD = "localhost:8092"
$env:ROCKETCHAT = "localhost:3000"
$env:SERVER_HOSTNAME = "localhost"
```

### 3. 运行实验示例

#### OwnCloud平台测试
```powershell
python run.py \
  --headless \
  --path_to_vm ./vmware_vm_data/RedTeamCUA_Ubuntu/RedTeamCUA_Ubuntu.vmx \
  --observation_type screenshot \
  --model "azure | gpt-4o" \
  --result_dir ./results \
  --test_all_meta_path ./evaluation_examples/test_all_owncloud.json \
  --domain owncloud \
  --max_steps 30
```

#### RocketChat平台测试
```powershell
python run.py \
  --headless \
  --path_to_vm ./vmware_vm_data/RedTeamCUA_Ubuntu/RedTeamCUA_Ubuntu.vmx \
  --observation_type screenshot \
  --model "azure | gpt-4o" \
  --result_dir ./results \
  --test_all_meta_path ./evaluation_examples/test_all_rocketchat.json \
  --domain rocketchat \
  --max_steps 30
```

#### 支持的模型类型

##### 国际模型
- `"azure | gpt-4o"` - Azure OpenAI GPT-4o
- `"azure | computer-use-preview"` - Azure Computer Use Preview
- `"openai | gpt-4o"` - 标准OpenAI GPT-4o
- `"openai | gpt-3.5-turbo"` - 标准OpenAI GPT-3.5
- `"aws | us.anthropic.claude-3-5-sonnet-20241022-v2:0"` - AWS Claude 3.5 Sonnet
- `"aws | us.anthropic.claude-3-5-sonnet-20241022-v2:0 | cua"` - AWS Claude 3.5 Sonnet CUA版本

##### 国内模型 (新增支持)
- `"kimi | moonshot-v1-8k"` - Kimi 8K模型 (推荐)
- `"kimi | moonshot-v1-32k"` - Kimi 32K模型
- `"deepseek | deepseek-chat"` - DeepSeek对话模型 (性价比高)
- `"deepseek | deepseek-coder"` - DeepSeek代码模型
- `"zhipu | glm-4"` - 智谱AI GLM-4
- `"zhipu | glm-4v"` - 智谱AI GLM-4V (多模态)
- `"qwen | qwen-turbo"` - 通义千问Turbo
- `"qwen | qwen-plus"` - 通义千问Plus
- `"baidu | ernie-4.0-8k"` - 文心一言4.0
- `"baidu | ernie-3.5"` - 文心一言3.5

##### 使用建议
- **首次测试**: 推荐使用 `kimi | moonshot-v1-8k` 或 `deepseek | deepseek-chat`
- **成本考虑**: 国内模型通常比OpenAI便宜，且访问更稳定
- **性能对比**: 可以用相同任务测试不同模型的效果

### 4. 实验参数说明

- `--headless`: 无头模式运行(推荐用于服务器)
- `--path_to_vm`: VMware虚拟机配置文件路径
- `--observation_type`: 观察类型 (screenshot, a11y_tree, screenshot_a11y_tree, som)
- `--model`: 要使用的模型
- `--result_dir`: 结果输出目录
- `--test_all_meta_path`: 测试配置文件路径
- `--domain`: 测试平台 (owncloud, rocketchat, reddit, 或 all)
- `--max_steps`: 最大步数限制

### 5. 结果查看

实验结果将保存在 `./results` 目录下，按以下结构组织：
```
results/
  └── pyautogui/
      └── screenshot/
          └── azure_gpt-4o/
              └── owncloud/
                  └── task_id/
                      ├── result.txt
                      ├── adversary_result.txt
                      └── screenshots/
```

### 6. 故障排除

#### 常见问题:
1. **VM未启动**: 确保VMware Workstation正在运行
2. **Web服务连接失败**: 检查Docker容器状态
3. **API密钥错误**: 验证环境变量设置正确
4. **超时问题**: 增加 `--max_steps` 参数值

#### 检查服务状态:
```powershell
# 检查Docker容器
docker ps

# 检查VM状态
vmrun -T ws list

# 检查Web服务
curl http://localhost:8092  # OwnCloud
curl http://localhost:3000  # RocketChat
```

### 7. 当前状态总结

✅ **已完成**:
- VM镜像下载和配置
- Docker Web服务运行 (OwnCloud: 8092, RocketChat: 3000)
- 配置文件生成 (864个对抗性测试案例)

⚠️ **需要完成**:
- 设置API密钥环境变量
- 运行具体的实验测试

---

**下一步**: 设置您的API密钥后，选择一个平台开始运行实验！
