import subprocess
import os

os.chdir(r'h:\ai_sport')

# 修改 remote 为 HTTPS 方式
result = subprocess.run(
    [r'H:\git\Git\cmd\git.exe', 'remote', 'set-url', 'origin', 'https://github.com/opponentss/sport_ai.git'],
    capture_output=True,
    text=True,
    shell=True
)
print(result.stdout)
print(result.stderr)

result = subprocess.run(
    [r'H:\git\Git\cmd\git.exe', 'branch', '-M', 'main'],
    capture_output=True,
    text=True,
    shell=True
)
print(result.stdout)
print(result.stderr)

result = subprocess.run(
    [r'H:\git\Git\cmd\git.exe', 'push', '-u', 'origin', 'main'],
    capture_output=True,
    text=True,
    shell=True
)
print(result.stdout)
print(result.stderr)
