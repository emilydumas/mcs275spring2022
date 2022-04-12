# MCS 275 Spring 2022 Lecture 35 
# Minimal Flask demo
from flask import Flask, render_template
import sqlite3

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


app.run()  # Start the web server; I lost control from here on

