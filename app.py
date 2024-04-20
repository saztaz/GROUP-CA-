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

        else:
         error = 'Username not found'
         return render_template('login.html', error=error)
 return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('unathorzied','please login','danger')
            return redirect(url_for(login())
    return wrap
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM survey WHERE name = %s", [session['username']])
    Responses = cur.fetchall()
    if result > 0:
        return render_template('dashboard.html', Responses=Responses)      
    else:
        msg = 'No Contact Tracing Activity Found'
        return render_template('dashboard.html', msg=msg)
    cur.close()

class ArticleForm(Form):
    name= StringField('Full Name', [validators.Length(min=1, max=200)])
    age = StringField('Age', [validators.length(min=1, max=200)])
    phone = StringField('Contact Number',[validators.length(min=1,max=15)])
    family_members = TextAreaField('Who else is in your family?', [validators.length(min=1)])
    symptoms=TextAreaField('Symptoms',[validators.length(min=5)])
    symptops_started = TextAreaField('When did you begin experiencing these symptoms?', [validators.Length(min=1)])
    closeness = TextAreaField('Have you been in close contact with someone exhibiting symptoms?',[validators.length(min=1)])
    other_medical_issues = TextAreaField('Do you have any chronic medical conditions? If so, please list them', [validators.length(min=2)])
    any_recent_travel = TextAreaField('Do you have any travel history? If yes, please provide details:', [validators.length(min=1)])
    same_symptoms = TextAreaField('Is anyone else in your household experiencing any of the same symptoms as you?', [validators.length(min=2)])

@app.route('/take_survey', methods=['GET', 'POST'])
@is_logged_in
def add_question():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        age = form.age.data
        phone = form.phone.data
        symptoms = form.symptoms.data
        symptops_started = form.symptops_started.data
        closeness = form.closeness.data
        other_medical_issues = form.other_medical_issues.data
        family_members = form.family_members.data
        any_recent_travel = form.any_recent_travel.data
        same_symptoms = form.same_symptoms.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO survey(name, age, phone, symptoms, symptops_started, closeness, other_medical_issues, family_members, any_recent_travel, same_symptoms) VALUES(%s, %s, %s,%s, %s, %s, %s, %s, %s, %s)", (name, age, phone, symptoms, symptops_started, closeness, other_medical_issues, family_members, any_recent_travel, same_symptoms))
        mysql.connection.commit()
        cur.close()
        flash('Response Submitted', 'success')
        return redirect(url_for('dashboard'))
    return render_template('take_survey.html', form=form)
  
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
                  
    





    
        




