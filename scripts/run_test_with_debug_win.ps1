# 设置执行策略以允许运行脚本
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 输出当前工作目录
Write-Output "Running tests in $(Get-Location)"

# 运行测试并生成覆盖率报告
pytest -s --cov=app --cov-report=term-missing --cov-branch tests

# 退出虚拟环境
deactivate