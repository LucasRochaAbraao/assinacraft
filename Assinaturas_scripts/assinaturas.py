from PIL import Image
from PIL import ImageDraw 
from PIL import ImageFont

import desenhar

elenco = list()
with open('elenco.csv', 'r') as arq:
    for linha in arq:
        elenco.append(linha.strip('\n').split(','))

for assinatura in elenco:
    img = Image.open("resources/template.png")

    draw = ImageDraw.Draw(img)

    # font = ImageFont.truetype(<font-file>, <font-size>)
    font_nome = ImageFont.truetype("/home/lucas/Dev/Assinaturas/resources/fonts/darwin-pro-cufonfonts/Los Andes Type  Darwin Pro SemiBold.otf", 20)
    font_setor = ImageFont.truetype("/home/lucas/Dev/Assinaturas/resources/fonts/darwin-pro-cufonfonts/Los Andes Type  Darwin Pro Regular.otf", 13)
    font_telefone = ImageFont.truetype("/home/lucas/Dev/Assinaturas/resources/fonts/estandar/Estandar-Regular.ttf", 13)
    font_email = ImageFont.truetype("/home/lucas/Dev/Assinaturas/resources/fonts/estandar/Estandar-Regular.ttf", 13)

    desenhar.nome(draw, font_nome, assinatura[0])
    desenhar.setor(draw, font_setor, assinatura[1])
    if assinatura[3] == '':
        desenhar.telefone(draw, font_telefone, assinatura[2], 1)
    else:
        desenhar.telefone(draw, font_telefone, assinatura[2:4], 2)
    desenhar.email(draw, font_email, assinatura[4])

    img.save(f'assinaturas_personalizadas/assn_{assinatura[0]}.png')
