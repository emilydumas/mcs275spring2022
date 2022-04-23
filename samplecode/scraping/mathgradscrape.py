"Scrape the web page with Fall 2022 UIC math graduate courses"
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import os
import sys

PAGEURL = "https://mscs.uic.edu/graduate/current-students/advising-and-registration/graduate-courses/"
CACHEFILE = "toscrape.html"
OUTFILE = "fall2022courses.csv"

def get_page_soup(force_update=False):
    if os.path.exists(CACHEFILE) and not force_update:
        print("Using file '{}' instead of downloading '{}'".format(CACHEFILE,PAGEURL))
        with open(CACHEFILE,"rb") as fp:
            return BeautifulSoup(fp,"html.parser")
    else:
        if force_update:
            print("Downloading '{}' (replacing cached copy)".format(PAGEURL))
        else:
            print("Downloading '{}' (no cached copy available)".format(PAGEURL))
        with urlopen(PAGEURL) as res:
            data = res.read()
            with open(CACHEFILE,"wb") as fp:
                fp.write(data)
            return BeautifulSoup(data,"html.parser")

# Main scraper logic

# Allow user to add --force to command line to insist on re-download
# If that is not given, prefer any cached copy that's present
force = "--force" in sys.argv[1:]

# 1. Grab the entire DOM
soup = get_page_soup(force_update=force)

# 2. Locate the table

# The page is divided into <section>s for the different semesters
# Let's locate the one for Fall 2022 using a loop that exits when 
# it is found.
for section in soup.find_all("section"):
    h2 = section.find("h2",id="fall-2022-graduate-courses")
    if h2:
        # This is the right section, so let's get its first table
        table = section.find("table")
        # No need to look further, so let's break out of the loop
        break

# 3. Basic error checking

if section is None:
    print("ERROR: No <section> tag with id fall-2022-graduate-courses")
    exit(1)

if table is None:
    print("ERROR: The fall 2022 <section> tag has no <table> in it")
    exit(1)

# 4. Convert table rows to CSV file rows

nrows = 0
with open(OUTFILE,"w",newline="",encoding="UTF-8") as fp:
    writer = csv.writer(fp)
    for row in table.find_all("tr"):
        row_cells = [ cell.text.replace("\n"," ") for cell in row.find_all( ["th", "td"] ) ]
        # list like ["Course","Description",...]
        writer.writerow(row_cells)
        nrows += 1
print("Found {} courses for Fall 2022.  Wrote '{}'.".format(nrows,OUTFILE))
