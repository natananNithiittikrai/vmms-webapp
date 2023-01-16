from vending_machine import VendingMachine
from product import Product
from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

# SECURITY WARNING:
# make sure the secret key is complex and secret in production
# this will be used to encrypt the cookies
app.secret_key = 'use-more-complex-secret-key-please'


@app.route("/")
def index():
    vending_machines = get_vending_machines()
    return render_template('index.html', vending_machines = vending_machines)


def get_vending_machines():
    vending_machines = []
    with sqlite3.connect('database/vending_machine.db') as connection:
        cursor = connection.cursor()
        results = cursor.execute('''
            SELECT * FROM vending_machines
        ''')
        for result in results.fetchall():
            vm_id, name, location = result
            vending_machine = VendingMachine(vm_id, name, location, get_stocks(vm_id))
            vending_machines.append(vending_machine)
        return vending_machines


def get_stocks(vm_id):
    with sqlite3.connect('database/vending_machine.db') as connection:
        cursor = connection.cursor()
        results = cursor.execute(f'''
            SELECT s.prod_id, p.name, p.price, s.stock FROM stocks AS s
            LEFT JOIN vending_machines AS v
                ON s.vm_id = v.id
            LEFT JOIN products AS p
                ON s.prod_id = p.id
            WHERE v.id = {vm_id}            
        ''')
        stocks = {}
        for result in results.fetchall():
            prod_id, name, price, stock = result
            stocks[Product(prod_id, name, price)] = stock
        return stocks


'''
initialize database by creating the .db file and necessary tables if they do not exist
'''
def init_database():
    if not os.path.exists('database'):
        os.makedirs('database')
    with sqlite3.connect('database/vending_machine.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vending_machines (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                name VARCHAR(50), 
                location VARCHAR(100)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                name VARCHAR(50), 
                price DECIMAL(10, 5)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                vm_id INTEGER, 
                prod_id INTEGER,
                stock INTEGER, 
                FOREIGN KEY(vm_id) REFERENCES vending_machines(id),
                FOREIGN KEY(prod_id) REFERENCES products(id),
                PRIMARY KEY (prod_id, vm_id)
            )
        ''')


if __name__ == '__main__':
    init_database()
    app.run(debug = True)
