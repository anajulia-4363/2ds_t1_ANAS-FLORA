# cadastro.py

from conexao_SQL import Conexao
from hashlib import sha256



  
def cadastrar_usuario():
    # Conectando ao banco de dados
    try:
        mydb = Conexao.conectar()
        cursor = mydb.cursor()

        # Solicitar os detalhes do cadastro do usuário
        nome = input("Digite o nome completo: ")
        cpf = input("Digite o CPF: ")
        email = input("Digite o email: ")
        endereco = input("Digite o endereço: ")
        senha = input("Digite a senha: ")
        nascimento = input("Digite a data de nascimento (no formato AAAA-MM-DD): ")
        telefone = input("Digite o telefone: ")

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

        print("Usuário cadastrado com sucesso!")

    except Exception as e:
        print("Erro ao cadastrar usuário:", e)

    finally:
        cursor.close()
        mydb.close()

if __name__ == "__main__":
    cadastrar_usuario()
