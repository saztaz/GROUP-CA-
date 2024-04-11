from flask import Flask
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

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

@app.route('/take_survey', methods=['GET', 'POST'])
@is_logged_in
def add_question():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        any_recent_travel = form.any_recent_travel.data
        same_symptoms = form.same_symptoms.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO survey(name, age, phone, symptoms, symptops_started, closeness, other_medical_issues, family_members, any_recent_travel, same_symptoms) VALUES(%s, %s, %s,%s, %s, %s, %s, %s, %s, %s)", (name, age, phone, symptoms, symptops_started, closeness, other_medical_issues, family_members, any_recent_travel, same_symptoms))
        mysql.connection.commit()
        cur.close()
        flash('Response Submitted', 'success')
        return redirect(url_for('dashboard'))
    return render_template('take_survey.html', form=form)

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
