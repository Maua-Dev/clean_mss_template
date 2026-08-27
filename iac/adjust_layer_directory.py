import os
import shutil
import subprocess
from pathlib import Path 

# Tenha certeza de que BUILD_DIRECTORY tenha o mesmo valor na criação da lambda layer em constructs/lambda_construct.py
BUILD_DIRECTORY = "build"
PYTHON_TOP_LEVEL_DIR = os.path.join(BUILD_DIRECTORY, "python")
REQUIREMENTS_FILE = "requirements-app.txt"

# Pega o diretório do projeto (a top folder que no caso do template é clean mss template) subindo um nível a partir do script atual
PROJECT_ROOT = Path(__file__).parent.parent 
# O 3 parâmetro passado no join precisa corresponder exatamente a pasta ao lado de modules, geralmente a shared
# Essa será a pasta em que as depências que nosso projeto estarão presentes. Mais especificamente: será a lambda layer!
SHARED_CODE_SOURCE = os.path.join(PROJECT_ROOT, "src", "shared")


def adjust_layer_directory():
    """
    Prepara um diretório 'build' para uma Lambda Layer do AWS CDK.
    
    A função junta o código local compartilhado e as dependências externas (pip)
    na estrutura de pastas que a Lambda espera (/python).
    """

    # Garante que o build seja sempre limpo, removendo qualquer artefato antigo
    if os.path.exists(BUILD_DIRECTORY):
        shutil.rmtree(BUILD_DIRECTORY)
    
    # Cria a estrutura de pastas 'build/python/src/'
    # Isso é necessário para que os imports 'from src.shared...' funcionem na Lambda
    shared_code_intermediate_dir = os.path.join(PYTHON_TOP_LEVEL_DIR, "src")
    os.makedirs(shared_code_intermediate_dir)

    # Copia o código compartilhado (de 'src/shared') para dentro da estrutura da Layer
    # O resultado final será 'build/python/src/shared'
    print(f"Copiando código de: {SHARED_CODE_SOURCE}") # adicionado para debug
    shared_code_dest = os.path.join(shared_code_intermediate_dir, os.path.basename(SHARED_CODE_SOURCE))
    shutil.copytree(SHARED_CODE_SOURCE, shared_code_dest)

    # Se o arquivo de dependências existir, instala todas as bibliotecas
    # O arquivo de requirements também precisa ser lido a partir da raiz!!!
    requirements_path = os.path.join(PROJECT_ROOT, REQUIREMENTS_FILE)
    if os.path.exists(requirements_path):
        # Instala os pacotes diretamente na pasta 'build/python'
        # Isso permite que a Lambda importe as bibliotecas de forma padrão (ex: import requests)
        # Aqui usamos também uma distribuição do linux, visto que isso é o runtime da lambda
        # Esse problema do linux surge na instalação de bibliotecas como numpy ou pandas, que assumem / precisam de uma versão diferente quando rodam
        # no runtime da lambda
        subprocess.check_call(
            [
                "pip", "install",
                "-r", requirements_path,
                "-t", PYTHON_TOP_LEVEL_DIR,
                "--no-cache-dir",
                "--platform", "manylinux2014_x86_64",
                "--python-version", "3.13",
                "--only-binary=:all:"
            ]
        )
    else:
        # Apenas um aviso caso o arquivo não seja encontrado
        print(f"Aviso: Arquivo '{requirements_path}' não encontrado. Nenhuma dependência externa será instalada.")


# Ponto de entrada do script
if __name__ == '__main__':
    adjust_layer_directory()