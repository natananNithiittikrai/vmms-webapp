"""Test: Delete Product Stock API."""

import unittest

from app import create_app
from database.database_service import DatabaseService


class TestAPIDeleteProductStock(unittest.TestCase):
    """A class used to test deleting product stock API."""

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
        self.client.post(
            "/api/vending_machines/add",
            data={
                "name": "test_vm_001",
                "location": "test_loc_001",
            },
        )
        self.client.post(
            "/api/product_stocks/add/1",
            data={
                "prod_id": 2,
                "stock": 100,
            },
        )
        response = self.client.post("/api/product_stocks/delete/1/2")
        assert response.status_code == 200

    def test_response_json(self) -> None:
        self.client.post(
            "/api/vending_machines/add",
            data={
                "name": "test_vm_001",
                "location": "test_loc_001",
            },
        )
        self.client.post(
            "/api/product_stocks/add/1",
            data={
                "prod_id": 2,
                "stock": 100,
            },
        )
        response = self.client.post("/api/product_stocks/delete/1/2")
        response_json = response.get_json()
        response_data = response_json["data"]
        assert response_data is None
        assert response_json["status"] == "success"
        assert (
            response_json["message"]
            == "product 2 is successfully deleted from vending machine 1"
        )

    def test_response_json_fail_not_exist(self) -> None:
        response = self.client.post("/api/product_stocks/delete/1/2")
        response_json = response.get_json()
        response_data = response_json["data"]
        assert response_data is None
        assert response_json["status"] == "error"
        assert (
            response_json["message"]
            == "unable to delete product 2 from vending machine 1"
        )
