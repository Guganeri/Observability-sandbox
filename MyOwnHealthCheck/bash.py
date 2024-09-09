import subprocess
import json
import datetime
import logging
import traceback
from logging.handlers import RotatingFileHandler
import os
import time

log_file = 'log_status.json'

def carregar_ou_criar_arquivo_log():
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {"logs": []}
    else:
        return {"logs": []} 

def salvar_logs(logs):
    with open(log_file, 'w', encoding='utf-8') as file:
        json.dump(logs, file, ensure_ascii=False, indent=4)

def executar_comando_bash(comando):
    """Executa um comando bash e registra a saída e status."""
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True)
        status_code = result.returncode
        saida = result.stdout
        erro = result.stderr

        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "comando": comando,
            "status_code": status_code,
            "level": "info" if status_code == 0 else "error",
            "message": "Comando executado com sucesso" if status_code == 0 else "Erro ao executar o comando"
        }

        if status_code != 0:
            log_entry["stderr"] = erro
        else:
            log_entry["stdout"] = saida

        print(f"Comando executado. Status: {status_code}.")
        return log_entry

    except Exception as e:
        tb = traceback.format_exc()

        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "comando": comando,
            "level": "error",
            "message": "Erro ao executar o comando Bash",
            "error": str(e),
            "traceback": tb
        }

        print(f"Erro ao executar o comando: {e}")
        return log_entry

# Comando Bash a ser executado
comando = "curl google.com"

# Loop para executar o comando a cada 30 minutos (ou ajustar conforme necessidade)
while True:
    logs = carregar_ou_criar_arquivo_log()
    log_entry = executar_comando_bash(comando)
    logs["logs"].append(log_entry)

    salvar_logs(logs)

    time.sleep(1800)
