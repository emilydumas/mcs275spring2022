# ScreamDeck

MCS 275 Spring 2022 Project 4 by Emily Dumas

## Assignment

Create a simple chat application using Flask that allows users of the site to
view recent messages (in chronological order) and to post their own messages.
Use a SQLite database to store the messages.  The application does not need to
have any authentication system; instead, it can prompt for both a username and a
message in the submission form.

## How to test

Run the main program `screamdeck.py`, which is a Flask app that listens for HTTP
connections at the default address and port number that Flask selects
(typically, localhost:8000).  Open the root document (`/`) of the address that
Flask reports it is listening to see the message feed.  It is pre-populated with
a sample converstaion.  The HTML form at the bottom of the message feed can be
used to post new messages.

The main program requires the SQLite database `screamdeck.db` to already exist, and
the one included with this submission should suffice for testing.  The script
`resetdb.py` can be used to create the database if it is missing, or to clear
the contents of an existing one.

## Personal contribution

I designed and wrote the entire application from scratch: The Python programs,
database schema and queries, HTML template, and CSS stylesheet.  The design uses
things covered in most Flask tutorials, and my main contribution was to strip
away anything that wasn't absolutely necessary so that the application code
could be explained in a few MCS 275 lectures without the need for an extensive
preliminary discussion of things like HTML templating, session data, Flask
globals (the _g object), and so on.

## Sources and credits

I referred to the MCS 275 slides from Lecture 34 to recall how to add a CSS
stylesheet to an existing HTML document
(https://www.dumas.io/teaching/2022/spring/mcs275/slides/lecture34.html#/13).

The basic structure of the Flask app, and the choice to make a separate function
to open the database, were influenced by the Flask tutorial at
https://flask.palletsprojects.com/en/1.1.x/tutorial/, though no code was copied
or adapted from that source.  I also read parts of the book "Flask Web
Development, 2nd Edition" by Miguel Grinberg (O'Reilly Media, 2018, ISBN
9781491991732,
https://www.oreilly.com/library/view/flask-web-development/9781491991725/) and
an Flask tutorial by Miguel Grinberg
(https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world),
again without adapting any code directly from these sources.

I looked at the HTML for the front pages of several popular web sites that
follow the "submit and vote" pattern in order to see what tag structures are
most often used.  Specifically, I checked the markup of: * https://reddit.com/ *
https://lobste.rs/ * https://news.ycombinator.com/ The patterns I saw there were
originally used to design another application (Whinge), and this chat
application was designed later by removing some features from that one (i.e.
scores and voting).  In this way, the review of the sites listed above
ultimately influenced the markup produced by Yellaro.

I used https://www.w3schools.com/html/html_forms.asp as a reference while
preparing the HTML forms, and https://www.w3schools.com/css/ as a reference for
CSS selectors while I was building the stylesheet.
