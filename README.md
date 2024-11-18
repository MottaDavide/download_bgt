# Download Budget from Sharepoint

This project provides a graphical user interface (GUI) for managing the process of downloading, converting, and tagging budget files stored on a SharePoint server. Built using customtkinter, it streamlines workflows for handling budget-related tasks efficiently. In a nutshell, it permits to:

1. Download files from SharePoint
2. Put a tag on the very same file in the SharePoint to prevent future downloads.

![alt text](image.png)

## Features
Features

- **Release Selection**: Select specific releases from a list of available options.
- **File Download**: Download budget files from a SharePoint directory and convert them into the required format.
- **File Tagging**: Tag processed files with a custom label (e.g., “UPLOADED”).
- **Logging**: View real-time logs of the processes for better traceability.

## Project Structure
```
download_bgt/
│
├── script/
│   ├── core/
│   │   ├── config_loader.py       # Handles configuration loading.
│   │   ├── sharepoint.py          # Resolves SharePoint paths.
│   │
│   ├── gui/
│   │   ├── components.py          # Contains reusable GUI components like checkboxes.
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