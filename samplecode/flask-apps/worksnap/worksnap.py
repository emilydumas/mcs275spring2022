# MCS 275 Spring 2022 Lectures 35-38
# Work order tracking system
from flask import Flask, render_template, request, redirect, abort
import sqlite3
import time
import datetime
import os

DBFILE="worksnap.db"

app = Flask(__name__)

@app.route("/")
def front():
    "Simple front page"
    return """
    <!doctype html>
    <html><body>
    <p>There's no front page.  Available views:</p>
    <ul><li><a href="/worker/ddumas">Worker status page for ddumas</a></li><li><a href="/wo/new/">Create new work order</a></ul>
    </body></html>"""

@app.route("/worker/<username>/")
def workerview(username):
    """Render the worker view template"""

    con = sqlite3.connect(DBFILE)
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
        dtstr = datetime.datetime.fromtimestamp(row[2]).strftime("%Y-%m-%d %H:%M")
        currently_assigned.append(
            {
                "description": row[1],
                "woid": row[0],
                "datetime": dtstr,
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
        dtstr = datetime.datetime.fromtimestamp(row[2]).strftime("%Y-%m-%d %H:%M")
        available.append(
            {
                "description": row[1],
                "woid": row[0],
                "datetime": dtstr,
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
    "Display the new work order form"
    return render_template("newworkorder.html")

@app.route("/wo/post/",methods=["GET","POST"])
def create_new_work_order():
    "Insert a new work order based on form data"
    con = sqlite3.connect(DBFILE)
    con.execute("""
    INSERT INTO orders (description, time_created)
    VALUES (?,?);
    """,(
        request.values.get("description"),
        time.time()
    ))
    res = con.execute("SELECT last_insert_rowid();")
    # res should have one row it
    # that row should one integer in it
    # and that integer is the woid
    # res.fetchone() # gets something like [275]
    woid=res.fetchone()[0] # gets something like 275
    con.commit()
    con.close()
    return redirect("/wo/{}/".format(woid))  # what is woid?

@app.route("/wo/<int:woid>/")
def order_status(woid):
    """
    Show info about one work order
    """
    con = sqlite3.connect(DBFILE)
    res = con.execute("""
    SELECT description,assigned_to,time_created,completed
    FROM orders
    WHERE woid=?;
    """, [woid])
    row = res.fetchone()
    if row == None:
        # No row returned => woid doesn't exist.  Return 404 NOT FOUND error
        abort(404)

    # If we end up here, it means the woid was found.  Unpack row data into
    # named variables.
    description = row[0]
    assigned_to = row[1]
    time_created = row[2]
    completed = row[3]
    if completed:
        status = "Completed by {}".format(assigned_to)
    elif assigned_to:
        status = "Assigned to {}".format(assigned_to)
    else:
        status = "Open, not yet assigned to a worker"
    return render_template(
        "workorderstatus.html",
        woid=woid,
        description=description,
        status=status,
        datetime=datetime.datetime.fromtimestamp(time_created).strftime("%Y-%m-%d %H:%M")
    )

@app.route("/wo/<int:woid>/assign_to/<username>/")
def order_assign(woid,username):
    """
    assign work order with id `woid` to user with
    name `username`
    """
    con = sqlite3.connect(DBFILE)
    con.execute("""
    UPDATE orders
    SET assigned_to=?
    WHERE woid=?
    AND assigned_to IS NULL;
    """, (username,woid))
    res = con.execute("SELECT changes();")
    num_rows_updated = res.fetchone()[0]
    assert num_rows_updated <= 1
    if num_rows_updated == 1:
        print("SUCCESS!  Work order {} was assigned to {}.".format(woid,username))
    elif num_rows_updated == 0:
        print("FAILURE: Work order {} could not be assigned to {}.".format(woid,username))        
    con.commit()
    con.close()
    return redirect("/worker/{}/".format(username))

@app.route("/wo/<int:woid>/unassign_from/<username>/")
def order_unassign(woid,username):
    """
    return work order `woid` to having no assignment, if it is    
    currently assigned to worker `username`
    """
    con = sqlite3.connect(DBFILE)
    con.execute("""
    UPDATE orders
    SET assigned_to=NULL
    WHERE woid=?
    AND assigned_to=?;
    """, (woid,username))
    con.commit()
    con.close()
    return redirect("/worker/{}/".format(username))

@app.route("/wo/<int:woid>/complete_by/<username>/")
def order_complete(woid,username):
    """
    return work order `woid` to having no assignment, if it is    
    currently assigned to worker `username`
    """
    con = sqlite3.connect(DBFILE)
    con.execute("""
    UPDATE orders
    SET completed=1
    WHERE woid=?
    AND assigned_to=?
    AND completed=0;
    """, (woid,username))
    con.commit()
    con.close()
    return redirect("/worker/{}/".format(username))

# Make sure the working directory is the directory that contains
# this script file.  (Fixes some errors caused by running from
# VS code, for example.)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Make sure database exists, creating it if not
if not os.path.exists(DBFILE):
    print("#####################################################################")
    print("# Database file was not found.  Creating it and adding sample data. #")
    print("#####################################################################")
    con = sqlite3.connect(DBFILE)
    con.execute("""
    CREATE TABLE orders (
            "woid" INTEGER PRIMARY KEY, 
            "description" TEXT,
            "assigned_to" TEXT,
            "time_created" REAL,
            completed INTEGER DEFAULT 0
        );
    """)
    sampledata = [
        ("Post attendance data to Blackboard",1649700951.0),
        ("Hold office hours",1649700921.0),
    ]
    for desc,ts in sampledata:
        con.execute("INSERT INTO orders (description,time_created) VALUES (?,?);",(desc,ts))
    con.commit()
    con.close()

app.run()  # Start the web server

