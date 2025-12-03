import mysql.connector

def conectar():
    conn = mysql.connector.connect (
    host="localhost",
    port=3406,
    user="root",
    password="" 
    )
    return conn