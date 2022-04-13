# MCS 275 Spring 2022 Lecture 35 
# Minimal Flask demo
from flask import Flask, render_template, request, redirect
import sqlite3
import time

app = Flask(__name__)

@app.route("/worker/<username>/")
def workerview(username):
    """Render the worker view template"""

    con = sqlite3.connect("worksnap.db")
    res = con.execute("""
    SELECT woid, description, time_created
    FROM orders
    WHERE assigned_to=?
    AND completed=0;
    """, (username,) )   # (5,) is a one-element tuple with element 5
    # Translate the list of tuples returned by SQLite
    # into the list of dictionaries expected by our template
    currently_assigned = []
    for row in res:
        currently_assigned.append(
            {
                "description": row[1],
                "woid": row[0],
                "datetime": row[2],
            }
        )

    res = con.execute("""
    SELECT woid, description, time_created
    FROM orders
    WHERE assigned_to IS NULL
    AND completed=0;
    """)
    # Translate the list of tuples returned by SQLite
    # into the list of dictionaries expected by our template
    available = []
    for row in res:
        available.append(
            {
                "description": row[1],
                "woid": row[0],
                "datetime": row[2],
            }
        )

    # We're done with DB stuff
    con.close()

    return render_template(
        "workerview.html",
        username=username,
        currently_assigned=currently_assigned,
        available=available
    )

@app.route("/wo/new/")
def new_work_order_form():
    return render_template("newworkorder.html")

@app.route("/wo/post/",methods=["GET","POST"])
def create_new_work_order():
    con = sqlite3.connect("worksnap.db")
    con.execute("""
    INSERT INTO orders (description, time_created)
    VALUES (?,?);
    """,(
        request.values.get("description"),
        time.time()
    ))
    con.commit()
    con.close()
    return redirect("/wo/create/")  # FOR NOW, redirect back to the form.

@app.route("/wo/<int:woid>/")
def order_status(woid):
    return "Placeholder"

@app.route("/wo/<int:woid>/assign_to/<username>/")
def order_assign(woid,username):
    """
    assign work order with id `woid` to user with
    name `username`
    """
    con = sqlite3.connect("worksnap.db")
    con.execute("""
    UPDATE orders
    SET assigned_to=?
    WHERE woid=?
    AND assigned_to IS NULL;
    """, (username,woid))
    con.commit()
    con.close()
    return redirect("/worker/{}/".format(username))

@app.route("/wo/<int:woid>/unassign/")
def order_unassign(woid):
    return "Placeholder"

@app.route("/wo/<int:woid>/complete/")
def order_complete(woid):
    return "Placeholder"

app.run()  # Start the web server; I lost control from here on

