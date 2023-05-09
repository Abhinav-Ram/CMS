
import os
import pathlib
import db
import numpy as np
import requests
from flask import Flask, session, abort, redirect, request, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from db import connect_db, FoodItem, CartItem, Order
from datetime import datetime

apps = Flask(__name__)


db = connect_db(apps, 'food_items.db')


apps.secret_key = "$U9GpV0Up"


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


@apps.route("/admin")
def hello():
    if 'username' in session:
        username = session['username']
        return redirect('/admin/dashboard')
    return render_template('admin_login.html', error="")


@apps.route('/admin/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    # Check if the username and password are valid
    if username == 'root' and password == 'ssn':
        # Set the user's username in the session
        session['username'] = username
        return redirect('/admin/dashboard')
    else:
        # Invalid credentials, redirect back to login page with an error message
        return


@apps.route("/admin/dashboard")
def main():
    cart_dict = dict()
    cart_items = CartItem.query.all()
    for cart_item in cart_items:
        if cart_item.id not in cart_dict:
            cart_dict[cart_item.id] = list()
        cart_dict[cart_item.id].append(
            cart_item.name + ' +' + str(cart_item.qty))
    if 'username' not in session:
        return redirect('/admin')
    return render_template('admin_dashboard.html', items=cart_dict, dashboard=" active")


@apps.route("/admin/menu")
def menu():
    food_items = FoodItem.query.all()
    if 'username' not in session:
        return redirect('/admin')
    return render_template('admin_menu.html', items=food_items, menu=" active")

@apps.route("/admin/menu/add",methods=['GET','POST'])
def add_item():
    food_items = FoodItem.query.all()
    if 'username' not in session:
        return redirect('/admin')
    return render_template('admin_menu_add.html', items=food_items, menu=" active")

@apps.route("/admin/menu/add/added",methods=['GET','POST'])
def added_item():
    if request.method == "POST":
        name = request.form["name"]
        print("Name=",name)
        price = request.form["price"]
        print("Price=",price)
        count = len(FoodItem.query.all())
        fooditem = FoodItem(id=count+1,name=name,price=price)
        db.session.add(fooditem)
        db.session.commit()
    return redirect('/admin/menu')

@apps.route("/admin/about")
def about():
    return render_template('admin_credits.html', about=" active")


@apps.route("/admin/logout")
def logout():
    session.clear()
    session.modified = True
    return redirect('/admin')


@apps.route("/admin/deliver-order/<string:id>")
def deliver(id):
    order = Order(id=id, date=datetime.now(), order_items=[])
    rem_order = CartItem.query.filter_by(id=id).all()
    for ind_rem_order in rem_order:
        order.order_items.append(ind_rem_order)
    for ind_rem_order in rem_order:
        db.session.delete(ind_rem_order)
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('main'))


if __name__ == "__main__":
    apps.run(debug=True, port=5050)
