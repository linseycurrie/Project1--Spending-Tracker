from flask import Flask, render_template, request, redirect
from flask import Blueprint
from ..models.transaction import Transaction
from ..repositories import merchant_repository as merchant_repository
from ..repositories import transaction_repository as transaction_repository
from ..repositories import user_repository as user_repository
from ..repositories import category_repository as category_repository

transactions_blueprint = Blueprint("transactions", __name__)

@transactions_blueprint.route("/transactions")
def transactions():
    all_transactions = transaction_repository.select_all()
    total = transaction_repository.total_amount(all_transactions)
    transactions = transaction_repository.sort_transactions(all_transactions)
    users = user_repository.select_all()
    categorys = category_repository.select_all()
    return render_template("transactions/index.html", transactions=transactions, total=total, categorys=categorys, users=users)

@transactions_blueprint.route("/transactions/new", methods=['GET'])
def new_transaction():
    merchants = merchant_repository.select_all()
    categorys = category_repository.select_all()
    users = user_repository.select_all()
    return render_template("transactions/new.html", merchants=merchants, categorys=categorys, users=users)

@transactions_blueprint.route("/transactions", methods=['POST'])
def create_transactions():
    amount      = request.form['amount']
    category    = category_repository.select(request.form['category_id'])
    date        = request.form['date']
    merchant    = merchant_repository.select(request.form['merchant_id'])
    user        = user_repository.select(request.form['user_id'])
    transaction = Transaction(amount, category, date, merchant, user)
    transaction_repository.save(transaction)
    return redirect("/transactions")

@transactions_blueprint.route("/transactions/<id>/edit", methods=['GET'])
def edit_transaction(id):
    transaction = transaction_repository.select(id)
    merchants = merchant_repository.select_all()
    categorys = category_repository.select_all()
    users = user_repository.select_all()
    return render_template("transactions/edit.html", transaction=transaction, merchants=merchants, categorys=categorys, users=users)

@transactions_blueprint.route("/transactions/<id>", methods=['POST'])
def update_transaction(id):
    amount = request.form['amount']
    category = category_repository.select(request.form['category_id'])
    date = request.form['date']
    merchant = merchant_repository.select(request.form['merchant_id'])
    user = user_repository.select(request.form['user_id'])
    transaction = Transaction(amount, category, date, merchant, user, id)
    transaction_repository.update(transaction)
    return redirect("/transactions")

@transactions_blueprint.route("/transactions/<id>/delete", methods=['POST'])
def delete_transaction(id):
    transaction_repository.delete(id)
    return redirect("/transactions")

@transactions_blueprint.route("/transactions/filteredmonth", methods=['POST'])
def filter_month():
    filter = request.form['filter']
    filtered_transactions = transaction_repository.filter_by_month(filter)
    categorys = category_repository.select_all()
    users = user_repository.select_all()
    total = transaction_repository.total_amount(filtered_transactions)
    return render_template("transactions/index.html", transactions=filtered_transactions, categorys=categorys, users=users, total=total)

@transactions_blueprint.route("/transactions/filteredcategory", methods=['POST'])
def filter_category():
    filter = request.form['filter']
    filtered_transactions = transaction_repository.filter_by_category(filter)
    categorys = category_repository.select_all()
    users = user_repository.select_all()
    total = transaction_repository.total_amount(filtered_transactions)
    return render_template("transactions/index.html", transactions=filtered_transactions, categorys=categorys, users=users, total=total)