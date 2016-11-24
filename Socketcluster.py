import websocket
import json
import Parser
import Emitter
import time
import threading


class socket(Emitter.emitter):
    def emitack(self, event, object, ack):
        emitobject = json.loads('{}')
        emitobject["event"] = event
        emitobject["data"] = object
        emitobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(emitobject, sort_keys=True))
        # self.ws.send("{\"event\":\"" + event + "\",\"data\":\"" + object + "\",\"cid\":" + self.getandincrement() + "}")
        self.acks[self.cnt] = [event, ack]

    def emit(self, event, object):
        emitobject = json.loads('{}')
        emitobject["event"] = event
        emitobject["data"] = object
        emitobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(emitobject, sort_keys=True))
        print "Emit data is "+json.dumps(emitobject, sort_keys=True)
        # self.ws.send("{\"event\":\"" + event + "\",\"data\":\"" + object + "\",\"cid\":" + self.getandincrement() + "}")

    def subscribe(self, channel):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#subscribe"
        object = json.loads('{}')
        object["channel"] = channel
        subscribeobject["data"] = object
        subscribeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(subscribeobject, sort_keys=True))
        # self.ws.send(
        #     "{\"event\":\"#subscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + self.getandincrement() + "}")

    def subscribeack(self, channel, ack):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#subscribe"
        object = json.loads('{}')
        object["channel"] = channel
        subscribeobject["data"] = object
        subscribeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(subscribeobject, sort_keys=True))
        # self.ws.send(
        #     "{\"event\":\"#subscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + self.getandincrement() + "}")
        self.acks[self.cnt] = [channel, ack]

    def unsubscribe(self, channel):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#unsubscribe"
        object = json.loads('{}')
        object["channel"] = channel
        subscribeobject["data"] = object
        subscribeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(subscribeobject, sort_keys=True))
        # self.ws.send(
        #     "{\"event\":\"#unsubscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + self.getandincrement() + "}")

    def unsubscribeack(self, channel, ack):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#unsubscribe"
        object = json.loads('{}')
        object["channel"] = channel
        subscribeobject["data"] = object
        subscribeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(subscribeobject, sort_keys=True))
        # self.ws.send(
        #     "{\"event\":\"#unsubscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + self.getandincrement() + "}")
        self.acks[self.cnt] = [channel, ack]

    def publish(self, channel, data):
        publishobject = json.loads('{}')
        publishobject["event"] = "#publish"
        object = json.loads('{}')
        object["channel"] = channel
        object["data"] = data
        publishobject["data"] = object
        publishobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(publishobject, sort_keys=True))
        # self.ws.send(
        #     "{\"event\":\"#publish\",\"data\":{\"channel\":\"" + channel + "\",\"data\":\"" + data + "\"},\"cid\":" + self.getandincrement() + "}")

    def publishack(self, channel, data, ack):

        publishobject = json.loads('{}')
        publishobject["event"] = "#publish"
        object = json.loads('{}')
        object["channel"] = channel
        object["data"] = data
        publishobject["data"] = object
        publishobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(publishobject, sort_keys=True))
        # self.ws.send(
        #     "{\"event\":\"#publish\",\"data\":{\"channel\":\"" + channel + "\",\"data\":\"" + data + "\"},\"cid\":" + self.getandincrement() + "}")
        self.acks[self.cnt] = [channel, ack]

    def Ack(self, cid):
        ws = self.ws

        def MessageAck(error, data):
            ws.send("{\"error\":\"" + error + "\",\"data\":\"" + data + "\",\"rid\":" + str(cid) + "}")

        return MessageAck

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
                self.authToken = None
                print "remove token got called"
            elif result == 4:
                print "set token got called"
                if self.onSetAuthentication is not None:
                    self.onSetAuthentication(self, dataobject["token"])
            elif result == 5:
                print "Event got called"
                if self.haseventack(event):
                    self.executeack(event, dataobject, self.Ack(cid))
                else:
                    self.execute(event, dataobject)
            else:
                print "Ack receive got called"
                if self.acks.has_key(rid):
                    tuple = self.acks[rid]
                    if tuple is not None:
                        ack = tuple[1]
                        ack(tuple[0], mainobject["error"], mainobject["data"])
                    else:
                        print "Ack function not found for rid"

    def on_error(self, ws, error):
        if self.onConnectError is not None:
            self.onConnectError(self, error)
            # self.reconnect()

    def on_close(self, ws):
        if self.onDisconnected is not None:
            self.onDisconnected(self)
        self.reconnect()
        # print "### closed ###"

    def getandincrement(self):
        self.cnt += 1
        return self.cnt

    def resetvalue(self):
        self.cnt = 0

    def on_open(self, ws):
        # print "on open got called"
        self.resetvalue()
        if self.onConnected is not None:
            self.onConnected(self)

        handshakeobject = json.loads('{}')
        handshakeobject["event"] = "#handshake"
        object = json.loads('{}')
        object["authToken"] = self.authToken
        handshakeobject["data"] = object
        handshakeobject["cid"] = self.getandincrement()
        # print "data for authentication is" + json.dumps(handshakeobject, sort_keys=True)
        self.ws.send(json.dumps(handshakeobject, sort_keys=True))

        # data = "{\"event\": \"#handshake\",\"data\": {\"authToken\":" + self.authToken + "},\"cid\": " + self.getandincrement() + "}"
        # print "data for authentication is" + data
        # self.ws.send(data)

    def setAuthtoken(self, token):
        self.authToken = str(token)
        # print "Token is"+self.authToken

    def __init__(self, url):
        self.cnt = 0
        self.authToken = None
        self.url = url
        self.acks = {}
        self.ws = self.onConnected = self.onDisconnected = self.onConnectError = self.onSetAuthentication = self.OnAuthentication = None
        Emitter.emitter.__init__(self)

    def connect(self):
        # websocket.enableTrace(True)
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

    def reconnect(self):
        time.sleep(3)
        self.connect()
        # self.ws.run_forever()
        # threading.Timer(3, self.connect()).start()

    def setAuthenticationListener(self, onSetAuthentication, OnAuthentication):
        self.onSetAuthentication = onSetAuthentication
        self.OnAuthentication = OnAuthentication
