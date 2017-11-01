import unittest
from qix_engine import QixEngine


class TestQixEngine(unittest.TestCase):

    def setUp(self):
        self.qixe = QixEngine('ws://localhost:4848/app')
        self.opened_app = ''

    def test_create_open_reload_delete_app(self):
        app = self.qixe.create_app('test_app')
        self.assertTrue(app.endswith('.qvf'), 'Failed to create app')
        self.opened_app = self.qixe.open_app(app)

        script = file('./test_data/ctrl00_script.qvs').read()
        self.assertTrue(self.qixe.load_script(script), 'Failed to load script')
        select_result = self.qixe.select_in_dimension('Alpha', ['A', 'C', 'E'])
        self.assertTrue(select_result[1] == [1,2], "Failed to select values")
        self.assertTrue(select_result[0]['qReturn'], "Failed to select values")
        hc = self.qixe.create_hypercube(['Dim1', 'Dim2'], ['=Sum(Expression1)', '=Sum(Expression2)', '=Sum(Expression3)'])
        hc_cols = self.qixe.convert_hypercube_to_matrix(hc[0], hc[1])
        self.assertTrue(len(hc_cols) == 5, 'Failed to return proper number of columns')
        print self.qixe.convert_hypercube_to_inline_table(hc[0], 'MyTable', hc[1])

    def tearDown(self):
        self.assertTrue(self.qixe.delete_app(self.opened_app), 'Failed to delete app')


if __name__ == '__main__':
    unittest.main()
