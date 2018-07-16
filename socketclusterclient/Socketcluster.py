import json
from threading import Timer
import websocket
import logging
import importlib

Emitter = importlib.import_module(".Emitter", package="socketclusterclient")
Parser = importlib.import_module(".Parser", package="socketclusterclient")

sclogger = logging.getLogger(__name__)
sclogger.addHandler(logging.StreamHandler())
sclogger.setLevel(logging.WARNING)


class socket(Emitter.emitter):
    def enablelogger(self, enabled):
        if (enabled):
            sclogger.setLevel(logging.NOTSET)
        else:
            sclogger.setLevel(logging.WARNING)

    def getlogger(self):
        return sclogger

    def emitack(self, event, object, ack):
        emitobject = json.loads('{}')
        emitobject["event"] = event
        emitobject["data"] = object
        emitobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(emitobject, sort_keys=True))
        sclogger.debug("Emit data is " + json.dumps(emitobject, sort_keys=True))
        self.acks[self.cnt] = [event, ack]

    def emit(self, event, object):
        emitobject = json.loads('{}')
        emitobject["event"] = event
        emitobject["data"] = object
        self.ws.send(json.dumps(emitobject, sort_keys=True))

    def subscribe(self, channel):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#subscribe"
        object = json.loads('{}')
        object["channel"] = channel
        subscribeobject["data"] = object
        subscribeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(subscribeobject, sort_keys=True))
        self.channels.append(channel)

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
        self.acks[self.cnt] = [channel, ack]

    def unsubscribe(self, channel):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#unsubscribe"
        subscribeobject["data"] = channel
        subscribeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(subscribeobject, sort_keys=True))
        self.channels.remove(channel)

    def unsubscribeack(self, channel, ack):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#unsubscribe"
        subscribeobject["data"] = channel
        subscribeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(subscribeobject, sort_keys=True))
        self.channels.remove(channel)
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

    def publishack(self, channel, data, ack):
        publishobject = json.loads('{}')
        publishobject["event"] = "#publish"
        object = json.loads('{}')
        object["channel"] = channel
        object["data"] = data
        publishobject["data"] = object
        publishobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(publishobject, sort_keys=True))
        self.acks[self.cnt] = [channel, ack]

    def getsubscribedchannels(self):
        return self.channels

    def subscribechannels(self):
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

        return MessageAck

    class BlankDict(dict):
        def __missing__(self, key):
            return ''

    def on_message(self, ws, message):
        if message == "#1":
            self.ws.send("#2")
        else:
            sclogger.debug(message)
            mainobject = json.loads(message, object_hook=self.BlankDict)
            dataobject = mainobject["data"]
            rid = mainobject["rid"]
            cid = mainobject["cid"]
            event = mainobject["event"]
            result = Parser.parse(dataobject, rid, cid, event)
            if result == 1:
                self.subscribechannels()
                if self.OnAuthentication is not None:
                    self.id = dataobject["id"]
                    self.OnAuthentication(self, dataobject["isAuthenticated"])
            elif result == 2:
                self.execute(dataobject["channel"], dataobject["data"])
                sclogger.debug("publish event received for channel :: " + dataobject["channel"])
            elif result == 3:
                self.authToken = None
                sclogger.debug("remove token event received")
            elif result == 4:
                sclogger.debug("set token event received")
                if self.onSetAuthentication is not None:
                    self.onSetAuthentication(self, dataobject["token"])
            elif result == 5:
                sclogger.debug("received data for event :: " + event)
                if self.haseventack(event):
                    self.executeack(event, dataobject, self.Ack(cid))
                else:
                    self.execute(event, dataobject)
            else:
                if rid in self.acks:
                    tuple = self.acks[rid]
                    if tuple is not None:
                        sclogger.debug("Ack received for event :: " + tuple[0])
                        ack = tuple[1]
                        ack(tuple[0], mainobject["error"], mainobject["data"])
                    else:
                        sclogger.warning("Ack function not found for rid :: " + rid)

    def on_error(self, ws, error):
        if self.onConnectError is not None:
            self.onConnectError(self, error)
            # self.reconnect()

    def on_close(self, ws):
        if self.onDisconnected is not None:
            self.onDisconnected(self)
        if self.enablereconnection:
            self.reconnect()

    def getandincrement(self):
        self.cnt += 1
        return self.cnt

    def resetvalue(self):
        self.cnt = 0

    def on_open(self, ws):
        self.resetvalue()

        handshakeobject = json.loads('{}')
        handshakeobject["event"] = "#handshake"
        object = json.loads('{}')
        object["authToken"] = self.authToken
        handshakeobject["data"] = object
        handshakeobject["cid"] = self.getandincrement()
        self.ws.send(json.dumps(handshakeobject, sort_keys=True))

        if self.onConnected is not None:
            self.onConnected(self)

    def setAuthtoken(self, token):
        self.authToken = str(token)

    def getAuthtoken(self):
        return self.authToken

    def __init__(self, url):
        self.id = ""
        self.cnt = 0
        self.authToken = None
        self.url = url
        self.acks = {}
        self.channels = []
        self.enablereconnection = False
        self.delay = 3
        self.ws = self.onConnected = self.onDisconnected = self.onConnectError = self.onSetAuthentication = self.OnAuthentication = None
        Emitter.emitter.__init__(self)

    def connect(self, sslopt=None, http_proxy_host=None, http_proxy_port=None):
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
        Timer(self.delay, self.connect).start()

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
