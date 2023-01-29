import csv
import subprocess
import yaml
from pathlib import Path
import os
import PySimpleGUI as sg
import pkg_resources
from assinacraft.app.signature import Signature
from assinacraft.config import GUIConfig, AppConfig

gui_config = GUIConfig()
theme_menu = [
    # original theme names: 'DarkBlue4', 'DarkBlue14', 'DarkGrey10', 'DarkTeal12', 'random'
    'menu', ['Roxo Claro', 'Azul Escuro', 'Escuro', 'Padrão', 'Aleatório']
]


class GUI:
    app_config = AppConfig()
    gui_config = GUIConfig()

    @classmethod
    def main_gui(cls):

        window = cls.create_main_window(cls.gui_config.theme)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, '-CLOSE-'):
                break

            if event in theme_menu[1]:
                if event == 'Roxo Claro':
                    event = 'DarkBlue4'
                elif event == 'Azul Escuro':
                    event = 'DarkBlue14'
                elif event == 'Escuro':
                    event = 'DarkGrey10'
                elif event == 'Padrão':
                    event = 'DarkTeal12'
                elif event == 'Aleatório':
                    event = 'random'
                with open('app/theme.yml', 'w') as theme_file:
                    if event == 'random':
                        yaml.dump({'theme': 'DarkTeal12'},
                                  theme_file)  # quando selecionar um aleatório, não guardar como padrão
                    else:
                        yaml.dump({'theme': event}, theme_file)
                window.close()
                window = cls.create_main_window(event)

            if event in ('\r', cls.app_config.key_codes['QT_ENTER_KEY1'],
                         cls.app_config.key_codes['QT_ENTER_KEY2']):  # Check for ENTER key
                elem = window.find_element_with_focus()
                if elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON:  # if it's a button element, click it
                    print(f"Found {elem.Type}")
                    elem.Click()

            # process menu choices
            if event == 'Versão':
                window.disappear()
                sg.popup(
                    'Versão 1.0\nPrograma grátis!\nMas caso queira ajudar o\nprogramador com qualquer '
                    'valor:\npix@lucasrochaabraao.com.br\nLucas Rocha Abraão',
                    title='Assinaturas',
                    font=cls.gui_config.font_primary,
                    auto_close=True,
                    auto_close_duration=10,
                    grab_anywhere=True,
                    no_titlebar=True,
                )
                window.reappear()

            elif event == 'Properties':
                cls.confirmation_mass_gen()

            # check for buttons that have been clicked
            elif event == '-GERAR-':
                # Se for repetido, vai funcionar até 3 assinaturas. Eventualmente vou fazer uma checagem na hora de
                # criar.
                nome = values['-NOME-']
                setor = values['-SETOR-']
                telefone1 = values['-TELEFONE1-']
                telefone2 = values['-TELEFONE2-']
                email = values['-EMAIL-']
                signature = Signature(nome, setor, [telefone1, telefone2], email)
                print(f'Validating signature: {signature}')
                if not cls.validate_existing(signature):
                    signature.generate()
                else:
                    window.disappear()
                    sg.popup(
                        f'Essa assinatura já existe!',
                        title='Assinaturas',
                        font=cls.gui_config.font_primary,
                        auto_close=True,
                        auto_close_duration=3,
                        grab_anywhere=True,
                        no_titlebar=True
                    )
                window.reappear()
                # Abrir file explorer where the signature was generated
                subprocess.Popen(f"explorer {cls.get_assinacraft_path('assinaturas_prontas')}")

            elif event == '-GERAR_MASSA-':
                cls.delete_current_signatures()
                cls.create_signature_mass(cls.app_config.config_dir / cls.app_config.signatures_csv)
                print('Gerando assinaturas em massa')
                subprocess.Popen(f"explorer {cls.get_assinacraft_path('assinaturas_prontas')}")

        window.close()

    @classmethod
    def confirmation_mass_gen(cls) -> None:
        layout = [
            [sg.Text('Tem certeza que deseja gerar assinaturas em massa?')],
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

    @classmethod
    def create_main_window(cls, theme: str) -> sg.Window:
        sg.theme(theme)
        sg.set_options(
            font=gui_config.font_primary,
            element_padding=(0, 0)
            # button_color=('Blue', 'White')
        )
        # Right Click Menu layout
        rc_menu = ['RightClickMenu', ['Tema', theme_menu[1], 'Versão']]

        # main layout
        layout = [
            [  # no default title bar, this is the custom one
                sg.Text('Assinaturas', font=gui_config.font_secondary, pad=((10, 0), (0, 0))),
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
                sg.Input(size=(32, 1), pad=((0, 0), (0, 5)), key='-SETOR-')
            ],
            [
                sg.Text('Telefone particular'),
                sg.Push(),
                sg.Input(size=(32, 1), pad=((0, 0), (0, 5)), key='-TELEFONE1-',
                         tooltip="Opcional, se ficar em branco será selecionado a assinatura com apenas 1 ícone de "
                                 "telefone.")
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

        icon = pkg_resources.resource_filename('assinacraft', f"resources/img/assinatura_64px.ico")
        return sg.Window(
            title='Assinaturas',
            layout=layout,
            return_keyboard_events=True,
            grab_anywhere=True,
            right_click_menu=rc_menu,
            icon=icon
            # no_titlebar = True,
        )

    @classmethod
    def validate_existing(cls, signature: Signature) -> bool:
        """ This function guarantees that each signature created is also
            inserted into the csv file, in case it is not already there."""
        signatures_csv = cls.app_config.config_dir / cls.app_config.signatures_csv
        with open(file=signatures_csv, encoding='utf-8', mode='r') as csvfile:
            reader_colaboradores = csv.DictReader(csvfile)
            for colaborador in reader_colaboradores:  # validating the new signature against all items in csv
                if colaborador['NOME'] == signature.name and \
                        colaborador['SETOR/CARGO'] == signature.department and \
                        [colaborador['TELEFONE 1'], colaborador['TELEFONE 2']] == [signature.phone_personal,
                                                                                   signature.phone_company] and \
                        colaborador['EMAIL'] == signature.email:
                    return True  # returns True if already in csv

        # Otherwise, we need to insert it into the csv to become  persistent, especially
        # when generating en masse. Obs: make sure the csv file always has a blank line
        # at the end.
        with open(file=signatures_csv, mode='a', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['NOME', 'SETOR/CARGO', 'TELEFONE 1', 'TELEFONE 2', 'EMAIL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'NOME': signature.name,
                'SETOR/CARGO': signature.department,
                'TELEFONE 1': signature.phone_personal,
                'TELEFONE 2': signature.phone_company,
                'EMAIL': signature.email
            })
        return False

    @classmethod
    def get_assinacraft_path(cls, assinacraft_dir: str) -> Path:
        full_assinacraft_path = str(cls.app_config.config_dir / assinacraft_dir)
        resource_dir = os.path.expanduser(full_assinacraft_path)
        if not os.path.exists(resource_dir):
            print(f"creating resource directory for: {assinacraft_dir}")
            # make sure the resource dir exists
            os.makedirs(resource_dir, exist_ok=True)

        return Path(resource_dir)
    @classmethod
    def delete_current_signatures(cls) -> None:
        if os.scandir('assinaturas_personalizadas'):
            for file in os.scandir('assinaturas_personalizadas'):
                os.remove(file.path)

    @classmethod
    def create_signature_mass(cls, csv_file: Path) -> None:
        with open(file=csv_file, encoding='utf-8') as csvfile:
            reader_employees = csv.DictReader(csvfile)
            for colaborador in reader_employees:
                name = colaborador['NOME']
                department = colaborador['SETOR/CARGO']
                phone = [colaborador['TELEFONE 1'], colaborador['TELEFONE 2']]
                email = colaborador['EMAIL']
                Signature(name, department, phone, email).generate()
