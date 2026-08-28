import sqlite3

from fastapi import FastAPI
app=FastAPI()
conn=sqlite3.connect("Pandit.db",check_same_thread=False)

Cursor=conn.cursor()

Cursor.execute("""



CREATE TABLE IF NOT EXISTS Todos (
id INTEGER PRIMARY KEY,
Title TEXT
Completed TEXT
)

""")
conn.commit()


@app.get("/")
def connection_sql():
    return {
        "Message":"Jai shree ram"
    }
