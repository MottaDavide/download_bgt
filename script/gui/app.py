
# Standard Libs
from pathlib import Path
import customtkinter

# Local Imports
from gui.components import MyCheckboxFrame
from core.config_loader import ConfigLoader
from utils.tools import find_and_convert_files, put_tag

class App(customtkinter.CTk):
    def __init__(self, releases: list[str], config: ConfigLoader, sharepoint_path:  str | Path):
        super().__init__()
        self.releases = releases
        self.config = config
        self.sharepoint_path = sharepoint_path

        self.title("Download Budget From SharePoint")
        self.geometry("600x550")
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
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        
    def log_message(self, message):
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")  # Scroll to the end

    def clear_log(self):
        """Clears the log textbox."""
        self.log_textbox.delete("1.0", "end")
        

    def _handle_download(self):
        for release in self.releases:
            year = release[-4:]
            save_path = Path(__file__).parents[2] / year / release
        
            self.log_message(f"Starting download for release: {release}")
            
            dataframes, errors = find_and_convert_files(
                release=release, 
                pattern=self.config.get('pattern file'), 
                search_path=self.sharepoint_path, 
                regions=self.config.get('regions'), 
                budget_definition_folder=self.config.get('budget_folder'),
                save_path=save_path,
                log_func=self.log_message 
            )
            self.log_message("End of process\n\n")

    def _handle_put_tag(self):
        self.clear_log()
        releases = self.checkbox_frame.get()
        for release in releases:
            year = release[-4:]
            save_path = Path(__file__).parents[2] / year / release
            
            self.log_message(f"Starting labelling process for release: {release}")
            
            put_tag(
                release= release,
                pattern= self.config.get('pattern file'), 
                search_path=save_path, 
                sharepoint_path=self.sharepoint_path,
                regions=self.config.get('regions'), 
                budget_definition_folder=self.config.get('budget_folder'),
                tag='UPLOADED',
                log_func=self.log_message
                )