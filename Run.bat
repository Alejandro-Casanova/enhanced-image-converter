@ECHO OFF

REM Check if .venv exists
IF NOT EXIST ".venv" (
    ECHO Virtual environment not found. Please run Setup.bat first.
    EXIT /B 1
)

REM Activate the existing virtual environment
CALL .venv\Scripts\activate.bat
ECHO Virtual environment activated.

REM Run the main application
ECHO Starting the application...
python main.py

REM Check error level
IF %ERRORLEVEL% NEQ 0 (
    ECHO An error occurred while running the application. Please check the messages above.
)

REM PAUSE to keep the window open
PAUSE
EXIT /B %ERRORLEVEL%