@echo off
echo Installing main project dependencies...
call npm install

echo.
echo Installing specific dependencies: vuex, chartjs-adapter-date-fns, date-fns...
call npm install vuex chartjs-adapter-date-fns date-fns keycloak-js

echo.
echo Starting Keycloak...
if exist kc.bat (
  call kc.bat start-dev
) else (
  echo [ERROR] kc.bat not found in current directory.
  pause
  exit /b
)

echo Starting the development server...
start /min cmd /c "timeout /t 3 >nul && start http://localhost:5173"
call npm run dev

pause
