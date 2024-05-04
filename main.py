from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def pagina__inicial():
  return render_template('index.html')

@app.route("/login-cadastro")
def pagina__login_cadastro():
  return render_template('login.html')

@app.route("/produtos")
def pagina__produtos():
  return render_template('produtos.html')

@app.route("/carrinho")
def pagina__carrinho():
  return render_template('carrinho.html')

@app.route("/produto-escolhido")
def pagina__produto_escolhido():
  return render_template('produto_escolhido.html')

if __name__ == "__main__":
 app.run(debug=True)
