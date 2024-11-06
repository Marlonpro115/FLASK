# SE IMPORTA EL MODULO FLASK DESDE EL PAQUETE FLASK
from flask import Flask

# Crea una instancia de la clase flask
# El argumento __name__ la dice a flask
# Que utilice el nombre del archivo actual main.py
app = Flask(__name__)

# Este es un decorador que define una ruta
# Corresponde a la pagina principal del app
@app.route("/")
# Cuando alguien visite app (por ejemplo, http://localhost:5000)
# La funcion hello() sera ejecutada
def hello():
    return "<h1>Hello, World flask! </h1>"

# Solo se ejecuta si el archivo es ejecutado directamente
# Arranca la aplicacion flask en modo de depuracion (debug=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)