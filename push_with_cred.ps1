$env:GIT_TERMINAL_PROMPT = "0"
cd h:\ai_sport
& "H:\git\Git\cmd\git.exe" config credential.helper store
& "H:\git\Git\cmd\git.exe" push -u origin main
