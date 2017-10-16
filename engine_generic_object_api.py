import json


class EngineGenericObjectApi:

    def __init__(self, socket):
        self.engine_socket = socket

    def get_layout(self, handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetLayout", "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)

    def get_hypercube_data(self, handle, path="/qHyperCubeDef", pages=[]):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetHyperCubeData",
                          "params": [path,pages]})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)["result"]
