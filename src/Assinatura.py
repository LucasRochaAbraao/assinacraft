import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Assinatura:
    def __init__(self, nome, setor, telefone, email):
        # Definindo cores das letras
        self.DOURADO = (255,151,0)
        self.BRANCO = (255, 255, 255)
        self.AZUL = (0,102,183)
        self.SOMBRA = (100, 100, 100)

        self.nome = nome
        self.setor = setor
        self.telefone_celular = telefone[0]
        self.telefone_fixo = telefone[1]
        self.email = email
        if self.telefone_celular: # carregar o template com ou sem ícone de celular
            self.image = Image.open(f"resources/assinatura_template_low_res_2tel.jpg")
            self.draw = ImageDraw.Draw(self.image)
        else:
            self.image = Image.open(f"resources/assinatura_template_low_res_1tel.jpg")
            self.draw = ImageDraw.Draw(self.image)

    def caps(self, alvo):
        resultado = list()
        for palavra in alvo.split():
            resultado.append(palavra.capitalize())
        return ' '.join(resultado)            
  
    def validar_nome(self, nome):
        arquivo_path = f'/home/lucas/Dev/Assinatura-gen/Assinaturas_scripts/assinaturas_personalizadas/{nome}.png'
        arquivo_path_ = f'/home/lucas/Dev/Assinatura-gen/Assinaturas_scripts/assinaturas_personalizadas/{nome}_.png'
        if os.path.exists(arquivo_path) or os.path.exists(arquivo_path_):
            print("existe:", nome)
            if os.path.exists(arquivo_path_):
                return f'/home/lucas/Dev/Assinatura-gen/Assinaturas_scripts/assinaturas_personalizadas/{nome}__.png'
            return f'/home/lucas/Dev/Assinatura-gen/Assinaturas_scripts/assinaturas_personalizadas/{nome}_.png'
        return arquivo_path


    def gravar(self):
        # nome
        font = ImageFont.truetype("/home/lucas/Dev/Assinatura-gen/Assinaturas_scripts/resources/fonts/darwin-pro-cufonfonts/Los Andes Type  Darwin Pro SemiBold.otf", 21)
        self.draw.text(xy=(261, 42), text=self.caps(self.nome), fill=self.DOURADO, font=font, align='right', anchor='la')

        # setor
        if len(self.setor) > 20:
            font = ImageFont.truetype("/home/lucas/Dev/Assinatura-gen/Assinaturas_scripts/resources/fonts/darwin-pro-cufonfonts/Los Andes Type  Darwin Pro Regular.otf", 13)
        else:
            font = ImageFont.truetype("/home/lucas/Dev/Assinatura-gen/Assinaturas_scripts/resources/fonts/darwin-pro-cufonfonts/Los Andes Type  Darwin Pro Regular.otf", 14)
        self.draw.text((261, 67), text=self.caps(self.setor), fill=self.BRANCO, font=font, align='right', anchor='la')

        # telefone
        font = ImageFont.truetype("/home/lucas/Dev/Assinatura-gen/Assinaturas_scripts/resources/fonts/estandar/Estandar-Regular.ttf", 13)
        if self.telefone_celular: # se tem um número de celular
            self.draw.text(((281, 104)), self.telefone_celular, self.BRANCO, font=font, align='right', anchor='la')
            self.draw.text(((300, 127)), self.telefone_fixo, self.BRANCO, font=font, align='right', anchor='la')
        else:
            self.draw.text(((300, 127)), self.telefone_fixo, self.BRANCO, font=font, align='right', anchor='la')

        # email
        font = ImageFont.truetype("/home/lucas/Dev/Assinatura-gen/Assinaturas_scripts/resources/fonts/estandar/Estandar-Regular.ttf", 14)
        self.draw.text(((261, 82)), self.email, self.BRANCO, font=font, align='right', anchor='la')
        
        #nome_arquivo = f'/home/lucas/Dev/Assinatura-gen/Assinaturas_scripts/assinaturas_personalizadas/{nome}'
        nome_arquivo = self.validar_nome("_".join(self.nome.split()))
            
        self.image.save(nome_arquivo)

    def __repr__(self): # para testes no terminal
        if self.telefone_celular:
            return f"{self.nome} ({self.email}): {self.telefone_celular} | {self.telefone_fixo}"
        else:
            return f"{self.nome} ({self.email}): {self.telefone_fixo}"

