"""Test: Add Product Stock API."""

import pytest
from flask.testing import FlaskClient

END_POINT = "/api/product_stocks/add"


@pytest.mark.parametrize(
    "vending_machine",
    [
        {"name": "vm_001", "location": "loc_001"},
        {"name": "vm_002", "location": "loc_002"},
        {"name": "vm_003", "location": "loc_003"},
    ],
)
def test_set_up(client: FlaskClient, vending_machine: dict):
    response = client.post("/api/vending_machines/add", data=vending_machine)
    assert response.status_code == 200


def test_add_product_stocks_status(client: FlaskClient):
    test = client.get("/api/vending_machines/")
    print(test.get_json())
    response = client.post(
        f"{END_POINT}/1",
        data={
            "prod_id": 2,
            "stock": 100,
        },
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    "product_stock",
    [
        {"vm_id": 2, "prod_id": 2, "stock": 200},
        {"vm_id": 3, "prod_id": 3, "stock": 300},
    ],
)
def test_add_product_stocks_response_success(client: FlaskClient, product_stock: dict):
    response = client.post(
        f"{END_POINT}/{product_stock['vm_id']}",
        data=product_stock,
    )
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data["post"] == product_stock
    assert response_json["status"] == "success"
    assert (
        response_json["message"] == f"new product stock is successfully added "
        f"to vending machine {product_stock['vm_id']}"
    )


@pytest.mark.parametrize(
    "product_stock",
    [
        {"vm_id": 4, "prod_id": 4, "stock": 400},
        {"vm_id": 5, "prod_id": 5, "stock": 500},
    ],
)
def test_add_product_stocks_response_fail(client: FlaskClient, product_stock: dict):
    response = client.post(
        f"{END_POINT}/{product_stock['vm_id']}",
        data=product_stock,
    )
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data["post"] == {}
    assert response_json["status"] == "error"
    assert (
        response_json["message"] == f"unable to add new product stock "
        f"to vending machine {product_stock['vm_id']}"
    )


@pytest.mark.parametrize("vending_machine", [{"id": 1}, {"id": 2}, {"id": 3}])
def test_tear_down(client: FlaskClient, vending_machine: dict):
    response = client.post(f"/api/vending_machines/delete/{vending_machine['id']}")
    assert response.status_code == 200
