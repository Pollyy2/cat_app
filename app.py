from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import SubmitField



# creating a flask app
app = Flask(__name__)



# configuring MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'poli20'  # MySql password 
app.config['MYSQL_DB'] = 'cat_app'
#configurating for photos upload
app.config['SECRET_KEY'] = '123321'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'


mysql = MySQL(app)

# defining routes for the app
@app.route('/')
# route for login page to check if the user is logged in or not
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    return render_template('register.html', msg=msg)

# route for admin page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (session['username'],))
    account = cursor.fetchone()
    if 'loggedin' in session and session['username'] == account['username']:
        return render_template('admin.html', username=session['username'])
    return redirect(url_for('admin'))

# route for user page
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
            FileRequired('File was empty!')
        ]
    )
    submit = SubmitField('Upload')
    
@app.route('/user', methods=['GET', 'POST'])
def user():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (session['username'],))
    account = cursor.fetchone()
    if 'loggedin' in session and session['username'] == account['username']:
        return render_template('user.html', username=session['username'])
    return redirect(url_for('user'))

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route('/post', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
    return render_template('post.html', form=form, file_url=file_url)


if __name__ == '__main__':
    app.run(debug=True)
