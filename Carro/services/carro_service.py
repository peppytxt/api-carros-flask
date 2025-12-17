import storage
from utils.buscar_carro import buscar_carro_por_id


def andar_carro(id, velocidade):
    carro, carros = buscar_carro_por_id(id)

    if carro is None:
        return None, "Carro não encontrado"

    if not isinstance(velocidade, int):
        return None, "Velocidade inválida"

    if velocidade < 0 or velocidade > 200:
        return None, "Velocidade deve estar entre 0 e 200"

    carro["velocidade"] = velocidade
    storage.salvar_carros(carros)

    return carro, None


def parar_carro(id):
    carro, carros = buscar_carro_por_id(id)

    if carro is None:
        return None, "Carro não encontrado"

    carro["velocidade"] = 0
    storage.salvar_carros(carros)

    return carro, None


def atualizar_carro(id, dados):
    campos_permitidos = {"marca", "modelo", "cor"}

    for campo in dados:
        if campo not in campos_permitidos:
            return None, f"Campo inválido: {campo}"

    carro, carros = buscar_carro_por_id(id)

    if carro is None:
        return None, "Carro não encontrado"

    for campo in dados:
        carro[campo] = dados[campo]

    storage.salvar_carros(carros)
    return carro, None


def deletar_carro(id):
    carro, carros = buscar_carro_por_id(id)

    if carro is None:
        return False, "Carro não encontrado"

    carros.remove(carro)
    storage.salvar_carros(carros)

    return True, None
