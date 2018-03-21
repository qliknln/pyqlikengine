import tempfile
import unittest

from engine_app_api import EngineAppApi
from engine_communicator import EngineCommunicator
from engine_field_api import EngineFieldApi
from engine_global_api import EngineGlobalApi
from structs import Structs

from engine_generic_object_api import EngineGenericObjectApi


# Unittest class for the methods in EngineGlobalApi. All tests methods must have the "test_" prefix.


class TestGlobalApi(unittest.TestCase):
    # Constructor to prepare everything before running the tests.
    def setUp(self):
        url = 'ws://localhost:4848/app'
        self.conn = EngineCommunicator(url)
        self.ega = EngineGlobalApi(self.conn)
        self.eaa = EngineAppApi(self.conn)
        self.egoa = EngineGenericObjectApi(self.conn)
        self.efa = EngineFieldApi(self.conn)
        self.struct = Structs()

    def test_get_doclist(self):
        response = self.ega.get_doc_list()
        self.assertTrue(len(response) > 0)

    def test_app_methods(self):
        response_create = self.ega.create_app("test_app")['qAppId']
        self.assertTrue(response_create.endswith(".qvf"), "Failed to create app. Response did not end with .qvf")
        #response_copy = self.ega.copy_app("test_app_copy", response_create)
        #print response_copy
        response_open = self.ega.open_doc("test_app")
        #response_open = self.ega.open_doc_ex("test_app_asdf")
        self.assertEqual(response_open['qReturn']["qHandle"], 1,
                         "Failed to retrieve a proper document handle with open_doc method")
        self.assertTrue(response_open['qReturn']["qGenericId"].endswith(".qvf"),
                        'Generic id does not contain any app file extension using open_doc method')
        self.assertEqual(response_open['qReturn']["qType"],"Doc",'Unknown doc type returned using open_doc method')
        response_get_active_doc = self.ega.get_active_doc()
        self.assertEqual(response_get_active_doc['qReturn']["qHandle"], 1, "Failed to retrive a proper document handle with "
                                                                "get_active_doc method")
        self.assertTrue(response_get_active_doc['qReturn']["qGenericId"].endswith(".qvf"),
                        'Generic id does not contain any app file extension  using get_active_doc method')
        self.assertEqual(response_get_active_doc['qReturn']["qType"], "Doc", 'Unknown doc type returned using get_active_doc '
                                                                  'method')
        response_delete = self.ega.delete_app(response_create)['qSuccess']
        #self.ega.delete_app(response_copy)
        self.assertTrue(response_delete, "Failed to delete app")

    # May be a meaningless test since there are no commands to abort??
    def test_abort_all(self):
        response = self.ega.abort_all()
        self.assertEqual(response,{},'abort_all method returned unexpected object')

    # May be a meaningless test since there is no request with id 1?
    def test_abort_request(self):
        response = self.ega.abort_request(1)
        self.assertEqual(response, {}, 'abort_request method returned unexpected object')

    def test_configure_reload(self):
        response_pos = self.ega.configure_reload(True, True, True)
        self.assertEqual(response_pos, {}, 'configure_reload method returned unexpected object')
        response_neg = self.ega.configure_reload('dummy',True,True)['message']
        self.assertEqual(response_neg, "Invalid method parameter(s)")

    def test_create_session_app(self):
        response = self.ega.create_session_app()['qSessionAppId']
        self.assertTrue(response.startswith("SessionApp_"),"Failed to create session app")

    def test_create_session_app_from_app(self):
        response_create = self.ega.create_app("test_app")['qAppId']
        response = self.ega.create_session_app_from_app(response_create)['qSessionAppId']
        self.ega.delete_app(response_create)
        self.assertTrue(response.startswith("SessionApp_"),"Failed to create session app")

    def test_export_app(self):
        tmp_folder = tempfile.gettempdir()
        response_create = self.ega.create_app("test_app")['qAppId']
        response = self.ega.export_app(tmp_folder,response_create)
        self.ega.delete_app(response_create)
        print("BUG returns method not found. Reported")

    def test_replace_app_from_id(self):
        response_create = self.ega.create_app("test_app")['qAppId']
        tmp_folder = tempfile.gettempdir()
        response = self.ega.replace_app_from_id(tmp_folder, response_create)
        print("Same bug as CopyApp and ExportApp")
        self.ega.delete_app(response_create)

    def test_get_auth_user(self):
        response = self.ega.get_auth_user()
        self.assertTrue(type(response) is dict, "Failed to retrieve authenticated user")

    def test_is_desktop_mode(self):
        response = self.ega.is_desktop_mode(0)['qReturn']
        self.assertTrue(type(response) is bool,'Failed to check desktop mode')

    # Clean up after the tests have been run
    def tearDown(self):
        self.conn.close_qvengine_connection(self.conn)


if __name__ == '__main__':
    unittest.main()

    # def make_selection(self):
    # self.ega.open_doc('SelectApp')
    # doc = self.ega.get_active_doc()
    # time.sleep(1)
    # h=self.ega.get_handle(doc)
    # lod = self.struct.list_object_def("$","",["Alpha"],["my field"],[{"qSortByLoadOrder": 1}],[{"qTop": 0, "qLeft": 0, "qHeight": 3, "qWidth": 1}])
    # lobj= self.eaa.create_object(h,"LB01","ListObject","qListObjectDef",lod)
    # h3=self.ega.get_handle(lobj['qReturn'])
    # self.egoa.get_layout(h3)
    # fld = self.eaa.get_field(h, 'Alpha')
    # h2 = self.ega.get_handle(fld)
    # val = [{"qText": "A"}, {"qText": "B"}]
    # self.efa.select_values(h2,val)
    # print self.egoa.get_layout(h3)


    # conn.connect()
    # print ega.get_doc_list()
    # print conn.get_os_name()
    # ega.create_app('theApp')
    # time.sleep(1)
    # ega.open_doc('theApp')
    # doc = ega.get_active_doc()
    # time.sleep(1)
    # handle = ega.get_doc_handle(doc)
    # eaa.set_script(handle,'Load RecNo() as Field autogenerate 10;')
    # print eaa.do_reload(handle)
    # print eaa.do_reload_ex(handle)
    # ega.delete_app('C:\\Users\\Niklas\\Documents\\Qlik\\Sense\\Apps\\theApp.qvf')
    # conn.close_qvengine_connection(conn)
