import os
import MySQLdb

def get_db():
    return MySQLdb.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        ssl={"ssl": {}}
    )


def init_db():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cat_name VARCHAR(100),
        cat_age INT,
        cat_breed VARCHAR(100),
        contact VARCHAR(100),
        image VARCHAR(255),
        user_id INT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50),
        password VARCHAR(255),
        email VARCHAR(100)
    )
    """)

    db.commit()
    db.close()


