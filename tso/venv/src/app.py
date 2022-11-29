from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from src.Config import config
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = 'mysecretkey'


@app.route("/")
def inicio():
    return render_template('index.html')


@app.route('/usuarios', methods=['GET'])
def listarusuarios():
    cursor = mysql.connection.cursor()
    sql = "Select * from entidadbancaria.usuarios"
    cursor.execute(sql)
    datos = cursor.fetchall()
    print(datos)
    usuarios = []
    for fila in datos:
        usuario = {'Nombre': fila[0],
                   'Apellido': fila[1], 'cedula': fila[3]}
        usuarios.append(usuario)
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/usuarios/<Nombre>', methods=['GET'])
def leer_usuarios(Nombre):
    cursor = mysql.connection.cursor()
    sql = "select * from usuarios where Nombre = '{0}'".format(Nombre)
    cursor.execute(sql)
    usuario = cursor.fetchone()
    usuarioResult = {
        'Nombre': usuario[0], 'Apellido': usuario[1], 'Direccion': usuario[2], 'Cedula': usuario[3], 'Correo': usuario[4], 'Telefono': usuario[5]}
    return render_template('ver.html', usuario=usuarioResult)


@app.route('/agregar')
def agregar():
    return render_template('agregar.html')


@app.route('/registrar_usuarios', methods=['POST'])
def registrar_usuarios():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Apellido = request.form['Apellido']
        Direccion = request.form['Direccion']
        Cedula = int(request.form['Cedula'])
        Correo = request.form['Correo']
        Telefono = int(request.form['Telefono'])
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO entidadbancaria.usuarios (Nombre,Apellido,Direccion,Cedula,Correo,Telefono) VALUES (%s,%s,%s,%s,%s,%s)', (Nombre, Apellido, Direccion, Cedula, Correo, Telefono))
        mysql.connection.commit()
        return redirect(url_for('listarusuarios'))


@app.route('/actualizar/<Cedula>', methods=['POST'])
def actualizar(Cedula):
    if request.method == 'POST':
        Direccion = request.form['Direccion']
        Correo = request.form['Correo']
        Telefono = request.form['Telefono']
        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE usuarios SET Direccion=%s, Correo=%s ,Telefono=%s where Cedula =%s""", (
            Direccion, Correo, Telefono, Cedula))
        mysql.connection.commit()
        return redirect(url_for('listarusuarios'))


@app.route('/eliminar/<Cedula>')
def eliminar_usuario(Cedula):
    cur = mysql.connection.cursor()
    sql = "DELETE FROM usuarios where Cedula ='{0}'".format(Cedula)
    cur.execute(sql)
    mysql.connection.commit()
    flash('usuario eliminado')
    return redirect(url_for('listarusuarios'))


@app.route('/editar/<Cedula>')
def actualizar_usuario(Cedula):
    cursor = mysql.connection.cursor()
    sql = "select * from usuarios where Cedula = '{0}'".format(Cedula)
    cursor.execute(sql)
    usuario = cursor.fetchone()
    usuarioResult = {
        'Nombre': usuario[0], 'Apellido': usuario[1], 'Direccion': usuario[2], 'Cedula': usuario[3], 'Correo': usuario[4], 'Telefono': usuario[5]}
    return render_template('editar.html', usuario=usuarioResult)


def pagina_no_encontrada(error):
    return "<h1>En construccion - Probando - MS - SO</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, "pagina_no_encontrada")
    app.run()
