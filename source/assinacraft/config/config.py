import os
import shutil
from dataclasses import dataclass
from pathlib import Path
import pkg_resources
import yaml


@dataclass()
class Config:
    # Config path in user's documents directory, which we will use
    config_dir = Path(os.path.expanduser('~/Documents/assinacraft'))

    __config_file = 'config/config.yml'
    fullpath_config_file = str(config_dir / __config_file)

    # Default config file path, in case the user has removed from user directory.
    # Note this comes from the packaged app
    __default_config_file = pkg_resources.resource_filename(__name__, 'config.yml')

    def __init__(self):
        if not os.path.exists(self.config_dir):
            # make sure the config dir exists
            os.makedirs(os.path.dirname(self.config_dir), exist_ok=True)

        if not os.path.exists(self.fullpath_config_file):
            # Copy default config file
            os.makedirs(self.config_dir / 'config', exist_ok=True)
            shutil.copy(self.__default_config_file, self.fullpath_config_file)

        with open(self.__config_file, 'r') as file:
            config: dict = yaml.load(file, Loader=yaml.FullLoader)

        self.config = config


@dataclass()
class AppConfig(Config):
    def __init__(self):
        super().__init__()
        self.window_size = self.config['app']['window_size']
        self.title = self.config['app']['title']
        self.icon = self.config['app']['icon']
        self.signatures_csv = self.config['app']['signatures_csv']
        self.output_dir = self.config['app']['output_dir']
        self.key_codes = self.config['app']['key_codes']


@dataclass()
class GUIConfig(Config):
    def __init__(self):
        super().__init__()
        font_primary = pkg_resources.resource_filename(
            'assinacraft', f"resources/fonts/{self.config['gui']['font_primary']}"
        )
        font_secondary = pkg_resources.resource_filename(
            'assinacraft', f"resources/fonts/{self.config['gui']['font_secondary']}"
        )
        self.font_primary = font_primary
        self.font_primary_size = self.config['gui']['font_primary_size']
        self.font_primary_attr = self.config['gui']['font_primary_attr']
        self.font_secondary = font_secondary
        self.font_secondary_size = self.config['gui']['font_secondary_size']
        self.font_secondary_attr = self.config['gui']['font_secondary_attr']
        self.theme = self.config['gui']['theme']


@dataclass()
class SignatureConfig(Config):
    def __init__(self):
        super().__init__()
        self.default_optional_tel = self.config['signature']['default_optional_tel']
        self.primary_signature_img_template = self.config['signature']['primary_signature_img_template']
        self.secondary_signature_img_template = self.config['signature']['secondary_signature_img_template']
        self.enable_all_caps = self.config['signature']['enable_all_caps']
        self.output_dir = self.config['signature']['output_dir']

        name_font = pkg_resources.resource_filename(
            'assinacraft', f"resources/fonts/{self.config['signature']['name_font']}"
        )
        self.name_font = name_font
        self.name_font_size = self.config['signature']['name_font_size']
        self.name_font_color = self.config['signature']['name_font_color']
        self.name_xy_coords = self.config['signature']['name_xy_coords']

        department_font = pkg_resources.resource_filename(
            'assinacraft', f"resources/fonts/{self.config['signature']['department_font']}"
        )
        self.department_font = department_font
        self.department_font_size = self.config['signature']['department_font_size']
        self.department_font_color = self.config['signature']['department_font_color']
        self.department_xy_coords = self.config['signature']['department_xy_coords']

        tel_font = pkg_resources.resource_filename(
            'assinacraft', f"resources/fonts/{self.config['signature']['tel_font']}"
        )
        self.tel_font = tel_font
        self.tel_font_size = self.config['signature']['tel_font_size']
        self.tel_font_color = self.config['signature']['tel_font_color']
        self.tel_xy_coords_personal = self.config['signature']['tel_xy_coords_personal']
        self.tel_xy_coords_company = self.config['signature']['tel_xy_coords_company']

        email_font = pkg_resources.resource_filename(
            'assinacraft', f"resources/fonts/{self.config['signature']['email_font']}"
        )
        self.email_font = email_font
        self.email_font_size = self.config['signature']['email_font_size']
        self.email_font_color = self.config['signature']['email_font_color']
        self.email_xy_coords = self.config['signature']['email_xy_coords']
