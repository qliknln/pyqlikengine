import unittest
from pyqlikengine import QixEngine
import os


class TestLabs(unittest.TestCase):

    def setUp(self):
        self.qixe = QixEngine('ws://localhost:4848/app')

    def test_select_in_field(self):
        print ('sdfasef')
        app = os.path.join("C:/", "Users", "nln", "Documents", "Qlik", "Sense", "Apps", "Consumer Sales.qvf")
        self.qixe.open_app(app)
        print(self.qixe.select_in_dimension('Product Sub Group', ['Cheese']))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()