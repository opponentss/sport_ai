import subprocess
import os

os.chdir(r'h:\ai_sport')

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
