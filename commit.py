import subprocess
import os

os.chdir(r'h:\ai_sport')

result = subprocess.run(
    [r'H:\git\Git\cmd\git.exe', 'commit', '-m', 'Initial commit'],
    capture_output=True,
    text=True,
    shell=True
)
print(result.stdout)
print(result.stderr)
