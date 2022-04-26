# MCS 275 Spring 2022 
# "paint chip" demo of serving images
from re import S
from flask import Flask, Response
import random
import PIL.Image
import io

app = Flask(__name__)

@app.route("/")
def front():
    """Return howto"""
    s = ""
    for _ in range(10):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        hc = "{:02x}{:02x}{:02x}".format(r,g,b)
        s += "<li><a href=\"/chip/{0}/\"><code>/chip/{0}/</code></a></li>".format(hc)
    return """<!doctype html>
<html>
<head><style>body { font-family: sans-serif; max-width: 38rem;
padding: 2rem; margin: auto; }
a { text-decoration: none; }
a.hover { text-decoration: underline; }</style></head>
<body>
<h1>Paint Chip Generator</h1>
<p>To use this program, request a URL with a 6-digit hexadecimal color code such as:
<ul>"""+s+"""
</ul>
</body>
</html>
"""

@app.route("/chip/<hc>/image/")
def chipimage(hc):
    "Generate a solid color JPEG and return it as an image/jpeg HTTP response"
    assert len(hc)==6
    r = int(hc[:2],16)
    g = int(hc[2:4],16)
    b = int(hc[4:6],16)
    img = PIL.Image.new("RGB",(256,256),(r,g,b))
    # PIL only knows how to save to a file-like object
    # BytesIO is a file-like object that lets us capture to memory
    # and get the data as a bytes object.  So we use that to provide
    # PIL a "fake file" to write to.
    with io.BytesIO() as b:
        img.save(b,"JPEG")
        return Response(response=b.getvalue(), status=200, mimetype="image/jpeg")

@app.route("/chip/<hc>/")
def chip(hc):
    "Return HTML referencing a dynamically-generated JPEG of a given color"
    return """<!doctype html>
<html>
<head><style>body { font-family: sans-serif; max-width: 38rem;
padding: 2rem; margin: auto; }
a { text-decoration: none; }
a.hover { text-decoration: underline; }</style></head>
<body>
<h1>Paint chip</h1>""" + """
<p>Here is a 256x256 JPEG image of solid color <code>#{0}</code>.</p><img src="/chip/{0}/image/">
<p>Note: This artisanal JPEG was created just for your request, from scratch, by a dedicated staff of Python interpreters running PIL.  Enjoy it in good health.</p>
</body>
</html>""".format(hc)

app.run()
