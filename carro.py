class Carro:
    def __init__(self, id, marca, modelo, cor, velocidade=0):
        self.id = id
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.velocidade = velocidade

    def andar(self, velocidade):
        self.velocidade = velocidade

    def parar(self):
        self.velocidade = 0

    def to_dict(self):
        return {
            "id": self.id,
            "marca": self.marca,
            "modelo": self.modelo,
            "cor": self.cor,
            "velocidade": self.velocidade
        }
