from engine_communicator import EngineCommunicator
from engine_global_api import EngineGlobalApi
from engine_app_api import EngineAppApi
from engine_generic_object_api import EngineGenericObjectApi
from engine_field_api import EngineFieldApi
from structs import Structs
import time
import unittest
import tempfile


class TestAppApi(unittest.TestCase):

    # Constructor to prepare everything before running the tests.
    def setUp(self):
        url = 'ws://localhost:4848/app'
        self.conn = EngineCommunicator(url)
        self.ega = EngineGlobalApi(self.conn)
        self.eaa = EngineAppApi(self.conn)
        self.egoa = EngineGenericObjectApi(self.conn)
        self.efa = EngineFieldApi(self.conn)
        self.struct = Structs()
        self.app = self.ega.create_app("TestApp")
        opened_app = self.ega.open_doc(self.app)
        self.app_handle = self.ega.get_handle(opened_app)

    def test_add_alternate_state(self):
        response = self.eaa.add_alternate_state(self.app_handle,"MyState")
        self.assertEqual(response, {}, "Failed to add alternate state")

    def test_create_hypercube_object(self):
        script = file('./test/test_data/ctrl00_script.qvs').read()
        self.eaa.set_script(self.app_handle,script)
        self.eaa.do_reload_ex(self.app_handle)
        hc_inline_dim = Structs.nx_inline_dimension_def(["Alpha"])
        hc_mes_sort = Structs.nx_sort_by()
        hc_inline_mes = Structs.nx_inline_measure_def("=Sum(Num)")
        hc_dim = Structs.nx_hypercube_dimensions(hc_inline_dim)
        hc_mes = Structs.nx_hypercube_measure(hc_mes_sort, hc_inline_mes)
        nx_page = Structs.nx_page(0, 0, 26, 2)
        hc_def = Structs.hypercube_def("$", [hc_dim],[hc_mes], [nx_page])
        hc_response = self.eaa.create_object(self.app_handle, "CH01", "Chart", "qHyperCubeDef", hc_def)
        hc_handle = self.ega.get_handle(hc_response)
        self.egoa.get_layout(hc_handle)
        hc_data = self.egoa.get_hypercube_data(hc_handle,"/qHyperCubeDef",[nx_page])
        self.assertTrue(type(hc_data is {}), "Unexpected type of hypercube data")
        first_element_number = hc_data["qDataPages"][0]["qMatrix"][0][0]["qElemNumber"]
        first_element_text = hc_data["qDataPages"][0]["qMatrix"][0][0]["qText"]
        self.assertTrue(first_element_number == 0, "Incorrect value in first element number")
        self.assertTrue(first_element_text == 'A', "Incorrect value in first element text")

    def tearDown(self):
        self.ega.delete_app(self.app)
        self.conn.close_qvengine_connection(self.conn)


if __name__ == '__main__':
    unittest.main()
