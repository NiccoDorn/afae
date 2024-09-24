@echo off
setlocal

set "PYTHON_VERSION=3.10.11"
set "DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe"
set "REQUIREMENTS_FILE=requirements.txt"

python3 --version >nul 2>&1
if %errorlevel%==0 (
    echo Python is already installed.
) else (
    echo Downloading Python %PYTHON_VERSION%...
    powershell -command "Invoke-WebRequest -Uri %DOWNLOAD_URL% -OutFile python_installer.exe"
    if errorlevel 1 (
        echo Failed to download Python installer. Exiting...
        exit /b 1
    )
    echo Installing Python...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    echo Python %PYTHON_VERSION% installed successfully.
)

pip --version >nul 2>&1
if %errorlevel%==0 (
    echo pip is already installed.
) else (
    echo pip is not installed. Please install pip manually.
    exit /b 1
)

if exist "%REQUIREMENTS_FILE%" (
    echo Installing packages from %REQUIREMENTS_FILE%...
    pip install -r "%REQUIREMENTS_FILE%"
    if errorlevel 1 (
        echo Failed to install some packages. Check requirements.txt for details.
    ) else (
        echo All packages installed successfully.
    )
) else (
    echo %REQUIREMENTS_FILE% not found. No packages installed.
)

endlocal
pause