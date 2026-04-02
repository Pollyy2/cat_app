from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import re
from db import get_db
import MySQLdb.cursors
load_dotenv()



# creating a flask app
app = Flask(__name__)



# configuring MySQL database connection
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_PORT'] = int(os.getenv("MYSQL_PORT"))
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
app.config['MYSQL_SSL'] = {'ssl': {}}
#configurating for photos upload
app.config['SECRET_KEY'] = '123321'
app.config['UPLOAD_FOLDER'] = 'uploads'


# defining routes for the app
@app.route('/')
# route for login page to check if the user is logged in or not
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return render_template('index.html', msg='Logged in successfully!')
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

# route for logout that removes the session data and redirects to login page
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# route for registration page to create a new account and check common errors
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            db.commit()
            msg = 'You have successfully registered!'
    return render_template('register.html', msg=msg)

# route for admin page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (session['username'],))
    account = cursor.fetchone()
    if 'loggedin' in session and session['username'] == account['username']:
        return render_template('admin.html', username=session['username'])
    return redirect(url_for('login'))

# route for user page
@app.route('/user', methods=['GET', 'POST'])
def user():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (session['username'],))
    account = cursor.fetchone()
    if 'loggedin' in session and session['username'] == account['username']:
        return render_template('user.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


      
#route for catalogue page
@app.route('/catalogue', methods=['GET', 'POST'])
def catalogue():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        cat_age = request.form['cat_age']
        cat_breed = request.form['cat_breed']
        contact = request.form['contact']
        file = request.files.get('photo')

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                'INSERT INTO cats (cat_name, cat_age, cat_breed, contact, image, user_id) VALUES (%s,%s,%s,%s,%s,%s)',
                (cat_name, cat_age, cat_breed, contact, filename, session['id'])
            )
            db.commit()
            print("INSERT OK")

        except Exception as e:
            print("INSERT ERROR:", e)

        return redirect(url_for('cats'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM cats')
    cats = cursor.fetchall()
    return render_template('catalogue.html', cats=cats)

@app.route('/cats')
def cats():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM cats')
    cats = cursor.fetchall()
    return render_template('cats.html', cats=cats)

print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
