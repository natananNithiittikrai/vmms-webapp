"""Test: Delete Vending Machine API."""

import pytest
from flask.testing import FlaskClient

END_POINT = "/api/vending_machines/delete"


def test_delete_vending_machine_status(client: FlaskClient):
    response = client.post(f"{END_POINT}/1")
    assert response.status_code == 200


@pytest.mark.parametrize("vending_machine", [{"id": 2}, {"id": 3}])
def test_delete_vending_machine_response_success(
    client: FlaskClient, vending_machine: dict
):
    response = client.post(f"{END_POINT}/{vending_machine['id']}")
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data is None
    assert response_json["status"] == "success"
    assert (
        response_json["message"]
        == f"vending machine {vending_machine['id']} is successfully deleted"
    )


@pytest.mark.parametrize("vending_machine", [{"id": 4}, {"id": 5}])
def test_delete_vending_machine_response_fail(
    client: FlaskClient, vending_machine: dict
):
    response = client.post(f"{END_POINT}/{vending_machine['id']}")
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data is None
    assert response_json["status"] == "error"
    assert (
        response_json["message"]
        == f"unable to delete vending machine {vending_machine['id']}"
    )
