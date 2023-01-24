# Made with <3 by Christian Brechenmacher

from flask import Flask, render_template, request, send_file
from what_bereich_am_i import parse_function

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    args = []
    bereich=None
    if 'bereich' in request.args:
        bereich = request.args['bereich'].upper()
        func, bereich = parse_function(bereich)

        args = func(bereich)
    return render_template(
        'index.html',
        results=args,
        bereich=bereich
    )