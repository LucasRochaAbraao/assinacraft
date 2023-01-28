import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Signature:
    def __init__(self, name, department, tel, email):
        # Definindo cores das letras
        self.GOLDEN = (255,151,0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0,102,183)
        self.SHADOW = (100, 100, 100)

        self.name = name
        self.department = department
        self.tel_primary = tel[0]
        self.tel_secondary = tel[1]
        self.email = email
        if not self.tel_secondary:
            self.tel_secondary = '24 3344-2250' # TODO: read from config file
        if self.tel_primary: # loads the template with or without cellphone icon
            self.image = Image.open(f"resources/assinatura_template_low_res_2tel.jpg")
            self.draw = ImageDraw.Draw(self.image)
        else: # se o secundário tiver vazio, será usado o da empresa
            self.image = Image.open(f"resources/assinatura_template_low_res_1tel.jpg")
            self.draw = ImageDraw.Draw(self.image)

    def caps(self, target):
        result = list()
        for word in target.split():
            result.append(word.capitalize())
        return ' '.join(result)            
  
    def validate_name(self, nome):
        file_path = f'assinaturas_personalizadas/{nome}.png'
        file_path_ = f'assinaturas_personalizadas/{nome}_.png' # TODO: This is a hack for people with 2 signatures, need to rework this!
        if os.path.exists(file_path) or os.path.exists(file_path_):
            print("existe:", nome)
            if os.path.exists(file_path_):
                return f'assinaturas_personalizadas/{nome}__.png'
            return f'assinaturas_personalizadas/{nome}_.png'
        return file_path

    def generate(self):
        # name
        font = ImageFont.truetype("resources/fonts/darwin-pro-cufonfonts/Los Andes Type  Darwin Pro SemiBold.otf", 21)
        self.draw.text(xy=(261, 42), text=self.caps(self.name), fill=self.GOLDEN, font=font, align='right', anchor='la')

        # department
        if len(self.department) > 20:
            font = ImageFont.truetype("resources/fonts/darwin-pro-cufonfonts/Los Andes Type  Darwin Pro Regular.otf", 13)
        else:
            font = ImageFont.truetype("resources/fonts/darwin-pro-cufonfonts/Los Andes Type  Darwin Pro Regular.otf", 14)
        self.draw.text((261, 67), text=self.caps(self.department), fill=self.WHITE, font=font, align='right', anchor='la')

        # tel
        font = ImageFont.truetype("resources/fonts/estandar/Estandar-Regular.ttf", 13)
        if self.tel_primary:
            self.draw.text(((281, 104)), self.tel_primary, self.WHITE, font=font, align='right', anchor='la')
        self.draw.text(((300, 127)), self.tel_secondary, self.WHITE, font=font, align='right', anchor='la')

        # email
        font = ImageFont.truetype("resources/fonts/estandar/Estandar-Regular.ttf", 14)
        self.draw.text(((261, 82)), self.email, self.WHITE, font=font, align='right', anchor='la')
        
        # filename = f'assinaturas_personalizadas/{name}'
        new_signature_filename = self.validate_name("_".join(self.name.split()))
            
        self.image.save(new_signature_filename)

    def __repr__(self): # for debugging through terminal
        if self.tel_primary:
            return f"{self.name} ({self.email}): {self.tel_primary} | {self.tel_secondary}"
        else:
            return f"{self.name} ({self.email}): {self.tel_secondary}"

