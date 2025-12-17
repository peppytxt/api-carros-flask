from flask import Flask, jsonify, request
from utils.buscar_carro import buscar_carro_por_id
from services.carro_service import andar_carro, deletar_carro
from carro import Carro
import storage

app = Flask(__name__)

@app.route("/")
def home():
    return "API Funcionando :)"

@app.route("/carros", methods=["POST"])
def criar_carro():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    for campo in ["marca", "modelo", "cor"]:
        if campo not in dados:
            return jsonify({"erro": f"Campo '{campo}' é obrigatório"}), 400

    novo_id = storage.gerar_novo_id()

    carro = Carro(
        id=novo_id,
        marca=dados["marca"],
        modelo=dados["modelo"],
        cor=dados["cor"]
    )

    carros = storage.carregar_carros()
    carros.append(carro.to_dict())
    storage.salvar_carros(carros)

    return jsonify({
        "mensagem": "Carro cadastrado com sucesso",
        "carro": carro.to_dict()
    }), 201

@app.route("/carros", methods=["GET"])
def listar_carros():
    carros = storage.carregar_carros()
    return jsonify(carros)


@app.route("/carros/<int:id>", methods=["GET"])
def obter_carro(id):
    carros = storage.carregar_carros()
    
    for carro in carros:
        if carro["id"] == id:
            return jsonify(carro)
        
    return jsonify({"erro": "Carro não encontrado"}), 404


@app.route("/carros/<int:id>/andar", methods=["POST"])
def andar(id):
    dados = request.get_json()

    if not dados or "velocidade" not in dados:
        return jsonify({"erro": "Velocidade é obrigatória"}), 400

    try:
        velocidade = int(dados["velocidade"])
    except (ValueError, TypeError):
        return jsonify({"erro": "Velocidade inválida"}), 400

    carro, erro = andar_carro(id, velocidade)

    if erro:
        return jsonify({"erro": erro}), 404

    return jsonify({
        "mensagem": "Carro em movimento",
        "carro": carro
    })
    
@app.route("/carros/<int:id>/parar", methods=["POST"])
def parar_carro(id):
    carro, carros = buscar_carro_por_id(id)
    
    if not carro:
        return jsonify({"erro": "Carro não encontrado"}), 404
    
    carro["velocidade"] = 0
    storage.salvar_carros(carros)
    
    return jsonify({
        "mensagem": "Carro parado",
        "carro": carro
    })
    
    
@app.route("/carros/<int:id>", methods=["PUT"])
def atualizar_carro(id):
    dados = request.get_json()
    
    if not dados:
        return jsonify({"erro": "JSON Inválido"}), 400
    
    campos_permitidos = {"marca", "modelo", "cor"}
    for campo in dados:
        if campo not in campos_permitidos:
            return jsonify({"erro", f"Campo inválido: {campo}"}), 
        
    carro, carros = buscar_carro_por_id(id)
    
    if carro is None:
        return jsonify({"erro": "Carro não encontrado"}), 404
                
    for campo in dados:
        carro[campo] = dados[campo]
                
    storage.salvar_carros(carros)
    return jsonify(carro), 200
    

@app.route("/carros/<int:id>", methods=["DELETE"])
def deletar(id):
    sucesso, erro = deletar_carro(id)

    if not sucesso:
        return jsonify({"erro": erro}), 404

    return jsonify({"mensagem": "Carro deletado com sucesso"})
    
if __name__ == "__main__":
    app.run(debug=True)
    
