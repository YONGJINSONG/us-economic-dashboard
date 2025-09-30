Write-Host "Installing required Python packages..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host ""
Write-Host "Starting RRG Indicator..." -ForegroundColor Green
python RRGIndicator.py

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
