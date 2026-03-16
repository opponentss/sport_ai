import subprocess
import os
import sys

os.chdir(r'h:\ai_sport')
git_path = r'H:\git\Git\cmd\git.exe'

# 设置凭据帮助器
subprocess.run([git_path, 'config', 'credential.helper', 'store'])

# 使用 Popen 来处理交互式输入
process = subprocess.Popen(
    [git_path, 'push', '-u', 'origin', 'main'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# 等待进程完成
stdout, stderr = process.communicate()

print("STDOUT:", stdout)
print("STDERR:", stderr)
print("Return code:", process.returncode)
