import pytest
from app import app
from unittest.mock import patch

fake_carros = []

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "API Funcionando" in response.get_data(as_text=True)


def test_criar_carro(client):
    with patch("storage.carregar_carros", return_value=fake_carros), \
         patch("storage.salvar_carros"):

        response = client.post(
            "/carros",
            json={
                "marca": "Honda",
                "modelo": "Civic",
                "cor": "Preto"
            }
        )

        data = response.get_json()

        assert response.status_code == 201
        assert data["carro"]["marca"] == "Honda"


def test_listar_carros(client):
    response = client.get("/carros")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_andar_carro(client):
    fake_carros = [{
        "id": 1,
        "marca": "Honda",
        "modelo": "Civic",
        "cor": "Preto",
        "velocidade": 0
    }]

    with patch("storage.carregar_carros", return_value=fake_carros), \
         patch("storage.salvar_carros"):

        response = client.post(
            "/carros/1/andar",
            json={"velocidade": 80}
        )

        data = response.get_json()

        assert response.status_code == 200
        assert data["carro"]["velocidade"] == 80


def test_parar_carro(client):
    fake_carros = [{
        "id": 1,
        "marca": "Honda",
        "modelo": "Civic",
        "cor": "Preto",
        "velocidade": 80
    }]

    with patch("storage.carregar_carros", return_value=fake_carros), \
         patch("storage.salvar_carros"):

        response = client.post("/carros/1/parar")

        data = response.get_json()

        assert response.status_code == 200
        assert data["carro"]["velocidade"] == 0

