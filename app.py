from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from database import utils
from models.base import Base

app = Flask(__name__)

# SECURITY WARNING:
# make sure the secret key is complex and secret in production
# this will be used to encrypt the cookies
app.secret_key = 'use-more-complex-secret-key-please'

# setup database
engine = create_engine(f'sqlite:///{utils.DATABASE_PATH}')
# create tables
Base.metadata.create_all(engine, checkfirst = True)
# populate products table so that every functionality can be used
utils.populate_products()

@app.route("/")
def index():
    vms = utils.get_vending_machines()
    return render_template(
        'index.html',
        data = [
            (vm, utils.get_product_choices_by_vm_id(vm.vm_id), utils.get_stocks_by_vm_id(vm.vm_id))
            for vm in vms
        ]
    )


@app.route("/vending_machines/add")
def add_vending_machine():
    return render_template('add.html')


@app.route("/vending_machines/update/<vm_id>")
def update_vending_machine(vm_id):
    vm = utils.get_vending_machine_by_id(vm_id)
    return render_template('update.html', vending_machine = vm)


@app.route("/api/vending_machines/add", methods = ["POST"])
def api_add_vending_machine():
    response = {}
    try:
        with utils.get_connection() as connection:
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


@app.route("/api/vending_machines/update/<vm_id>", methods = ["POST"])
def api_update_vending_machine(vm_id):
    response = {}
    try:
        with utils.get_connection() as connection:
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
        with utils.get_connection() as connection:
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


@app.route("/api/product_stocks/add/<vm_id>", methods = ["POST"])
def api_add_product_stock(vm_id):
    response = {}
    try:
        with utils.get_connection() as connection:
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


@app.route("/api/product_stocks/update/<vm_id>/<prod_id>", methods = ["POST"])
def api_update_product_stock(vm_id, prod_id):
    response = {}
    try:
        with utils.get_connection() as connection:
            keys = ['stock']
            updated_vending_machine = { key: request.form[key] for key in keys }
            cursor = connection.cursor()
            cursor.execute('''
                        UPDATE stocks
                        SET stock = ?
                        WHERE
                            vm_id = ? AND prod_id = ? 
                    ''', (updated_vending_machine['stock'], vm_id, prod_id))
            connection.commit()
            response['status'] = 'success'
            response['data'] = {
                'post': {'vm_id': vm_id, 'prod_id' : prod_id } | updated_vending_machine
            }
            response['message'] = f'product {prod_id} is successfully updated in vending machine {vm_id}'
    except Exception as e:
        response['status'] = 'error'
        response['data'] = {'post': {}}
        response['message'] = f'unable to update product {prod_id} in vending machine {vm_id}: {str(e)}'
    return jsonify(response)

@app.route("/api/product_stocks/delete/<vm_id>/<prod_id>", methods = ["POST"])
def api_delete_product_stock(vm_id, prod_id):
    response = {}
    try:
        with utils.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(f'''
                    DELETE FROM stocks WHERE vm_id = {vm_id} AND prod_id = {prod_id}
                ''')
            connection.commit()
            response['status'] = 'success'
            response['data'] = None
            response['message'] = f'product {prod_id} is successfully deleted from vending machine {vm_id}'
    except Exception as e:
        response['status'] = 'error'
        response['data'] = None
        response['message'] = f'unable to delete product {prod_id} from vending machine {vm_id}: {str(e)}'
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug = True)
