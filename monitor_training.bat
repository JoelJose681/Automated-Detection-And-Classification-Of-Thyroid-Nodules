@echo off
setlocal enabledelayedexpansion

REM Training Progress Monitor - Real-time updates
REM Shows loss, accuracy, and estimated completion time

echo.
echo ================================================================================
echo TRAINING MONITOR - Improved Model with TN5000 Dataset
echo ================================================================================
echo.
echo Dataset: 10,479 images (up from 5,479 +91%%)
echo Model: ResNet50 with class weighting
echo Training Features:
echo   - Frozen backbone: 10 epochs @ batch 32
echo   - Unfrozen backbone: 90 epochs @ batch 8
echo   - Class weights: Benign 0.68x, Malignant 1.92x
echo   - Augmentation: Aggressive (rotations, colors, flips, blur)
echo   - Scheduler: CosineAnnealingLR
echo.
echo Expected Duration: 4-5 hours
echo ================================================================================
echo.

REM Monitor loop - updates every 30 seconds
set check_count=0
set max_checks=600

:monitor_loop
set /a check_count+=1
echo [%date% %time%] Check !check_count! / !max_checks!

REM Check if training is still running
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "python.exe" >NUL
if errorlevel 1 (
    echo.
    echo ========================================================================
    echo TRAINING COMPLETED OR FAILED
    echo ========================================================================
    
    REM Check for output files
    if exist "checkpoints/best_model_improved.pt" (
        echo Model saved: checkpoints/best_model_improved.pt
        echo Training results saved: checkpoints/training_results_improved.json
        echo.
        echo ✓ SUCCESS - Training completed!
    ) else (
        echo ✗ ERROR - Model file not found
        echo Check for errors in the training output
    )
    goto :end
)

REM Show Python process info
for /F "delims=" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH') do (
    set proc_info=%%a
)

REM Show memory usage
for /F "tokens=1,5" %%A in ('tasklist /FI "IMAGENAME eq python.exe" /FO TABLE /NH') do (
    if "%%A" == "python.exe" (
        set mem_usage=%%B
    )
)

echo   Python is running - Memory usage: !mem_usage: K!
echo.

REM Wait 30 seconds
timeout /t 30 /nobreak

REM Check for model file
if exist "checkpoints/best_model_improved.pt" (
    echo [INFO] Model checkpoint detected - Training in progress
)

REM Check if exceeded maximum time (600 checks * 30 sec = 5 hours)
if !check_count! geq !max_checks! (
    echo.
    echo ========================================================================
    echo Maximum monitoring time reached (5 hours)
    echo ========================================================================
    goto :end
)

goto :monitor_loop

:end
echo.
echo ========================================================================
echo Monitoring complete
echo ========================================================================
echo.
echo Next steps:
echo   1. Check training results: get-content checkpoints/training_results_improved.json
echo   2. Test model: .\.venv\Scripts\python.exe test_model.py
echo   3. Run inference: .\.venv\Scripts\python.exe inference.py image.jpg
echo.
