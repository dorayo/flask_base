# 设置执行策略以允许运行脚本
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 删除 migrations 目录
Remove-Item -Recurse -Force .\migrations

# 提示用户输入 MySQL 密码
Write-Host "Please enter the password of MySQL"

# 创建数据库和用户，并授权
$sqlCommands = @"
CREATE DATABASE IF NOT EXISTS flask_base CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'flask_base'@'%' IDENTIFIED BY '123456';  
GRANT ALL ON flask_base.* TO 'flask_base'@'%'; 
FLUSH PRIVILEGES;
"@

# 执行 MySQL 命令
$sqlCommands | mysql -u root -p

# 设置环境变量
$env:FLASK_APP = "flask_base"
$env:FLASK_CONFIG = "development"

# 初始化数据库表并更新
flask db init
flask db migrate -m "init table"
flask db upgrade

# 退出虚拟环境
deactivate
