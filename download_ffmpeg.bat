@echo off
echo ======================================
echo       DOWNLOADING FFMPEG
echo ======================================
echo.

cd ffmpeg

echo Downloading FFmpeg...
echo This may take a few minutes...

curl -L "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip" -o ffmpeg.zip

if exist ffmpeg.zip (
    echo.
    echo Extracting FFmpeg...
    powershell -command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force"
    
    echo Moving files...
    for /d %%i in (ffmpeg-master-*) do (
        xcopy "%%i\bin\*" "bin\" /Y
        rmdir "%%i" /S /Q
    )
    
    del ffmpeg.zip
    
    echo.
    echo ======================================
    echo       FFMPEG INSTALLED SUCCESSFULLY!
    echo ======================================
    echo.
    echo Files installed:
    if exist "bin\ffmpeg.exe" echo   ✓ ffmpeg.exe
    if exist "bin\ffprobe.exe" echo   ✓ ffprobe.exe
    echo.
    echo Ready to build with: pyinstaller YouTube-Downloader.spec
    
) else (
    echo ERROR: Failed to download FFmpeg
    echo Please check your internet connection
)

cd ..
pause
