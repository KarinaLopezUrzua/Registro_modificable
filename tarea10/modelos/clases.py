from tarea10.config.mysqlconnection import conectarMySQL

class Usuarios:
    def __init__(self, data): #en cada uno de los atributos de objetos estamos almacenando el valor de la clave de ese diccionario que obtenemos de la bd de nuestra tabla 
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.update_at = data["upgrate_at"] #lo anote mal en la tabla que realice

    @classmethod # ahora usamos métodos de clase para consultar o leer nuestra base de datos. NADA MAS
    def obtener_todo(cls):
        query = "SELECT * FROM usuarios;" #aqui llamamos a la tabla e nuestra base de datos
        results = conectarMySQL('usuarios_schema').query_db(query) #result serian un diccionario en donde conectamos con el nombre de nuestra base de datos y  vamos a llamar a la función conectarMySQL con el esquema al que te diriges
        
        usuarios_instancias = []   # creamos una lista vacía para agregar nuestras instancias de usuarios
        for usuario_variable in results: # Iterar sobre los resultados de la base de datos y crear instancias de usuarios_instancias con cls
            usuarios_instancias.append(cls(usuario_variable)) #convertimos una lista de diccionarios en una lista de objetos
        return usuarios_instancias #retornamos una lista de objetos, lo transformamos a un objeto para poder usarlo en logica compleja desde html

#METODO CREATE con INSERT
    @classmethod
    def registro_usuario(cls, data): #(nombre de las columnas en nuestra tabla y en VALUES nombre de las claves de nuestro diccionario del controlador de forma sanitizada)
        query = """INSERT INTO usuarios (nombre, apellido, email) 
        VALUES(%(nombre)s, %(apellido)s, %(email)s);""" #se coloca al final NOW(), NOW()), solo si por defecto nuesrta tabla no lo tiene predeterminado y arriba created_at y update_at
        return conectarMySQL('usuarios_schema').query_db(query, data)
#no es necesario transformsarlo en objeto ya que solo estamos guardando informacion

#para obtener un usuario a traves de su id
    @classmethod  # ahora usamos métodos de clase para consultar nuestra base de datos de forma sanitizada
    def obtener_un_usuario(cls, data):
        query = "SELECT * FROM usuarios WHERE id=%(id_usuario)s;" #aca la variable que queremos es el WHERE id=1 (2 o 3, etc), debemos sanitizarla con % y s
        results =  conectarMySQL('usuarios_schema').query_db(query, data)
        return cls(results[0]) #aca retorna solo el diccionario, no objetos

#update para modificar un usuario
    @classmethod
    def editar_usuario(cls,data):
        query = "UPDATE usuarios SET nombre=%(nombre)s, apellido=%(apellido)s, email=%(email)s, upgrate_at = NOW() WHERE id=%(id)s" #esta mal escrito pq asi lo puse en la tabla upgrate
        return conectarMySQL('usuarios_schema').query_db(query, data)

#METODO DELETE, eliminar un usuario 
    @classmethod
    def eliminar_usuario(cls,data):
        query = "DELETE FROM usuarios WHERE id=%(id_usuario)s;"
        return conectarMySQL('usuarios_schema').query_db(query, data)