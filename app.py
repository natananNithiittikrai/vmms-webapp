from vending_machine import VendingMachine
from product import Product
from flask import Flask, render_template, request, jsonify
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
    product_choices = get_product_choices()
    vending_machines_product_choices = []
    for vending_machine in vending_machines:
        choices = filter(
            lambda choice : choice.id not in map(lambda product : product.id, vending_machine.products.keys()),
            product_choices
        )
        vending_machines_product_choices.append(
            (vending_machine, list(choices))
        )
    return render_template('index.html', vending_machines = vending_machines_product_choices)


@app.route("/vending_machines/add")
def add_vending_machine():
    return render_template('add.html')


@app.route("/vending_machines/update/<vm_id>")
def update_vending_machine(vm_id):
    vending_machine = get_vending_machine_by_id(vm_id)
    return render_template('update.html', vending_machine = vending_machine)


@app.route("/api/product_stocks/add/<vm_id>", methods = ["POST"])
def api_add_product_stock(vm_id):
    response = {}
    try:
        with sqlite3.connect('database/vending_machine.db') as connection:
            keys = ['prod_id', 'stock']
            added_product_stock = { key: request.form[key] for key in keys }
            cursor = connection.cursor()
            cursor.execute('''
                    INSERT INTO stocks VALUES (
                        ?, ?, ?
                    )
                ''', tuple([vm_id]) + tuple(added_product_stock.values()))
            connection.commit()
            response['status'] = 'success'
            response['data'] = {
                'post': {'vm_id': vm_id} | added_product_stock
            }
            response['message'] = f'new product stock is successfully added'
    except Exception as e:
        response['status'] = 'error'
        response['data'] = {'post': {}}
        response['message'] = f'unable to add new product stock: {str(e)}'
    return jsonify(response)


@app.route("/api/vending_machines/update/<vm_id>", methods = ["POST"])
def api_update_vending_machine(vm_id):
    response = {}
    try:
        with sqlite3.connect('database/vending_machine.db') as connection:
            keys = ['name', 'location']
            updated_vending_machine = { key : request.form[key] for key in keys }
            cursor = connection.cursor()
            cursor.execute('''
                    UPDATE vending_machines
                    SET name = ?,
                        location = ?
                    WHERE
                        id = ?
                ''', tuple(updated_vending_machine.values()) + tuple([vm_id]))
            connection.commit()
            response['status'] = 'success'
            response['data'] = {
                'post': {'id': vm_id} | updated_vending_machine
            }
            response['message'] = f'vending machine {vm_id} is successfully updated'
    except Exception as e:
        response['status'] = 'error'
        response['data'] = {'post': {}}
        response['message'] = f'unable to update vending machine {vm_id}: {str(e)}'
    return jsonify(response)


@app.route("/api/vending_machines/delete/<vm_id>", methods = ["POST"])
def api_delete_vending_machine(vm_id):
    response = {}
    try:
        with sqlite3.connect('database/vending_machine.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'''
                DELETE FROM vending_machines WHERE id = {vm_id}
            ''')
            connection.commit()
            response['status'] = 'success'
            response['data'] = None
            response['message'] = f'vending machine {vm_id} is successfully deleted'
    except Exception as e:
        response['status'] = 'error'
        response['data'] = None
        response['message'] = f'unable to delete vending machine {vm_id}: {str(e)}'
    return jsonify(response)


@app.route("/api/vending_machines/add", methods = ["POST"])
def api_add_vending_machine():
    response = {}
    try:
        with sqlite3.connect('database/vending_machine.db') as connection:
            keys = ['name', 'location']
            added_vending_machine = { key : request.form[key] for key in keys }
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO vending_machines VALUES (
                    ?, ?, ?
                )
            ''', tuple([None]) + tuple(added_vending_machine.values()))
            connection.commit()
            response['status'] = 'success'
            response['data'] = {
                'post' : { 'id' : cursor.lastrowid } | added_vending_machine
            }
            response['message'] = f'vending machine {cursor.lastrowid} is successfully added'
    except Exception as e:
        response['status'] = 'error'
        response['data'] = { 'post' : {} }
        response['message'] = f'unable to add new vending machine: {str(e)}'
    return jsonify(response)


def get_vending_machine_by_id(vm_id):
    with sqlite3.connect('database/vending_machine.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f'''
            SELECT * FROM vending_machines WHERE id = {vm_id} 
        ''')
        result = cursor.fetchone()
        vm_id, name, location = result
        return VendingMachine(vm_id, name, location, get_stocks(vm_id))


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


def get_product_choices():
    product_choices = []
    with sqlite3.connect('database/vending_machine.db') as connection:
        cursor = connection.cursor()
        results = cursor.execute('''
                SELECT * FROM products
            ''')
        for result in results.fetchall():
            prod_id, name, price = result
            product = Product(prod_id, name, price)
            product_choices.append(product)
        return product_choices

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
