from flask import Flask, render_template, request, redirect, flash
import controlador_juegos

app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route("/")
@app.route("/juegos")
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

@app.route("/agregar_juego")
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]

    if not nombre or not descripcion or not precio:
        flash("Todos los campos son obligatorios", "error")
        return redirect("/agregar_juego")
    
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    flash("Juego agregado exitosamente", "success")
    return redirect("/juegos")

@app.route("/eliminar_juego", methods=["POST"])
def eliminar_juego():
    id = request.form["id"]
    controlador_juegos.eliminar_juego(id)
    flash("Juego eliminado exitosamente", "success")
    return redirect("/juegos")

@app.route("/formulario_editar_juego/<int:id>")
def formulario_editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    if not juego:
        flash("Juego no encontrado", "error")
        return redirect("/juegos")
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
def actualizar_juego():
    # Recibir datos del formulario
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]

    # Validar campos
    if not id or not nombre or not descripcion or not precio:
        flash("Todos los campos son obligatorios", "error")
        return redirect(f"/formulario_editar_juego/{id}")

    # Actualizar el juego
    controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
    flash("Juego actualizado exitosamente", "success")
    return redirect("/juegos")

@app.route("/formulario_editar_juego/<int:id>")
def editar_juego(id):
    # Obtener el juego por ID
    juego = controlador_juegos.obtener_juego_por_id(id)
    if not juego:
        flash("Juego no encontrado", "error")
        return redirect("/juegos")
    return render_template("editar_juego.html", juego=juego)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)