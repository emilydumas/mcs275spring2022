# Create or reset the database for worksnap flask example
import sqlite3
import sys

con = sqlite3.connect("worksnap.db")

if "--clear" in sys.argv[1:]:
    print("Erasing existing database (if any) and creating tables.")
    con.execute("DROP TABLE IF EXISTS orders;")
else:
    print("""Ensuring database tables exist.
(Add --clear command line option to also erase existing data.""")
    con.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        "woid" INTEGER PRIMARY KEY, 
        "description" TEXT,
        "assigned_to" TEXT,
        "time_created" REAL,
        completed INTEGER DEFAULT 0
    );
    """)

con.commit()
con.close()
