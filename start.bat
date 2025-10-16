@echo off
echo Starting Smart Task Manager Flask Backend...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo Please edit .env file with your MySQL database credentials before running the app.
    echo.
    pause
    exit /b 1
)

REM Start the Flask application
echo Starting Flask application...
echo API will be available at: http://localhost:5000
echo.
python app.py

pause


