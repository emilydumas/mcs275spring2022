# MCS 275 Spring 2022 Lecture 35
from flask import Flask, render_template, request, redirect
import os
import sqlite3

# Make sure the working directory is the directory that contains
# this script file.  (Fixes some errors caused by running from
# VS code, for example.)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# The database filename used by the application
DBFILE = "speakerslate.db"


def reset_db_to_initial_state():
    """
    Initialize the database file, erasing existing data if present.
    Used in two ways:
      * Runs at application startup if database cannot be found
      * Is called by the route for resetting the schedule
    """
    con = sqlite3.connect(DBFILE)
    con.execute("DROP TABLE IF EXISTS schedule;")
    con.execute(
        """
    CREATE TABLE schedule (
        slotid INTEGER PRIMARY KEY,
        datetime TEXT NOT NULL,
        speaker TEXT
    );"""
    )
    for s in [
        "Saturday 9am",
        "Saturday 10am",
        "Saturday 11am",
        "Saturday 2pm",
        "Sunday 11am",
        "Sunday 2pm",
    ]:
        con.execute(
            """
        INSERT INTO schedule (datetime) VALUES (?);
        """,
            [s],
        )
    con.commit()
    con.close()


app = Flask(__name__)

# -----------------------------------------------
#        START OF FLASK ROUTE DEFINITIONS
# -----------------------------------------------


@app.route("/")
def front():
    "Show the application front page"
    return render_template("front.html")


@app.route("/reset/")
def reset():
    "Erase all scheduled lectures"
    reset_db_to_initial_state()
    return render_template("reset_done.html")


@app.route("/userinfo/")
def userinfo():
    "Show user info form"
    return render_template("userinfo.html")


@app.route("/choose/", methods=["GET", "POST"])
def showchoices():
    """
    Route for submission of the user information form.
    With the username now known, presents choices of speaking
    slots that aren't already assigned.  Each choice links to
    a URL like
      /assign/<slotid>/to/<username>/
    so that clicking the link will assign the speaking slot to
    this user.
    """
    #############################################
    #############################################
    #####                                   #####
    #####  WRITE THE BODY OF THIS FUNCTION  #####
    #####                                   #####
    #############################################
    #############################################
    return "This function hasn't been written yet!"


@app.route("/assign/<int:slotid>/to/<username>/")
def assign_slot_to_person(slotid, username):
    """
    Record that `username` is speaking at slot with id `slotid`,
    then redirect to the schedule page.
    """
    #############################################
    #############################################
    #####                                   #####
    #####  WRITE THE BODY OF THIS FUNCTION  #####
    #####                                   #####
    #############################################
    #############################################
    return "This function hasn't been written yet!"


@app.route("/schedule/")
def show_schedule():
    "Display the schedule of all assigned speaking slots"
    con = sqlite3.connect(DBFILE)
    res = con.execute(
        "SELECT slotid,datetime,speaker FROM schedule WHERE speaker IS NOT NULL;"
    )
    # Now we have all the slots as an iterable of tuples.
    # The template expects a list of dictionaries, so we convert.
    scheduled_lectures = []
    for row in res:
        scheduled_lectures.append(
            {"slotid": row[0], "datetime": row[1], "speaker": row[2]}
        )
    con.close()
    # Pass the list of dicts to the template.
    # NOTE: This template doesn't require the username, since the schedule
    # can be viewed without entering any information.
    return render_template("schedule.html", scheduled_lectures=scheduled_lectures)


# -----------------------------------------------
#        END OF FLASK ROUTE DEFINITIONS
# -----------------------------------------------


# -----------------------------------------------
#                MAIN PROGRAM
# -----------------------------------------------

# Make sure the database exists and is ready
if not os.path.exists(DBFILE):
    print("The database file '{}' does not exist.  Initializing it.".format(DBFILE))
    reset_db_to_initial_state()

# Start the web server
app.run()
