"Debugging example: Try to split address into number and street"
import csv
import sys

def represents_integer(s):
    "Can `s` be converted to an integer?"    
    try:
        n = int(s)
        return True
    except ValueError:
        return False


def split_street(address):
    """
    Split street address like
       123 Morgan St.
    into a number (123) and name (Morgan St.).  Returns a dict
    with keys `street` (for the given address), `street_number`,
    and `street_name`.
    """
    d = { "street": address,
          "street_number": "",
          "street_name": "" }
    parts = address.split()
    if len(parts)>1:
        if represents_integer(parts[0]):
            d["street_number"] = parts[0]
            d["street_name"] = address[len(parts[0]):].strip()
    return d

def usage():
    "Print usage message and exit"
    print("Usage: {} INFILE.csv".format(sys.argv[0]))
    print("Reads a CSV file that includes columns 'name', 'street' and")
    print("prints a report on each row where 'street' value is split into")
    print("number and name, if possible.")
    exit(1)

if len(sys.argv)!=2:
    usage()

with open(sys.argv[1],"r",newline="",encoding="UTF-8") as input_fobj:
    rdr = csv.DictReader(input_fobj)
    for k,row in enumerate(rdr):
        streetdata = split_street(row["street"])
        print("Row {}\n\tname='{}'\n\tstreet='{}'\n\tstreet_number='{}'\n\tstreet_name='{}'".format(
            k+1,
            row["name"],
            streetdata["street"],
            streetdata["street_number"],
            streetdata["street_name"]
        ))
