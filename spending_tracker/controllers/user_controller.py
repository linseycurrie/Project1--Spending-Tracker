from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.user import User
import repositories.transaction_repository as transaction_repository
import repositories.user_repository as user_repository

users_blueprint = Blueprint("users", __name__)

@users_blueprint.route("/users")
def users():
    return render_template("users/index.html", users=users)

@users_blueprint.route("/users/new", methods=['GET'])
def new_users():
    return render_template("users/new.html")

@users_blueprint.route("/users", methods=['POST'])
def create_user():
    name = request.form['name']
    savings_goal = request.form['savings_goal']
    spending_limit = request.form['spending_limit']
    user = User(name, spending_limit, savings_goal)
    user_repository.save(user)
    return render_template("/users/index.html", user=user)

@users_blueprint.route("/users/<id>", methods=['GET'])
def show_user_transactions():
    user = user_repository.select(id)
    filter_transactions = transaction_repository.filter_by_user(user)
    return render_template("/users/show.html", user=user, filter_transactions=filter_transactions)
