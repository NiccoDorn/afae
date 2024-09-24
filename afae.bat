@echo off
cd /d "%~dp0afae"
call setup_python.bat
python3 ./pyscripts/main.py
pause
