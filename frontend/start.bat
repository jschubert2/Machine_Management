@echo off
cd /d %~dp0

@REM echo Installing main project dependencies...
@REM call npm install

@REM echo.
@REM echo Installing specific dependencies: vuex, chartjs-adapter-date-fns, date-fns...
@REM call npm install vuex chartjs-adapter-date-fns date-fns

echo.
echo Starting the development server...
call npm run dev

pause
