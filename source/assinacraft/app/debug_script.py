import csv
import os
from pathlib import Path
from assinacraft.app.signature import Signature


def delete_existing_signatures(results_dir: Path) -> None:
    if os.scandir(results_dir):
        for file in os.scandir(results_dir):
            os.remove(file.path)


def create_signatures(source_csv: Path, result_dir: Path) -> None:
    with open(source_csv, encoding='utf-8') as csv_reader:
        csvfile = csv.DictReader(csv_reader)

        for employee in csvfile:
            name = employee['NOME']
            department = employee['SETOR/CARGO']
            phone = [employee['TELEFONE 1'], employee['TELEFONE 2']]
            email = employee['EMAIL']
            signature = Signature(name, department, phone, email)
            print(signature)
            signature.generate()


def get_assinacraft_path(assinacraft_dir: str) -> Path:
    full_assinacraft_path = str(Path("~/Documents/Assinacraft/" + assinacraft_dir))
    resource_dir = os.path.expanduser(full_assinacraft_path)
    if not os.path.exists(resource_dir):
        print(f"creating resource directory: {resource_dir}")
        # make sure the resource dir exists
        os.makedirs(resource_dir, exist_ok=True)

    return Path(resource_dir)


def main():
    results_dir = get_assinacraft_path('assinaturas_prontas')
    source_csv = get_assinacraft_path('assinaturas') / 'elenco.csv'

    delete_existing_signatures(results_dir)
    create_signatures(source_csv, results_dir)


if __name__ == '__main__':
    main()
