import subprocess
import os
import sys
import getpass

os.chdir(r'h:\ai_sport')
git_path = r'H:\git\Git\cmd\git.exe'

# 获取 GitHub 用户名和密码
username = input("GitHub username: ")
password = getpass.getpass("GitHub password (or personal access token): ")

# 使用凭据帮助器
subprocess.run([git_path, 'config', 'credential.helper', 'store'])

# 创建凭据文件
cred_content = f"https://{username}:{password}@github.com"
cred_file = os.path.expanduser("~/.git-credentials")

with open(cred_file, 'w') as f:
    f.write(cred_content)

# 尝试推送
result = subprocess.run(
    [git_path, 'push', '-u', 'origin', 'main'],
    capture_output=True,
    text=True
)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
