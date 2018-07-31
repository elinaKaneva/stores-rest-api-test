from tests.unit.unit_base_test import UnitBaseTest

from models.store import StoreModel


class TestStore(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('test')

        self.assertEqual(store.name, 'test')