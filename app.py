
import os
import pathlib
import db
import numpy as np
import requests
from flask import Flask, session, abort, redirect, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from db import connect_db, FoodItem, CartItem, Order

app = Flask(__name__)


db = connect_db(app, 'food_items.db')


app.secret_key = "@209AoRQeFkeW"


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


GOOGLE_CLIENT_ID = "1048242188244-fupluigctbeesj717dmtg1rn2fteoi6t.apps.googleusercontent.com"
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")


flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/main")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return render_template('index.html', value="Login")


@app.route("/main")
@login_is_required
def protected_area():
    if "cart" not in session:
        print("cart not in session")
        session["cart"] = []
    print("adding ", session["cart"])
    cart = session["cart"]
    naming = session["google_id"]
    fooditems = FoodItem.query.all()
    return render_template('home.html', value="Logout", fooditems=fooditems, naming=naming, cart=cart)


@app.route("/add_to_cart/<int:id>-<string:name>-<float:price>")
def add_to_cart(id, name, price):
    found = False
    for item in session["cart"]:
        if item.get("id") == id:
            item["qty"] += 1
            found = True
            break

    if not found:
        cart_dict = {"id": id, "name": name, "price": price, "qty": 1}
        session["cart"].append(cart_dict)
        print("added ", session["cart"])

    print(session["cart"])

    session.modified = True
    return redirect("/main")


@app.route("/delete_from_cart/<int:id>")
def delete_from_cart(id):
    print("deleting", session["cart"])
    for item in session["cart"]:
        if item.get("id") == id:
            session["cart"].remove(item)
            print("deleted", session["cart"])
            break
    session.modified = True
    return redirect("/cart")


@app.route('/added_to_cart')
def added_to_cart():
    for item in session["cart"]:
        CartItem.query.all()
        cartitem = CartItem(id=session["google_id"], item_id=item["id"],
                            name=item["name"], price=item["price"], qty=item["qty"])
        db.session.add(cartitem)
    db.session.commit()
    hello_cart = session["cart"]
    amount = 0
    for item in session["cart"]:
        amount += item["qty"] * item["price"]
    return render_template('checkout.html', cart=hello_cart, value='Logout', amount=amount)


@app.route('/checkout')
def refresh():
    return redirect('/main')


@app.route('/orders')
def view_orders():
    orders = Order.query.filter_by(id=session["google_id"]).all()
    return render_template('orders.html', orders=orders, value="Logout")

@app.route('/payment')
def payment():
    session["cart"].clear()
    session.modified = True
    return render_template('payment.html', value="Logout")

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    print("now", session["cart"])
    amount = 0
    cart = session["cart"]
    print(cart)
    for item in session["cart"]:
        amount += item["qty"] * item["price"]

    return render_template('cart.html', value="Logout", cart=cart, amount=amount)



if __name__ == "__main__":
    app.run(debug=True)
