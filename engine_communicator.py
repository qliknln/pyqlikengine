from websocket import create_connection
import jwt
import ssl


class EngineCommunicator:

    def __init__(self, url):
        self.url = url
        self.ws = create_connection(self.url)
        self.session = self.ws.recv()  # Holds session object. Required for Qlik Sense Sept. 2017 and later
       
    @staticmethod
    def send_call(self, call_msg):
        self.ws.send(call_msg)
        return self.ws.recv()

    @staticmethod
    def close_qvengine_connection(self):
        self.ws.close()

class SecureEngineCommunicator(EngineCommunicator):

    def __init__(self, senseHost, proxyPrefix, userDirectory, userId, privateKeyPath, ignoreCertErrors=False):
        self.url = "wss://" + senseHost + "/" + proxyPrefix + "/app/engineData"
        sslOpts = {}
        if ignoreCertErrors:
            sslOpts = {"cert_reqs": ssl.CERT_NONE}
        
        privateKey = open(privateKeyPath).read()
        token = jwt.encode({'user': userId, 'directory': userDirectory}, privateKey, algorithm='RS256')

        self.ws = create_connection(self.url, sslopt=sslOpts, header=['Authorization: BEARER ' + str(token)])
        self.session = self.ws.recv()