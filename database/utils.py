from __future__ import annotations
from flask import Request
from models.vending_machine import VendingMachine
from models.product import Product
from models.stock import Stock
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from database.database_service import DatabaseService

DATABASE_PATH = f"sqlite:///{str(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vending_machine.db'))}"


def populate_products(database_service: DatabaseService) -> None:
    """Populates database with predefined products

    Args:
        database_service (DatabaseService): The object used to interact with database
    """
    try:
        with database_service.get_session().begin() as session:
            products = [
                Product(id=1, name='taro', price=20.0),
                Product(id=2, name='pringle', price=30.0),
                Product(id=3, name='lay\'s', price=50.0)
            ]
            session.add_all(products)
    except IntegrityError:
        pass
    except Exception as e:
        print('populate_products:', e)


def get_vending_machines(database_service: DatabaseService) -> list[VendingMachine]:
    """Gets all vending machines in vending_machines table

    Args:
        database_service (DatabaseService): The object used to interact with database

    Returns:
         list: A list of all vending machines in vending_machines table
    """
    session = database_service.get_session()()
    return session.query(VendingMachine).all()


def get_product_choices(database_service: DatabaseService) -> list[Product]:
    """Gets all products in products table

    Args:
        database_service (DatabaseService): The object used to interact with database

    Returns:
        list: A list of all products in products table
    """
    session = database_service.get_session()()
    return session.query(Product).all()


def get_vending_machine_by_id(database_service: DatabaseService, vm_id: int) -> VendingMachine:
    """Gets a vending machine with the specified id of vm_id

    Args:
        database_service (DatabaseService): The object used to interact with database
        vm_id (int): An id of the interested vending machine

    Returns:
        VendingMachine: A vending machine with the specified id of vm_id
    """
    session = database_service.get_session()()
    return session.query(VendingMachine).filter(VendingMachine.id == vm_id).first()


def get_product_choices_by_vm_id(database_service: DatabaseService, vm_id: int) -> list[Product]:
    """Gets products that can be added to a vending machine of the specified id of vm_id

    Args:
        database_service (DatabaseService): The object used to interact with database
        vm_id (int): An id of the interested vending machine

    Returns:
        list: A list of products that can be added to the vending machine vm_id
    """
    all_product_choices = get_product_choices(database_service)
    current_products = get_stocks_by_vm_id(database_service, vm_id).keys()
    current_products_ids = list(map(lambda product: product.id, current_products))
    return list(filter(
        lambda product_choice: product_choice.id not in current_products_ids,
        all_product_choices
    ))


def get_stocks_by_vm_id(database_service: DatabaseService, vm_id: int) -> dict[Product, int]:
    """Gets product stocks of a vending machine with the specified id of vm_id

    Args:
        database_service (DatabaseService): The object used to interact with database
        vm_id (int): An id of the interested vending machine

    Returns:
        dict: A dictionary mapping a product to its stock representing product stocks of the vending machine vm_id
    """
    session = database_service.get_session()()
    results = session.query(
        Stock.vm_id,
        Stock.prod_id,
        Product.name,
        Product.price,
        Stock.stock
    ).join(VendingMachine, VendingMachine.id == Stock.vm_id, isouter=True
           ).join(Product, Product.id == Stock.prod_id, isouter=True
                  ).filter(Stock.vm_id == vm_id).all()
    stocks = {}
    for result in results:
        _, prod_id, name, price, stock = result
        stocks[Product(prod_id, name, price)] = stock
    return stocks


def create_vending_machine_from_request(request: Request) -> VendingMachine:
    """Creates a vending machine from request

    Args:
        request (Request): A request that from the client

    Returns:
        VendingMachine: A vending machine with the specified values of attributes
    """
    return VendingMachine(request.form['name'], request.form['location'])


def add_vending_machine(database_service: DatabaseService, vending_machine: VendingMachine) -> dict:
    """Adds a vending machine to vending_machine table

    Args:
        database_service (DatabaseService): The object used to interact with database
        vending_machine (VendingMachine): A vending machine that needs to be added to the table

    Returns:
        dict: A dictionary representing the response
    """
    session = database_service.get_session()()
    session.add(vending_machine)
    session.commit()
    return {
        'status': 'success',
        'data': {
            'post': {'id': vending_machine.id} | vending_machine.to_dict()
        },
        'message': f'vending machine {vending_machine.id} is successfully added'
    }


