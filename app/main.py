import subprocess
import yaml
import PySimpleGUI as sg
from assinacraft.src.signature import Signature


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
            signature = Signature(nome, setor, [telefone1, telefone2], email)
            print(f'Validating signature: {signature}')
            if not validar_persistencia(signature):
                signature.gerar()
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


if __name__ == '__main__':
    main_app()
