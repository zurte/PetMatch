import sqlite3
from werkzeug.security import generate_password_hash as senha_hash
import os 




caminho_db = os.path.exists("./DataBase.db")

def criar_tabela_usuario():

    conexao = sqlite3.connect("DataBase.db")
    cursor = conexao.cursor()

    cursor.execute("""
        create table if not exists usuario(
        id integer primary key autoincrement,
        nome text,
        cpf text,
        email text,
        cep text,
        numero text,
        senha text
        )
        """)
    conexao.commit()
    conexao.close()

    
    
def add_usuario(usuario):
    """usuario"""

    print("ok")

    conexao = sqlite3.connect("DataBase.db")
    cursor = conexao.cursor()

    dados = (usuario["nome"], usuario["cpf"],usuario["email"],usuario["cep"],usuario["telefone"], senha_hash(usuario["senha"]))

    cursor.execute("insert into usuario (nome, cpf, email, cep, numero, senha) values(?,?,?,?,?,?)",dados)

    conexao.commit()
    conexao.close()




criar_tabela_usuario()