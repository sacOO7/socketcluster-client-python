import json
from threading import Timer
import websocket
import logging
import importlib

Emitter = importlib.import_module(".Emitter", package="socketclusterclient")
Parser = importlib.import_module(".Parser", package="socketclusterclient")

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


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
        # emitobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(emitobject, sort_keys=True))
        logging.info("Emit data is " + json.dumps(emitobject, sort_keys=True))
        # self.ws.send("{\"event\":\"" + event + "\",\"data\":\"" + object + "\",\"cid\":" + self.getandincrement() + "}")

    def subscribe(self, channel):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#subscribe"
        object = json.loads('{}')
        object["channel"] = channel
        subscribeobject["data"] = object
        subscribeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(subscribeobject, sort_keys=True))
        self.channels.append(channel)
        # self.ws.send(
        #     "{\"event\":\"#subscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + self.getandincrement() + "}")

    def sub(self, channel):
        self.ws.send(
            "{\"event\":\"#subscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + str(
                self.getandincrement()) + "}")

    def subscribeack(self, channel, ack):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#subscribe"
        object = json.loads('{}')
        object["channel"] = channel
        subscribeobject["data"] = object
        subscribeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(subscribeobject, sort_keys=True))
        self.channels.append(channel)
        # self.ws.send(
        #     "{\"event\":\"#subscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + self.getandincrement() + "}")
        self.acks[self.cnt] = [channel, ack]

    def unsubscribe(self, channel):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#unsubscribe"
        subscribeobject["data"] = channel
        subscribeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(subscribeobject, sort_keys=True))
        self.channels.remove(channel)
        # self.ws.send(
        #     "{\"event\":\"#unsubscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + self.getandincrement() + "}")

    def unsubscribeack(self, channel, ack):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#unsubscribe"
        subscribeobject["data"] = channel
        subscribeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(subscribeobject, sort_keys=True))
        self.channels.remove(channel)
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

    def getsubscribedchannels(self):
        return self.channels

    def subscribechannels(self):
        # subscribing to all channels
        for x in self.channels:
            self.sub(x)

    def Ack(self, cid):
        ws = self.ws

        def MessageAck(error, data):
            ackobject = json.loads('{}')
            ackobject["error"] = error
            ackobject["data"] = data
            ackobject["rid"] = cid
            ws.send(json.dumps(ackobject, sort_keys=True))
            # ws.send("{\"error\":\"" + error + "\",\"data\":\"" + data + "\",\"rid\":" + str(cid) + "}")

        return MessageAck

    class BlankDict(dict):
        def __missing__(self, key):
            return ''

    def SuscribeChannels(self):
        logging.info("subscribe got called")

    def on_message(self, ws, message):
        if message == "#1":
            # print ("got ping sending pong")
            self.ws.send("#2")
        else:
            logging.info(message)
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
                    self.id = dataobject["id"]
                    self.OnAuthentication(self, dataobject["isAuthenticated"])
                self.subscribechannels()
            elif result == 2:
                self.execute(dataobject["channel"], dataobject["data"])
                logging.info("publish got called")
            elif result == 3:
                self.authToken = None
                logging.info("remove token got called")
            elif result == 4:
                logging.info("set token got called")
                if self.onSetAuthentication is not None:
                    self.onSetAuthentication(self, dataobject["token"])
            elif result == 5:
                logging.info("Event got called")
                if self.haseventack(event):
                    self.executeack(event, dataobject, self.Ack(cid))
                else:
                    self.execute(event, dataobject)
            else:
                logging.info("Ack receive got called")
                if rid in self.acks:
                    tuple = self.acks[rid]
                    if tuple is not None:
                        ack = tuple[1]
                        ack(tuple[0], mainobject["error"], mainobject["data"])
                    else:
                        logging.info("Ack function not found for rid")

    def on_error(self, ws, error):
        if self.onConnectError is not None:
            self.onConnectError(self, error)
            # self.reconnect()

    def on_close(self, ws):
        if self.onDisconnected is not None:
            self.onDisconnected(self)
        if self.enablereconnection:
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
        self.id = ""
        self.cnt = 0
        self.authToken = None
        self.url = url
        self.acks = {}
        self.channels = []
        self.enablereconnection = True
        self.delay = 3
        self.ws = self.onConnected = self.onDisconnected = self.onConnectError = self.onSetAuthentication = self.OnAuthentication = None
        Emitter.emitter.__init__(self)

    def connect(self, sslopt=None, http_proxy_host=None, http_proxy_port=None):
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt=sslopt, http_proxy_host=http_proxy_host, http_proxy_port=http_proxy_port)

    def setBasicListener(self, onConnected, onDisconnected, onConnectError):
        self.onConnected = onConnected
        self.onDisconnected = onDisconnected
        self.onConnectError = onConnectError

    def reconnect(self):
        # print "Hello"
        Timer(self.delay, self.connect).start()
        print "delay"

    def setdelay(self, delay):
        self.delay = delay

    def setreconnection(self, enable):
        self.enablereconnection = enable

    def setAuthenticationListener(self, onSetAuthentication, OnAuthentication):
        self.onSetAuthentication = onSetAuthentication
        self.OnAuthentication = OnAuthentication

    def disconnect(self):
        self.enablereconnection = False
        self.ws.close()
