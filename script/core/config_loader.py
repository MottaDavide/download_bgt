import yaml
from pathlib import Path
from utils.tools import get_resource_path

class ConfigLoader:
    def __init__(self, config_path: str | Path):
        self.config_path = get_resource_path(config_path)
        with open(self.config_path, 'r') as file:
            self.config = yaml.safe_load(file)
            
    def get(self, key: str):
        return self.config.get(key)