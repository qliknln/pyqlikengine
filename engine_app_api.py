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

