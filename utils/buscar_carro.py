import storage

def buscar_carro_por_id(id):
    carros = storage.carregar_carros()
    
    for carro in carros:
        if carro["id"] == id:
            return carro, carros
    
    return None, carros
