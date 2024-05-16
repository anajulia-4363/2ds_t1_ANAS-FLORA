from flask import Flask, jsonify, render_template, request, redirect, session
from hashlib import sha256

from conexao_SQL import Conexao
app = Flask(__name__)
app = Flask(__name__)
app.secret_key = 'anas123'  # Defina uma chave secreta para a sessão


@app.route("/")
def pagina__inicial():
  return render_template('index.html')

@app.route("/login-cadastro")
def pagina__login_cadastro():
  return render_template('login.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    # Conectando ao banco de dados
    mydb = Conexao.conectar()
    cursor = mydb.cursor()

    cpf = request.form.get('cpf')
    nome = request.form.get('nome')
    email = request.form.get('email')
    endereco = request.form.get('endereco')
    senha = request.form.get('senha')
    nascimento = request.form.get('nascimento')
    telefone = request.form.get('telefone')

    # Verificar se o CPF já existe no banco de dados
    cursor.execute("SELECT COUNT(*) FROM Usuario WHERE cpf = %s", (cpf,))
    if cursor.fetchone()[0] > 0:
        print("CPF já está cadastrado.")
        return "CPF já está cadastrado."

    # Encriptar a senha usando SHA-256
    senha_hash = sha256(senha.encode()).hexdigest()

    # Inserir o novo usuário no banco de dados
    cursor.execute("INSERT INTO Usuario (cpf, nome, email, endereco, senha, nascimento, telefone) VALUES (%s, %s, %s, %s, %s, %s, %s)", (cpf, nome, email, endereco, senha_hash, nascimento, telefone))
    mydb.commit()

    cursor.close()
    mydb.close()

    # Retornar uma resposta indicando o sucesso do cadastro
    return render_template('produtos.html')

@app.route('/login', methods=['POST'])
def login():
    # Conectando ao banco de dados
    mydb = Conexao.conectar()
    cursor = mydb.cursor()

    email = request.form.get('email')
    senha = request.form.get('senha')

    # Verificar as credenciais do usuário
    cursor.execute("SELECT * FROM Usuario WHERE email = %s AND senha = %s", (email, sha256(senha.encode()).hexdigest()))
    usuario = cursor.fetchone()

    if usuario:
        # Iniciar uma sessão para o usuário
        session['usuario'] = usuario
        # Redirecionar para a página de produtos após o login
        return redirect('/produtos')
    else:
        alerta ="<script>alert(`Credenciais inválidas. Por favor, tente novamente.`);</script>"
        return render_template('login.html', alerta=alerta)


@app.route("/produtos")
def pagina__produtos():
    # Verificar se o usuário está autenticado
    if 'usuario' in session:
        return render_template('produtos.html')
    else:
        # Redirecionar para a página de login-cadastro se o usuário não estiver autenticado
        return redirect('/login-cadastro')

@app.route("/carrinho")
def pagina__carrinho():
  return render_template('carrinho.html')

@app.route("/produto-escolhido")
def pagina__produto_escolhido():
  return render_template('produto_escolhido.html')

if __name__ == "__main__":
 app.run(debug=True)
