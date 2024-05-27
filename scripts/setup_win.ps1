# 删除 .git 和 venv 目录
Remove-Item -Recurse -Force .\.git
Remove-Item -Recurse -Force .\venv

# 提示输入项目名称
Write-Host "Enter the project name:"
$project_name = Read-Host

# 重命名 flask_base.py 为项目名称对应的文件
Rename-Item -Path "flask_base.py" -NewName "${project_name}.py"

# 替换 README.md 和 config.py 中的 [Ff]lask_base 为项目名称
(Get-Content README.md) -replace "[Ff]lask_base", $project_name | Set-Content README.md
(Get-Content config.py) -replace "[Ff]lask_base", $project_name | Set-Content config.py

# 查找并替换 scripts 目录中所有文件（排除 setup.sh）中的 [Ff]lask_base 为项目名称
Get-ChildItem -Path .\scripts\* -Exclude setup.sh -File | ForEach-Object {
    (Get-Content $_.FullName) -replace "[Ff]lask_base", $project_name | Set-Content $_.FullName
}

# 设置虚拟环境
python -m venv venv
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt

# 执行数据库设置脚本
& .\scripts\setup_db.ps1

# 退出虚拟环境
deactivate
