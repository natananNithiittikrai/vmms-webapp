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
    return render_template('index.html')


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
                id INT, 
                name VARCHAR(50), 
                location VARCHAR(100)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INT, 
                vm_id INT, 
                name VARCHAR(50), 
                price DECIMAL(10, 2), 
                stock INT
            )
        ''')


if __name__ == '__main__':
    # init_database()
    app.run(debug = True)
