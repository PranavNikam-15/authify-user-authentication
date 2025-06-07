from flask import Blueprint, render_template, request, redirect, flash, session
from . import mysql

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def home_page():
    return render_template("homePage.html")


@auth_bp.route("/about")
def about():
    return render_template("about.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userEmail = request.form.get("loginEmail")
        userPassword = request.form.get("loginPassword")

        if not userEmail or not userPassword :
           flash("Please fill out all fields.", "warning")
           return redirect("/")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (userEmail,))
        user = cur.fetchone()
        cur.close()

        if user:
            if user[3] == userPassword:
                session["user_id"] = user[0]
                flash("Login successful!", "success")
                return redirect("/dashboard")
            else:
                flash("Password doesn't match.", "danger")
        else:
            flash("User not found.", "danger")

    return render_template("homePage.html")
    

@auth_bp.route("/signup", methods=["GET", "POST"])
def signUp():
    if request.method == "POST" :

       userName = request.form.get("signupUsername")
       userEmail = request.form.get("signupEmail")
       userPassword = request.form.get("signupPassword")

       if not userName or not userEmail or not userPassword :
           flash("Please fill out all fields.", "warning")
           return redirect("/")
       
       else :
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM users WHERE email = %s", (userEmail,))
        user = cur.fetchone()

        if user:
            flash("User already exist with same email.", "warning")
            return redirect("/")

        cur.execute( 
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (userName, userEmail, userPassword)  )
        mysql.connection.commit()
        cur.close()
        flash("Registration successful!")
        return redirect("/")

    else :
        return render_template("homePage.html")
    

@auth_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect("/login")
    return render_template("dashboard.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect("/")


@auth_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404