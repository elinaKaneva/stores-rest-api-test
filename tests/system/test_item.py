import json
from tests.base_test import BaseTest

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel


class TestItem(BaseTest):
    def setUp(self):
        super(TestItem, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')

                self.assertEqual(resp.status_code, 400) # while it should be 401

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                header = {'Authorization': self.access_token}

                resp = client.get('/item/test',
                                  headers = header)

                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                header = {'Authorization': self.access_token}

                resp = client.get('/item/test',
                                  headers = header)

                self.assertEqual(resp.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.delete('/item/test')

                self.assertEqual(resp.status_code, 200)
                self.assertEqual({'message': 'Item deleted'},
                                 json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.post('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertEqual({'name': 'test', 'price': 19.99},
                                 json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.post('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 400)
                self.assertEqual({'message': "An item with name 'test' already exists."},
                                 json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.put('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)
                self.assertEqual({'name': 'test', 'price': 19.99},
                                 json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 10.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 10.99)

                resp = client.put('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)
                self.assertEqual({'name': 'test', 'price': 19.99},
                                 json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.get('/items')

                self.assertEqual(resp.status_code, 200)
                self.assertEqual({'items': [{'name': 'test', 'price': 19.99}]},
                                 json.loads(resp.data))