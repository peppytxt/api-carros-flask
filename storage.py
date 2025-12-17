import json
import os

ARQUIVO = "Carro/data/carros.json"

def carregar_carros():
    if not os.path.exists(ARQUIVO):
        return []

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_carros(carros):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(carros, f, indent=4, ensure_ascii=False)


def gerar_novo_id():
    carros = carregar_carros()
    if not carros:
        return 1
    return max(c["id"] for c in carros) + 1

