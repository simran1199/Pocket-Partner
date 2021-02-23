import sqlite3
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from scrapper import get_product_details
from hashlib import md5
from mail import send_mail
from bs4 import BeautifulSoup
import schedule
import time
import threading


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__, template_folder='Templates')
app.config['SECRET_KEY'] = 'secret123'
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True


@app.route('/')
def index():
    if "logged_in" in session:
        redirect(url_for('dashboard'))
    return render_template("home.html")


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match!!')
    ])
    confirm = PasswordField('Confirm Password')


# registration route
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
        conn.execute("INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)",
                     (name, email, username, password))
        conn.commit()
        conn.close()
        flash("You are now registered and can Login", "success")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# User-Login route
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
                session["userid"] = results['id']

                flash("You are now logged in.", "success")
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid login"
                return render_template("login.html", error=error)
            # Close connection
            cur.close()

        else:
            error = "Email not found!!"
            return render_template("login.html", error=error)

    return render_template('login.html')


# check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorised, Please login to continue!!", 'danger')
            return redirect(url_for("login"))
    return wrap


# logout route
@app.route("/logout")
def logout():
    session.clear()
    flash("You are now LoggedOut.", "warning")
    return redirect(url_for("login"))


# Add new url //links form
class LinkForm(Form):
    url = StringField('Add New Product')


def gravatar(email, size):
    digest = md5(email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


# dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    conn = get_db_connection()
    form = LinkForm(request.form)
    glink = gravatar(session['email'], 128)
    links = conn.execute('SELECT * FROM links WHERE userid = ? ORDER BY link_date DESC',
                         [session['userid']]).fetchall()
    conn.close()
    return render_template("dashboard.html", links=links, form=form, glink=glink)


# add delete
@app.route('/delete/<string:id>', methods=['POST'])
@is_logged_in
def delete_url(id):
    # Create cursor
    cur = get_db_connection()
    # Execute
    cur.execute("DELETE FROM links WHERE id = ?", [id])
    # Commit to DB
    cur.commit()
    # Close connection
    cur.close()
    flash('URL Deleted', 'danger')
    return redirect(url_for('dashboard'))


# add url route
@app.route('/add', methods=['GET', 'POST'])
@is_logged_in
def add_url():
    form = LinkForm(request.form)
    if request.method == 'POST':
        url = form.url.data
        userid = session["userid"]
        detail = get_product_details(url)
        print(detail)
        # Create cursor
        conn = get_db_connection()
        conn.execute("INSERT INTO links(url ,product, price, availability, image_url, userid) VALUES(?,?,?,?,?,?)",
                     (detail['url'], detail['name'], detail['price'], detail['availability'], detail['image_url'], userid))
        # connection commit
        conn.commit()
        conn.close()
        redirect(url_for("dashboard"))
        flash("URL Added", 'success')

    return redirect(url_for('dashboard'))


def checkFunction():
    # get db conn
    print("checkFunction Called")
    conn = get_db_connection()
    products = conn.execute(
        "SELECT * FROM links INNER JOIN users ON links.userid=users.id").fetchall()
    conn.close()

    for product in products:
        newDetails = get_product_details(product['url'])
        print("Product: "+product['product'])
        print(product['price'])
        print(newDetails['price'])
        if newDetails['price'] < product['price']:
            send_mail(product, newDetails)
            print('Email has been sent to '+product['name'])
        # Create cursor
        conn = get_db_connection()
        conn.execute("UPDATE links SET price=? WHERE id=?",
                     (newDetails['price'], product['id']))
        # connection commit
        conn.commit()
        conn.close()

# Auto Scheduler doesn't run concurrently with Flask Server
# Threading needs to be implemented to automate both tasks
# To check the updation and email sending hit below endpoint


def updateThread():
    print("Update Thread Called")
    print(threading.current_thread().name)
    # schedule.every(1).minutes.do(checkFunction)
    schedule.every(6).hours.do(checkFunction)
    while True:
        # print("While loop of updateThread")
        schedule.run_pending()
        time.sleep(5)


# Updation Check Endpoint
# Hit this endpoint to manually update the Prices
# Can be given as an option to the user to refresh prices manually


@app.route('/update')
@is_logged_in
def update():
    checkFunction()
    return redirect(url_for("dashboard"))


@app.before_first_request
def thread_start():
    threading.Thread(target=updateThread).start()

    # For Production/Deployment
if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=False)


# if __name__ == "__main__":
#     threading.Thread(target=updateThread).start()
#     app.secret_key = 'secret123'

#     # For Production/Deployment
#     app.run()
#     # For Development
#     # app.run(debug=True)
