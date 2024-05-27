# flask_base 应用
## 运行环境要求
1. linux CentOS7.x 64位
2. Python3 + flask
3. mysql5.7+
4. redis-server

## 运行虚拟环境

```
python3 -m venv venv
source venv/bin/activate
```

## 安装依赖

```
pip install -r requirements.txt
```

## 数据库初始化

```
# 创建数据库
mysql -u root -p
CREATE DATABASE flask_base CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户并授权所有权限
grant all privileges on flask_base.* to "flask_base"@"localhost" identified by "123456";
flush privileges;

# 数据库表初始化及更新
export FLASK_APP=flask_base
flask db init
flask db migrate -m "init table"
flask db upgrade
```

## 启动单元测试
```
./scripts/run_test.sh
```

## 启动应用

```
./scripts/run.sh
```
