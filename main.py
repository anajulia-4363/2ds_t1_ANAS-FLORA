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

    # Iniciar uma sessão para o usuário
    session['usuario'] = {'cpf': cpf, 'nome': nome, 'email': email}

    cursor.close()
    mydb.close()

    # Retornar uma resposta indicando o sucesso do cadastro
    return redirect('/produtos')

@app.route('/login', methods=['POST'])
def login():
    # Conectando ao banco de dados
    mydb = Conexao.conectar()
    cursor = mydb.cursor()

    email = request.form.get('email')
    senha = request.form.get('senha')

    # Verificar as credenciais do usuário
    cursor.execute("SELECT cpf, nome, email FROM Usuario WHERE email = %s AND senha = %s", (email, sha256(senha.encode()).hexdigest()))
    usuario = cursor.fetchone()

    if usuario:
        cpf, nome, email = usuario  # Ajuste para desempacotar corretamente
        # Iniciar uma sessão para o usuário
        session['usuario'] = {'cpf': cpf, 'nome': nome, 'email': email}
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

        cursor.execute("SELECT * FROM Perfume WHERE genero = 'Masculino'")
        prdts_masculino = cursor.fetchall()

        cursor.execute("SELECT * FROM Perfume WHERE genero = 'Infantil'")
        prdts_infantil = cursor.fetchall()

        # Fechar cursor e conexão
        cursor.close()
        mydb.close()

        # Enviar os produtos para o template HTML dentro da classe prdts_feminino
        return render_template('produtos.html', 
                               prdts_feminino=prdts_feminino,
                               prdts_masculino=prdts_masculino,
                               prdts_infantil=prdts_infantil)
    else:
        # Redirecionar para a página de login-cadastro se o usuário não estiver autenticado
        return redirect('/login-cadastro')

@app.route('/cadastro-comentario/<id_perfume>', methods=['POST'])
def cadastrar_comentario(id_perfume):
    # Conectando ao banco de dados
    mydb = Conexao.conectar()
    cursor = mydb.cursor()

    # Recuperar o texto do comentário do formulário
    comentario = request.form.get('comentario')

    # Verificar se o usuário está autenticado
    if 'usuario' in session:
        # Recuperar o CPF e nome do usuário da sessão
        cpf_usuario = session['usuario']['cpf']
        nome_usuario = session['usuario']['nome']

        # Consultar o nome do usuário com base no CPF
        cursor.execute("SELECT nome FROM Usuario WHERE cpf = %s", (cpf_usuario,))
        nome_usuario = cursor.fetchone()[0]

        # Inserir o comentário no banco de dados
        cursor.execute("INSERT INTO Comentario (cpf, id_perfume, texto_comentario, data_comentario) VALUES (%s, %s, %s, NOW())", (cpf_usuario, id_perfume, comentario))
        mydb.commit()

        cursor.close()
        mydb.close()

        # Redirecionar de volta para a página do produto após cadastrar o comentário
        return redirect(f'/produto-escolhido/{id_perfume}')
    else:
        # Se o usuário não estiver autenticado, redirecionar para a página de login
        return redirect('/login-cadastro')

@app.route("/carrinho")
def pagina_carrinho():
    # Verificar se o usuário está autenticado
    if 'usuario' in session:
        # Recuperar o CPF do usuário da sessão
        cpf_usuario = session['usuario']['cpf']

        # Conectar ao banco de dados
        mydb = Conexao.conectar()
        cursor = mydb.cursor()

        # Consultar os itens do carrinho para o usuário atual
        cursor.execute("SELECT id_carrinho, nome_perfume, genero, preco, img_perfume FROM Carrinho_Produto WHERE cpf_usuario = %s", (cpf_usuario,))
        itens_carrinho = cursor.fetchall()

        # Fechar cursor e conexão
        cursor.close()
        mydb.close()

        # Enviar os itens do carrinho para o template HTML
        return render_template('carrinho.html', itens_carrinho=itens_carrinho)
    else:
        # Se o usuário não estiver autenticado, redirecionar para a página de login
        return redirect('/login-cadastro')

@app.route('/adicionar-carrinho', methods=['POST'])
def adicionar_carrinho():
    if 'usuario' in session:
        cpf_usuario = session['usuario']['cpf']
        id_produto = request.form.get('codigo_produto')
        
        # Conectar ao banco de dados
        mydb = Conexao.conectar()
        cursor = mydb.cursor()

        # Recuperar informações do produto e seu ID
        cursor.execute("SELECT id_perfume, nome_perfume, genero, preco, img_perfume FROM Perfume WHERE id_perfume = %s", (id_produto,))
        produto = cursor.fetchone()

        if produto:
            id_produto, nome_produto, genero, preco, img_produto = produto  # Desempacotando as informações do produto
            # Inserir o produto no carrinho com o CPF do usuário
            cursor.execute("INSERT INTO Carrinho_Produto (cpf_usuario, id_perfume, nome_perfume, genero, preco, img_perfume) VALUES (%s, %s, %s, %s, %s, %s)", (cpf_usuario, id_produto, nome_produto, genero, preco, img_produto))
            mydb.commit()

            cursor.close()
            mydb.close()

            return redirect('/carrinho')
        else:
            # Se o produto não existir, redirecione para alguma página de erro
            return redirect('/erro')
    else:
        # Se o usuário não estiver logado, redirecione para a página de login
        return redirect('/login-cadastro')

@app.route("/produto-escolhido/<id_prt_escolhido>")
def pagina_produto_escolhido(id_prt_escolhido):
    # Conectar ao banco de dados
    mydb = Conexao.conectar()
    cursor = mydb.cursor()

    # Recuperar informações do produto escolhido
    cursor.execute(f'SELECT * FROM Perfume WHERE id_perfume = {id_prt_escolhido}')
    perfume_escolhidoID = cursor.fetchone()

    # Recuperar comentários associados ao produto escolhido com o nome do usuário e o horário
    cursor.execute("SELECT c.texto_comentario, c.data_comentario, u.nome FROM Comentario c INNER JOIN Usuario u ON c.cpf = u.cpf WHERE c.id_perfume = %s", (id_prt_escolhido,))
    comentarios = cursor.fetchall()

    # Fechar cursor e conexão
    cursor.close()
    mydb.close()

    # Retornar o template com as informações do produto e os comentários
    return render_template('produto_escolhido.html',
                           perfume_escolhidoID=perfume_escolhidoID,
                           comentarios=comentarios)

@app.route('/remover-carrinho/<int:id_carrinho>', methods=['POST'])
def remover_item_carrinho(id_carrinho):
    if 'usuario' in session:
        cpf_usuario = session['usuario']['cpf']
        
        # Conectar ao banco de dados
        mydb = Conexao.conectar()
        cursor = mydb.cursor()

        # Verificar se o item do carrinho pertence ao usuário autenticado
        cursor.execute("DELETE FROM Carrinho_Produto WHERE cpf_usuario = %s AND id_carrinho = %s", (cpf_usuario, id_carrinho))
        mydb.commit()

        # Fechar cursor e conexão
        cursor.close()
        mydb.close()

    # Redirecionar de volta para a página do carrinho após excluir o item
    return redirect('/carrinho')

@app.route("/cep")
def pagina_cep():
    return render_template('cep.html')

if __name__ == "__main__":
    app.run(debug=True)
