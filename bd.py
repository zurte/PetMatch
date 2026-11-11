import sqlite3
import os 



conn = sqlite3.connect("DataBase.db")
cursor = conn.cursor()

caminho_db = os.path.exists("./DataBase.db")

def criar_tabela_usuario():

    
    cursor.execute("""
        create table if not exists usuario(
        id integer primary key autoincrement,
        nome text,
        cpf text,
        email text,
        cep text,
        numero text
        )
        """)
    
def add_usuario(usuario):
    """usuario"""

    dados = (usuario["nome"], usuario["cpf"],usuario["email"],usuario["cep"],usuario["numero"]),

    cursor.execute("insert into usuario (nome, cpf, email, cep, numero) values(?,?,?,?,?)",dados)

if caminho_db:
    criar_tabela_usuario()