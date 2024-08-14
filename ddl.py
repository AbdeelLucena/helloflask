import sqlite3
from flask import g
from Globals import DATABASE_NAME

#  conexão com o banco de dados
def get_db(): 
    db = getattr(g, '_database', None)  
                                        
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_NAME) # O objeto g é usado para armazenar dados.
        db.row_factory = sqlite3.Row
    return db


def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: # Função para fechar conexão com banco de dados quando o contexto termina
        db.close()

def init_db():
    db = get_db()
    with open('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit() 
# Função para inicializar o banco de dado
