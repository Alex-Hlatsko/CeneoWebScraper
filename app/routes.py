from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
@app.route('/index/<name>')
def index(name="Hello World"):
    return render_template("index.html.jinja", text=name)