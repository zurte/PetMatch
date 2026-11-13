import sqlite3
from werkzeug.security import generate_password_hash as senha_hash
from werkzeug.security import check_password_hash as senha_check
import os 




caminho_db = os.path.exists("./DataBase.db")

def criar_tabela_usuario():

    conexao = sqlite3.connect("DataBase.db")
    cursor = conexao.cursor()

    cursor.execute("""
        create table if not exists tutores(
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

    cursor.execute("insert into tutores (nome, cpf, email, cep, numero, senha) values(?,?,?,?,?,?)",dados)

    conexao.commit()
    conexao.close()


def checar_usuario(email,senha):

    conexao = sqlite3.connect("DataBase.db")
    cursor = conexao.cursor()

    cursor.execute("""
            SELECT senha 
            FROM tutores
            WHERE email = ?;
            """,(email,))

    senha_digitada = cursor.fetchone()
   

    conexao.close()

    if senha == None:
        return False

    senha_digitada = senha_digitada[0]

    print(senha)
    print(senha_digitada)
    print(senha_check(senha,senha_digitada))

    if not senha_check(senha_digitada,senha):
        return False

    return True

criar_tabela_usuario()