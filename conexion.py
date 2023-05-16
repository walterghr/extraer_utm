from os import remove
from sqlite3 import connect

def conectar():
    conexion = connect("coordenadas.sqlite3")
    return conexion

def borrar_db():
    try: remove("coordenadas.sqlite3")
    except: pass

def crear_tabla():
    conx = conectar()
    cursor = conx.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS puntos 
            (Punto INTEGER PRIMARY KEY AUTOINCREMENT, 
            Este REAL, Norte REAL)'''
    cursor.execute(sql)
    conx.commit()
    conx.close()

def add_punto(Este, Norte):
    conx = conectar()
    cursor = conx.cursor()
    sql = f"INSERT INTO puntos (Este, Norte) VALUES ({Este}, {Norte})"
    cursor.execute(sql)
    conx.commit()
    conx.close()