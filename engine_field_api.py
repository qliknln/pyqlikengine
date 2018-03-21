import json


class EngineFieldApi:

    def __init__(self, socket):
        self.engine_socket = socket

    def select_values(self, fld_handle, values=None):
        if values is None:
            values = []
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectValues",
                          "params": [values, False, False]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response
        except KeyError:
            return response["error"]

    def select_excluded(self, fld_handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectExcluded",
                          "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def select_possible(self, fld_handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectPossible",
                          "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def clear(self, fld_handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectExcluded",
                          "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_cardinal(self, fld_handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "GetCardinal",
                          "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]