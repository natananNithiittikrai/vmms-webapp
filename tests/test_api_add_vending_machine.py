"""Test: Add Vending Machine API."""

import unittest

from vmms_webapp.app import create_app
from vmms_webapp.database.database_service import DatabaseService


class TestAPIAddVendingMachine(unittest.TestCase):
    """A class used to test adding vending machine API."""

    def setUp(self) -> None:
        self.database_service = DatabaseService("sqlite://")
        self.app = create_app(self.database_service)
        self.app.config.update(
            {
                "TESTING": True,
            }
        )
        self.client = self.app.test_client()

    def test_basic(self) -> None:
        response = self.client.post(
            "/api/vending_machines/add",
            data={
                "name": "test_vm_001",
                "location": "test_loc_001",
            },
        )
        assert response.status_code == 200

    def test_response_json(self) -> None:
        response = self.client.post(
            "/api/vending_machines/add",
            data={
                "name": "test_vm_001",
                "location": "test_loc_001",
            },
        )
        response_json = response.get_json()
        response_data = response_json["data"]
        keys = ["id", "name", "location"]
        expected_values = [1, "test_vm_001", "test_loc_001"]
        assert all(
            [
                response_data["post"][key] == expected_value
                for key, expected_value in zip(keys, expected_values)
            ]
        )
        assert response_json["status"] == "success"
        assert response_json["message"] == "vending machine 1 is successfully added"
