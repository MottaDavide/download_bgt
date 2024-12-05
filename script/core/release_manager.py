import re
from pathlib import Path

class ReleaseManager:
    def __init__(self, sharepoint_path: Path, pattern: str):
        self.sharepoint_path = sharepoint_path
        self.pattern = pattern

    def get_available_releases(self):
        budget_path = self.sharepoint_path / "USA/BUDGET DEFINITION"
        return [
            entry.name for entry in budget_path.iterdir()
            if entry.is_dir() and re.compile(self.pattern).match(entry.name)
        ]