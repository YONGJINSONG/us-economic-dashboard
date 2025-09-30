@echo off
echo Installing required Python packages...
pip install -r requirements.txt

echo.
echo Starting RRG Indicator...
python RRGIndicator.py

pause
