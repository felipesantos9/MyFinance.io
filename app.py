import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

from util import apology, login_required, usd


# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///myfinance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":
        name = request.form.get("name")
        type = request.form.get("type")
        value = request.form.get("value")
        day = request.form.get("day")
        month_year = request.form.get("month_year")

        if not name:
            return apology("No Name")
        elif not value or not value.isdigit() or int(value) <= 0:
            return apology("Value not valid")


        if type is None:
            return apology("No type")

        cash = db.execute(
            "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
        )[0]["cash"]

        if type == "Expense":
            expense = int(value)

            if expense > cash:
                return apology("Not enough cash")

            db.execute(
                "UPDATE users SET cash= cash - :expense WHERE id = :user_id",
                expense=expense,
                user_id=session["user_id"],
            )

            if day == '' and month_year == '':
                db.execute(
                    "INSERT INTO transactions (user_id,value,type,name) VALUES (:user_id,:expense,:type,:name)",
                    user_id=session["user_id"],
                    expense=expense,
                    type=type,
                    name=name,
                )
            else:
                 db.execute(
                    "INSERT INTO transactions (user_id,value,day,month_year,type,name) VALUES (:user_id,:expense,:day,:month_year,:type,:name)",
                    user_id=session["user_id"],
                    expense=expense,
                    day=day,
                    month_year=month_year,
                    type=type,
                    name=name,
                )

            return redirect("/")
        else:
            db.execute(
                "UPDATE users SET cash= cash + :value WHERE id = :user_id",
                value=value,
                user_id=session["user_id"],
            )

            if day == '' and month_year == '':
                db.execute(
                    "INSERT INTO transactions (user_id,value,type,name) VALUES (:user_id,:value,:type,:name)",
                    user_id=session["user_id"],
                    value=value,
                    type=type,
                    name=name,
                )
            else:

                db.execute(
                    "INSERT INTO transactions (user_id,value,day,month_year,type,name) VALUES (:user_id,:value,:day,:month_year,:type,:name)",
                    user_id=session["user_id"],
                    value=value,
                    day=day,
                    month_year=month_year,
                    type=type,
                    name=name,
                )
            return redirect("/")
    else:
        """Show trasactions"""
        transactions = db.execute(
            "SELECT day,month_year,type,name,value FROM transactions WHERE user_id = :user_id",
            user_id=session["user_id"],
        )

        cash = db.execute(
            "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
        )[0]["cash"]


        return render_template("index.html", transactions=transactions, cash=cash)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        password = request.form.get("password")
        have_numbers = False
        for i in password:
            if i.isdigit():
                have_numbers = True

        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not have_numbers:
            return apology("password must have number(s)", 400)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("No match", 400)

        row = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(row) == 1:
            return apology("Username already registred", 400)

        db.execute(
            "INSERT INTO users (username, hash) VALUES(?,?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )
        row = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        session["user_id"] = row[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/history")
@login_required
def history():


    """Show trasactions"""
    transactions = db.execute(
        "SELECT month_year, SUM(CASE WHEN type == 'Income' THEN value ELSE 0 END) AS incomes,SUM(CASE WHEN type == 'Expense' THEN value ELSE 0 END) AS expenses, SUM(CASE WHEN type = 'Income' THEN value ELSE -value END) AS total FROM transactions WHERE user_id = :user_id GROUP BY month_year ORDER BY month_year",
        user_id=session["user_id"]
    )




    return render_template("history.html", transactions=transactions)
