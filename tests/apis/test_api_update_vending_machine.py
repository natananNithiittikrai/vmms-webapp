"""Test: Update Vending Machine API."""

import pytest
from flask.testing import FlaskClient

END_POINT = "/api/vending_machines/update"


def test_update_vending_machine_status(client: FlaskClient):
    client.post(
        "/api/vending_machines/add",
        data={"id": 1, "name": "test_vm_001", "location": "test_loc_001"},
    )
    response = client.post(
        f"{END_POINT}/1",
        data={
            "name": "vm_001",
            "location": "loc_001",
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
def test_update_vending_machine_response_success(
    client: FlaskClient, vending_machine: dict
):
    client.post("/api/vending_machines/add", data=vending_machine)
    new_vending_machine = {
        "id": vending_machine["id"],
        "name": vending_machine["name"][5:],
        "location": vending_machine["location"][5:],
    }
    response = client.post(
        f"{END_POINT}/{vending_machine['id']}",
        data=new_vending_machine,
    )
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data["post"] == new_vending_machine
    assert response_json["status"] == "success"
    assert (
        response_json["message"]
        == f"vending machine {vending_machine['id']} is successfully updated"
    )


@pytest.mark.parametrize(
    "vending_machine",
    [
        {"id": 4, "name": "vm_004", "location": "loc_004"},
        {"id": 5, "name": "vm_005", "location": "loc_005"},
    ],
)
def test_update_vending_machine_response_fail(
    client: FlaskClient, vending_machine: dict
):
    response = client.post(
        f"{END_POINT}/{vending_machine['id']}",
        data=vending_machine,
    )
    response_json = response.get_json()
    response_data = response_json["data"]
    assert response_data["post"] == {}
    assert response_json["status"] == "error"
    assert (
        response_json["message"]
        == f"unable to update vending machine {vending_machine['id']}"
    )
