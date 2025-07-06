#!/usr/bin/env python3
"""
简化的 OwnCloud Trusted Domains 修复工具
"""

import subprocess
import sys
import os

def run_docker_command(command):
    """运行Docker命令"""
    try:
        cmd = f"docker {command}"
        print(f"执行命令: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, 
                              encoding='utf-8', errors='ignore', timeout=60)
        
        if result.returncode == 0:
            print("✓ 命令执行成功")
            if result.stdout.strip():
                print(f"输出: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ 命令执行失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ 执行出错: {e}")
        return False

def main():
    print("OwnCloud Trusted Domains 简化修复工具")
    print("=" * 50)
    
    # 1. 检查容器状态
    print("\n1. 检查OwnCloud容器状态...")
    if not run_docker_command("ps | findstr owncloud"):
        print("OwnCloud容器未运行，请先启动容器")
        return
    
    # 2. 备份原配置
    print("\n2. 备份原配置文件...")
    run_docker_command("exec owncloud cp /var/www/owncloud/config/config.php /var/www/owncloud/config/config.php.backup")
    
    # 3. 修改trusted_domains配置
    print("\n3. 修改trusted_domains配置...")
    
    # 创建新的配置内容
    config_content = '''<?php
$CONFIG = array (
  'apps_paths' =>
  array (
    0 =>
    array (
      'path' => '/var/www/owncloud/apps',
      'url' => '/apps',
      'writable' => false,
    ),
    1 =>
    array (
      'path' => '/var/www/owncloud/custom',
      'url' => '/custom',
      'writable' => true,
    ),
  ),
  'trusted_domains' =>
  array (
    0 => 'localhost',
    1 => '127.0.0.1',
    2 => 'the-agent-company.com',
    3 => '192.168.229.1',
    4 => '192.168.229.1:8092',
    5 => '192.168.28.183',
    6 => '192.168.28.183:8092',
  ),
  'datadirectory' => '/mnt/data/files',
  'dbtype' => 'sqlite',
  'dbhost' => '',
  'dbname' => 'owncloud',
  'dbuser' => '',
  'dbpassword' => '',
  'dbtableprefix' => 'oc_',
  'log_type' => 'owncloud',
  'supportedDatabases' =>
  array (
    0 => 'sqlite',
    1 => 'mysql',
    2 => 'pgsql',
  ),
  'upgrade.disable-web' => true,
  'default_language' => 'en',
  'overwrite.cli.url' => 'http://localhost:8092/',
  'htaccess.RewriteBase' => '/',
  'logfile' => '/mnt/data/files/owncloud.log',
  'memcache.local' => '\\\\OC\\\\Memcache\\\\APCu',
  'filelocking.enabled' => true,
  'passwordsalt' => 'e9VYmHDYN8YDtaO/+PkXQrfVz3VofZ',
  'secret' => 'BxlR8Tzu1V4c1/kqmT03Zu/KLUARXaQkYJyOj15a4aZYDSIb',
  'version' => '10.13.4.1',
  'allow_user_to_change_mail_address' => '',
  'logtimezone' => 'UTC',
  'installed' => true,
  'instanceid' => 'ocobr5t36tar',
);'''
    
    # 将配置写入临时文件
    temp_config_file = "temp_config.php"
    with open(temp_config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    # 复制配置到容器
    if run_docker_command(f"cp {temp_config_file} owncloud:/var/www/owncloud/config/config.php"):
        print("✓ 配置文件已更新")
    else:
        print("✗ 配置文件更新失败")
        return
    
    # 删除临时文件
    try:
        os.remove(temp_config_file)
    except:
        pass
    
    # 4. 重启容器
    print("\n4. 重启OwnCloud容器...")
    if run_docker_command("restart owncloud"):
        print("✓ 容器重启成功")
    else:
        print("✗ 容器重启失败")
        return
    
    # 5. 等待容器启动
    print("\n5. 等待容器启动...")
    import time
    time.sleep(10)
    
    # 6. 验证配置
    print("\n6. 验证配置...")
    run_docker_command("exec owncloud cat /var/www/owncloud/config/config.php")
    
    print("\n修复完成！")
    print("现在可以尝试从虚拟机访问:")
    print("- http://192.168.229.1:8092")
    print("- http://the-agent-company.com:8092")

if __name__ == "__main__":
    main()
