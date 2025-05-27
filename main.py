from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
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
        if response.status_code == 200:  # <-- CORRETO
            data = response.json()
            gifs = [
                f"https://media.giphy.com/media/{gif['id']}/giphy.gif"
                for gif in data["data"]
            ]

    return render_template("index.html", gifs=gifs, query=query)

if __name__ == '__main__':
    app.run(debug=True)
