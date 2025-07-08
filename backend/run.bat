@echo off
cd /d "%~dp0"
python generateData.py
python app.py
pause