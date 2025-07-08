@echo off
cd /d "%~dp0"
start cmd /k "call backend\run.bat"
@REM start cmd /k "call frontend\start.bat"
