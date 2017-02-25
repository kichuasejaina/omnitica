@echo off
: top
start telegram.py
: check
TIMEOUT 5
tasklist  | find "python"
if %errorlevel% == 1 (goto :top) else (goto :check)