import unittest
from pyqlikengine import QixEngine


class TestQixEngine(unittest.TestCase):

    def setUp(self):
        self.qixe = QixEngine('ws://localhost:4848/app')
        app = self.qixe.create_app('test_app')
        self.assertTrue(app.endswith('.qvf'), 'Failed to create app')
        app_exists = self.qixe.create_app('test_app')
        self.assertTrue(app_exists == "App already exists", 'Failed to handle existing app exception')
        self.opened_app = self.qixe.open_app(app)
        with open('./test_data/ctrl00_script.qvs') as f:
            script = f.read()
        self.assertTrue(self.qixe.load_script(script), 'Failed to load script')

    def test_create_hypercube(self):
        hc = self.qixe.create_hypercube(['Dim1', 'Dim2'], ['=Sum(Expression1)', '=Sum(Expression2)', '=Sum(Expression3)'])
        hc_cols = self.qixe.convert_hypercube_to_matrix(hc[0], hc[1])
        self.assertTrue(len(hc_cols) == 5, 'Failed to return proper number of columns')
        self.inline_table = self.qixe.convert_hypercube_to_inline_table(hc[0], 'MyTable')
        self.assertTrue(self.inline_table.startswith('MyTable'), 'Failed to create inline statement from hypercube')
        self.mtrx = self.qixe.convert_hypercube_to_matrix(hc[0], hc[1])
        self.assertTrue(len(self.mtrx) == 5, 'Failed to create matrix from hypercube')

    def test_select_clear_in_dimension(self):
        select_result = self.qixe.select_in_dimension('Alpha', ['A', 'C', 'E'])
        self.assertTrue(select_result["change"] == [1, 2], "Failed to select values")
        self.assertTrue(select_result["result"]['qReturn'], "Failed to select values")
        self.assertTrue(self.qixe.clear_selection_in_dimension('Alpha'),'Failed to clear selection')

    def test_select_clear_all_in_dimension(self):
        select_result = self.qixe.select_in_dimension('Alpha', ['A', 'C', 'E'])
        self.assertTrue(select_result["change"] == [1, 2], "Failed to select values")
        self.assertTrue(select_result["result"]['qReturn'], "Failed to select values")
        self.qixe.clear_all_selections()

    def test_select_excluded(self):
        self.qixe.select_in_dimension('Alpha', ['A', 'C', 'E'])
        select_result = self.qixe.select_excluded_in_dimension('Alpha')
        self.assertTrue(select_result['qReturn'], 'Failed to select excluded')

    def test_select_possible(self):
        select_result = self.qixe.select_possible_in_dimension('Alpha')
        self.assertTrue(select_result['qReturn'], 'Failed to select possible')

    def test_get_list_object_data(self):
        self.assertTrue(len(self.qixe.get_list_object_data('Alpha')) == 26, 'Failed to get value list')

    def tearDown(self):
        self.assertTrue(self.qixe.delete_app(self.opened_app), 'Failed to delete app')


if __name__ == '__main__':
    unittest.main()
