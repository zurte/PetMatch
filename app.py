from flask import Flask, render_template,send_file,request,redirect,url_for,session
import bd
import os


caminho_script = os.path.abspath("static/script/script.js")




app = Flask(__name__)

app.secret_key = "petmatch_chave_secreta_2026"

@app.route("/")
def inicio():
     return render_template("formulario_login.html")

@app.route('/index', methods=['GET', 'POST'])
def index():
     if request.method == 'POST':

          email = request.form['email']
          senha = request.form['senha']

          tutor_id = bd.autenticar(email,senha)

          if tutor_id is not None:
               session['tutor_id'] = tutor_id

               return redirect(url_for('index'))
          else:
                return render_template('formulario_login.html',senha_incorreta="senha incorreta")

          
     especie_selecionada = request.args.get('especie','todas')

     
     animais = bd.listar_animais()
     especies = bd.listar_especie()

     animais_por_especie = {}

     for especie_id, nome_especie in especies:
          animais_por_especie[nome_especie] = []


     for animal in animais:
          nome_especie = animal[8]

          animais_por_especie[nome_especie].append(animal)

     print(animais_por_especie)

     return render_template('index.html', 
                              animais_por_especie=animais_por_especie, 
                              especies=especies,
                              especie_selecionada=especie_selecionada)
          

@app.route("/registrar", methods=["GET","POST"])
def registrar_usuario():
     return render_template("formulario_registro.html")

@app.route("/registrar_animal")
def registrar_animal():
     return render_template("formulario_adocao.html")

@app.route("/doacao")
def doacao():
     return render_template("doacao.html")

@app.route("/blog")
def blog():
     return render_template("blog.html")

@app.route("/adicionar_usuario",methods=["POST"])
def adicionar_usuario():

     novo_usuario = {
          "nome" : request.form["nome"],
          "email" : request.form["email"],
          "senha" : request.form["senha"],
          "telefone": request.form["telefone"],
          "cpf" : request.form["cpf"],
          "idade" : request.form["idade"],
          "cep" : request.form["cep"]
     }

     bd.add_usuario(novo_usuario)

     return render_template('index.html')

@app.route("/adicionar_animal",methods=["POST"])
def adcionar_animal():

     nova_imagem = request.files["imagem"]

     nova_imagem.save(os.path.join("static/img",nova_imagem.filename))

     novo_animal = {
          "nome": request.form["nome"],
          "idade": request.form["idade"],
          "idade_unidade": request.form["idade_unidade"],
          "raca_id": request.form["raca_id"],
          "sexo_id": request.form["sexo_id"],
          "cor_id": request.form["cor_id"],
          "peso_valor": request.form["peso_valor"],
          "peso_unidade": request.form["peso_unidade"],
          "castrado": request.form.get("castrado", "0"),
          "vacinacao_medicacao": request.form["vacinacao_medicacao"],
          "status_adocao": request.form["status_adocao"],
          "imagem": "static/img/" + nova_imagem.filename
     }

     bd.add_animal(novo_animal)

     return render_template('formulario_adocao.html', mensagem_sucesso="Animal adicionado com sucesso!")

@app.route('/detalhes_animal/<int:animal_id>')
def detalhes_animal(animal_id):
     animal = bd.buscar_animal(animal_id)

     if animal is None:
          return "animal não encontrado", 404

     tutor_id = session.get('tutor_id')

     tutor = bd.buscar_tutor(tutor_id)
     
     return render_template(f'detalhes_animal.html', animal=animal,tutor=tutor)



if __name__ == "__main__": app.run(debug=True)


