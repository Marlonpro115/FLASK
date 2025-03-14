from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.secret_key = "clave_secreta"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/mcdonalddatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    imagen = db.Column(db.String(255), nullable=False)
    productos = db.relationship('Producto', backref='categoria', lazy=True)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primer_nombre = db.Column(db.String(50), nullable=False)
    segundo_nombre = db.Column(db.String(50), nullable=True)
    primer_apellido = db.Column(db.String(50), nullable=False)
    segundo_apellido = db.Column(db.String(50), nullable=True)
    tipo_documento = db.Column(db.Enum("DNI", "Pasaporte", "Cedula", "Otro"), nullable=False)
    numero_documento = db.Column(db.String(20), unique=True, nullable=False)
    pais_origen = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())
    rol = db.Column(db.String(20), nullable=False, default='usuario')
    
class Sucursal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    horario_atencion = db.Column(db.String(50), nullable=False)
    empleados = db.relationship('Empleado', backref='sucursal', cascade='all, delete', lazy=True)
    ventas = db.relationship('Venta', backref='sucursal', cascade='all, delete', lazy=True)

class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefono = db.Column(db.String(15), nullable=True)
    cargo = db.Column(db.Enum('Cajero', 'Cocinero', 'Gerente', 'Supervisor', 'Limpieza', 'Repartidor'), nullable=False)
    sucursal_id = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    salario = db.Column(db.Numeric(10,2), nullable=False)
    fecha_contratacion = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(50), nullable=True)
    estado = db.Column(db.Enum('Activo', 'Inactivo'), default='Activo', nullable=False)
    ventas = db.relationship('Venta', backref='empleado', cascade='all, delete', lazy=True)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    telefono = db.Column(db.String(15), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    ciudad = db.Column(db.String(100), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())
    ventas = db.relationship('Venta', backref='cliente', cascade='all, delete', lazy=True)

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=True)
    sucursal_id = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    fecha_venta = db.Column(db.DateTime, default=db.func.current_timestamp())
    total = db.Column(db.Numeric(10,2), nullable=False)
    metodo_pago = db.Column(db.Enum('Efectivo', 'Tarjeta', 'Transferencia'), nullable=False)

# Crear las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

    # Insertar categorías si no existen
    categorias_data = [
        ("Hamburguesas", "img/hamburguesa.png"),
        ("Papas Fritas", "img/papas.png"),
        ("Bebidas", "img/bebidas.png"),
        ("Postres", "img/postres.png"),
        ("Combos", "img/combos.png"),
        ("Desayunos", "img/desayunos.png"),
    ]

    for nombre, imagen in categorias_data:
        if not Categoria.query.filter_by(nombre=nombre).first():
            db.session.add(Categoria(nombre=nombre, imagen=imagen))
    
    db.session.commit()

    # Insertar productos de ejemplo si no existen
    productos_data = [
        ("Big Mac", "Hamburguesa con carne de res y salsa especial", 5.99, "img/bigmac.png", "Hamburguesas"),
        ("McNuggets", "Porción de 10 piezas de nuggets de pollo", 4.99, "img/nuggets.png", "Combos"),
        ("Papas Grandes", "Papas fritas crujientes", 2.99, "img/papas_grandes.png", "Papas Fritas"),
        ("Coca Cola", "Refresco de cola 500ml", 1.99, "img/coca.png", "Bebidas"),
        ("Sundae", "Helado de vainilla con cobertura", 2.49, "img/sundae.png", "Postres"),
        ("McMuffin", "Sandwich de huevo y queso", 3.49, "img/mcmuffin.png", "Desayunos"),
    ]

    for nombre, descripcion, precio, imagen, categoria_nombre in productos_data:
        categoria = Categoria.query.filter_by(nombre=categoria_nombre).first()
        if categoria and not Producto.query.filter_by(nombre=nombre).first():
            db.session.add(Producto(nombre=nombre, descripcion=descripcion, precio=precio, imagen=imagen, categoria_id=categoria.id))

    db.session.commit()

@app.route("/")
@app.route("/menu")
def menu():
    categorias = Categoria.query.all()
    return render_template("index.html", categorias=categorias)

@app.route("/productos/<int:categoria_id>")
def productos_por_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    productos = Producto.query.filter_by(categoria_id=categoria_id).all()
    return render_template("productos.html", categoria=categoria, productos=productos)

