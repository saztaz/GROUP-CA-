from flask import,  render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)





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
        
       



