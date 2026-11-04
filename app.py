from flask import Flask, render_template

import sqlite3



conexao = sqlite3.connect('meu_banco.db')

ponteiro = sqlite3.Cursor(conexao)

ponteiro.execute("""CREATE TABLE IF NOT EXISTS animais(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT
)""")



app = Flask(__name__)

@app.route("/")

def inicio():
     return render_template("index.html") 

if __name__ == "__main__": app.run(debug=True)