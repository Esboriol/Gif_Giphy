from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import requests

load_dotenv()
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

app = Flask(__name__)

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')  # Agora usando o .env para isso

mail = Mail(app)

# Rota para exibir os gifs
@app.route('/', methods=['GET', 'POST'])
def buscar_gifs():
    gifs = []
    query = ""

    if request.method == 'POST':
        query = request.form['query']
        giphy_url = "https://api.giphy.com/v1/gifs/search"
        params = {
            "api_key": GIPHY_API_KEY,
            "q": query,
            "limit": 10,
            "rating": "pg"
        }

        response = requests.get(giphy_url, params=params)
        if response.status_code == 200:
            data = response.json()
            gifs = [
                f"https://media.giphy.com/media/{gif['id']}/giphy.gif"
                for gif in data["data"]
            ]

    return render_template("index.html", gifs=gifs, query=query)

# Rota para enviar o e-mail
@app.route('/enviar_email', methods=['POST'])
def enviar_email():
    if request.method == 'POST':
        destinatario = request.form['destinatario']
        assunto = request.form['assunto']
        corpo = request.form['corpo']

        # Criando o objeto de mensagem
        msg = Message(assunto,
                      recipients=[destinatario])
        msg.body = corpo

        try:
            # Enviando o e-mail
            mail.send(msg)
            return "E-mail enviado com sucesso!"
        except Exception as e:
            return f"Ocorreu um erro: {e}"

# Rota para a página de envio de e-mail
@app.route('/mail')
def pagina_email():
    return render_template('mail.html')

if __name__ == '__main__':
    app.run(debug=True)
