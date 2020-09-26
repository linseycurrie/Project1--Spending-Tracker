from db.run_sql import run_sql
from models.user import User
from models.merchant import Merchant
from models.transaction import Transaction
import repositories.merchant_repository as merchant_repository

def save(transaction):
    sql = "INSERT INTO transactions (amount, category, merchant_id) VALUES ( %s, %s, %s ) RETURNING *"
    values = [transaction.amount, transaction.category, transaction.merchant.id]
    results = run_sql(sql, values)
    id = results[0]['id']
    transaction.id = id
    return transaction

def select_all():
    transactions =[]

    sql= "SELECT * FROM transactions"
    results = run_sql(sql)
    
    for row in results:
        merchant = merchant_repository.select( row['merchant_id'] )
        transaction = Transaction( row['amount'], row['category'], merchant, row['id'] )
        transactions.append(transaction)
    return transactions

def select(id):
    transaction = None
    sql = "SELECT * FROM transactions WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    if result is not None:
        merchant = merchant_repository.select(result['merchant_id'])
        transaction = Transaction( result['amount'], result['category'], merchant, result['id'])
    return transaction