@echo off
echo ======================================
echo    CLEARING WINDOWS ICON CACHE
echo ======================================
echo.
echo This will refresh all icons in Windows Explorer
echo Press any key to continue or Ctrl+C to cancel
pause >nul

echo.
echo [1/4] Stopping Windows Explorer...
taskkill /f /im explorer.exe

echo [2/4] Clearing icon cache files...
del /f /s /q "%localappdata%\IconCache.db" 2>nul
del /f /s /q "%localappdata%\Microsoft\Windows\Explorer\iconcache*" 2>nul

echo [3/4] Waiting 2 seconds...
timeout /t 2 /nobreak >nul

echo [4/4] Restarting Windows Explorer...
start explorer.exe

echo.
echo ======================================
echo   ICON CACHE CLEARED SUCCESSFULLY!
echo ======================================
echo.
echo Your YouTube-Downloader.exe should now show
echo the correct icon at all sizes.
echo.
echo If you still see old icons:
echo 1. Right-click the exe file and select "Refresh"
echo 2. Or restart your computer
echo.
pause
