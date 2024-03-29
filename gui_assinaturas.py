import csv
from operator import mod
import pathlib
import subprocess
import os
import yaml
from cgitb import text
import PySimpleGUI as sg
from src.Assinatura import Assinatura

# CONSTANTS AND GLOBALS
QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEY2 = 'special 16777221'
FONT_MTSERRAT = 'resources/fonts/Montserrat/Montserrat-Regular.ttf 11'
FONT_GRANDSTANDER = 'resources/fonts/Grandstander/Grandstander-Black.ttf 15 bold'
PROJECT_PATH = pathlib.Path(__file__).parent.resolve()
THEME_MENU = [
    # original theme names: 'DarkBlue4', 'DarkBlue14', 'DarkGrey10', 'DarkTeal12', 'random'
    'menu', ['Roxo Claro', 'Azul Escuro', 'Escuro', 'Padrão', 'Aleatório']
]

def confirmation_mass_gen():
    layout = [
        [sg.Text('Tem certeza que deseja gerar assinaturaws em massa?')],
        [
            sg.Button('Confirmar', size=(10, 1), key='-CONFIRMAR_MASSA-'),
            sg.Button('Cancelar', size=(10, 1), key='-CANCELAR_MASSA-')
        ]
    ]

    window = sg.Window('Geração em massa de assinaturas', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-CANCELAR_MASSA-'):
            break
        if event == '-CONFIRMAR_MASSA-':
            print("Gerando x assinaturas em massa.")
    window.close()

def create_main_window(theme):
    sg.theme(theme)
    sg.set_options(
        font = FONT_MTSERRAT,
        element_padding=(0, 0)
        #button_color=('Blue', 'White')
    )
    # Right Click Menu layout
    rc_menu = ['RightClickMenu', ['Tema', THEME_MENU[1], 'Versão']]

    # main layout
    layout = [
        [ # no default title bar, this is the custom one
            sg.Text('Assinaturas', font=FONT_GRANDSTANDER, pad=((10, 0), (0, 0))),
            sg.Push(),
            # sg.Image(
            #     'resources/img/cross_16px.png',
            #     enable_events=True,
            #     key = '-CLOSE-',
            # )
            sg.Image(source='resources/img/logo.png', subsample=14, pad=((0, 20), (1, 5)))
        ],
        [sg.HorizontalSeparator(pad=((0, 0), (0, 10)))],
        [
            sg.Text('Nome *'),
            sg.Push(),
            sg.Input(size=(32, 1), pad=((0, 0), (0, 5)), key='-NOME-')
        ],
        [
            sg.Text('Setor/Cargo *'),
            sg.Push(),
            sg.Input(size=(32, 1),pad=((0, 0), (0, 5)), key='-SETOR-')
        ],
        [
            sg.Text('Telefone particular'),
            sg.Push(),
            sg.Input(size=(32, 1), pad=((0, 0), (0, 5)),key='-TELEFONE1-',
                tooltip="Opcional, se ficar em branco será selecionado a assinatura com apenas 1 ícone de telefone.")
        ],
        [
            sg.Text('Telefone secundário'),
            sg.Push(),
            sg.Input(size=(32, 1), pad=((0, 0), (0, 5)), key='-TELEFONE2-',
                tooltip="Opcional, caso fique vazio será usado o número da empresa automaticamente.")
        ],
        [
            sg.Text('Email *'),
            sg.Push(),
            sg.Input(size=(32, 1), pad=((0, 0), (0, 5)),
            key='-EMAIL-')
        ],
        [
            sg.Button('Gerar nova assinatura', size=(22, 1), key='-GERAR-', pad=(0, 5)),
            sg.Push(),
            sg.Button('Gerar assinaturas em massa', size=(22, 1), key='-GERAR_MASSA-')
        ]
    ]

    return sg.Window(
        title='Assinaturas',
        layout=layout,
        return_keyboard_events=True,
        grab_anywhere=True,
        right_click_menu=rc_menu,
        icon='resources\img/assinatura_64px.ico'
        #no_titlebar = True,
    )

def main_app():

    with open('src/theme.yml') as theme_file:
        theme = yaml.load(theme_file, Loader=yaml.FullLoader) 

    window = create_main_window(theme['theme'])

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-CLOSE-'):
            break

        if event in THEME_MENU[1]:
            if event == 'Roxo Claro': event = 'DarkBlue4'
            elif event == 'Azul Escuro': event = 'DarkBlue14'
            elif event == 'Escuro': event = 'DarkGrey10'
            elif event == 'Padrão': event = 'DarkTeal12'
            elif event == 'Aleatório': event = 'random'
            with open('src/theme.yml', 'w') as theme_file:
                if event == 'random':
                    yaml.dump({'theme': 'DarkTeal12'}, theme_file) # quando selecionar um aleatório, não guardar como padrão
                else:
                    yaml.dump({'theme': event}, theme_file)
            window.close()
            window = create_main_window(event)

        if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2): # Check for ENTER key
            elem = window.find_element_with_focus()
            if elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON: # if it's a button element, click it
                print(f"Found {elem.Type}")
                elem.Click()

        # process menu choices
        if event == 'Versão':
            window.disappear()
            sg.popup(
                f'Versão 1.0\nPrograma grátis!\nMas caso queira ajudar o\nprogramador com qualquer valor:\npix@lucasrochaabraao.com.br\nLucas Rocha Abraão',
                title = 'Assinaturas',
                font = FONT_MTSERRAT,
                auto_close=True,
                auto_close_duration=10,
                grab_anywhere=True,
                no_titlebar=True,
            )
            window.reappear()

        elif event == 'Properties':
            confirmation_mass_gen()

        # check for buttons that have been clicked
        elif event == '-GERAR-':
            # Se for repetido, vai funcionar até 3 assinaturas. Eventualmente vou fazer uma checagem na hora de criar.
            nome = values['-NOME-']
            setor = values['-SETOR-']
            telefone1 = values['-TELEFONE1-']
            telefone2 = values['-TELEFONE2-']
            email = values['-EMAIL-']
            assinatura = Assinatura(nome, setor, [telefone1, telefone2], email)
            print(f'Validando a assinatura: {assinatura}')
            if not validar_persistencia(assinatura):
                assinatura.gerar()
            else:
                window.disappear()
                sg.popup(
                    f'Essa assinatura já existe!',
                    title = 'Assinaturas',
                    font = FONT_MTSERRAT,
                    auto_close=True,
                    auto_close_duration=3,
                    grab_anywhere=True,
                    no_titlebar=True
                )
            window.reappear()
            ## abrir file explorer where the signature was generated
            subprocess.Popen(f'explorer {PROJECT_PATH}\\assinaturas_personalizadas')

        elif event == '-GERAR_MASSA-':
            delete_current_signatures() # por enquanto é necessário deletar todas assinaturas. Eventualmente vou fazer uma checagem na hora de criar.
            create_signature_mass()
            print('Gerando assinaturas em massa')
            subprocess.Popen(f'explorer {PROJECT_PATH}\\assinaturas_personalizadas')

    window.close()

