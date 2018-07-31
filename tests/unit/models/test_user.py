from tests.unit.unit_base_test import UnitBaseTest
from models.user import UserModel


class TestUser(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test', '1234')

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, '1234')