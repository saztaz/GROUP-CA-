from flask import,  render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root$@123'
app.config['MYSQL_DB'] = 'covid'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/contact_tracings')
def contact_tracings():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM survey")
    contact_tracings = cur.fetchall()
    if result > 0:
        return render_template('responses.html', contact_tracings=contact_tracings)
    else:
        msg = 'No Recent Activities Found'
        return render_template('responses.html', msg=msg)
    cur.close()
@app.route('/contact_tracings/<string:id>/')
def contact_tracing(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM survey WHERE id = %s", [id])
    contact_tracing = cur.fetchone()
    return render_template('response.html', contact_tracing=contact_tracing)
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        mysql.connection.commit()
        cur.close()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username= request.form['username']
        password_candidate= request.form['password']
        
        cur = mysql.connection.cursor()

        result= cur.execute("SELECT * FROM users WHERE username = %s", [username])


if result> 0:
    data=cur.fetchone()
    password= data['password']
    
    if sha256_crypt.verify(password_candidate, password):
        session['logged_in'] = True
        session['username'] = username
        
        flash('You are now logged in', 'success')
        return redirect(url_for('dashboard'))

    else:
         error = 'Invalid login'
         return render_template('login.html', error=error)
         cur.close()






    
        




