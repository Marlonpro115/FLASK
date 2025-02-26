from flask import Flask, render_template, request, redirect, flash, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route("/")
@app.route("/menu")
def menu():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contraseña = request.form["password"]

        if usuario == "admin" and contraseña == "1234":
            session["usuario"] = usuario
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("menu"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template("login.html", page="login")

@app.route("/recuperacion")
def recuperacion():
    return render_template("recuperacion.html", page="recuperacion")

@app.route("/registro")
def registro():
    return render_template("registro.html", page="registro")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Has cerrado sesión", "info")
    return redirect(url_for("menu"))

@app.route("/dashboard")
def dashboard():  # Se cambia el nombre de la función
    return render_template("dashboard.html", page="dashboard")

@app.route("/categorias")
def categorias():
    return render_template("categorias.html", page="categorias")

@app.route("/menu_mcdonalds")
def menu_mcdonalds():
    return render_template("menu_mcdonalds.html", page="menu_mcdonalds")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)