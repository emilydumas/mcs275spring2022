# Mark all tasks unassigned and uncompleted
import sqlite3

con = sqlite3.connect("worksnap.db")

con.execute("""
CREATE TABLE IF NOT EXISTS orders (
    "woid" INTEGER PRIMARY KEY, 
    "description" TEXT,
    "assigned_to" TEXT,
    "time_created" REAL,
    completed INTEGER DEFAULT 0
);
""")
con.execute("""
UPDATE orders SET completed=0, assigned_to=NULL;
""")
con.commit()
con.close()
