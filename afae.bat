@echo off
cd /d "%~dp0afae"
call setup_python.bat
cd /d "%~dp0afae"
python ./pyscripts/main.py
pause
