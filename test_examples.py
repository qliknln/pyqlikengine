from engine_communicator import EngineCommunicator
from engine_global_api import EngineGlobalApi
from engine_app_api import EngineAppApi
from  engine_generic_object_api import EngineGenericObjectApi
from engine_field_api import EngineFieldApi
from structs import Structs
import time

url = 'ws://localhost:4848/app'
conn = EngineCommunicator(url)
ega = EngineGlobalApi(conn)
eaa = EngineAppApi(conn)
egoa = EngineGenericObjectApi(conn)
efa = EngineFieldApi(conn)
struct = Structs()


def make_selection():
    ega.open_doc('SelectApp')
    doc = ega.get_active_doc()
    time.sleep(1)
    h=ega.get_handle(doc)
    lod = struct.list_object_def("$","",["Alpha"],["my field"],[{"qSortByLoadOrder": 1}],[{"qTop": 0, "qLeft": 0, "qHeight": 3, "qWidth": 1}])
    lobj= eaa.create_object(h,"LB01","ListObject","qListObjectDef",lod)
    lobj['qReturn']
    h3=ega.get_handle(lobj['qReturn'])
    egoa.get_layout(h3)
    fld = eaa.get_field(h, 'Alpha')
    h2 = ega.get_handle(fld)
    print h2
    val = [{"qText": "A"}, {"qText": "B"}]
    efa.select_values(h2,val)
    print egoa.get_layout(h3)

make_selection()

#conn.connect()
#print conn.get_doc_list()
#print conn.get_os_name()
#ega.create_app('theApp')
#time.sleep(1)
#ega.open_doc('theApp')
#doc = ega.get_active_doc()
#time.sleep(1)
#handle = ega.get_doc_handle(doc)
#eaa.set_script(handle,'Load RecNo() as Field autogenerate 10;')
#print eaa.do_reload(handle)
#print eaa.do_reload_ex(handle)
#ega.delete_app('C:\\Users\\Niklas\\Documents\\Qlik\\Sense\\Apps\\theApp.qvf')
conn.close_qvengine_connection(conn)

