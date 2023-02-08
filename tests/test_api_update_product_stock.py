"""Test: Update Product Stock API."""

import pytest
from flask.testing import FlaskClient

END_POINT = "/api/product_stocks/update"


@pytest.mark.parametrize(
    "product_stocks",
    [
        {
            "vending_machine": {"id": 1, "name": "vm_001", "location": "loc_001"},
            "prod_id": 1,
            "stock": 0,
        },
        {
            "vending_machine": {"id": 2, "name": "vm_002", "location": "loc_002"},
            "prod_id": 2,
            "stock": 0,
        },
        {
            "vending_machine": {"id": 3, "name": "vm_003", "location": "loc_003"},
            "prod_id": 3,
            "stock": 0,
        },
    ],
)
def test_set_up(client: FlaskClient, product_stocks: dict):
    client.post("/api/vending_machines/add", data=product_stocks["vending_machine"])
    response = client.post(
        f"/api/product_stocks/add/{product_stocks['vending_machine']['id']}",
        data=product_stocks,
    )
    assert response.status_code == 200


def test_update_product_stocks_status(client: FlaskClient):
    response = client.post(
        f"{END_POINT}/1/1",
        data={
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
def test_update_product_stocks_response_success(
    client: FlaskClient, product_stock: dict
):
    response = client.post(
        f"{END_POINT}/{product_stock['vm_id']}/{product_stock['prod_id']}",
        data=product_stock,
    )
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data["post"] == product_stock
    assert response_json["status"] == "success"
    assert (
        response_json["message"]
        == f"product {product_stock['prod_id']} stock is successfully updated "
        f"in vending machine {product_stock['vm_id']}"
    )


@pytest.mark.parametrize(
    "product_stock",
    [
        {"vm_id": 4, "prod_id": 4, "stock": 400},
        {"vm_id": 5, "prod_id": 5, "stock": 500},
    ],
)
def test_update_product_stocks_response_fail(client: FlaskClient, product_stock: dict):
    test = client.get("/api/vending_machines")
    print(test.get_json())
    response = client.post(
        f"{END_POINT}/{product_stock['vm_id']}/{product_stock['prod_id']}",
        data=product_stock,
    )
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data["post"] == {}
    assert response_json["status"] == "error"
    assert (
        response_json["message"]
        == f"unable to update product {product_stock['prod_id']} "
        f"in vending machine {product_stock['vm_id']}"
    )


@pytest.mark.parametrize("vending_machine", [{"id": 1}, {"id": 2}, {"id": 3}])
def test_tear_down(client: FlaskClient, vending_machine: dict):
    response = client.post(f"/api/vending_machines/delete/{vending_machine['id']}")
    assert response.status_code == 200
