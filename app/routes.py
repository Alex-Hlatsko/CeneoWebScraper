from app import app
from flask import render_template, redirect, url_for, request
import os
from app.models.product import Product

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/extract', methods=["POST", "GET"])
def extract():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        product = Product(product_id)
        product.extract_product().process_stats().draw_charts()
        # product.save_stats()
        product.save_opinions()
        
        return redirect(url_for("product", product_id=product_id))
    else:
        return render_template("extract.html")

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
    product.read_from_json()
    opinions = product.opinions_do_df()
    stats = product.stats_to_dict()
    return render_template("product.html", stats=stats, product_id=product_id, opinions=opinions)