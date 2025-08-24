from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal
@app.route("/")
def home():
    return render_template("index.html")

# Ruta dinámica con nombre
@app.route("/usuario/<nombre>")
def usuario(nombre):
    return render_template("usuario.html", nombre=nombre)

# Otra ruta estática
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

   
    