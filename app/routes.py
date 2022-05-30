from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/extraction')
def extraction():
    return render_template("extraction.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/products')
def products():
    return render_template("products.html")

@app.errorhandler(404)
def not_found(e):
    return render_template('not_found.html')
