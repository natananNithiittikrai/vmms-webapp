"""Test: Utilities."""

import pytest

from vmms_webapp.database import utils
from vmms_webapp.database.database_service import DatabaseService
from vmms_webapp.models.product import Product
from vmms_webapp.models.stock import Stock
from vmms_webapp.models.vending_machine import VendingMachine


def test_populate_products(database_service: DatabaseService):
    assert utils.get_products(database_service) == []
    utils.populate_products(database_service)
    assert utils.get_products(database_service) == [
        Product(id=1, name="taro", price=20.0),
        Product(id=2, name="pringle", price=30.0),
        Product(id=3, name="lay's", price=50.0),
    ]


def test_get_vending_machines(database_service: DatabaseService):
    assert utils.get_vending_machines(database_service) == []
    utils.add_vending_machine(
        database_service, VendingMachine(name="vm_001", location="loc_001")
    )
    assert len(utils.get_vending_machines(database_service)) == 1


def test_get_products(database_service: DatabaseService):
    assert len(utils.get_products(database_service)) == 3
    assert utils.get_products(database_service) == [
        Product(id=1, name="taro", price=20.0),
        Product(id=2, name="pringle", price=30.0),
        Product(id=3, name="lay's", price=50.0),
    ]


def test_get_vending_machine_by_id(database_service: DatabaseService):
    assert utils.get_vending_machine_by_id(database_service, 0) is None
    assert utils.get_vending_machine_by_id(database_service, 1).to_dict() == {
        "id": 1,
        "name": "vm_001",
        "location": "loc_001",
    }


def test_get_product_by_id(database_service: DatabaseService):
    assert utils.get_product_by_id(database_service, 0) is None
    assert utils.get_product_by_id(database_service, 1).to_dict() == {
        "name": "taro",
        "price": 20.0,
    }


@pytest.mark.parametrize(
    "product_stock",
    [
        {"vm_id": 1, "prod_id": 2, "stock": 200},
        {"vm_id": 1, "prod_id": 3, "stock": 300},
    ],
)
def test_get_stock_by_vm_id_and_prod_id(
    database_service: DatabaseService, product_stock: dict
):
    assert utils.get_stock_by_vm_id_and_prod_id(database_service, 0, 0) is None
    utils.add_product_stock(
        database_service,
        Stock(product_stock["vm_id"], product_stock["prod_id"], product_stock["stock"]),
    )
    assert (
        utils.get_stock_by_vm_id_and_prod_id(
            database_service, product_stock["vm_id"], product_stock["prod_id"]
        ).to_dict()
        == product_stock
    )


def test_get_product_choices_by_vm_id(database_service: DatabaseService):
    assert len(utils.get_product_choices_by_vm_id(database_service, 1)) == 1
    assert utils.get_product_choices_by_vm_id(database_service, 1) == [
        Product(id=1, name="taro", price=20.0),
    ]


def test_get_stocks_by_vm_id(database_service: DatabaseService):
    assert len(utils.get_stocks_by_vm_id(database_service, 1)) == 2
    assert utils.get_stocks_by_vm_id(database_service, 1) == {
        Product(id=2, name="pringle", price=30.0): 200,
        Product(id=3, name="lay's", price=50.0): 300,
    }
