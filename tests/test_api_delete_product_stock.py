"""Test: Delete Product Stock API."""

import pytest
from flask.testing import FlaskClient

END_POINT = "/api/product_stocks/delete"


@pytest.mark.parametrize(
    "product_stocks",
    [
        {"vm_id": 1, "prod_id": 1, "stock": 100},
        {"vm_id": 2, "prod_id": 2, "stock": 200},
        {"vm_id": 3, "prod_id": 3, "stock": 300},
    ],
)
def test_set_up(client: FlaskClient, product_stocks: dict):
    response = client.post(
        f"/api/product_stocks/add/{product_stocks['vm_id']}", data=product_stocks
    )
    assert response.status_code == 200


def test_delete_product_stocks_status(client: FlaskClient):
    response = client.post(f"{END_POINT}/1/1")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "product_stock", [{"vm_id": 2, "prod_id": 2}, {"vm_id": 3, "prod_id": 3}]
)
def test_delete_product_stocks_response_success(
    client: FlaskClient, product_stock: dict
):
    response = client.post(
        f"{END_POINT}/{product_stock['vm_id']}/{product_stock['prod_id']}"
    )
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data is None
    assert response_json["status"] == "success"
    assert (
        response_json["message"]
        == f"product {product_stock['prod_id']} is successfully deleted "
        f"from vending machine {product_stock['vm_id']}"
    )


@pytest.mark.parametrize(
    "product_stock", [{"vm_id": 4, "prod_id": 4}, {"vm_id": 5, "prod_id": 5}]
)
def test_delete_product_stocks_response_fail(client: FlaskClient, product_stock: dict):
    response = client.post(
        f"{END_POINT}/{product_stock['vm_id']}/{product_stock['prod_id']}"
    )
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data is None
    assert response_json["status"] == "error"
    assert (
        response_json["message"]
        == f"unable to delete product {product_stock['prod_id']} "
        f"from vending machine {product_stock['vm_id']}"
    )
