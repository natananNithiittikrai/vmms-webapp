"""Test: Add Vending Machine API."""

import pytest
from flask.testing import FlaskClient

END_POINT = "/api/vending_machines/add"


def test_add_vending_machine_status(client: FlaskClient):
    response = client.post(
        END_POINT,
        data={
            "name": "test_vm_001",
            "location": "test_loc_001",
        },
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    "vending_machine",
    [
        {"id": 2, "name": "test_vm_002", "location": "test_loc_002"},
        {"id": 3, "name": "test_vm_003", "location": "test_loc_003"},
    ],
)
def test_add_vending_machine_response_success(
    client: FlaskClient, vending_machine: dict
):
    response = client.post(END_POINT, data=vending_machine)
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data["post"] == vending_machine
    assert response_json["status"] == "success"
    assert (
        response_json["message"]
        == f"vending machine {vending_machine['id']} is successfully added"
    )


@pytest.mark.parametrize(
    "vending_machine",
    [
        {"name": "test_vm_004"},
        {"location": "test_loc_005"},
    ],
)
def test_add_vending_machine_response_fail(client: FlaskClient, vending_machine: dict):
    response = client.post(END_POINT, data=vending_machine)
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data["post"] == {}
    assert response_json["status"] == "error"
    assert response_json["message"] == "unable to add new vending machine"
