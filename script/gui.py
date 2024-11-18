import customtkinter
import yaml
from pathlib import Path
import re
import datetime


# Local import
from utils.constant import OS, USER, MAC_OS, WINDOWS_OS
from utils.tools import find_and_convert_files, put_tag

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


customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")


class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values, title):
        super().__init__(master)
        self.values = values
        self.checkboxes = []
        self.title = title

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="#39597B", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        
        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(15,0), sticky="ew")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


## ALL IN CLASS
class App(customtkinter.CTk):
    def __init__(self, values):
        super().__init__()
        self.values = values

        self.title("Download Budget From Sharepoint")
        self.geometry("600x550")  # Adjusted width to fit both columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  # Added second column
        self.grid_rowconfigure(0, weight=1)  # Row for expanding checkboxes and log
        self.grid_rowconfigure(1, weight=0)  # Row for the button at the bottom
        self.grid_rowconfigure(2, weight=0)  # Row for the button at the bottom

        # Checkbox Frame for Release selection on the left
        self.checkbox_frame_1 = MyCheckboxFrame(master=self, values=self.values, title="Release")
        self.checkbox_frame_1.grid(row=0, column=0, padx=15, pady=(10,0), sticky="nsew")

        # Log Textbox for displaying logs on the right
        self.log_textbox = customtkinter.CTkTextbox(self, height=10)
        self.log_textbox.grid(row=0, column=1, padx=15, pady=(10,0), sticky="nsew")

        # Download button positioned below the checkbox and log box, spanning both columns
        self.button1 = customtkinter.CTkButton(self, text="Download", command=self.button_callback, fg_color='#39597B')
        self.button1.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Download button positioned below the checkbox and log box, spanning both columns
        self.button2 = customtkinter.CTkButton(self, text="Put 'UPLOADED'", command=self.button_tag, fg_color='#39597B')
        self.button2.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def log_message(self, message):
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")  # Scroll to the end

    def clear_log(self):
        """Clears the log textbox."""
        self.log_textbox.delete("1.0", "end")

    def button_callback(self):
        self.clear_log()
        releases = self.checkbox_frame_1.get()
        
        for release in releases:
            year = release[-4:]
            save_path = Path(__file__).parents[2] / year / release
            
            self.log_message(f"Starting download for release: {release}")

            # Pass self.log_message as log_func to find_and_convert_files
            dataframes, errors = find_and_convert_files(
                release=release, 
                pattern=config['pattern file'], 
                search_path=sharepoint_path, 
                regions=config['regions'], 
                budget_definition_folder=config['budget_folder'],
                save_path=save_path,
                log_func=self.log_message  # Redirect logs to the GUI
            )
        self.log_message("End of process\n\n")
        
    
    def button_tag(self):
        self.clear_log()
        releases = self.checkbox_frame_1.get()
        for release in releases:
            year = release[-4:]
            save_path = Path(__file__).parents[2] / year / release
            
            self.log_message(f"Starting labelling process for release: {release}")
            
        put_tag(release= release,
                    pattern= config['pattern file'], 
                    search_path=save_path, 
                    sharepoint_path=sharepoint_path,
                    regions=config['regions'], 
                    budget_definition_folder=config['budget_folder'],
                    tag='UPLOADED',
                    log_func=self.log_message
                    )

app = App(values=available_release)
app.mainloop()
