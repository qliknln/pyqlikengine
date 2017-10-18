import json


class EngineFieldApi:

    def __init__(self, socket):
        self.engine_socket = socket

    def select_values(self, fld_handle, values=None):
        if values is None:
            values = []
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectValues",
                          "params": [values, False, False]})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)["result"], json.loads(response)["change"]
