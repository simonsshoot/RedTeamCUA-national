# RedTeamCUA Docker Setup Guide for Windows

## 第二步：混合沙箱环境设置 - Web服务部分

### 前提条件

1. **安装Docker Desktop**
   - 访问：https://docs.docker.com/desktop/install/windows/
   - 下载并安装Docker Desktop for Windows
   - 安装完成后重启电脑
   - 启动Docker Desktop并确保它正在运行

2. **验证Docker安装**
   ```powershell
   docker --version
   docker-compose --version
   ```

### 手动设置Web服务（如果Docker安装遇到问题）

如果Docker Desktop安装遇到问题，您可以选择以下替代方案：

#### 方案1：使用云服务器
1. 租用一个云服务器（如AWS EC2、阿里云ECS等）
2. 在云服务器上安装Docker并运行Web服务
3. 配置安全组开放端口：3000, 8092, 9999

#### 方案2：使用现有的演示服务器
根据README，您可以暂时使用以下测试URL：
- Reddit Forum: http://metis.lti.cs.cmu.edu:9999/
- OwnCloud: 需要自己设置
- RocketChat: 需要自己设置

### Docker安装完成后运行以下命令：

```powershell
# 1. 确保在项目目录下
cd "G:\redteamcua\RedTeamCUA-main"

# 2. 运行Web服务设置脚本
.\setup-web-services.ps1
```

### 验证服务运行状态

```powershell
# 检查容器状态
docker ps

# 检查服务访问
# 在浏览器中访问：
# - http://localhost:9999  (Reddit Forum)
# - http://localhost:8092  (OwnCloud)
# - http://localhost:3000  (RocketChat)
```

### 常见问题解决

1. **端口冲突**
   ```powershell
   # 检查端口占用
   netstat -ano | findstr :3000
   netstat -ano | findstr :8092
   netstat -ano | findstr :9999
   ```

2. **容器无法启动**
   ```powershell
   # 查看日志
   docker-compose logs
   ```

3. **浏览器无法访问**
   - 使用无痕模式访问
   - 在Chrome中禁用"始终使用安全连接"

### 下一步

Web服务设置完成后，您可以继续进行第三步：实验配置生成

```powershell
# 生成配置文件
bash generate_config.sh
```

或者使用PowerShell版本：
```powershell
# 如果没有bash，可以手动执行配置生成
python generate_config.py
```
