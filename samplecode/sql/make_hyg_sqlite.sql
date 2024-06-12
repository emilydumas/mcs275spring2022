-- MCS 275 Spring 2022 - Emily Dumas

-- SQLite command line shell commands to convert hygdata_v3.csv from
--     https://github.com/astronexus/HYG-Database/blob/master/hygdata_v3.csv?raw=true
-- to a sqlite3 database for use in MCS 275 problems.

-- The source CSV is part of the HYG database archive created by David Nash
-- and available under a CC license.  See http://www.astronexus.com/hyg

-- STEP 0: Set our output filename
.open "hyg_data.sqlite"

-- STEP 1: Drop table if it already exists
DROP TABLE IF EXISTS stars;

-- STEP 2: Create the table `stars`

-- This is necessary because if we directly import a CSV and let it create
-- a table, then every column will have type TEXT.

CREATE TABLE stars (
  id INTEGER PRIMARY KEY,
  hip INTEGER,
  hd INTEGER,
  hr INTEGER,
  gl TEXT,
  bf TEXT,
  proper TEXT,
  ra REAL,
  dec REAL,
  dist REAL,
  pmra REAL,
  pmdec REAL,
  rv REAL,
  mag REAL,
  absmag REAL,
  spect TEXT,
  ci REAL,
  x REAL,
  y REAL,
  z REAL,
  vx REAL,
  vy REAL,
  vz REAL,
  rarad REAL,
  decrad REAL,
  pmrarad REAL,
  pmdecrad REAL,
  bayer TEXT,
  flam INTEGER,
  con TEXT,
  comp INTEGER,
  comp_primary INTEGER,
  base TEXT,
  lum REAL,
  var TEXT,
  var_min REAL,
  var_max REAL
);

-- STEP 3: Import the CSV

-- Now configure for CSV importing and add the rows to
-- table `stars`.  These are not SQL commands, but SQLite
-- command line shell commands, which start with ".".

.separator ,
.header on
.import "hygdata_v3.csv" stars


-- STEP 4: Cleaning

-- Finally, search for empty string ("") values in columns and
-- replace them with null values.
-- For some reason, importing CSV into SQLite allows the empty
-- string to end up as a value in some numeric columns, distinct
-- from the value NULL, so we include every column in this list
-- of UPDATEs.


UPDATE stars SET hip=NULL WHERE hip="";
UPDATE stars SET hd=NULL WHERE hd="";
UPDATE stars SET hr=NULL WHERE hr="";
UPDATE stars SET gl=NULL WHERE gl="";
UPDATE stars SET bf=NULL WHERE bf="";
UPDATE stars SET proper=NULL WHERE proper="";
UPDATE stars SET ra=NULL WHERE ra="";
UPDATE stars SET dec=NULL WHERE dec="";
UPDATE stars SET dist=NULL WHERE dist="";
UPDATE stars SET pmra=NULL WHERE pmra="";
UPDATE stars SET pmdec=NULL WHERE pmdec="";
UPDATE stars SET rv=NULL WHERE rv="";
UPDATE stars SET mag=NULL WHERE mag="";
UPDATE stars SET absmag=NULL WHERE absmag="";
UPDATE stars SET spect=NULL WHERE spect="";
UPDATE stars SET ci=NULL WHERE ci="";
UPDATE stars SET x=NULL WHERE x="";
UPDATE stars SET y=NULL WHERE y="";
UPDATE stars SET z=NULL WHERE z="";
UPDATE stars SET vx=NULL WHERE vx="";
UPDATE stars SET vy=NULL WHERE vy="";
UPDATE stars SET vz=NULL WHERE vz="";
UPDATE stars SET rarad=NULL WHERE rarad="";
UPDATE stars SET decrad=NULL WHERE decrad="";
UPDATE stars SET pmrarad=NULL WHERE pmrarad="";
UPDATE stars SET pmdecrad=NULL WHERE pmdecrad="";
UPDATE stars SET bayer=NULL WHERE bayer="";
UPDATE stars SET flam=NULL WHERE flam="";
UPDATE stars SET con=NULL WHERE con="";
UPDATE stars SET comp=NULL WHERE comp="";
UPDATE stars SET comp_primary=NULL WHERE comp_primary="";
UPDATE stars SET base=NULL WHERE base="";
UPDATE stars SET lum=NULL WHERE lum="";
UPDATE stars SET var=NULL WHERE var="";
UPDATE stars SET var_min=NULL WHERE var_min="";
UPDATE stars SET var_max=NULL WHERE var_max="";

