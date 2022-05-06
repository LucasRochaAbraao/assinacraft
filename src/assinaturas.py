import csv
import os
from Assinatura import Assinatura

def delete_current_signatures():
    for file in os.scandir('../assinaturas_personalizadas'):
        os.remove(file.path)
    open('../assinaturas_personalizadas/.gitkeep', 'a').close() # importante para manter o versionamento do git quando não tiver nada aqui

def criar_assinaturas():
    arquivo_csv = csv.DictReader(open("../elenco.csv", encoding='utf-8'))
    for colaborador in arquivo_csv:
        nome = colaborador['NOME']
        setor = colaborador['SETOR/CARGO']
        telefone = [colaborador['TELEFONE 1'], colaborador['TELEFONE 2']]
        email = colaborador['EMAIL']
        assinatura = Assinatura(nome, setor, telefone, email)
        print(assinatura)
        assinatura.gravar()

if __name__ == '__main__':
    delete_current_signatures() # por enquanto é necessário deletar todas assinaturas. Eventualmente vou fazer uma checagem na hora de criar.
    criar_assinaturas()
