import os
import string

from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from assinacraft.config import SignatureConfig


class Signature:
    def __init__(self, name: str, department: str, tel: list[str], email: str):

        self.config = SignatureConfig()

        self.name = name
        self.department = department
        self.phone_personal = tel[0]
        self.phone_company = tel[1]
        self.email = email
        if not self.phone_company:
            self.phone_company = self.config.default_optional_tel
        if self.phone_personal:  # loads the template with or without cellphone icon
            self.image = Image.open(f"resources/{self.config.secondary_signature_img_template}")
            self.draw = ImageDraw.Draw(self.image)
        else:  # there are two phone options, so loading appropriate template
            self.image = Image.open(f"resources/{self.config.primary_signature_img_template}")
            self.draw = ImageDraw.Draw(self.image)

    @staticmethod
    def caps(enable_caps: bool, target: str) -> str:
        if not enable_caps:
            return target

        result = list()
        for word in target.split():
            result.append(word.capitalize())
        return ' '.join(result)

    @staticmethod
    def validate_name(name: string) -> Path:
        # TODO: Below is a hack for people with 2 signatures, need to rework this!
        file_path = f'assinaturas_personalizadas/{name}.png'
        file_path_ = f'assinaturas_personalizadas/{name}_.png'
        if os.path.exists(file_path) or os.path.exists(file_path_):
            print("existe:", name)
            if os.path.exists(file_path_):
                return Path(f'assinaturas_personalizadas/{name}__.png')
            return Path(f'assinaturas_personalizadas/{name}_.png')
        return Path(file_path)

    def generate(self) -> None:
        caps = self.config.enable_all_caps

        # name
        font = ImageFont.truetype(self.config.name_font, self.config.name_font_size)
        self.draw.text(
            xy=self.config.name_xy_coords,
            text=self.caps(caps, self.name),
            fill=self.config.name_font_color,
            font=font, align='right', anchor='la')

        # department
        if len(self.department) > 20:
            font = ImageFont.truetype(self.config.department_font, int(self.config.department_font_size) - 1)
        else:
            font = ImageFont.truetype(self.config.department_font, int(self.config.department_font_size))
        self.draw.text(
            xy=self.config.department_xy_coords,
            text=self.caps(caps, self.department),
            fill=self.config.department_font_color,
            font=font, align='right', anchor='la')

        # tel
        font = ImageFont.truetype(self.config.tel_font, self.config.tel_font_size)
        if self.phone_personal:
            self.draw.text(
                xy=self.config.tel_xy_coords_personal,
                text=self.phone_personal,
                fill=self.config.tel_font_color,
                font=font, align='right', anchor='la')
        self.draw.text(
            xy=self.config.tel_xy_coords_company,
            text=self.phone_company,
            fill=self.config.tel_font_color,
            font=font, align='right', anchor='la')

        # email
        font = ImageFont.truetype(self.config.email_font, self.config.email_font_size)
        self.draw.text(
            xy=self.config.email_xy_coords,
            text=self.email,
            fill=self.config.email_font_color,
            font=font, align='right', anchor='la')
        
        # filename = f'assinaturas_personalizadas/{name}'
        new_signature_filename = self.validate_name("_".join(self.name.split()))
            
        self.image.save(Path(self.config.output_dir) / new_signature_filename)

    def __repr__(self):  # for debugging through terminal
        if self.phone_personal:
            return f"{self.name} ({self.email}): {self.phone_personal} | {self.phone_company}"
        else:
            return f"{self.name} ({self.email}): {self.phone_company}"