def obtener_usuario(usuario):
    """Busca un usuario en la base de datos por su email."""
    return Usuario.query.filter_by(email=usuario).first()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("usuario")
        contraseña = request.form.get("password")
        rol = request.form.get("rol")

        usuario = obtener_usuario(email)  # Obtener usuario desde la base de datos

        if usuario is None:
            flash("Usuario no encontrado", "danger")
        elif not check_password_hash(usuario.password_hash, contraseña):
            flash("Contraseña incorrecta", "danger")
        elif usuario.rol != rol:
            flash("Rol incorrecto", "danger")
        else:
            # Guardar el primer nombre del usuario en la sesión
            session["usuario"] = usuario.primer_nombre  
            session["rol"] = usuario.rol
            flash("Inicio de sesión exitoso", "success")

            return redirect(url_for("dashboard"))

    return render_template("login.html", page="login")

@app.route("/recuperacion")
def recuperacion():
    return render_template("recuperacion.html", page="recuperacion")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        primer_nombre = request.form["primer_nombre"]
        segundo_nombre = request.form.get("segundo_nombre", None)
        primer_apellido = request.form["primer_apellido"]
        segundo_apellido = request.form.get("segundo_apellido", None)
        tipo_documento = request.form["tipo_documento"]
        numero_documento = request.form["numero_documento"]
        pais_origen = request.form["pais_origen"]
        email = request.form["email"]
        telefono = request.form.get("telefono", None)
        password = request.form["password"]
        rol = request.form.get("rol", "usuario")  # Valor por defecto: usuario

        # Verificar si el email o documento ya existen
        if Usuario.query.filter((Usuario.email == email) | (Usuario.numero_documento == numero_documento)).first():
            flash("El email o número de documento ya están registrados", "danger")
            return redirect(url_for("registro"))

        # Verificar si el rol es válido
        if rol not in ["usuario", "admin"]:
            flash("Rol inválido", "danger")
            return redirect(url_for("registro"))

        # Encriptar la contraseña antes de guardarla
        password_hash = generate_password_hash(password)

        # Crear nuevo usuario con la contraseña hasheada
        nuevo_usuario = Usuario(
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            pais_origen=pais_origen,
            email=email,
            telefono=telefono,
            password_hash=password_hash,
            rol=rol  # Guardar el rol correctamente
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Registro exitoso, ahora puedes iniciar sesión", "success")
        return redirect(url_for("login"))

    return render_template("registro.html", page="registro")

@app.route("/logout")
def logout():
    session.clear()  # Elimina todos los datos de la sesión
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        flash("Debes iniciar sesión primero", "warning")
        return redirect(url_for("login"))

    return render_template("dashboard/dashboard.html", page="dashboard", usuario=session["usuario"])

@app.route('/productos')
def productos():
    categorias = Categoria.query.all()
    return render_template('productos.html', categorias=categorias, page="productos")

@app.route("/menu_categorias")
def menu_categorias():
    categorias = Categoria.query.all()
    return render_template("menu_categorias.html", categorias=categorias, page="menu_categorias")

@app.route("/gestionar_categoria/<int:categoria_id>")
def gestionar_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    return render_template("gestionar_categoria.html", categoria=categoria)

# Categorias

@app.route("/actualizar_producto/<int:producto_id>", methods=["POST"])
def actualizar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)

    nombre = request.form["nombre"]
    precio = request.form["precio"]

    producto.nombre = nombre
    producto.precio = float(precio)

    db.session.commit()
    flash("Producto actualizado correctamente", "success")

    return redirect(url_for("gestionar_categoria", categoria_id=producto.categoria_id))

@app.route("/agregar_producto", methods=["GET", "POST"])
def agregar_producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        categoria_id = int(request.form["categoria_id"])  # Asegúrate de pasar esta info en el formulario

        nuevo_producto = Producto(nombre=nombre, precio=precio, categoria_id=categoria_id)

        db.session.add(nuevo_producto)
        db.session.commit()
        flash("Producto agregado correctamente", "success")

        return redirect(url_for("categoria_productos", categoria_id=categoria_id))

    categorias = Categoria.query.all()  # Para mostrar en el formulario
    return render_template("agregar_producto.html", categorias=categorias)

@app.route("/editar_producto/<int:producto_id>", methods=["GET", "POST"])
def editar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)  # Busca el producto, si no existe, devuelve 404

    if request.method == "POST":
        producto.nombre = request.form["nombre"]
        producto.precio = float(request.form["precio"])

        db.session.commit()
        flash("Producto actualizado correctamente", "success")

        return redirect(url_for("categoria_productos", categoria_id=producto.categoria_id))

    return render_template("editar_producto.html", producto=producto)

