from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/menu")
def menu():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/recuperacion")
def recuperacion():
    return render_template("recuperacion.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)