def validar_persistencia(assinatura):
    """ essa função garante que cada assinatura criada individualmente
        também é inserida no arquivo elenco.csv, caso já não esteja."""
    with open(file='elenco.csv', encoding='utf-8', mode='r') as csvfile:
        reader_colaboradores = csv.DictReader(csvfile)
        for colaborador in reader_colaboradores: # valida a assinatura nova contra cada item do csv
            if colaborador['NOME'] == assinatura.nome and\
                colaborador['SETOR/CARGO'] == assinatura.setor and\
                [colaborador['TELEFONE 1'], colaborador['TELEFONE 2']] == [assinatura.telefone_particular, assinatura.telefone_secundario] and\
                colaborador['EMAIL'] == assinatura.email:
                    return True # retorna verdadeiro caso já existe no elenco.csv
    # se não retornou verdadeiro acima, precisamos inserir no elenco.csv para
    # persistência (no caso de gerar em massa). Obs: garanta que o arquivo csv
    # tenha a última linha em branco sempre.
    with open(file='elenco.csv', mode='a', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['NOME', 'SETOR/CARGO', 'TELEFONE 1', 'TELEFONE 2', 'EMAIL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'NOME': assinatura.nome,
            'SETOR/CARGO': assinatura.setor,
            'TELEFONE 1': assinatura.telefone_particular,
            'TELEFONE 2': assinatura.telefone_secundario,
            'EMAIL': assinatura.email
        })
    return False # já que precisa gerar a imagem da assinatura também.

def delete_current_signatures():
    for file in os.scandir('assinaturas_personalizadas'):
        os.remove(file.path)
    open('assinaturas_personalizadas/.gitkeep', 'a').close() # importante para manter o versionamento do git quando não tiver nada aqui

def create_signature_mass():
    with open(file='elenco.csv', encoding='utf-8') as csvfile:
        reader_colaboradores = csv.DictReader(csvfile)
        for colaborador in reader_colaboradores:
            nome = colaborador['NOME']
            setor = colaborador['SETOR/CARGO']
            telefone = [colaborador['TELEFONE 1'], colaborador['TELEFONE 2']]
            email = colaborador['EMAIL']
            assinatura = Assinatura(nome, setor, telefone, email)
            print(assinatura)
            assinatura.gerar()

if __name__ == '__main__':
    main_app()
