from engine_communicator import EngineCommunicator
from engine_global_api import EngineGlobalApi
import json


class EngineAppApi:

    def __init__(self, socket):
        self.engine_socket = socket

    def get_script(self, doc_handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": doc_handle, "method": "GetScript", "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']['qScript']

    def set_script(self, doc_handle, script):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": doc_handle, "method": "SetScript", "params": [script]})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)

    def do_reload(self, doc_handle, param_list=[]):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": doc_handle, "method": "DoReload", "params": param_list})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']['qReturn']

    def do_reload_ex(self, doc_handle, param_list=[]):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": doc_handle, "method": "DoReloadEx", "params": param_list})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']['qResult']

    def get_app_layout(self, doc_handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": doc_handle, "method": "GetAppLayout", "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']

    def get_object(self, doc_handle, param_list=[]):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": doc_handle, "method": "GetObject", "params": param_list})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']

    def get_field(self, doc_handle, field_name, state_name=""):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": doc_handle, "method": "GetField", "params": {"qFieldName": field_name, "qStateName": state_name}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']['qReturn']

    def create_object(self, doc_handle, q_id = "LB01", q_type = "ListObject", struct_name="qListObjectDef", ob_struct={}):
        msg=json.dumps({"jsonrpc": "2.0", "id": 0, "method": "CreateObject", "handle": doc_handle,
                        "params": [{"qInfo": {"qId": q_id, "qType": q_type},struct_name: ob_struct}]})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']