from app import create_app
from database.database_service import DatabaseService
import unittest


class TestAPIDeleteVendingMachine(unittest.TestCase):

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
        response = self.client.post("/api/vending_machines/delete/1")
        assert response.status_code == 200

    def test_response_json(self):
        self.client.post("/api/vending_machines/add", data={
            'name': 'test_vm_001',
            'location': 'test_loc_001',
        })
        response = self.client.post("/api/vending_machines/delete/1")
        response_json = response.get_json()
        response_data = response_json['data']
        assert response_data is None
        assert response_json['status'] == 'success'
        assert response_json['message'] == 'vending machine 1 is successfully deleted'

    def test_response_json_fail_not_exist(self):
        response = self.client.post("/api/vending_machines/delete/1", data={
            'name': 'vm_001',
            'location': 'loc_001',
        })
        response_json = response.get_json()
        response_data = response_json['data']
        assert response_data is None
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'unable to delete vending machine 1'
