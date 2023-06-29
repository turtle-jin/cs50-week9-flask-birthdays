import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")


        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?);", name, month, day)

        # go back to the homepage
        return redirect("/")

    else:

        # Display the entries in the database on index.html
        rows = db.execute("SELECT * FROM birthdays;")


        return render_template("index.html", rows=rows)


@app.route("/delete_confirm", methods=["POST"])
def delete_confirm():

    id = int(request.form.get("id"))

    row = db.execute("SELECT * FROM birthdays WHERE id = (?);", id)
    delete_name = row[0]["name"]
    month = row[0]["month"]
    day = row[0]["day"]
    id_value = row[0]["id"]

    return render_template("delete.html", delete_name=delete_name, id_value=id_value, month=month, day=day)




@app.route("/delete", methods=["POST"])
def delete():
    id = int(request.form.get("id"))
    #row = db.execute("SELECT * FROM birthdays WHERE id = (?);", id)
    db.execute("DELETE FROM birthdays WHERE id = (?);", id)
    return redirect("/")


@app.route("/edit", methods=["POST", "GET"])
def edit():
    id = int(request.form.get("id"))
    print(id)
    row = db.execute("SELECT * FROM birthdays WHERE id = (?);", id)
    edit_name = row[0]["name"]
    month = row[0]["month"]
    day = row[0]["day"]
    id_value = row[0]["id"]

    return render_template("edit.html", edit_name=edit_name, id_value=id_value, month=month, day=day)


@app.route("/update", methods=["POST"])
def update():
    id = int(request.form.get("id"))
    name = request.form.get("name")
    month = request.form.get("month")
    day = request.form.get("day")

    db.execute("UPDATE birthdays SET name = :name, month = :month, day = :day WHERE id = :id;",
               name=name, month=month, day=day, id=id)

    # go back to the homepage
    return redirect("/")









