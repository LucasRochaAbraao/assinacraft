# Assinatura-gen

![Desktop App](resources/img/assinaturas_gui.png)

Esse repositório hospeda o código do Gerador de assinaturas de e-mail dos colaboradores da QUICK FIBRA. A manutenção da criação de assinaturas de e-mails é desgastante, pois com mudanças no quadro de colaboradores e na mudança de cargos, é necessário criar / excluir / alterar cada campo das assinaturas, que são editadas por uma agência de marketing. Eu criei esse app para que o setor de RH possa ter gestão dessa atividade. Dessa forma, fica muito mais fácil manter tudo atualizado, principalmente com o crescimento do quadro de colaboradores.

Minha assinatura como exemplo (note que cada campo de texto na porte da direita da imagem é gerado pelo script):

![Minha assinatura como exemplo](assinaturas_personalizadas/Lucas_Rocha.png)

### Instalação
Em breve vou disponibilizar um zip com o executável e arquivos auxiliáres, com instrução de como utilizar.

#### Status do projeto (em desenvolvimento):
Inicialmente pensava em fazer uma página web onde cada funcionário poderia gerenciar sua própria assinatura. Mas mudei de ideia, e estou fazerendo um simples desktop app (usando SimplePyGui) onde o RH gerencia essas assinaturas. Eventualmente posso pensar em refazer o projeto todo em Pygame (ou parecido), onde terei mais possibilidades de manipular a imagem diretamente, permitindo trocar até o template da assinatura. Mas por enquanto funciona bem o app com um template pré estabelecido. Caso seja necessário trocar o template da assinatura no futuro, será necessário compilar um novo binário.

### Instalação do zero (criando o executávio) do app com interface gráfica
Para instalar o app e criar um executável, faça assim:
- Tenha a versão atual do [Python](https://www.python.org/downloads/) instalado.
- Baixe os arquivos desse repositório
- Instale os pacotes do requirements.txt (`pip install -r requirements.txt`)
- Dentro do diretório do projeto, execute o comando: `python -m pysimplegui-exemaker.pysimplegui-exemaker`
- Na nova janela, busque pelo código fonte (`gui_assinaturas.py`) e o ícone (`resources/img/assinatura_64px.ico`), e clique no botão 'Make EXE'.

Em alguns segundos haverá um executável (.exe) no mesmo diretório do projeto. Caso queira colocar o executável em outro local, criei um atalho. O arquivo original deve sempre estar na mesma pasta relativa que os arquivos e pastas `assinaturas_personalizadas`, `elenco.csv`, `resources`, `src`. Caso queira colocar esses arquivos em outro lugar, basta levar a pasta do projeto toda junto. Já o atalho pode ser colocado em qualquer lugar sozinho, que vai conseguir encontrar esses arquivos e pastas originais sem problemas.

#### TODO
- Permitir rodar o botão de gerar assinaturas em massa sem precisar apagar tudo antes (o script já faz isso, mas o ideal é ter uma checagem).
- Criar um release com zip de todos arquivos necessários, já com o executável compilado.