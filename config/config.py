import os
import shutil
from dataclasses import dataclass
import yaml

@dataclass
class Config:
    # Default config file path, in case the user has removed from user directory
    default_config_file = 'config/config.yml'

    # Config file path in user's documents directory, which we will use
    config_file = os.path.expanduser('~/Documents/assinacraft/assinacraft_config.yml')

    # App config options
    window_size: tuple
    window_title: str
    window_icon: str

    # GUI config options
    font: str
    icons: dict
    theme: str
    key_codes: dict


    def __post_init__(self):
        if not os.path.exists(self.config_file):
            # Copy default config file
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            shutil.copy(self.default_config_file, self.config_file)

        with open(self.config_file, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        self.window_size = config['window_size']
        self.window_title = config['window_title']
        self.window_icon = config['window_icon']
        self.font = config['font']
        self.icons = config['icons']
        self.theme = config['theme']
        self.key_codes = config['key_codes']
