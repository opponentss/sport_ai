import subprocess
import os

os.chdir(r'h:\ai_sport')

result = subprocess.run(
    [r'H:\git\Git\cmd\git.exe', 'push', '-u', 'origin', 'main', '--verbose'],
    capture_output=True,
    text=True,
    shell=True,
    env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'}
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
