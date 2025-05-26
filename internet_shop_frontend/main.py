import binascii
import os

from flask import Flask, render_template, redirect, url_for, flash

from src.data import data_actions
from src.data.forms import LoginForm, SignUpForm


app = Flask(__name__, template_folder="src/templates")
app.secret_key = binascii.hexlify(os.urandom(24))


@app.get("/")
def index():
    products = data_actions.get_products()
    return render_template("index.html", products=products)


@app.get("/product/<id>/")
def get_product(id):
    product = data_actions.get_product(id)
    return render_template("product.html", product=product)


@app.get("/buy_product/<id>/")
def buy_product(id):
    return render_template("index.html")


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        data_actions.signup(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for("login"))
    
    return render_template("signup.html", form=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        msg = data_actions.login(email=form.email.data, password=form.password.data)
        if msg:
            flash(msg)
            return redirect(url_for("cabinet"))
        else:
            return redirect(url_for("login"))
        
    return render_template("login.html", form=form)


@app.get("/cabinet/")
def cabinet():
    user = data_actions.get_user()
    if user:
        return render_template("cabinet.html", user=user)
    else:
        flash("Для входу в кабінет спочатку увійдіть в свій акаунт.")
        return redirect(url_for("login"))


@app.get("/shop_list/<id>/")
def get_shop_list(id):
    pass

if __name__ == "__main__":
    app.run(debug=True, port=5000)
