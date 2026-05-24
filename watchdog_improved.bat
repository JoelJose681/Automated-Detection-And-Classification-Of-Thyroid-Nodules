@echo off
REM ===========================================================================
REM Training Watchdog - Monitors improved training and auto-restarts if needed
REM Checks every 5 minutes - Run BEFORE starting training
REM ===========================================================================

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo THYROID CLASSIFICATION - IMPROVED MODEL TRAINING WATCHDOG
echo ================================================================================
echo.
echo This script will monitor training_improved.log and auto-restart if needed
echo Check interval: 5 minutes
echo Max restart attempts: 5
echo.
echo START TRAINING FIRST:
echo   .\.venv\Scripts\python.exe fine_tune_improved.py ^> training_improved.log 2^>^&1
echo.
timeout /t 10 /nobreak
echo.

set restart_count=0
set max_restarts=5

:check_loop
echo [%date% %time%] Checking training status...

REM Check if process is running
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "python.exe" >NUL
if errorlevel 1 (
    REM Python not running
    echo ! WARNING: Training process not running!
    
    REM Check if log exists and has recent updates
    if exist "training_improved.log" (
        for /F %%A in ('powershell -Command "Get-Item training_improved.log | Select-Object -ExpandProperty LastWriteTime"') do (
            set last_write=%%A
        )
        echo   Last update: !last_write!
        
        REM Check if training completed
        powershell -Command "Select-String -Path training_improved.log -Pattern 'TRAINING COMPLETE' -Quiet"
        if errorlevel 0 (
            echo   ✅ Training completed successfully!
            goto :eof
        )
        
        REM Try to restart
        set /a restart_count+=1
        if !restart_count! LEQ !max_restarts! (
            echo   ⚠️  Restarting training (attempt !restart_count! of !max_restarts!)...
            .\.venv\Scripts\python.exe fine_tune_improved.py >> training_improved.log 2>&1
        ) else (
            echo   ✗ Max restart attempts reached. Manual intervention needed.
            goto :eof
        )
    ) else (
        echo   ERROR: training_improved.log not found!
        echo   Make sure to run: .\.venv\Scripts\python.exe fine_tune_improved.py ^> training_improved.log 2^>^&1
        goto :eof
    )
) else (
    echo   ✅ Training running
    
    REM Get last few lines of log to show progress
    powershell -Command "Get-Content training_improved.log -Tail 3"
)

echo.
echo   Next check in 5 minutes...
echo.

REM Wait 5 minutes (300 seconds)
timeout /t 300 /nobreak
goto check_loop

REM End of script
:eof
echo.
echo ================================================================================
echo Training monitoring complete.
echo Check training_improved.log for full results
echo ================================================================================
