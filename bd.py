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
                animais.id,
                animais.nome,
                animais.image,
                animais.idade,
                animais.idade_unidade,
                racas.raca,
                sexos.descricao,
                cores.nome_cor,
                especies.nome_especie
    
            FROM animais
    
            JOIN racas ON animais.raca_id = racas.id
            JOIN especies ON racas.especie_id = especies.id
            JOIN sexos ON animais.sexo_id = sexos.id
            JOIN cores ON animais.cor_id = cores.id
        """)
    
    animais = cursor.fetchall()

    cursor.close()
    conexao.close()

    return animais

def listar_especie():
    conexao = sqlite3.connect("DataBase.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome_especie FROM especies")
    especies = cursor.fetchall()

    cursor.close()
    conexao.close()

    return especies

def buscar_animal(animal_id):
    conexao = sqlite3.connect("DataBase.db")
    cursor = conexao.cursor()
    
    cursor.execute(""" 

                    SELECT
                    animais.id,  
                    animais.nome,
                    animais.image,
                    animais.idade,
                    animais.idade_unidade,
                    racas.raca,
                    especies.nome_especie,
                    sexos.descricao,
                    cores.nome_cor,
                    animais.peso_valor,
                    animais.peso_unidade,
                    animais.castrado,
                    animais.vacinacao_medicacao

                    FROM animais

                    JOIN racas ON animais.raca_id = racas.id

                    JOIN sexos ON animais.sexo_id = sexos.id

                    JOIN cores ON animais.cor_id = cores.id

                    JOIN especies ON racas.especie_id = especies.id

                    WHERE animais.id = ?;
                    """, (animal_id,))
    
    id, nome, imagem, idade, idade_unidade, raca, especie, sexo, cor, peso_valor, peso_unidade, castrado, vacinacao_medicacao = cursor.fetchone()


    animal = {
        "id": id,
        "nome": nome,
        "imagem": imagem,
        "idade": idade,
        "idade_unidade": idade_unidade,
        "raca": raca,
        "especie": especie,
        "sexo": sexo,
        "cor": cor,
        "peso_valor": peso_valor,
        "peso_unidade": peso_unidade,
        "castrado": castrado,
        "vacinacao_medicacao": vacinacao_medicacao
    }

    cursor.close()
    conexao.close()

    return animal

def autenticar(email, senha):
    conexao = sqlite3.connect('DataBase.db')
    cursor = conexao.cursor()

    cursor.execute("""
                    SELECT id,senha
                    FROM tutores
                    WHERE email = ?
                    """,(email,))
    
    usuario = cursor.fetchall()
    cursor.close()
    conexao.close()

    if usuario is None:
        return None

    usuario_id, senha_hash = usuario[0]


    if not senha_check(senha_hash,senha):
        return None

    return usuario_id

def buscar_tutor(tutor_id):
    conexao = sqlite3.connect('DataBase.db')
    cursor = conexao.cursor()

    cursor.execute("""
                    SELECT id, nome, cpf, email, cep, numero
                    FROM tutores
                    WHERE id = ?
                    """,(tutor_id,))
    tutor = cursor.fetchall()

    cursor.close()
    conexao.close()

    if tutor is None:
        return None
    
    return {
    "id": tutor[0][0],
    "nome": tutor[0][1],
    "cpf": tutor[0][2],
    "email": tutor[0][3],
    "cep": tutor[0][4],
    "telefone": tutor[0][5]
    }


criar_tabela_usuario()
criar_tabela_animais()



