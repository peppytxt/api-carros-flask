from services.carro_service import andar_carro, parar_carro, deletar_carro
from unittest.mock import patch

def test_andar_carro_sucesso():
    carros_fake = [
        {"id": 1, "marca": "Ford", "modelo": "Ka", "cor": "Preto", "velocidade": 0}
    ]

    with patch("services.carro_service.buscar_carro_por_id") as mock_busca, \
         patch("services.carro_service.storage.salvar_carros"):

        mock_busca.return_value = (carros_fake[0], carros_fake)

        carro, erro = andar_carro(1, 80)

        assert erro is None
        assert carro["velocidade"] == 80


def test_andar_carro_inexistente():
    with patch("services.carro_service.buscar_carro_por_id") as mock_busca:
        mock_busca.return_value = (None, [])

        carro, erro = andar_carro(99, 50)

        assert carro is None
        assert erro == "Carro não encontrado"
        
        
def test_andar_carro_velocidade_invalida():
    carros_fake = [
        {"id": 1, "velocidade": 0}
    ]

    with patch("services.carro_service.buscar_carro_por_id") as mock_busca:
        mock_busca.return_value = (carros_fake[0], carros_fake)

        carro, erro = andar_carro(1, 500)

        assert carro is None
        assert erro == "Velocidade deve estar entre 0 e 200"
        

def test_parar_carro():
    carros_fake = [
        {"id": 1, "velocidade": 100}
    ]

    with patch("services.carro_service.buscar_carro_por_id") as mock_busca, \
         patch("services.carro_service.storage.salvar_carros"):

        mock_busca.return_value = (carros_fake[0], carros_fake)

        carro, erro = parar_carro(1)

        assert erro is None
        assert carro["velocidade"] == 0


def test_deletar_carro():
    carros_fake = [
        {"id": 1},
        {"id": 2}
    ]

    with patch("services.carro_service.buscar_carro_por_id") as mock_busca, \
         patch("services.carro_service.storage.salvar_carros"):

        mock_busca.return_value = (carros_fake[0], carros_fake)

        sucesso, erro = deletar_carro(1)

        assert sucesso is True
        assert erro is None
        assert len(carros_fake) == 1