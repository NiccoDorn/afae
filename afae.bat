
@echo off
cd /d "%~dp0afae"
call install_python.bat
cd /d "%~dp0afae"
python3 main.py
pause
