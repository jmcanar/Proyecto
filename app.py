from flask import Flask, render_template, request
import json, csv, os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

# ---------- Configuración SQLite ----------
Base = declarative_base()
DB_PATH = "database/usuarios.db"
engine = create_engine("sqlite:///datos.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    email = Column(String)
    segmento = Column(String)

Base.metadata.create_all(engine)

# ---------- Rutas ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    email = request.form['email']
    segmento = request.form['segmento']

    # Guardar en TXT
    with open("datos/datos.txt", "a", encoding="utf-8") as f:
        f.write(f"{nombre},{email},{segmento}\n")

    # Guardar en JSON
    nuevo_dato = {"nombre": nombre, "email": email, "segmento": segmento}
    if os.path.exists("datos/datos.json") and os.path.getsize("datos/datos.json") > 0:
        with open("datos/datos.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append(nuevo_dato)
    with open("datos/datos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # Guardar en CSV
    with open("datos/datos.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([nombre, email, segmento])

    # Guardar en SQLite
    usuario = Usuario(nombre=nombre, email=email, segmento=segmento)
    session.add(usuario)
    session.commit()

    return render_template('resultado.html', nombre=nombre)

@app.route('/ver_json')
def ver_json():
    with open("datos/datos.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"usuarios": data}

@app.route('/ver_csv')
def ver_csv():
    with open("datos/datos.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        filas = list(reader)
    return {"usuarios": filas}

@app.route('/ver_sqlite')
def ver_sqlite():
    usuarios = session.query(Usuario).all()
    return {"usuarios": [{"id": u.id, "nombre": u.nombre, "email": u.email, "segmento": u.segmento} for u in usuarios]}

if __name__ == '__main__':
    app.run(debug=True)
