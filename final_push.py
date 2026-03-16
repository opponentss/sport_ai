import subprocess
import os
import sys

os.chdir(r'h:\ai_sport')
git_path = r'H:\git\Git\cmd\git.exe'

# 设置凭据帮助器
subprocess.run([git_path, 'config', 'credential.helper', 'store'])

# 尝试推送
result = subprocess.run(
    [git_path, 'push', '-u', 'origin', 'main'],
    capture_output=False
)

sys.exit(result.returncode)
