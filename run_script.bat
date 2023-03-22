@echo off

:start
python main.py
echo Restarting in 5 minutes...
timeout /t 300 >nul
goto start