from setuptools import setup, find_packages

description = " "

setup(
    name='assinacraft',
    version='0.0.1',
    author='Lucas Rocha Abraão',
    author_email='lucasrabraao@gmail.com',
    description=description,
    license='GPLv3+',
    python_requires=">=3.8",
    include_package_data=True,
    data_files=[("config", ["config/config.yml"])],
    package_data={'assinacraft': ['resources/*']},
    install_requires=[
        'altgraph==0.17.2',
        'Pillow==9.1.0',
        'pyinstaller==5.0.1',
        'pyinstaller-hooks-contrib==2022.4',
        'PySimpleGUI==4.59.0',
        'pysimplegui-exemaker==1.3.0',
        'PyYAML==6.0',
    ],
    packages=find_packages('source', exclude=['tests']),
    package_dir={'': 'source'},
    entry_points={
        'console_scripts': [
            'assinacraft=assinacraft.app.main:main_app',
        ],
    },
)
