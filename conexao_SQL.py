import mysql.connector

class Conexao():
    @staticmethod
    def conectar():
        #conectando 
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="ANAS",
            password="12345",
            database="anas_flora"
        )

        return mydb

# Criar uma conexão com o banco de dados
mydb = Conexao.conectar()

try:
    # Criar um objeto cursor para executar instruções SQL
    mycursor = mydb.cursor()

    # Execute suas operações com o banco de dados aqui...

finally:
    # Fechar o cursor e a conexão para liberar recursos
    mycursor.close()
    mydb.close()
