import sqlite3
from werkzeug.security import generate_password_hash as senha_hash
from werkzeug.security import check_password_hash as senha_check
import os 

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

def criar_tabela_animais():
    conexao = sqlite3.connect('DataBase.db')
    cursor = conexao.cursor()
    


    cursor.executescript("""
                    PRAGMA foreign_keys = ON;

                    CREATE TABLE IF NOT EXISTS sexos (
                    id INTEGER PRIMARY KEY,
                    descricao TEXT NOT NULL);

                    CREATE TABLE IF NOT EXISTS especies(
                    id INTEGER PRIMARY KEY AUTOINCREMENT ,
                    nome_especie TEXT NOT NULL);

                    CREATE TABLE IF NOT EXISTS  cores(
                    id INTEGER PRIMARY KEY AUTOINCREMENT ,
                    nome_cor TEXT NOT NULL);

                    CREATE TABLE IF NOT EXISTS racas(
                    id INTEGER PRIMARY KEY AUTOINCREMENT ,
                    raca TEXT NOT NULL,
                    porte TEXT NOT NULL,
                    especie_id INTEGER NOT NULL REFERENCES especies(id));
                    

                    CREATE TABLE IF NOT EXISTS vacinas(
                    id INTEGER PRIMARY KEY AUTOINCREMENT ,
                    especie_id INTEGER NOT NULL REFERENCES especies(id),
                    especie_animal TEXT NOT NULL,
                    nome_vacina TEXT NOT NULL,
                    doencas_protegidas TEXT NOT NULL,
                    obrigatoriedade TEXT NOT NULL);

                    CREATE TABLE IF NOT EXISTS historico_vacinas(
                    id INTEGER PRIMARY KEY AUTOINCREMENT ,
                    animal_id INTEGER NOT NULL REFERENCES animais(id),
                    vacina_id INTEGER NOT NULL REFERENCES vacinas(id),
                    data_aplicacao DATE NOT NULL,
                    proxima_dose DATE);

                    CREATE TABLE IF NOT EXISTS animais(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    idade INTEGER,
                    raca_id INTEGER NOT NULL REFERENCES racas(id),
                    sexo_id INTEGER NOT NULL REFERENCES sexos(id),
                    cor_id INTEGER NOT NULL REFERENCES cores(id),
                    castrado BOOLEAN NOT NULL DEFAULT 0 CHECK (castrado IN (0,1))
                    );
                """)
                   
    
def add_usuario(usuario):

    conexao = sqlite3.connect("DataBase.db")
    cursor = conexao.cursor()

    dados = (usuario["nome"], usuario["cpf"],usuario["email"],usuario["cep"],usuario["telefone"], senha_hash(usuario["senha"]))

    cursor.execute("insert into tutores (nome, cpf, email, cep, numero, senha) values(?,?,?,?,?,?)",dados)

    conexao.commit()
    conexao.close()

def add_animal(animal):
    conexao = sqlite3.connect("DataBase.db")
    cursor = conexao.cursor()

    dados = (
    animal["nome"],
    animal["idade"],
    animal["idade_unidade"],
    animal["raca_id"],
    animal["sexo_id"],
    animal["cor_id"],
    animal["peso_valor"],
    animal["peso_unidade"],
    animal["castrado"],
    animal["vacinacao_medicacao"],
    animal["status_adocao"],
    animal["imagem"]
    )

    cursor.execute("""
        INSERT INTO animais (
            nome,
            idade,
            idade_unidade,
            raca_id,
            sexo_id,
            cor_id,
            peso_valor,
            peso_unidade,
            castrado,
            vacinacao_medicacao,
            status_adocao,
            image
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, dados)

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

def listar_animais():
    conexao = sqlite3.connect("DataBase.db")
    cursor = conexao.cursor()

    cursor.execute(""" 

                    SELECT  
                    animais.nome,
                    animais.image,
                    animais.idade,
                    animais.idade_unidade,
                    racas.raca,
                    sexos.descricao,
                    cores.nome_cor

                    FROM animais
                    
                    JOIN racas ON animais.raca_id = racas.id

                    JOIN sexos ON animais.sexo_id = sexos.id

                    JOIN cores ON animais.cor_id = cores.id;

                    
                    """)
    animais = cursor.fetchall()

    cursor.close()
    conexao.close()

    return animais


criar_tabela_usuario()
criar_tabela_animais()


