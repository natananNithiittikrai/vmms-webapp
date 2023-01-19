from models.vending_machine import VendingMachine
from models.product import Product
from models.stock import Stock
import sqlite3

DATABASE_PATH = 'database/vending_machine.db'

SELECT_ALL_DATA_SQL = '''
    SELECT s.vm_id, s.prod_id, p.name, p.price, s.stock FROM stocks AS s
    LEFT JOIN vending_machines AS v
        ON s.vm_id = v.id
    LEFT JOIN products AS p
        ON s.prod_id = p.id         
'''


"""
return an SQL statement for selecting all from a specified table

args:
    table (str): a table name

returns:
    str: an SQL select all statement for a specified table
"""
def select_all_from(table):
    return f'SELECT * FROM {table}'


"""
create a database connection to the SQLite database

returns:
    Connection object or None
"""
def get_connection():
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        print(e)
    return connection


"""
populate data in products table
"""
def populate_products():
    products = [
        (1, 'taro', 20.0),
        (2, 'pringle', 30.0),
        (3, 'lay', 50.0)
    ]
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.executemany('''
                INSERT INTO products VALUES (
                    ?, ?, ?
                )
            ''', products)
            connection.commit()
    except Exception as e:
        pass


"""
return a list of vending machines in vending_machines table

returns:
    list: a list of VendingMachine objects
"""
def get_vending_machines():
    vending_machines = []
    with get_connection() as connection:
        cursor = connection.cursor()
        results = cursor.execute(select_all_from('vending_machines'))
        for result in results:
            vm_id, name, location = result
            vending_machine = VendingMachine(vm_id, name, location)
            vending_machines.append(vending_machine)
    return vending_machines


"""
return a list of products in products table

returns:
    list: a list of Product objects 
"""
def get_product_choices():
    product_choices = []
    with get_connection() as connection:
        cursor = connection.cursor()
        results = cursor.execute(select_all_from('products'))
        for result in results.fetchall():
            prod_id, name, price = result
            product = Product(prod_id, name, price)
            product_choices.append(product)
    return product_choices


"""
return a dictionary mapping each product in the vending machine to the number of remaining stock

args:
    vm_id (int): an id of vending machine
    
returns:
    dict: a dictionary of Product to number of stock in int
"""
def get_stocks_by_vm_id(vm_id):
    stocks = {}
    with get_connection() as connection:
        cursor = connection.cursor()
        results = cursor.execute(SELECT_ALL_DATA_SQL + f'WHERE s.vm_id = {vm_id}')
        for result in results.fetchall():
            _, prod_id, name, price, stock = result
            stocks[Product(prod_id, name, price)] = stock
    return stocks


"""
return a list of products that the specified vending machine does not currently have

args: 
    vm_id (int): an id of vending machine
    
returns:
    list: a list of Product that are not in the specified vending machine
"""
def get_product_choices_by_vm_id(vm_id):
    all_product_choices = get_product_choices()
    current_products = get_stocks_by_vm_id(vm_id).keys()
    return list(filter(
        lambda choice : choice.prod_id not in map(lambda product : product.prod_id, current_products),
        all_product_choices
    ))


"""
return a vending machine with the specified vm_id

args: 
    vm_id (int): an id of vending machine
    
returns:
    VendingMachine: a vending machine with the specified vm_id
"""
def get_vending_machine_by_id(vm_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(f'''
            SELECT * FROM vending_machines WHERE id = {vm_id} 
        ''')
        result = cursor.fetchone()
        vm_id, name, location = result
        return VendingMachine(vm_id, name, location)
