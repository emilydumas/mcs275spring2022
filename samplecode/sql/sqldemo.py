"SQL demo program"
# MCS 275 Spring 2022 Lecture 30

import sqlite3

# Open the database connection
# (creates the file, if it doesn't exist)
con = sqlite3.connect("solarsystem.sqlite")

print("Removing table planets (if it exists)")
con.execute("""
DROP TABLE IF EXISTS planets;
""")

print("Creating table planets")
con.execute("""
CREATE TABLE planets (
    name TEXT,
    dist REAL,
    year_discovered INTEGER
);
""")

print("Inserting rows")
con.execute(
    "INSERT INTO planets VALUES (?,?,?);",
    ("Earth", 1.0, None)
)
con.execute(
    "INSERT INTO planets VALUES (?,?,?);",
    ("Neptune", 30.1, 1846)
)
con.execute(
    "INSERT INTO planets VALUES (?,?,?);",
    ("Mars", 1.5, None)
)

print("Selecting all rows")
res = con.execute(
    "SELECT * FROM planets;"
)
for row in res:
    print("Planet with:")
    print("\tName =",row[0])
    print("\tDistance (AU) =",row[1])
    print("\tYear discovered =",row[2])

# CLEANUP
# Commit changes to disk
print("Committing changes")
con.commit()
# Close the connection
print("Closing connection")
con.close()