@app.route("/categoria/<int:categoria_id>")
def categoria_productos(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)  # Obtiene la categoría o muestra error 404
    productos = Producto.query.filter_by(categoria_id=categoria_id).all()  # Obtiene los productos de la categoría

    return render_template("categoria_productos.html", categoria=categoria, productos=productos)

# Separador #
@app.route("/eliminar_producto/<int:producto_id>", methods=["POST"])
def eliminar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    categoria_id = producto.categoria_id
    db.session.delete(producto)
    db.session.commit()
    flash("Producto eliminado correctamente", "info")
    return redirect(url_for("gestionar_categoria", categoria_id=categoria_id))

@app.route('/empleados')
def empleados():
    empleados = Empleado.query.all()
    return render_template('dashboard/empleados/empleados.html', empleados=empleados, page="empleados")

@app.route('/agregar_empleado', methods=['GET', 'POST'])
def agregar_empleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form.get('telefono')
        cargo = request.form['cargo']
        sucursal_id = request.form['sucursal_id']
        salario = request.form['salario']
        fecha_contratacion = request.form['fecha_contratacion']
        horario = request.form.get('horario')
        estado = request.form['estado']

        # Crear nuevo empleado
        nuevo_empleado = Empleado(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            cargo=cargo,
            sucursal_id=sucursal_id,
            salario=salario,
            fecha_contratacion=fecha_contratacion,
            horario=horario,
            estado=estado
        )

        db.session.add(nuevo_empleado)
        db.session.commit()
        flash('Empleado agregado exitosamente', 'success')
        return redirect(url_for('empleados'))

    # Obtener todas las sucursales para el formulario
    sucursales = Sucursal.query.all()
    return render_template('dashboard/empleados/agregar_empleado.html', sucursales=sucursales, page="agregar_empleado")

@app.route('/editar_empleado/<int:empleado_id>', methods=['GET', 'POST'])
def editar_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    sucursales = Sucursal.query.all()  # Obtener todas las sucursales para el select

    if request.method == 'POST':
        empleado.nombre = request.form['nombre']
        empleado.apellido = request.form['apellido']
        empleado.email = request.form['email']
        empleado.telefono = request.form['telefono']
        empleado.cargo = request.form['cargo']
        empleado.sucursal_id = request.form['sucursal_id']
        empleado.salario = request.form['salario']
        empleado.fecha_contratacion = request.form['fecha_contratacion']
        empleado.horario = request.form['horario']
        empleado.estado = request.form['estado']

        try:
            db.session.commit()
            flash('Empleado actualizado correctamente', 'success')
            return redirect(url_for('empleados'))  # Redirige a la lista de empleados
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el empleado: {str(e)}', 'danger')

    return render_template('dashboard/empleados/editar_empleado.html', empleado=empleado, sucursales=sucursales, page="editar_empleado")

@app.route('/eliminar_empleado/<int:empleado_id>', methods=['POST'])
def eliminar_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    
    try:
        db.session.delete(empleado)
        db.session.commit()
        flash(f'Empleado {empleado.nombre} {empleado.apellido} eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el empleado.', 'danger')
    
    return redirect(url_for('empleados'))

@app.route('/clientes')
def clientes():
    clientes = Cliente.query.all()
    return render_template('dashboard/clientes/clientes.html', clientes=clientes, page="clientes")

@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        ciudad = request.form.get('ciudad')

        # Crear nuevo cliente
        nuevo_cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            direccion=direccion,
            ciudad=ciudad
        )

        db.session.add(nuevo_cliente)
        db.session.commit()
        flash('Cliente agregado exitosamente', 'success')
        return redirect(url_for('clientes'))

    return render_template('dashboard/clientes/agregar_cliente.html', page="agregar_cliente")

