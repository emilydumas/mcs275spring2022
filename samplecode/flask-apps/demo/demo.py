# MCS 275 Spring 2022 Lecture 35 
# Minimal Flask demo
from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def front():
    """Return howto"""
    return """<!doctype html>
<html>
<body>
<h1>Demo app</h1>
<p>This is a simple Flask demo.  The front page doesn't do anything interesting.</p>
<p>To see the actual demonstrations, visit <a href="/greeting"><code>/greeting</code></a> or <a href="/admonition"><code>/admonition</code></a>.</p>
</body>
</html>
"""

@app.route("/greeting")   # <-- Flask decorator indicates URL for a function
def f():                  # (The name of this function doesn't matter)             
    """Return HTML for a greeting"""
    return """<!doctype html>
<html>
<body>
<h1>Hello there!!!</h1>
<p>Your random number for today is: {}</p>
<p>Here is an image, included as a static file served from the <code>/static</code> subdirectory:</p>
<img src="static/sample_image.jpg">
</body>
</html>""".format(random.randint(1,100))

@app.route("/admonition")   # <-- Flask decorator indicates URL for a function
def g():                    # (The name of this function doesn't matter)             
    """Return HTML for a warning"""
    x = random.randint(1,100)
    # Load the file admon.html in the templates subdir
    # In it, replace any instance of {{ random_integer }}
    # with the value of the variable x.  Then, make the
    # resulting HTML the response to this HTTP request
    return render_template("admon.html",random_integer=x)

app.run()  # Start the web server; I lost control from here on

