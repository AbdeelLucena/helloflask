from flask import Flask, request, jsonify
from ddl import init_db, get_db, close_connection

app = Flask(__name__)

# Registra uma função para fechar a conexão com o banco de dadoss
app.teardown_appcontext(close_connection)

#  usado para abrir uma conexão.
with app.app_context():
    init_db()

# Funçao para executar as consultas no banco de dados
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)   # executa a consulta
    get_db().commit()  # confirma a transação
    rv = cur.fetchall()  # retorna todos os resultados disponiveis
    cur.close()  # fecha cursor depois de executar a consulta
    return (rv[0] if rv else None) if one else rv

# Função para retornar todos os usuarios do banco de dados
def getUsuarios():
    users = query_db('SELECT * FROM tb_usuario')
    return [dict(row) for row in users]  # retorna uma lista de dicionários

def addUsuario(args):
    query_db('INSERT INTO tb_usuario(nome, nascimento) values (?, ?)', [args['nome'], args['nascimento']], one=False)
    return dict(args)


def getUsuarioById(id):
    user = query_db('SELECT * FROM tb_usuario WHERE id = ?', [id], one=True) # Função para obter o usuário pelo ID
    return dict(user) if user else None


def updateUsuario(args):
    updated_user = query_db('UPDATE tb_usuario SET nome = ?, nascimento = ? WHERE id = ?', args, one=True) # Função para atualizar os dados de usuário
    return jsonify(updated_user)


def deleteFisicoUsuario(id):
    query_db('DELETE FROM tb_usuario WHERE id = ?', [id], one=True) # Função para deletar usuário 
    return 'Usuário excluído com sucesso'

# função para deletar logicamente o usuário
def deleteLogicoUsuario(id):
    query_db('UPDATE tb_usuario SET is_deleted = TRUE WHERE id = ?', [id], one=False)
    return 'Usuário deletado logicamente com sucesso'


@app.route("/")
def index():
    return (jsonify({"versao": 1}), 200)


@app.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    if request.method == 'GET':
        # Listagem d usuários
        users = getUsuarios()
        return jsonify(users), 200
    elif request.method == 'POST':
        
        data = request.json
        data = addUsuario(data)
        return jsonify(data), 201


@app.route("/usuarios/<int:id>", methods=['GET', 'DELETE', 'PUT'])
def usuario(id):
    if request.method == 'GET':
        usuario = getUsuarioById(id)
        if usuario is not None:
            return jsonify(usuario), 200
        else:
            return {}, 404
    elif request.method == 'PUT':
        # Recuperar dados da requisição-tipo json
        data = request.json
        args = (data['nome'], data['nascimento'], id)
        row_update = updateUsuario(args)
        if row_update != 0:
            return (data, 201)
        else:
            return (data, 304)
    elif request.method == 'DELETE':
       
        usuario = deleteLogicoUsuario(id)
        if usuario is not None:
            return jsonify(usuario), 200
        else:
            return {}, 404
        
        
if __name__ == "__main__":
    app.run(debug=True)
