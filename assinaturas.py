import csv
from src.Assinatura import Assinatura


def criar_assinaturas():
    arquivo_csv = csv.DictReader(open("elenco.csv"))
    for colaborador in arquivo_csv:
        nome = colaborador['NOME']
        setor = colaborador['SETOR/CARGO']
        telefone = [colaborador['TELEFONE 1'], colaborador['TELEFONE 2']]
        email = colaborador['EMAIL']
        assinatura = Assinatura(nome, setor, telefone, email)
        print(assinatura)
        assinatura.gravar()

if __name__ == '__main__':
    criar_assinaturas()
