from re import split
from app import app
from app.models.product import Product
from flask import render_template, redirect, url_for, request
import os

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/extract', methods=["POST","GET"])
def extract():
    if request.method == 'POST':
        productId = request.form.get('productId')
        product = Product(productId)
        product.extractName()
        if product.productName is not None:
            product.extractProduct()
            product.exportProduct()
            return redirect(url_for('product', productId=productId))
        error = "Podana wartość nie jest poprawnym kodem produktu!"
        return render_template('extract.html', error=error)
    return render_template('extract.html')

@app.route('/products')
def products():
    products = [filename.split(".")[0] for filename in os.listdir("app/opinions")]
    return render_template("products.html", products=products)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/product/<product_id>')
def product(product_id):
    product = Product(product_id)
    product.importProduct()
    return render_template('product.html', product=str(product), productName=product.productName)