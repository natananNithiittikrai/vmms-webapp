from app import create_app
from database.database_service import DatabaseService
import unittest


class TestAPIUpdateProductStock(unittest.TestCase):

    def setUp(self) -> None:
        self.database_service = DatabaseService('sqlite://')
        self.app = create_app(self.database_service)
        self.app.config.update({
            'TESTING': True,
        })
        self.client = self.app.test_client()

    def test_basic(self):
        self.client.post("/api/vending_machines/add", data={
            'name': 'test_vm_001',
            'location': 'test_loc_001',
        })
        self.client.post("/api/product_stocks/add/1", data={
            'prod_id': 2,
            'stock': 100,
        })
        response = self.client.post("/api/product_stocks/update/1/2", data={
            'stock': 200,
        })
        assert response.status_code == 200

    def test_response_json(self):
        self.client.post("/api/vending_machines/add", data={
            'name': 'test_vm_001',
            'location': 'test_loc_001',
        })
        self.client.post("/api/product_stocks/add/1", data={
            'prod_id': 2,
            'stock': 100,
        })
        response = self.client.post("/api/product_stocks/update/1/2", data={
            'stock': 200,
        })
        response_json = response.get_json()
        response_data = response_json['data']
        keys = ['vm_id', 'prod_id', 'stock']
        expected_values = [1, 2, 200]
        assert all([response_data['post'][key] == expected_value for key, expected_value in zip(keys, expected_values)])
        assert response_json['status'] == 'success'
        assert response_json['message'] == 'product 2 stock is successfully updated in vending machine 1'

    def test_response_json_fail_not_exist(self):
        response = self.client.post("/api/product_stocks/update/1/2", data={
            'stock': 200,
        })
        response_json = response.get_json()
        response_data = response_json['data']
        assert response_data['post'] == {}
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'unable to update product 2 in vending machine 1'
