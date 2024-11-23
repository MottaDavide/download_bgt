# Download Budget from Sharepoint

This project provides a graphical user interface (GUI) for managing the process of downloading, converting, and tagging budget files stored on a SharePoint server. Built using customtkinter, it streamlines workflows for handling budget-related tasks efficiently. In a nutshell, it permits to:

1. Download files from SharePoint
2. Put a tag on the very same file in the SharePoint to prevent future downloads.

![alt text](icon/sample.png)
## Features

- **Release Selection**: Select specific releases from a list of available options.
- **File Download**: Download budget files from a SharePoint directory and convert them into the required format.
- **File Tagging**: Tag processed files with a custom label (e.g., “UPLOADED”).
- **Logging**: View real-time logs of the processes for better traceability.


## Usage

0. Activate the `conda` environment via `conda activate \\luxapplp04\Share\Gruppo_Demand_Planning\02_NPI\BUDGET_INSERTION\EXCEL_TXT_INSERIMENTI\download_bgt\.condaw`
1. Execute the main script to start the GUI: `script/main.py`
2. Choose the release you want to process from the list of checkboxes
3. Click **Download** to fetch and convert files
4. (Outside this GUI) Upload the downloaded files into SAP.
5. Click **Put 'UPLOADED'** to tag the original file in the sharepoint to prevent future downloads.

## Configuration
The `script/config.yaml` file contains key settings for the application. Here an example
```yaml
pattern file: '^(?!.*UPLOADED)((?=.*SKU)|(?=.*YELLOW))(.*XLSX)'
pattern release: '^[A-Za-z0-9]{2} \d{4}$'
regions: ('BRA', 'FIL','JPN','LATAM','USA')
budget_folder: 'BUDGET DEFINITION'
```

- `pattern file`: regex  pattern used to identify the files to process
- `pattern release`: regex pattern used to keep only the correct release format
- `regions`: list of regions/areas/type launches from where and to where process the files
- `budget_folder`: name for the SharePoint folder where the files are stored

## Create .exe file

0. Create the virtual environment if needed
```
conda env create --prefix .condaw -f environment.yml
```
1. Activate the virtual environment via 
```
conda activate \\luxapplp04\Share\Gruppo_Demand_Planning\02_NPI\BUDGET_INSERTION\EXCEL_TXT_INSERIMENTI\download_bgt\.condaw
```


2. Run `pyinstaller`

On **MacOS**
```
pyinstaller --noconsole --onedir --add-data "script/config.yaml:." --add-data "script/core:core" --add-data "script/gui:gui" --add-data "script/utils:utils" --hidden-import openpyxl.cell._writer --name "download_bgt_from_sharepoint" --workpath macos/build --distpath macos/dist script/main.py
```

On **Windows**
```
 pyinstaller --noconsole --onedir --add-data "script\config.yaml;." --add-data "script\core;core" --add-data "script\gui;gui" --add-data "script\utils;utils" --hidden-import openpyxl.cell._writer --name "download_bgt_from_sharepoint" --workpath windows\build --distpath windows\dist script\main.py 
```

## Project Structure

```yaml
download_bgt/
│
├── script/
│   ├── core/
│   │   ├── config_loader.py       # Handles configuration loading.
│   │   ├── sharepoint.py          # Resolves SharePoint paths.
│   │
│   ├── gui/
│   │   ├── components.py          # Contains reusable GUI components like checkboxes.
|   |   ├── app.py                 # Main GUI.
│   │
│   ├── utils/
│   │   ├── tools.py               # Utility functions for file processing.
│   │   ├── constants.py           # OS and user-related constants.
│   │
│   ├── __pycache__/               # Compiled Python files.
│   │
│   ├── main.py                    # Entry point for the application.
│
├── config.yaml                    # Configuration file for patterns and paths.
├── README.md                      # Project documentation (this file).
```


## License

This project is licensed under the MIT License.
