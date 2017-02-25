@echo off
: top
start /min telegram.py
: check
TIMEOUT 5
tasklist  | find "python"
if %errorlevel% == 1 (goto :top) else (goto :check)