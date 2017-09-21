from websocket import create_connection


class EngineCommunicator:

    def __init__(self, url):
        self.url = url
        self.ws = create_connection(self.url)
        self.session = self.ws.recv()  # Holds session object. Required for Qlik Sense Sept. 2017 and later.

    @staticmethod
    def send_call(self, call_msg):
        self.ws.send(call_msg)
        return self.ws.recv()

    @staticmethod
    def close_qvengine_connection(self):
        self.ws.close()
