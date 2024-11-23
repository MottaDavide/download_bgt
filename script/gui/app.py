
# Standard Libs
from pathlib import Path
import customtkinter
import sys

# Local Imports
from gui.components import MyCheckboxFrame
from core.config_loader import ConfigLoader
from utils.tools import find_and_convert_files, put_tag

class App(customtkinter.CTk):
    """
    Main application class for managing the SharePoint budget process via a GUI.

    This application provides functionality for:
    - Downloading and converting budget files for selected releases.
    - Tagging processed budget files with a custom label ("UPLOADED").

    Attributes:
        releases (list[str]): List of release names available for processing.
        config (ConfigLoader): Configuration loader instance containing file patterns, regions, and folder paths.
        sharepoint_path (Path): Path to the SharePoint directory containing budget files.
        checkbox_frame (MyCheckboxFrame): UI component for selecting releases via checkboxes.
        log_textbox (customtkinter.CTkTextbox): UI component for displaying logs and messages.
        download_button (customtkinter.CTkButton): Button to trigger the download process.
        tag_button (customtkinter.CTkButton): Button to trigger the tagging process.
    """
    def __init__(self, releases: list[str], config: ConfigLoader, sharepoint_path:  str | Path):
        """
        Initialize the App instance and set up the GUI components.

        Args:
            releases (list[str]): List of release names to populate the checkbox frame.
            config (ConfigLoader): Configuration loader containing settings and parameters for the process.
            sharepoint_path (str | Path): Path to the SharePoint directory containing the budget files.
        """
        super().__init__()
        self.releases = releases
        self.config = config
        self.sharepoint_path = sharepoint_path

        self.title("Download Budget From SharePoint")
        self.geometry("600x650")
        self._configure_layout()

        self.checkbox_frame = MyCheckboxFrame(self, values=self.releases, title="Release")
        self.checkbox_frame.grid(row=0, column=0, padx=15, pady=(10, 0), sticky="nsew")

        self.log_textbox = customtkinter.CTkTextbox(self, height=10)
        self.log_textbox.grid(row=0, column=1, padx=15, pady=(10, 0), sticky="nsew")

        self.download_button = customtkinter.CTkButton(
            self, text="Download", command=self._handle_download, fg_color="#39597B"
        )
        self.download_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.tag_button = customtkinter.CTkButton(
            self, text="Put 'UPLOADED'", command=self._handle_put_tag, fg_color="#39597B"
        )
        self.tag_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def _configure_layout(self):
        """
        Configure the layout of the main application window.

        This method defines a grid-based layout with two columns:
        - Column 0: Holds the checkbox frame for release selection.
        - Column 1: Holds the log text box for displaying messages.
        """
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

    def _create_widgets(self):
        """
        Create and position the GUI widgets.

        This method initializes:
        - A checkbox frame for selecting releases.
        - A log text box for displaying logs and messages.
        - Buttons for triggering the download and tagging processes.
        """
        # Checkbox frame for releases
        self.checkbox_frame = MyCheckboxFrame(self, values=self.releases, title="Release")
        self.checkbox_frame.grid(row=0, column=0, padx=15, pady=(10, 0), sticky="nsew")

        # Log text box
        self.log_textbox = customtkinter.CTkTextbox(self, height=10)
        self.log_textbox.grid(row=0, column=1, padx=15, pady=(10, 0), sticky="nsew")

        # Download button
        self.download_button = customtkinter.CTkButton(
            self, text="Download", command=self._handle_download, fg_color="#39597B"
        )
        self.download_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Tagging button
        self.tag_button = customtkinter.CTkButton(
            self, text="Put 'UPLOADED'", command=self._handle_put_tag, fg_color="#39597B"
        )
        self.tag_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")       

    def log_message(self, message: str):
        """
        Append a log message to the log text box.

        Args:
            message (str): The message to be logged.
        """
        self.log_textbox.insert("end", f"{message}\n")
        self.log_textbox.see("end")  # Scroll to the end

    def clear_log(self):
        """
        Clear all messages from the log text box.
        """
        self.log_textbox.delete("1.0", "end")
        

    def _get_save_path(self, release: str) -> Path:
        """
        Construct the save path for a given release.

        Args:
            release (str): The name of the release.

        Returns:
            Path: The computed save path based on the release name.
        """
        year = release[-4:]  # Extract the year from the release name
        if getattr(sys, 'frozen', False):
            return Path(__file__).parents[6] / year / release
        else:
            return Path(__file__).parents[3] / year / release
    
    def _process_releases(self, process_func, process_name: str):
        """
        Generalized method to process selected releases.

        This method handles common tasks such as:
        - Clearing the log box.
        - Iterating through selected releases.
        - Logging the start and end of the process.

        Args:
            process_func (callable): The function to apply to each release.
                It must accept two arguments: `release` (str) and `save_path` (Path).
            process_name (str): A descriptive name for the process (e.g., "download", "label").
        """
        self.clear_log()
        releases = self.checkbox_frame.get()
        for release in releases:
            save_path = self._get_save_path(release)
            self.log_message(f"Starting {process_name} process for release: {release}")
            process_func(release, save_path)
        self.log_message(f"{process_name.capitalize()} process completed.\n\n")
        

    def _handle_download(self):
        """
        Handle the download process for selected releases.

        This method uses the `_process_releases` method to:
        - Download files for each selected release.
        - Convert the downloaded files into the required format.
        """
        def download_process(release, save_path):
            find_and_convert_files(
                release=release,
                pattern=self.config.get('pattern file'),
                search_path=self.sharepoint_path,
                regions=self.config.get('regions'),
                budget_definition_folder=self.config.get('budget_folder'),
                save_path=save_path,
                log_func=self.log_message
            )

        self._process_releases(download_process, "download")

    def _handle_put_tag(self):
        """
        Handle the tagging process for selected releases.

        This method uses the `_process_releases` method to:
        - Apply a custom tag (e.g., "UPLOADED") to each selected release.
        """
        def tag_process(release, save_path):
            put_tag(
                release=release,
                pattern=self.config.get('pattern file'),
                search_path=save_path,
                sharepoint_path=self.sharepoint_path,
                regions=self.config.get('regions'),
                budget_definition_folder=self.config.get('budget_folder'),
                tag='UPLOADED',
                log_func=self.log_message
            )

        self._process_releases(tag_process, "label")