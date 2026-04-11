import sqlite3

def get_db():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = get_db()
    cur = con.cursor()
    cur.execute("CREATE TABLE if not exists cats(id INTEGER PRIMARY KEY AUTOINCREMENT, cat_name TEXT, cat_age INTEGER, cat_breed TEXT, contact TEXT, image TEXT, user_id INTEGER)")
    cur.execute("CREATE TABLE if not exists accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT)")
    con.commit()
    con.close()

def add_cat(cat_name, cat_age, cat_breed, contact, image, user_id):
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO cats (cat_name, cat_age, cat_breed, contact, image, user_id) VALUES (?, ?, ?, ?, ?, ?)", (cat_name, cat_age, cat_breed, contact, image, user_id))
    con.commit()
    con.close()

def add_account(username, password, email):
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO accounts (username, password, email) VALUES (?, ?, ?)", (username, password, email))
    con.commit()
    con.close()

