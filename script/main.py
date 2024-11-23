# Standard imports
from pathlib import Path
import openpyxl

# Local Imports
from core.config_loader import ConfigLoader
from core.sharepoint import SharePointPathResolver
from core.release_manager import ReleaseManager
from gui.app import App


if __name__ == "__main__":
    # Load config
    config = ConfigLoader(config_path=Path(__file__).parents[0] / "config.yaml")
    
    # Resolve SharePoint path
    resolver = SharePointPathResolver()
    
    # Get available releases
    release_manager = ReleaseManager(
        sharepoint_path=resolver.path,
        pattern=config.get("pattern release")
    )
    available_releases = release_manager.get_available_releases()
    
    # Launch the GUI
    app = App(releases=available_releases, config=config, sharepoint_path=resolver.path)
    app.mainloop()