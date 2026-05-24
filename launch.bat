@echo off
REM Launch script for Thyroid Nodule Project
SETLOCAL
echo Activating virtual environment if present...
if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
) else (
  echo No virtual environment found at .venv; using system Python.
)
echo Starting the Flask application...
python backend\app\app.py %*
if ERRORLEVEL 1 (
  echo.
  echo Application exited with error.
  pause
)
ENDLOCAL
exit /b 0