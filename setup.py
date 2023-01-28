from setuptools import setup, find_packages

setup(
    name='assinacraft',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    data_files=[("config", ["config/config.yml"])]
    install_requires=[
        'altgraph==0.17.2',
        'Pillow==9.1.0',
        'pyinstaller==5.0.1',
        'pyinstaller-hooks-contrib==2022.4',
        'PySimpleGUI==4.59.0',
        'pysimplegui-exemaker==1.3.0',
        'PyYAML==6.0',
    ],
    entry_points={
        'console_scripts': [
            'assinacraft = assinacraft.app.main:main'
        ]
    },
)