from flask import Flask, render_template, request, redirect, session
from hashlib import sha256
from conexao_SQL import Conexao

app = Flask(__name__)
app.secret_key = 'anas123'  # Defina uma chave secreta para a sessão

@app.route("/")
def pagina_inicial():
    return render_template('index.html')

@app.route("/login-cadastro")
def pagina_login_cadastro():
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
        alerta = "<script>alert(`Credenciais inválidas. Por favor, tente novamente.`);</script>"
        return render_template('login.html', alerta=alerta)


@app.route("/produtos")
def pagina_produtos():
    # Verificar se o usuário está autenticado
    if 'usuario' in session:
        # Conectar ao banco de dados
        mydb = Conexao.conectar()
        cursor = mydb.cursor()

        # Consulta SQL para obter os produtos do genero "Feminino"
        cursor.execute("SELECT * FROM Perfume WHERE genero = 'Feminino'")
        prdts_feminino = cursor.fetchall()

        # Fechar cursor e conexão
        cursor.close()
        mydb.close()

        # Enviar os produtos para o template HTML dentro da classe prdts_feminino
        return render_template('produtos.html', prdts_feminino=prdts_feminino)
    else:
        # Redirecionar para a página de login-cadastro se o usuário não estiver autenticado
        return redirect('/login-cadastro')
    








@app.route("/carrinho")
def pagina_carrinho():
    return render_template('carrinho.html')

@app.route("/produto-escolhido/<id_prt_escolhido>")
def pagina_produto_escolhido(id_prt_escolhido):
    return render_template('produto_escolhido.html')

if __name__ == "__main__":
    app.run(debug=True)
