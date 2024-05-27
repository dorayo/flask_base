source venv/bin/activate
rm -rf migrations
# 创建数据库
echo "Please enter the password of MySQL"
echo "
CREATE DATABASE IF NOT EXISTS flask_base CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# 创建用户并授权所有权限
# MySQL 8.0
CREATE USER 'flask_base'@'%' IDENTIFIED BY '123456';  
GRANT ALL ON flask_base.* TO 'flask_base'@'%'; 
# MySQL 5.7
#grant all privileges on flask_base.* to flask_base@localhost identified by '123456';
flush privileges;
" | mysql -u root -p
# 数据库表初始化及更新
export FLASK_APP=flask_base
export FLASK_CONFIG=development
flask db init
flask db migrate -m "init table"
flask db upgrade
