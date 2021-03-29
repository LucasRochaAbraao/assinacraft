DOURADO = (255,151,0)
BRANCO = (255, 255, 255)
AZUL = (0,102,183)
SOMBRA = (100, 100, 100)

def nome(draw, font, nome_texto):
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(xy=(418, 26), text=nome_texto, fill=DOURADO, font=font, align='right', anchor='ra')

def setor(draw, font, setor_texto):
    draw.text((418, 48), setor_texto, BRANCO, font=font, align='right', anchor='ra')

def telefone(draw, font, numero, quantidade):
    if quantidade == 1:
        draw.text(((418, 80)), numero, BRANCO, font=font, align='right', anchor='ra')
    elif quantidade == 2:
        draw.text(((340, 80)), numero[0], BRANCO, font=font, align='right', anchor='ra')
        draw.text(((418, 80)), numero[1], BRANCO, font=font, align='right', anchor='ra')

def email(draw, font, email_texto):
    draw.text(((418, 94)), email_texto, BRANCO, font=font, align='right', anchor='ra')
