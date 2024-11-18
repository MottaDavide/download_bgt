import yaml
from pathlib import Path

class ConfigLoader:
    def __init__(self, config_path: str | Path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
            
    def get(self, key: str):
        return self.config.get(key)