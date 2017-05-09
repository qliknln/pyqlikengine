from engine_communicator import EngineCommunicator
import json


class EngineApi:
    def __init__(self, url):
        self.url = url
        self.engine_socket = None

    def connect(self):
        self.engine_socket = EngineCommunicator(self.url)

    def disconnect(self):
        self.engine_socket.close_qvengine_connection(self.engine_socket)

    # returns an array of doc objects. The doc object contains doc name, size, file time etc
    def get_doc_list(self):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetDocList", "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']['qDocList']

    # returns the os name (always windowsNT). Obsolete?
    def get_os_name(self):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "OSName", "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']['qReturn']

    # returns the app id. If desktop is used the app id is the same as the full path to qvf
    # if it's running against Enterprise, app id will be a guid
    def create_app(self, app_name):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "CreateApp", "params": [app_name]})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']['qAppId']
