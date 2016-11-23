import websocket


class socket(object):
    def on_message(self, ws, message):
        if message == "#1":
            print ("got ping sending pong")
            self.ws.send("#2")
        print message

    def on_error(self, ws, error):
        print error

    def on_close(self, ws):
        print "### closed ###"

    def on_open(self, ws):
        print "on open got called"
        ws.send("{\"event\": \"#handshake\",\"data\": {\"authToken\":" + self.authToken + "},\"cid\": 1}")

    def setAuthtoken(self, token):
        self.authToken = token

    def __init__(self, url):
        self.authToken = "null"
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()
