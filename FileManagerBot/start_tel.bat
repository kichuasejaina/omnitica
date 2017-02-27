@echo off
: top
start /min telegram.py
: check
TIMEOUT 5
for /F "tokens=1" %%a in (telegram.py.pid) do (
set pidd=%%a
)
tasklist | find "%pidd%"
if %errorlevel% == 1 (goto :top) else (goto :check)
