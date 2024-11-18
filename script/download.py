# Standard Libs
import pandas as pd
from pathlib import Path
import re
import datetime
import yaml
import os
from datetime import datetime

# Local import
from utils.constant import OS, USER, MAC_OS, WINDOWS_OS
from utils.tools import find_and_convert_files, choose_release

# Config file
with open(Path(__file__).parents[1] / 'config.yaml', 'r') as file:
    config = yaml.safe_load(file)




# Define shared file path based on operating system
if OS == MAC_OS:
    sharepoint_path = Path(fr"/Users/{USER}/Library/CloudStorage/OneDrive-Raccoltecondivise-LuxotticaGroupS.p.A/NPI Demand Planning - Documents")
    
elif OS == WINDOWS_OS:
    sharepoint_path = Path(fr"C:\Users\{USER}\Luxottica Group S.p.A\NPI Demand Planning - Documents")
else:
    raise NotImplementedError("Unsupported operating system: expected MacOS or Windows")

# Define release
available_release  = (
    [entry.name for entry in (sharepoint_path / "BRA/BUDGET DEFINITION").iterdir() if entry.is_dir() 
    and re.compile(config['pattern release']).match(entry.name)]
)
release = choose_release(available_release=available_release)

# Define save path based on operating system
year = release[-4:]
save_path = Path(__file__).parents[2] / year / release

dataframes, errors =  find_and_convert_files(
                        release = release, 
                        pattern = config['pattern file'], 
                        search_path = sharepoint_path, 
                        regions = config['regions'], 
                        budget_definition_folder = config['budget_folder'],
                        save_path = save_path
                        )

if dataframes:
    aggregate_df = pd.concat(dataframes)
    
    answer = input("Do you wanna save the aggregation (yes/no)? [default yes]")
    if answer.lower() in ['y','','yes','ys']:
        timestamp = datetime.now().strftime("%Y_%m_%d")
        name = f"{timestamp}_aggregate"
        aggregate_df.to_csv(save_path / f"{name}.txt", header=False, index=False, sep='\t', mode='w')
        aggregate_df.to_excel(save_path / f"{name}.xlsx", index=False)
        print(f"\nfile {name} saved in {save_path}")
    else:
        print("Skipping the process")





