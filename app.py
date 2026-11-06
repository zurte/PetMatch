from flask import Flask, render_template,send_file,request
import os



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
     return render_template("formulario.html")

@app.route('/enviar-dados', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']

        return f"Olá, {nome}! Seu email é {email}."

    return render_template('index.html')

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


