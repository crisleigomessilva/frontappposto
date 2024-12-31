import os
import json

def load_config(file_path=None):
    if not file_path:
        # Define o caminho absoluto para o arquivo config.json
        file_path = os.path.join(os.path.dirname(__file__), "../config.json")
    
    try:
        with open(file_path, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        raise Exception(f"Arquivo de configuração '{file_path}' não encontrado.")
    except json.JSONDecodeError:
        raise Exception(f"Erro ao decodificar o arquivo de configuração '{file_path}'.")
