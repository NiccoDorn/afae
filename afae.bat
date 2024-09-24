@echo off
cd /d "%~dp0"  && cd afae
call setup_python.bat
cd /d "%~dp0" && cd afae
python ./pyscripts/main.py
pause
