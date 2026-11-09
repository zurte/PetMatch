from flask import Flask, render_template,send_file,request
import os

caminho_script = os.path.abspath("static/script/script.js")



app = Flask(__name__)

def gerar_arquivo(dados_animal):
     with app.app_context():
          pagina_html = render_template("base.html",animal=dados_animal)

          pasta_destino = 'templates'

          nome_arquivo = f"Pet - {dados_animal['id']}.html"

          caminho = os.path.join(pasta_destino,nome_arquivo)

          with open(caminho,'w',encoding='utf-8',) as f:
               f.write(pagina_html)
               print(f"Pagina {dados_animal['id']} gerada com sucesso")

          return caminho

          

@app.route('/criar_pagina')

def criar_pagina():
     animal_exemplo = {
          'id': 110,
          'image':'static/img/cachorro.jpeg',
          'nome': "Jeff",
          'descricao':'Esse é um cachoro com certeza'
     }

     caminho = gerar_arquivo(animal_exemplo)

     return send_file(caminho)

@app.route("/")

def inicio():
     return render_template("formulario_login.html")

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #aqui eu colocarei as funções que vão registrar o usuário dentro do bancod e dados
        email = request.form['email']
        senha = request.form['senha']

    return render_template('index.html')

@app.route("/registrar")
def registrar_usuario():
     return render_template("formulario_registro.html")

@app.route("/registrar_animal")
def registrar_animal():
     return render_template("formulario_adocao.html")

@app.route("/adocao")
def adocao():
     return render_template("adocao.html")

@app.route("/doacao")
def doacao():
     return render_template("doacao.html")

@app.route("/blog")
def blog():
     return render_template("blog.html")

if __name__ == "__main__": app.run(debug=True)


