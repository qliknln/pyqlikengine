import json


class EngineGenericObjectApi:

    def __init__(self, socket):
        self.engine_socket = socket

    def get_layout(self, handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetLayout", "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)
