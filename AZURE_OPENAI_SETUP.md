# Azure OpenAI 配置指南

## 🔑 如何获取 Azure OpenAI API 密钥

### 1. 创建 Azure OpenAI 资源
1. 登录 [Azure Portal](https://portal.azure.com)
2. 搜索并选择 "Azure OpenAI"
3. 点击 "创建" 按钮
4. 填写资源信息:
   - **订阅**: 选择您的Azure订阅
   - **资源组**: 创建新的或选择现有的
   - **区域**: 建议选择 East US 或 West Europe
   - **名称**: 为您的资源命名 (例如: my-openai-resource)
   - **定价层**: 选择 Standard S0

### 2. 部署模型
1. 资源创建完成后，进入资源页面
2. 点击左侧菜单中的 "模型部署" 或 "Deployments"
3. 点击 "创建新部署"
4. 选择模型:
   - **模型**: gpt-4o (推荐) 或 gpt-4
   - **部署名称**: 例如 "gpt-4o-deployment"
   - **版本**: 选择最新版本
5. 点击 "创建"

### 3. 获取配置信息
在您的 Azure OpenAI 资源页面:

#### API 密钥:
1. 点击左侧 "密钥和终结点" 或 "Keys and Endpoint"
2. 复制 "密钥 1" 或 "密钥 2"

#### 终结点:
- 在同一页面复制 "终结点" URL
- 格式类似: `https://your-resource-name.openai.azure.com/`

#### API 版本:
- 使用: `2024-02-15-preview` (当前推荐版本)

### 4. 配置示例
```powershell
# 在 set_openai_api.ps1 中替换这些值:
$env:AZURE_API_KEY = "1234567890abcdef1234567890abcdef"  # 您的API密钥
$env:AZURE_ENDPOINT = "https://my-openai-resource.openai.azure.com/"  # 您的终结点
$env:AZURE_API_VERSION = "2024-02-15-preview"  # API版本
```

### 5. 部署名称
- 在模型配置中，您还需要知道部署名称
- 这是您在步骤2中创建的部署名称
- 例如: "gpt-4o-deployment"

## 💰 费用预估
- GPT-4o: 约 $15/1M input tokens, $60/1M output tokens
- 一个典型的实验任务大约消耗 1000-5000 tokens
- 建议设置支出限制以控制成本

## 🔒 安全建议
1. 不要在代码中硬编码API密钥
2. 使用环境变量存储敏感信息
3. 定期轮换API密钥
4. 监控API使用情况和费用
