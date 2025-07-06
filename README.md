<<<<<<< HEAD
# RedTeamCUA-National

基于RedTeamCUA的国内大模型安全评估项目，新加Kimi、DeepSeek等国内模型的测试和安全性评估。

## 📋 项目简介

RedTeamCUA-National是基于原始[RedTeamCUA](https://github.com/poloclub/RedTeamCUA)项目的扩展版本，专门针对国内大语言模型进行了优化和适配。项目实现了：

-  **国内模型适配**: 支持Kimi、DeepSeek、通义千问等主流国内模型
-  **安全性评估**: 基于CIA三元组的系统性安全评估
-  **对比分析**: 与Claude、GPT等国外模型的详细对比
-  **一键部署**: 完整的Docker + VMware环境自动化部署
-  **可视化分析**: 丰富的ASR统计和安全性分析报告

## 🚀 快速开始

### 环境要求

- Windows 10/11 或 Ubuntu 18.04+
- Docker Desktop
- VMware Workstation Pro (用于虚拟机测试环境)
- Python 3.8+

### 安装步骤

1. **克隆项目**
```bash
git clone git@github.com:simonsshoot/RedTeamCUA-national.git
cd RedTeamCUA-national
```

2. **安装依赖**
```bash
pip install -r requirements.txt
# 或使用uv (推荐)
uv sync
```

3. **配置API密钥**
```bash
# 复制配置模板
cp .env.example .env
# 编辑.env文件，填入你的API密钥
```

4. **一键部署环境**
```bash
# 启动Docker服务
docker-compose up -d

# 配置OwnCloud trusted domains
python fix_owncloud_simple.py

# 验证环境
python test_setup.py
```

## 🔧 配置说明

### API密钥配置

在`.env`文件中配置以下API密钥：

```env
# Kimi (月之暗面)
KIMI_API_KEY=your_kimi_api_key

# DeepSeek
DEEPSEEK_API_KEY=your_deepseek_api_key

# OpenAI (可选，用于对比)
OPENAI_API_KEY=your_openai_api_key
```

### 虚拟机配置

项目需要VMware虚拟机作为测试环境：

1. 从[原始项目](https://github.com/poloclub/RedTeamCUA)下载虚拟机镜像
2. 将虚拟机文件放入`vmware_vm_data`目录
3. 更新`vmware_vm_data`路径配置

**注意**: 由于文件大小限制，虚拟机镜像未包含在此仓库中，需要单独下载。

## 🛠 使用说明

### 运行基础评估

```bash
# 测试Kimi模型
python run.py --model "kimi | moonshot-v1-8k" \
  --headless \
  --path_to_vm ./vmware_vm_data/Ubuntu0/Ubuntu0.vmx \
  --observation_type screenshot \
  --test_all_meta_path ./evaluation_examples/test_all_owncloud.json \
  --domain owncloud \
  --max_steps 50

# 测试DeepSeek模型
python run.py --model "deepseek | deepseek-chat" \
  --headless \
  --path_to_vm ./vmware_vm_data/Ubuntu0/Ubuntu0.vmx \
  --observation_type screenshot \
  --test_all_meta_path ./evaluation_examples/test_all_owncloud.json \
  --domain owncloud \
  --max_steps 50
```





## 📈 改进和优化

相比原始项目，本版本包含以下改进：

### 技术改进
- ✅ 国内模型API适配和优化
- ✅ 网络连接和防火墙问题解决
- ✅ OwnCloud trusted domains自动配置
- ✅ 完善的错误处理和日志记录
- ✅ 一键部署和环境验证脚本


## 🙏 致谢

- 原始[RedTeamCUA](https://github.com/poloclub/RedTeamCUA)项目团队
- Kimi（月之暗面）和DeepSeek团队提供的API支持
- 所有为项目改进提供建议和反馈的贡献者

---

**免责声明**: 本项目仅用于学术研究，使用者需自行承担使用风险和责任。
=======

