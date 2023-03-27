from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = "latihan_MYSQLDB"


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "latihan"

mysql = MySQL(app)


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    mesage = ""

    if request.method == "POST" and "email" in request.form and "password" in request.form:
        email = request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM user WHERE email = %s AND password =  %s ", (email, password))
        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session["userid"] = user["userid"]
            session["name"] = user["name"]
            session["email"] = user["email"]
            mesage = "Login berhasil!"
            return render_template("user.html", mesage=mesage)
        else:
            mesage = "Email / password Salah!"

    return render_template("login.html", mesage=mesage)


@app.route("/register", methods=["GET", "POST"])
def register():
    mesage = ""

    if request.method == "POST" and "name" in request.form and "password" in request.form and "email" in request.form:
        userName = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE email = %s", (email, ))
        account = cursor.fetchone()

        if account:
            mesage = "Acount sudah ada"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = "Alamat Email Salah"
        elif not userName or not password or not email:
            mesage = "Tolong isi form"
        else:
            cursor.execute(
                "INSERT INTO user VALUES (NULL, %s, %s, %s)", (userName, email, password))
            mysql.connection.commit()
            mesage = "Registrasi Berhasil"

    elif request.method == "POST":
        mesage = "Tolong isi form"
    return render_template("register.html", mesage=mesage)


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("userid", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=8080)
