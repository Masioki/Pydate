import sqlite3


def dodaj_pytanie():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO starter_question ('content') VALUES ('pytam')")
    conn.commit()
    conn.close()

dodaj_pytanie()