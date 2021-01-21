import sqlite3
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route('/')
def index():
    conn = get_db_connection()

    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template("home.html", users=users)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.hash(str(form.password.data))
        print(str(form.password.data)+': '+password)
        conn = get_db_connection()
        users = conn.execute("INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)",
                             (name, email, username, password))
        conn.commit()
        conn.close()

        flash("Registration done!!", "success")
        return redirect(url_for('index'))

        return render_template("register.html", users=users)

    return render_template('register.html', form=form)

# User Login


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password = request.form['password']

        # Create cursor
        conn = get_db_connection()
        cur = conn.cursor()

        # Get user by username
        find_user = ("SELECT * FROM users WHERE email = ?")
        cur.execute(find_user, [email])
        results = cur.fetchone()
        if results:
            if sha256_crypt.verify(password, results['password']):
                # Passed
                session["logged_in"] = True
                session["email"] = email
                session["name"] = results['name']

                flash("You are now logged in.", "success")
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid login"
                return render_template("login.html", error=error)
            # Cose connection
            cur.close()

        else:
            error = "Email not found."
            return render_template("login.html", error=error)

    return render_template('login.html')

# check if user is logged in


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorised , Please login", 'danger')
            return redirect(url_for("login"))
    return wrap


# logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logout.", "success")
    return redirect(url_for("login"))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)
