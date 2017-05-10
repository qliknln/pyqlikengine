from engine_api import EngineApi
import time

conn = EngineApi('ws://localhost:4848/app')

conn.connect()
print conn.get_doc_list()
print conn.get_os_name()
print conn.create_app('theApp')
time.sleep(1)
print conn.open_doc('theApp')
print conn.get_active_doc()
time.sleep(1)
print conn.delete_app('C:\\Users\\Niklas\\Documents\\Qlik\\Sense\\Apps\\theApp.qvf')
conn.disconnect()
