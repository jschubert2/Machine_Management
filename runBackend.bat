@echo off

echo -----------------------------------------
echo You are about to start the backend...
echo Please wait while it launches.
echo -----------------------------------------


backend\dist\generateData.exe
backend\dist\app\app.exe

pause