from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

@app.route("/")
def index():
    url = "https://pokeapi.co/api/v2/pokemon?limit=20"
    response = requests.get(url)
    data = response.json()["results"]

    pokemons = []
    for item in data:
        detail = requests.get(item["url"]).json()
        pokemons.append({
            "name": detail["name"],
            "image": detail["sprites"]["front_default"]
        })

    return render_template("index.html", pokemons=pokemons)

@app.route("/search")
def search():
    name = request.args.get("name", "").strip().lower()
    if name:
        return redirect(f"/pokemon/{name}")
    else:
        return render_template("index.html", pokemons=[], error="Por favor, ingresa un nombre válido.")

@app.route("/pokemon/<name>")
def pokemon_detail(name):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        response = requests.get(url)
        pokemon = response.json()
        return render_template("detalle.html", pokemon=pokemon)
    except:
        return render_template("index.html", pokemons=[], error="¡Pokémon no encontrado!")

if __name__ == "__main__":
    app.run(debug=True)
