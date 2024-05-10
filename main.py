from flask import Flask, render_template, request
from hashlib import sha256
from conexao_SQL import Conexao
import mysql.connector
app = Flask(__name__)

# ------------------------------------------------------
@app.route("/")
def pagina__inicial():
  return render_template('index.html')
# ------------------------------------------------------





@app.route("/login-cadastro" , methods=['POST'])
def pagina__login_cadastro():
  return render_template('login.html')

@app.route("")
def cadastro():
  mydb = Conexao.conectar()
  cursor = mydb.cursor()

  cpf = request.form['cpf']
  nome = request.form['nome']
  email = request.form['email']
  endereco = request.form['endereco']
  senha = request.form['senha']
  senha = request.form['senha']
  nascimento = request.form['nascimento']
  telefone = request.form['telefone']

  # Verificar se o CPF já existe no banco de dados
  cursor.execute("SELECT COUNT(*) FROM Usuario WHERE cpf = %s", (cpf,))
  if cursor.fetchone()[0] > 0:
      print("CPF já está cadastrado.")
      return

  # Encriptar a senha usando SHA-256
  senha_hash = sha256(senha.encode()).hexdigest()

  # Inserir o novo usuário no banco de dados
  cursor.execute("INSERT INTO Usuario (cpf, nome, email, endereco, senha, nascimento, telefone) VALUES (%s, %s, %s, %s, %s, %s, %s)", (cpf, nome, email, endereco, senha_hash, nascimento, telefone))
  mydb.commit()

  cursor.close()
  mydb.close()
  return render_template('produtos.html')


  







# ------------------------------------------------------
@app.route("/produtos")
def pagina__produtos():
  return render_template('produtos.html')
# ------------------------------------------------------
@app.route("/carrinho")
def pagina__carrinho():
  return render_template('carrinho.html')
# ------------------------------------------------------
@app.route("/produto-escolhido")
def pagina__produto_escolhido():
  return render_template('produto_escolhido.html')
# ------------------------------------------------------
if __name__ == "__main__":
 app.run(debug=True)
