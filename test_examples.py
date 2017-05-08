from engine_api import EngineApi

conn = EngineApi('ws://localhost:4848/app')

conn.connect()
conn.get_doc_list()
conn.get_os_name()
conn.disconnect()
