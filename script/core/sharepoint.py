from pathlib import Path
from utils.constants import OS, USER, MAC_OS, WINDOWS_OS

class SharePointPathResolver:
    def __init__(self):
        self.path = self._resolve_path()

    def _resolve_path(self) -> Path:
        base_path = None
        if OS == MAC_OS:
            base_path = Path(fr"/Users/{USER}/Library/CloudStorage/OneDrive-Raccoltecondivise-LuxotticaGroupS.p.A")
        elif OS == WINDOWS_OS:
            base_path = Path(fr"C:\Users\{USER}\Luxottica Group S.p.A")
        else:
            raise NotImplementedError("Unsupported OS: Only MacOS and Windows are supported.")

        # Check for either 'Documents' or 'Documenti'
        for folder_name in ["NPI Demand Planning - Documents", "NPI Demand Planning - Documenti"]:
            potential_path = base_path / folder_name
            if potential_path.exists():
                return potential_path

        # Raise an error if neither folder exists
        raise FileNotFoundError("Neither 'Documents' nor 'Documenti' found in the expected location.")