import os

import MySQLdb

db = MySQLdb.connect(
    host="cat-app1-abv-fe39.i.aivencloud.com",
    user="avnadmin",
    password = os.getenv("DB_PASSWORD"),
    database="defaultdb",
    port=19532,
    ssl={"ssl": {"ca": ""}}  
)

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
cursor.execute("SHOW TABLES")
for table in cursor.fetchall():
    print(table)

cursor.execute("SELECT * FROM cats")
rows = cursor.fetchall()
for row in rows:
    print(row)

db.commit()
db.close()


