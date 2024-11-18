@echo off
REM delete the Y network drive
net use Y: /delete

REM Map the network drive (if needed)
net use Y: "\\luxapplp04\Share\Gruppo_Demand_Planning\02_NPI\BUDGET_INSERTION\EXCEL_TXT_INSERIMENTI"

REM Change directory to the project folder
cd /d "Y:\download_bgt"

REM Run the Python script using the environment�s Python interpreter
if exist "Y:\download_bgt\.env\python.exe" (
    "Y:\download_bgt\.env\python.exe" "Y:\download_bgt\script\gui.py"
) else (
    echo Error: Python executable not found in environment. Please check the installation.
    pause
    exit /b
)

REM Optionally pause to see any output before the window closes
pause
