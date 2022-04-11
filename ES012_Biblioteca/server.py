from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True

books = [
    {
        "id": 0,
        "title": "Il nome della Rosa",
        "author": "Umberto Eco",
        "year_published": '1980'
    },
    {
        "id": 1,
        "title": "Il problema dei tre corpi",
        "author": "Liu Cixin",
        "year_published": '2008'
    },
    {
        "id": 2,
        "title": "Fondazione",
        "author": "Isaac Asimov",
        "year_published": '1951'
    }
]


@app.route("/", methods=["GET"])
def home():
    return "<h1>Biblioteca online</h1><p>Prototipo di web API.</p>"


@app.route("/api/v1/resources/books/all", methods=["GET"])
def api_all():
    return jsonify(books)


@app.route("/api/v1/resources/books", methods=["GET"])
def api_id():
    if "id" in request.args:
        id = int(request.args["id"])
    else:
        return "Error: No id field provided. Please specify"

    results = []

    con = sqlite3.connect('./libri.db')
    cur = con.cursor()
    # selezione riga casuale da tabellastati
    cur.execute(f"SELECT * FROM Libro WHERE ID={id};")
    libro = cur.fetchall()
    for row in libro:
        ID = row[0]
        Title = row[1]
        Author = row[2]
        Year = row[3]
    print(ID, Title, Author,Year)
    results=[ID,Title,Author,Year]

    return jsonify(results)


app.run()