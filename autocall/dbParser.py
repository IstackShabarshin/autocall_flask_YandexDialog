import sqlite3
import time

DATABASE = 'autocall/data/session.db'
LIFETIME = 120 # время жизни записи в секундах

def createTable():
    conn = sqlite3.connect(DATABASE)
    with conn:
        cursor = conn.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS sessions
                       (id text, state text, life_time integer)
                       """)
        conn.commit()

def deleteTable():
    conn = sqlite3.connect(DATABASE)
    with conn:
        cursor = conn.cursor()
        cursor.execute(""" TRUNCATE TABLE sessions """)
        conn.commit()

def selectId(id):
    conn = sqlite3.connect(DATABASE)
    with conn:
        cursor = conn.cursor()
        deleteDeath(conn, cursor)
        sql = "SELECT state FROM sessions WHERE id=?"
        cursor.execute(sql, [str(id)])
        return cursor.fetchone()[0]

def insertSession(id, state):
    conn = sqlite3.connect(DATABASE)
    with conn:
        cursor = conn.cursor()
        deleteDeath(conn, cursor)
        sql = "INSERT INTO sessions VALUES (?, ?, ?)"
        cursor.execute(sql, [str(id), str(state), time.time() + LIFETIME])
        conn.commit()

def changeState(id, state):
    conn = sqlite3.connect(DATABASE)
    with conn:
        cursor = conn.cursor()
        deleteDeath(conn, cursor)
        sql = "UPDATE sessions SET state = ?, life_time = ? WHERE id = ?" 
        cursor.execute(sql, [state, time.time() + LIFETIME ,id])
        conn.commit()

def deleteSession(id):
    conn = sqlite3.connect(DATABASE)
    with conn:
        cursor = conn.cursor()
        sql = "DELETE FROM sessions WHERE id = ?"
        cursor.execute(sql, [id])
        conn.commit()

def deleteDeath(conn, cursor):
    with conn:
        sql = "DELETE FROM sessions WHERE life_time < ?"
        cursor.execute(sql, [time.time()])
        conn.commit()

def _selectAll():
    conn = sqlite3.connect(DATABASE)
    with conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM sessions"
        cursor.execute(sql)
        return cursor.fetchall()
