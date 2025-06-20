# Importa copy para duplicar objetos y evitar modificar los originales
import copy

# Importa pyodbc para conectarse y trabajar con bases de datos ODBC (como Access)
import pyodbc

# Importa dataclass para definir estructuras de datos con menos código repetitivo
from dataclasses import dataclass

# Clase que maneja la conexión y operaciones con la base de datos Access
class DBConnector:
    # Constructor: se ejecuta al crear una instancia de la clase
    def __init__(self):
        # Establece la conexión a la base de datos Access usando el driver ODBC
        # Usa la ruta del archivo actual (__file__) y reemplaza el nombre del archivo por el de la base de datos
        self.__conn = pyodbc.connect(
            'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + __file__.replace("dbconnector.py", "personal.accdb")
        )
        # Crea el cursor para ejecutar comandos SQL
        self.__cursor = self.__conn.cursor()
    
    # Método para seleccionar (leer) datos desde la base de datos
    def select(self, entity: dataclass) -> list[dataclass]:
        # Ejecuta un SELECT con los campos del dataclass y el nombre de su clase como tabla
        self.__cursor.execute(
            "SELECT %s FROM %s;" % (
                ", ".join(entity.__dict__.keys()),
                entity.__class__.__name__
            )
        )
        # Crea una lista de instancias del dataclass con los datos obtenidos
        return [entity.__class__(*p) for p in list(self.__cursor)]
    
    # Método para insertar uno o más registros en la base de datos
    def insert(self, *entity: dataclass):
        # Itera sobre cada entidad a insertar
        for e in entity:
            # Si alguna entidad no es del mismo tipo que la primera, se descarta (esto es redundante realmente)
            if entity[0].__class__.__name__ != e.__class__.__name__:
                del e  # Este del no tiene efecto fuera del bucle
            else:
                # Elimina el campo 'id' para que la base de datos lo genere automáticamente
                del e.__dict__["id"]

        # Construye la sentencia INSERT con campos y signos de interrogación para los valores
        sql = "INSERT INTO {}({}) VALUES({});".format(
            entity[0].__class__.__name__,
            ", ".join(entity[0].__dict__.keys()),
            ", ".join(["?"] * len(entity[0].__dict__.values()))
        )

        # Crea una lista de listas con los valores de cada entidad
        values = [list(e.__dict__.values()) for e in entity]

        # Ejecuta múltiples inserciones con los datos
        self.__cursor.executemany(sql, values)
        # Guarda los cambios en la base de datos
        self.__conn.commit()
    
    # Método para eliminar registros por id
    def delete(self, entity: dataclass, *id: int):
        # Ejecuta un DELETE para cada id especificado
        self.__cursor.executemany(
            f"DELETE FROM {entity.__class__.__name__} WHERE id=?;",
            list(map(lambda i: [i], id))  # Convierte cada id en lista para ejecutemany
        )
        # Guarda los cambios
        self.__conn.commit()
    
    # Método para actualizar un registro existente
    def update(self, entity: dataclass):
        # Crea una copia del diccionario de atributos del objeto para no modificar el original
        e = copy.deepcopy(entity.__dict__)
        # Elimina el campo 'id' porque no se actualiza, solo se usa en la condición WHERE
        del e["id"]
        
        # Ejecuta el UPDATE con los nuevos valores
        self.__cursor.execute(
            "UPDATE " + entity.__class__.__name__ +
            " SET " + (", ".join([f + "=?" for f in e.keys()])) +
            " WHERE id=?;",
            list(e.values()) + [entity.id]  # Agrega el id al final para el WHERE
        )
        # Guarda los cambios
        self.__conn.commit()