def update_vending_machine(database_service: DatabaseService, new_vending_machine: VendingMachine, vm_id: int) -> dict:
    """Updates attributes of a vending machine with the specified id of vm_id

    Args:
        database_service (DatabaseService): The object used to interact with database
        new_vending_machine (VendingMachine): A vending machine with the desired values of attributes
        vm_id (int): An id of the interested vending machine

    Returns:
        dict: A dictionary representing the response
    """
    session = database_service.get_session()()
    vending_machine = session.query(VendingMachine).filter(VendingMachine.id == vm_id).first()
    vending_machine.name = new_vending_machine.name
    vending_machine.location = new_vending_machine.location
    session.commit()
    return {
        'status': 'success',
        'data': {
            'post': {'id': vending_machine.id} | vending_machine.to_dict()
        },
        'message': f'vending machine {vending_machine.id} is successfully updated'
    }


def delete_vending_machine(database_service: DatabaseService, vm_id: int) -> dict:
    """Deletes a vending machine with the specified id of vm_id

    Args:
        database_service (DatabaseService): The object used to interact with database
        vm_id (int): An id of the interested vending machine

    Returns:
        dict: A dictionary representing the response
    """
    session = database_service.get_session()()
    vending_machine = session.query(VendingMachine).filter(VendingMachine.id == vm_id).first()
    session.delete(vending_machine)
    session.query(Stock).filter(Stock.vm_id == vending_machine.id).delete()
    session.commit()
    return {
        'status': 'success',
        'data': None,
        'message': f'vending machine {vending_machine.id} is successfully deleted'
    }


def create_product_stock_from_request(request: Request, vm_id: int, prod_id: int = None) -> Stock:
    """Creates a product stock of a vending machine with the specified id of vm_id from request

    Args:
        request (Request): A request that from the client
        vm_id (int): An id of the interested vending machine
        prod_id (int): An id of the interested product
            (default is None)
    Returns:
        Stock: A product stock of the vending machine vm_id
    """
    if not prod_id:
        prod_id = request.form['prod_id']
    return Stock(vm_id, prod_id, request.form['stock'])


def add_product_stock(database_service: DatabaseService, product_stock: Stock) -> dict:
    """Adds a product stock to stocks table

    Args:
        database_service (DatabaseService): The object used to interact with database
        product_stock (Stock): A product stock that needs to be added to the table

    Returns:
        dict: A dictionary representing the response
    """
    session = database_service.get_session()()
    session.add(product_stock)
    session.commit()
    return {
        'status': 'success',
        'data': {
            'post': product_stock.to_dict()
        },
        'message': f'new product stock is successfully added to vending machine {product_stock.vm_id}'
    }


def update_product_stock(database_service: DatabaseService, new_product_stock: Stock) -> dict:
    """Updates attributes of a vending machine with the specified id of vm_id

    Args:
        database_service (DatabaseService): The object used to interact with database
        new_product_stock (Stock): A product stock with the desired values of attributes

    Returns:
        dict: A dictionary representing the response
    """
    session = database_service.get_session()()
    product_stock = session.query(Stock).filter(Stock.vm_id == new_product_stock.vm_id).first()
    product_stock.stock = new_product_stock.stock
    session.commit()
    return {
        'status': 'success',
        'data': {
            'post': product_stock.to_dict()
        },
        'message': f'product {product_stock.prod_id} stock is successfully updated in vending machine {product_stock.vm_id}'
    }


def delete_product_stock(database_service: DatabaseService, vm_id: int, prod_id: int) -> dict:
    """Deletes a product stock with the specified vm_id and prod_id

    Args:
        database_service (DatabaseService): The object used to interact with database
        vm_id (int): An id of the interested vending machine
        prod_id (int): An id of the interested product

    Returns:
        dict: A dictionary representing the response
    """
    session = database_service.get_session()()
    product_stock = session.query(Stock).filter(Stock.vm_id == vm_id, Stock.prod_id == prod_id).first()
    session.delete(product_stock)
    session.commit()
    return {
        'status': 'success',
        'data': None,
        'message': f'product {product_stock.prod_id} is successfully deleted from vending machine {product_stock.vm_id}'
    }
