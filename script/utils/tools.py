
import pandas as pd
from pathlib import Path   
import re
import math
from typing import Callable, Optional
from datetime import datetime
import openpyxl

import sys
import os

def get_resource_path(relative_path):
    """Ottieni il percorso assoluto del file, tenendo conto dell'esecuzione tramite PyInstaller."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def choose_release(available_release: list) -> str:
    print("Available releases:")
    for release in sorted(available_release, reverse=True):
        print(" ", release)

    while True:
        release_chosen = input(f"Insert release [default {release}]: ").strip()
        
        # Set release to default if input is empty
        if release_chosen == "":
            release_chosen = release

        # Check if chosen release is in the available options
        if release_chosen in available_release:
            release = release_chosen
            print(f"You chose release {release}")
            break  # Exit the loop if a valid release is chosen
        else:
            print("Error: Release not available. Please choose a valid release from the list above.")
    return release
    

def normal_round(n):
    """
    Rounds a number to the nearest integer, following traditional rounding rules.

    Parameters:
    - n (float): The number to be rounded.

    Returns:
    - int: The rounded integer value. If the fractional part of `n` is less than 0.5, 
      the function returns the floor of `n`; otherwise, it returns the ceiling of `n`.

    Example:
    >>> normal_round(3.2)
    3
    >>> normal_round(3.7)
    4
    >>> normal_round(3.5)
    4
    """
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)



def convert_file(file_path: str | Path, save_path: str | Path, log_func: Optional[Callable[[str], None]] = None) -> pd.DataFrame | str | Path :
    """
    Convert an Excel file to the desired format, saving both .txt and .xlsx versions.

    Parameters:
    - file_path (str | Path): The path of the Excel file to convert. Do specify the name of the file like 'C:/User/.../file.xlsx'
    - save_path (str | Path): The path where to save the converted file. Do not specify the name of the file like 'C:/User/.../folder/'
    
    Return:
    - Dataframe of the converted file
    - str or Path if the process encounters an error
    """
    
    def log(message):
        if log_func:
            log_func(message)
        else:
            print(message)

    try:
        # Extract file name for saving (same as SharePoint file name)
        file_name = Path(file_path).stem

        # Load Excel file with specified columns and data types
        df = pd.read_excel(
            file_path,
            usecols="A:F",
            dtype={"A": "str", "B": "str", "C": "str", "D": "str", "E": "str", "F": "float"},
            engine="openpyxl"
        )

        # Clean and prepare data
        df = df.dropna()
        df.columns = ['REGION', 'MODEL', 'SIZE', 'COLOR', 'P', 'QTY']

        # Convert 'QTY' column to integers, rounding if needed
        df["QTY"] = df["QTY"].apply(lambda x: int(normal_round(x)))
        
        # Output total budget for verification
        total_budget = int(df["QTY"].sum())
        if total_budget > 50000:
            log(f"\tWARNING: Total Budget for the file: {total_budget}. The total is pretty high, check the file manually.")
        else:
            log(f"\tTotal Budget for the file: {total_budget}")
        log('\t----------\n')

        # Define the save path and ensure directories exist
        save_path = Path(save_path)
        save_path.mkdir(parents=True, exist_ok=True)

        # Save as .txt and .xlsx with standardized naming
        df.to_csv(save_path / f"{file_name}.txt", header=False, index=False, sep='\t', mode='w')
        df.to_excel(save_path / f"{file_name}.xlsx", index=False)
        
        return df

    except Exception as e:
        log(f"Error processing file '{file_path}': {e}")
        log(f"Please, check the file manually")
        
        return file_path   
    
    
            
        

def find_and_convert_files(release: str, 
                           pattern: str | re.Pattern[str], 
                           search_path: str | Path, 
                           regions: list | tuple | set, 
                           budget_definition_folder: str,
                           save_path: str | Path,
                           log_func: Optional[Callable[[str], None]] = None) -> None:
    """
    Find all files matching a pattern in subdirectories of a given path.
    Convert the files to the desired format and save them in designated folders.
    
    Parameters:
    - release (str): The release name to look for.
    - pattern (str | re.Pattern): The pattern to match file names against.
    - search_path (str | Path): The path in which to search for files.
    - log_func (Optional[Callable[[str], None]]): A function to handle log messages.
    
    Return:
    - None
    """
    
    dataframes = []
    errors = []
    if isinstance(pattern, str):
        pattern = re.compile(pattern)
    
    def log(message):
        if log_func:
            log_func(message)
        else:
            print(message)

    for root_dir in Path(search_path).glob("*"):
        region = root_dir.name
        if region in regions:
            log(f"\nProcessing region: {region}")

            # Search for folders matching the release name in the region directory
            for sub_dir in (root_dir / budget_definition_folder).rglob("*"):
                folder_name_cleaned = re.sub(r"\W", " ", sub_dir.name)
                release_cleaned = re.sub(r"\W", " ", release)

                
                if folder_name_cleaned == release_cleaned:
                    for file in sub_dir.rglob("*"):
                        if pattern.match(file.name.upper()):
                            log(f"\tFile found: {file.name}")
                            
                            df = convert_file(file_path=file,
                                        save_path=save_path/region,
                                        log_func=log_func)
                            
                            if isinstance(df, pd.DataFrame):
                                dataframes.append(df)
                            elif isinstance(df, Path):
                                errors.append(df)
            log('-------------------------------')
            
    if dataframes:
        aggregate_df = pd.concat(dataframes)
        timestamp = datetime.now().strftime("%Y_%m_%d")
        name = f"{timestamp}_aggregate"
        aggregate_df.to_csv(save_path / f"{name}.txt", header=False, index=False, sep='\t', mode='w')
        aggregate_df.to_excel(save_path / f"{name}.xlsx", index=False)
        log(f"Data saved in {save_path}")
    else:
        log("No files found")
        
    return dataframes, errors


def put_tag(release: str,
            pattern: str | re.Pattern[str], 
            search_path: str | Path, 
            sharepoint_path: str | Path,
            regions: list | tuple | set, 
            budget_definition_folder: str,
            tag: str = 'UPLOADED',
            log_func: Optional[Callable[[str], None]] = None
            ) -> None:
    

    def log(message):
        if log_func:
            log_func(message)
        else:
            print(message) 

    if isinstance(pattern, str):
        pattern = re.compile(pattern)


    for root_dir in Path(search_path).rglob("*"):
        region = root_dir.name
        if region in regions:
            log(f"\nProcessing region: {region}")
            files = [f for f in root_dir.iterdir() if f.is_file()]
            newest_time = max(f.stat().st_mtime for f in files)
            newest_files = [f.name for f in files if f.stat().st_mtime == newest_time]

            for file in Path(sharepoint_path / region / budget_definition_folder / release).rglob("*"):
                if file.name in newest_files:
                    new_name = file.with_name(f"{tag}_" + file.name)
                    file.rename(new_name)
                    log(f" File renamed: {file.name}") 
            log('-------------------------------')
  