import websocket
import json
import Parser
import Emitter


class socket(Emitter.emitter):
    def emit(self, event, object, ack):
        self.ws.send("{\"event\":\"" + event + "\",\"data\":\"" + object + "\",\"cid\":" + self.getandincrement() + "}")

    def emit(self, event, object):
        self.ws.send("{\"event\":\"" + event + "\",\"data\":\"" + object + "\",\"cid\":" + self.getandincrement() + "}")

    def subscribe(self, channel):
        self.ws.send(
            "{\"event\":\"#subscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + self.getandincrement() + "}")

    def subscribe(self, channel, ack):
        self.ws.send(
            "{\"event\":\"#subscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + self.getandincrement() + "}")

    def unsubscribe(self, channel):
        self.ws.send(
            "{\"event\":\"#unsubscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + self.getandincrement() + "}")

    def unsubscribe(self, channel, ack):
        self.ws.send(
            "{\"event\":\"#unsubscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + self.getandincrement() + "}")

    def publish(self, channel, data):
        self.ws.send(
            "{\"event\":\"#publish\",\"data\":{\"channel\":\"" + channel + "\",\"data\":\"" + data + "\"},\"cid\":" + self.getandincrement() + "}")

    def publish(self, channel, data, ack):
        self.ws.send(
            "{\"event\":\"#publish\",\"data\":{\"channel\":\"" + channel + "\",\"data\":\"" + data + "\"},\"cid\":" + self.getandincrement() + "}")

    class BlankDict(dict):
        def __missing__(self, key):
            return ''

    def SuscribeChannels(self):
        print "subscribe got called"

    def on_message(self, ws, message):
        if message == "#1":
            print ("got ping sending pong")
            self.ws.send("#2")
        else:
            print message
            mainobject = json.loads(message, object_hook=self.BlankDict)
            dataobject = mainobject["data"]
            rid = mainobject["rid"]
            cid = mainobject["cid"]
            event = mainobject["event"]

            result = Parser.parse(dataobject, rid, cid, event)
            # print "result is" + str(result)
            if result == 1:
                # print "authentication got called"
                if self.OnAuthentication is not None:
                    self.OnAuthentication(self, dataobject["isAuthenticated"])
            elif result == 2:
                self.execute(dataobject["channel"], dataobject["data"])
                print "publish got called"
            elif result == 3:
                self.setAuthtoken("null")
                print "remove token got called"
            elif result == 4:
                print "set token got called"
                if self.onSetAuthentication is not None:
                    self.onSetAuthentication(self, dataobject["token"])
            elif result == 5:
                print "Event got called"
                self.execute(event, dataobject)
            else:
                print "Ack receive got called"

    def on_error(self, ws, error):
        if self.onConnectError is not None:
            self.onConnectError(self, error)
        print error

    def on_close(self, ws):
        if self.onDisconnected is not None:
            self.onDisconnected(self)
        print "### closed ###"

    def getandincrement(self):
        self.cnt += 1
        return str(self.cnt)

    def on_open(self, ws):
        # print "on open got called"
        if self.onConnected is not None:
            self.onConnected(self)
        ws.send(
            "{\"event\": \"#handshake\",\"data\": {\"authToken\":" + self.authToken + "},\"cid\": " + self.getandincrement() + "}")

    def setAuthtoken(self, token):
        self.authToken = token

    def __init__(self, url):
        self.cnt = 0
        self.authToken = "null"
        self.url = url
        self.ws = self.onConnected = self.onDisconnected = self.onConnectError = self.onSetAuthentication = self.OnAuthentication = None
        Emitter.emitter.__init__(self)

    def connect(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def setBasicListener(self, onConnected, onDisconnected, onConnectError):
        self.onConnected = onConnected
        self.onDisconnected = onDisconnected
        self.onConnectError = onConnectError

    def setAuthenticationListener(self, onSetAuthentication, OnAuthentication):
        self.onSetAuthentication = onSetAuthentication
        self.OnAuthentication = OnAuthentication

    class channel(object):
        def __init__(self, channelname):
            self.channelname = channelname
