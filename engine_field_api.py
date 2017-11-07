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
        if 'error' in response:
            error_msg = response["error"]["message"]
            code = response["error"]["code"]
            return "Error code - " + str(code) + ", Error Msg: " + error_msg
        else:
            return json.loads(response)["result"], json.loads(response)["change"]

    def select_excluded(self, fld_handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectExcluded",
                          "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        if 'error' in response:
            error_msg = response["error"]["message"]
            code = response["error"]["code"]
            return "Error code - " + str(code) + ", Error Msg: " + error_msg
        else:
            return json.loads(response)["result"], json.loads(response)["change"]

    def select_possible(self, fld_handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectPossible",
                          "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        if 'error' in response:
            error_msg = response["error"]["message"]
            code = response["error"]["code"]
            return "Error code - " + str(code) + ", Error Msg: " + error_msg
        else:
            return json.loads(response)["result"], json.loads(response)["change"]

    def clear(self, fld_handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectExcluded",
                          "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        if 'error' in response:
            error_msg = response["error"]["message"]
            code = response["error"]["code"]
            return "Error code - " + str(code) + ", Error Msg: " + error_msg
        else:
            return json.loads(response)["result"]

    def get_cardinal(self, fld_handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "GetCardinal",
                          "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        if 'error' in response:
            error_msg = response["error"]["message"]
            code = response["error"]["code"]
            return "Error code - " + str(code) + ", Error Msg: " + error_msg
        else:
            return json.loads(response)["result"]["qReturn"]