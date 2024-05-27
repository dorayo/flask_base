# 查找并删除所有 __pycache__ 目录，排除 venv 目录
Get-ChildItem -Path . -Recurse -Directory -Exclude 'venv' | Where-Object { $_.Name -eq '__pycache__' } | ForEach-Object { Remove-Item -Recurse -Force $_.FullName }
