@ECHO OFF

REM Check if .venv exists
IF NOT EXIST ".venv" (
    REM Create a new virtual environment
    ECHO Creating virtual environment...
    python -m venv .venv
    ECHO Virtual environment created.
    SET FIRST_TIME=1

    REM Activate the existing virtual environment
    CALL .venv\Scripts\activate.bat
    ECHO Virtual environment activated.

    REM Install required packages
    ECHO Installing required packages...
    pip install -r requirements.txt
    ECHO Required packages installed.
) ELSE (
    ECHO Virtual environment already set up. Skipping package installation.
)

REM Check error level
IF %ERRORLEVEL% NEQ 0 (
    ECHO An error occurred during setup. Please check the messages above.
)

REM PAUSE to keep the window open
PAUSE

EXIT /B %ERRORLEVEL%