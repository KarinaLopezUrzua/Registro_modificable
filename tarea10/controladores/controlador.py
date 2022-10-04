from tarea10 import app
from flask import render_template, redirect, session, request 
from tarea10.modelos.clases import Usuarios

#RUTAS FORMULARIO READ
@app.route("/") 
def formulario():
    return render_template("formulario.html") #Pagina inicio se dirige a html hijo

#RUTA CREAD
@app.route("/crear", methods=["POST"]) #ruta que se redigire action del formulario
def crear_usuario():
    datos = { #creamos un diccionario que obtendra la informacion de nuestro formulario
        "nombre":request.form["nombre"], #["nombre"] es el name que se coloco en el imput del formulario
        "apellido":request.form["apellido"],
        "email":request.form["email"],
    }
    print(datos)
    id_usuario = Usuarios.registro_usuario(datos) #le agregamos una variable para poder retornar un numero y asi traquear al usuario para darle seguimiento con session. se llama al metodo para guardar la informacion en la base de datos
    print(id_usuario)
    session["id_usuario"] = id_usuario #estamos almacenando la variable en una clave
    return redirect("/todo") #se redirige a la pagina donde se muestra la informacion del usuario

#queremos validar si el usuario esta registrado y tiene se session activa, solo ahi podra tener acceso a la pagina /todo

""" COMENTADO PARA QUE NO NOS PIDA A CADA RATO UN NUEVO USUARIO
@app.route("/todo") 
def todos_los_usuarios():
    if "id_usuario" not in session:
        return redirect("/")
    todos_los_usuarios = Usuarios.obtener_todo()
    return render_template("info_usuario.html", lista_usuarios=todos_los_usuarios) #abre html hijo con todos los resultados 
"""

@app.route("/todo") 
def todos_los_usuarios():
    todos_los_usuarios = Usuarios.obtener_todo()
    return render_template("info_usuario.html", lista_usuarios=todos_los_usuarios) #abre html hijo con todos los resultados 

#ruta read para mostrar la informacion de un usuario
@app.route("/usuario/<int:id_usuario>")
def ver_usuario(id_usuario):
    datos = {
        "id_usuario": id_usuario
    }
    ver_un_usuario = Usuarios.obtener_un_usuario(datos)
    return render_template("info_un_usuario.html", ver_un_usuario=ver_un_usuario)

#ruta MIXTA para modificar los datos del usuario (se puede realizar en 2 rutas distintas)
@app.route("/editar/<int:id_usuario>", methods=["GET","POST"]) #va a recibir 2 metodos
def editar_usuario(id_usuario):
    if request.method == "GET": #si entra un metodo get, se entra a esta linea y se obtienen los datos del usuario para modificarlos
        datos = {
        "id_usuario": id_usuario
        }
        ver_un_usuario = Usuarios.obtener_un_usuario(datos)
        return render_template("formulario_modificar.html", ver_un_usuario=ver_un_usuario)
    datos = {
        "nombre":request.form["nombre"], #["nombre"] es el name que se coloco en el imput del formulario
        "apellido":request.form["apellido"],
        "email":request.form["email"],
        "id":id_usuario
    }
    Usuarios.editar_usuario(datos) #una vez modificado entrara a la tabla y se mostrara en la pagina
    return redirect("/todo")

#ruta para eliminar un usuario
@app.route("/borrar/<int:id_usuario>")
def borrar_usuario(id_usuario):
    datos={
        "id_usuario": id_usuario
    }
    Usuarios.eliminar_usuario(datos)
    return redirect("/todo")

@app.errorhandler(404)
def pagina_no_encontrada():
    return  'ESTA RUTA NO FUE ENCONTRADA', 404  