@app.route('/editar_cliente/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)

    if request.method == 'POST':
        try:
            cliente.nombre = request.form['nombre']
            cliente.apellido = request.form['apellido']
            cliente.email = request.form.get('email')
            cliente.telefono = request.form.get('telefono')
            cliente.direccion = request.form.get('direccion')
            cliente.ciudad = request.form.get('ciudad')

            db.session.commit()
            flash('Cliente actualizado correctamente', 'success')
            return redirect(url_for('clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el cliente: {str(e)}', 'danger')

    return render_template('dashboard/clientes/editar_cliente.html', cliente=cliente, page="editar_cliente")

@app.route('/eliminar_cliente/<int:cliente_id>', methods=['POST'])
def eliminar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash(f'Cliente {cliente.nombre} {cliente.apellido} eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el cliente.', 'danger')
    
    return redirect(url_for('clientes'))

@app.route('/sucursales')
def sucursales():
    sucursales = Sucursal.query.all()
    return render_template('dashboard/sucursales/sucursales.html', sucursales=sucursales, page="sucursales")

@app.route('/agregar_sucursal', methods=['GET', 'POST'])
def agregar_sucursal():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        telefono = request.form['telefono']
        horario_atencion = request.form['horario_atencion']

        nueva_sucursal = Sucursal(
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            telefono=telefono,
            horario_atencion=horario_atencion
        )

        db.session.add(nueva_sucursal)
        db.session.commit()
        flash('Sucursal agregada exitosamente', 'success')
        return redirect(url_for('sucursales'))

    return render_template('dashboard/sucursales/agregar_sucursal.html', page="agregar_sucursal")

@app.route('/editar_sucursal/<int:sucursal_id>', methods=['GET', 'POST'])
def editar_sucursal(sucursal_id):
    sucursal = Sucursal.query.get_or_404(sucursal_id)

    if request.method == 'POST':
        try:
            sucursal.nombre = request.form['nombre']
            sucursal.direccion = request.form['direccion']
            sucursal.ciudad = request.form['ciudad']
            sucursal.telefono = request.form['telefono']
            sucursal.horario_atencion = request.form['horario_atencion']

            db.session.commit()
            flash('Sucursal actualizada correctamente', 'success')
            return redirect(url_for('sucursales'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la sucursal: {str(e)}', 'danger')

    return render_template('dashboard/sucursales/editar_sucursal.html', sucursal=sucursal, page="editar_sucursal")

@app.route('/eliminar_sucursal/<int:sucursal_id>', methods=['POST'])
def eliminar_sucursal(sucursal_id):
    sucursal = Sucursal.query.get_or_404(sucursal_id)
    
    try:
        db.session.delete(sucursal)
        db.session.commit()
        flash(f'Sucursal {sucursal.nombre} eliminada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la sucursal.', 'danger')
    
    return redirect(url_for('sucursales'))

@app.route('/ventas')
def ventas():
    ventas = Venta.query.all()
    return render_template('dashboard/ventas/ventas.html', ventas=ventas, page="ventas")

@app.route('/agregar_venta', methods=['GET', 'POST'])
def agregar_venta():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        empleado_id = request.form.get('empleado_id')
        sucursal_id = request.form['sucursal_id']
        total = request.form['total']
        metodo_pago = request.form['metodo_pago']

        nueva_venta = Venta(
            cliente_id=cliente_id,
            empleado_id=empleado_id,
            sucursal_id=sucursal_id,
            total=total,
            metodo_pago=metodo_pago
        )

        db.session.add(nueva_venta)
        db.session.commit()
        flash('Venta agregada exitosamente', 'success')
        return redirect(url_for('ventas'))

    # Obtener datos de la base de datos para la plantilla
    sucursales = Sucursal.query.all()
    empleados = Empleado.query.all()
    clientes = Cliente.query.all()

    return render_template(
        'dashboard/ventas/agregar_venta.html',
        sucursales=sucursales,
        empleados=empleados,
        clientes=clientes,
        page="agregar_venta"
    )

@app.route('/editar_venta/<int:venta_id>', methods=['GET', 'POST'])
def editar_venta(venta_id):
    venta = Venta.query.get_or_404(venta_id)

    if request.method == 'POST':
        try:
            venta.cliente_id = request.form.get('cliente_id')
            venta.empleado_id = request.form.get('empleado_id')
            venta.sucursal_id = request.form['sucursal_id']
            venta.total = request.form['total']
            venta.metodo_pago = request.form['metodo_pago']

            db.session.commit()
            flash('Venta actualizada correctamente', 'success')
            return redirect(url_for('ventas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la venta: {str(e)}', 'danger')

    return render_template('dashboard/ventas/editar_venta.html', venta=venta, page="editar_venta")

@app.route('/eliminar_venta/<int:venta_id>', methods=['POST'])
def eliminar_venta(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    
    try:
        db.session.delete(venta)
        db.session.commit()
        flash(f'Venta {venta.id} eliminada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la venta.', 'danger')
    
    return redirect(url_for('ventas'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)