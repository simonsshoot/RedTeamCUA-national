#!/usr/bin/env python3
"""
修复OwnCloud trusted domains配置问题的脚本
"""

import subprocess
import sys
import time

def run_docker_command(command):
    """执行Docker命令"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def fix_owncloud_trusted_domains():
    """修复OwnCloud的trusted domains配置"""
    print("正在修复OwnCloud trusted domains配置...")
    
    # 1. 备份原始配置文件
    print("1. 备份原始配置文件...")
    backup_cmd = "docker exec owncloud cp /var/www/owncloud/config/config.php /var/www/owncloud/config/config.php.backup"
    success, output = run_docker_command(backup_cmd)
    if success:
        print("   ✓ 配置文件备份成功")
    else:
        print(f"   ✗ 备份失败: {output}")
    
    # 2. 创建新的配置内容
    print("2. 更新trusted domains配置...")
    
    # 用Python脚本在容器内执行配置修改
    python_script = '''
import re

# 读取配置文件
with open("/var/www/owncloud/config/config.php", "r") as f:
    content = f.read()

# 定义新的trusted_domains配置
new_trusted_domains = """  'trusted_domains' =>
  array (
    0 => 'localhost',
    1 => '127.0.0.1',
    2 => 'the-agent-company.com',
    3 => '192.168.229.1',
    4 => '192.168.229.1:8092',
    5 => '*',
  ),"""

# 使用正则表达式替换trusted_domains部分
pattern = r"'trusted_domains'\s*=>\s*array\s*\([^)]*\),"
content = re.sub(pattern, new_trusted_domains, content, flags=re.DOTALL)

# 写回文件
with open("/var/www/owncloud/config/config.php", "w") as f:
    f.write(content)

print("配置文件已更新")
'''
    
    # 执行Python脚本
    update_cmd = f'docker exec owncloud python3 -c "{python_script}"'
    success, output = run_docker_command(update_cmd)
    
    if success:
        print("   ✓ trusted domains配置更新成功")
    else:
        print(f"   ✗ 配置更新失败: {output}")
        # 如果Python方式失败，尝试sed命令
        print("   尝试使用替代方法...")
        
        # 直接替换整个trusted_domains数组
        sed_cmd = '''docker exec owncloud sh -c "
sed -i '/trusted_domains/,/),/c\\
  '"'"'trusted_domains'"'"' =>\\
  array (\\
    0 => '"'"'localhost'"'"',\\
    1 => '"'"'127.0.0.1'"'"',\\
    2 => '"'"'the-agent-company.com'"'"',\\
    3 => '"'"'192.168.229.1'"'"',\\
    4 => '"'"'192.168.229.1:8092'"'"',\\
    5 => '"'"'*'"'"',\\
  ),' /var/www/owncloud/config/config.php
"'''
        
        success2, output2 = run_docker_command(sed_cmd)
        if success2:
            print("   ✓ 使用sed命令更新成功")
        else:
            print(f"   ✗ sed命令也失败: {output2}")
    
    # 3. 验证配置文件
    print("3. 验证配置文件...")
    verify_cmd = "docker exec owncloud cat /var/www/owncloud/config/config.php"
    success, output = run_docker_command(verify_cmd)
    
    if success:
        if "'*'," in output or "192.168.229.1" in output:
            print("   ✓ 配置验证成功，包含所需的域名")
        else:
            print("   ⚠ 配置可能不完整，请手动检查")
    else:
        print(f"   ✗ 验证失败: {output}")
    
    # 4. 重启OwnCloud容器
    print("4. 重启OwnCloud容器...")
    restart_cmd = "docker restart owncloud"
    success, output = run_docker_command(restart_cmd)
    
    if success:
        print("   ✓ 容器重启成功")
        print("   等待容器完全启动...")
        time.sleep(10)
    else:
        print(f"   ✗ 容器重启失败: {output}")
    
    # 5. 测试访问
    print("5. 测试OwnCloud访问...")
    test_cmd = "docker exec owncloud curl -s -o /dev/null -w %{http_code} http://localhost:8080"
    success, output = run_docker_command(test_cmd)
    
    if success and output.strip() in ["200", "302"]:
        print(f"   ✓ OwnCloud服务测试成功 (HTTP {output.strip()})")
    else:
        print(f"   ⚠ OwnCloud服务测试: {output}")

def main():
    """主函数"""
    print("OwnCloud Trusted Domains 修复工具")
    print("=" * 40)
    
    # 检查Docker是否运行
    print("检查Docker状态...")
    success, output = run_docker_command("docker ps")
    if not success:
        print("✗ Docker未运行或无法访问")
        sys.exit(1)
    
    # 检查OwnCloud容器是否存在
    success, output = run_docker_command("docker ps --filter name=owncloud")
    if "owncloud" not in output:
        print("✗ OwnCloud容器未运行")
        sys.exit(1)
    
    print("✓ Docker和OwnCloud容器正常运行")
    print()
    
    # 执行修复
    fix_owncloud_trusted_domains()
    
    print()
    print("修复完成！")
    print("现在可以尝试从虚拟机访问:")
    print("- http://192.168.229.1:8092")
    print("- http://the-agent-company.com:8092")

if __name__ == "__main__":
    main()
