@echo off
cd /d %~dp0

echo Installing main project dependencies...
call npm install

echo.
echo Installing specific dependencies: vuex, chartjs-adapter-date-fns, date-fns...
call npm install vuex chartjs-adapter-date-fns date-fns

echo.

echo Starting the development server...
start /min cmd /c "timeout /t 3 >nul && start http://localhost:5173"
call npm run dev

pause
