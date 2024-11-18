#!/bin/bash

# Map the network drive if needed (Mac usually auto-mounts, so this might not be necessary)
# Note: Uncomment the line below if you have a specific mount command for the drive.
# mount -t smbfs //username:password@server/share /Volumes/Share

# Navigate to the project directory
cd "/Volumes/Share/Gruppo_Demand_Planning/02_NPI/BUDGET_INSERTION/EXCEL_TXT_INSERIMENTI/download_bgt"

# Activate the virtual environment
source .venv/bin/activate

# Run the Python script
python script/gui.py