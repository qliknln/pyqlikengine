import unittest

from engine_app_api import EngineAppApi
from engine_communicator import EngineCommunicator
from engine_field_api import EngineFieldApi
from engine_global_api import EngineGlobalApi
from structs import Structs

from engine_generic_object_api import EngineGenericObjectApi


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
        self.app = self.ega.create_app("TestApp")['qAppId']
        opened_app = self.ega.open_doc(self.app)
        self.app_handle = self.ega.get_handle(opened_app['qReturn'])

    def test_add_alternate_state(self):
        response = self.eaa.add_alternate_state(self.app_handle,"MyState")
        self.assertEqual(response, {}, "Failed to add alternate state")

    def test_create_hypercube_object(self):
        with open('./test/test_data/ctrl00_script.qvs') as f:
            script = f.read()
        self.eaa.set_script(self.app_handle,script)
        self.eaa.do_reload_ex(self.app_handle)

        #Create the inline dimension structures
        hc_inline_dim1 = Structs.nx_inline_dimension_def(["Alpha"])
        hc_inline_dim2 = Structs.nx_inline_dimension_def(["Num"])

        #Create a sort structure
        hc_mes_sort = Structs.nx_sort_by()

        #Create the measure structures
        hc_inline_mes1 = Structs.nx_inline_measure_def("=Sum(Num)")
        hc_inline_mes2 = Structs.nx_inline_measure_def("=Avg(Num)")

        #Create hypercube dimensions from the inline dimension structures
        hc_dim1 = Structs.nx_hypercube_dimensions(hc_inline_dim1)
        hc_dim2 = Structs.nx_hypercube_dimensions(hc_inline_dim2)

        # Create hypercube measures from the inline measure structures
        hc_mes1 = Structs.nx_hypercube_measure(hc_mes_sort, hc_inline_mes1)
        hc_mes2 = Structs.nx_hypercube_measure(hc_mes_sort, hc_inline_mes2)

        # Create the paging model/structure (26 rows and 4 columns)
        nx_page = Structs.nx_page(0, 0, 26, 4)

        # Create a hypercube definition with arrays of hc dims, measures and nxpages
        hc_def = Structs.hypercube_def("$", [hc_dim1, hc_dim2], [hc_mes1, hc_mes2], [nx_page])

        # Create a Chart object with the hypercube definitions as parameter
        hc_response = self.eaa.create_object(self.app_handle, "CH01", "Chart", "qHyperCubeDef", hc_def)

        #Get the handle to the chart object (this may be different in my local repo. I have made some changes to this
        # for future versions)
        hc_handle = self.ega.get_handle(hc_response['qReturn'])

        # Validate the chart object by calling get_layout
        self.egoa.get_layout(hc_handle)

        # Call the get_hypercube_data to get the resulting json object, using the handle and nx page as paramters
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
