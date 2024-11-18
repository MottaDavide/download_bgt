from pathlib import Path
from utils.constants import OS, USER, MAC_OS, WINDOWS_OS

class SharePointPathResolver:
    def __init__(self):
        self.path = self._resolve_path()

    def _resolve_path(self) -> Path:
        if OS == MAC_OS:
            return Path(fr"/Users/{USER}/Library/CloudStorage/OneDrive-Raccoltecondivise-LuxotticaGroupS.p.A/NPI Demand Planning - Documents")
        elif OS == WINDOWS_OS:
            return Path(fr"C:\Users\{USER}\Luxottica Group S.p.A\NPI Demand Planning - Documents")
        else:
            raise NotImplementedError("Unsupported OS: Only MacOS and Windows are supported.")