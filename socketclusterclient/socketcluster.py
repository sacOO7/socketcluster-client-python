import json
from threading import Timer
import websocket
import logging
import importlib

emitter = importlib.import_module(".emitter", package="socketclusterclient")
parser = importlib.import_module(".parser", package="socketclusterclient")


class Socket(emitter.Emitter):

    def _init_logger(self):
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.WARNING)

    def enable_logger(self, enabled):
        if enabled is True:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.WARNING)

    def get_logger(self):
        return self.logger

    def emit_ack(self, event, object, ack):
        emit_object = json.loads('{}')
        emit_object["event"] = event
        emit_object["data"] = object
        emit_object["cid"] = self.increment_counter()
        self.ws.send(json.dumps(emit_object, sort_keys=True))
        self.logger.debug("Emit data is " + json.dumps(emit_object, sort_keys=True))
        self.acks[self.cnt] = [event, ack]

    def emit(self, event, object):
        emit_object = json.loads('{}')
        emit_object["event"] = event
        emit_object["data"] = object
        self.ws.send(json.dumps(emit_object, sort_keys=True))

    def subscribe(self, channel):
        subscribe_object = json.loads('{}')
        subscribe_object["event"] = "#subscribe"
        object = json.loads('{}')
        object["channel"] = channel
        subscribe_object["data"] = object
        subscribe_object["cid"] = self.increment_counter()
        self.ws.send(json.dumps(subscribe_object, sort_keys=True))
        self.channels.append(channel)

    def sub(self, channel):
        self.ws.send(
            "{\"event\":\"#subscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + str(
                self.increment_counter()) + "}")

    def subscribe_ack(self, channel, ack):
        subscribe_object = json.loads('{}')
        subscribe_object["event"] = "#subscribe"
        object = json.loads('{}')
        object["channel"] = channel
        subscribe_object["data"] = object
        subscribe_object["cid"] = self.increment_counter()
        self.ws.send(json.dumps(subscribe_object, sort_keys=True))
        self.channels.append(channel)
        self.acks[self.cnt] = [channel, ack]

    def unsubscribe(self, channel):
        subscribe_object = json.loads('{}')
        subscribe_object["event"] = "#unsubscribe"
        subscribe_object["data"] = channel
        subscribe_object["cid"] = self.increment_counter()
        self.ws.send(json.dumps(subscribe_object, sort_keys=True))
        self.channels.remove(channel)

    def unsubscribe_ack(self, channel, ack):
        subscribe_object = json.loads('{}')
        subscribe_object["event"] = "#unsubscribe"
        subscribe_object["data"] = channel
        subscribe_object["cid"] = self.increment_counter()
        self.ws.send(json.dumps(subscribe_object, sort_keys=True))
        self.channels.remove(channel)
        self.acks[self.cnt] = [channel, ack]

    def publish(self, channel, data):
        publish_object = json.loads('{}')
        publish_object["event"] = "#publish"
        channel_object = json.loads('{}')
        channel_object["channel"] = channel
        channel_object["data"] = data
        publish_object["data"] = channel_object
        publish_object["cid"] = self.increment_counter()
        self.ws.send(json.dumps(publish_object, sort_keys=True))

    def publish_ack(self, channel_object, data, ack):
        publish_object = json.loads('{}')
        publish_object["event"] = "#publish"
        channel_object = json.loads('{}')
        channel_object["channel"] = channel_object
        channel_object["data"] = data
        publish_object["data"] = channel_object
        publish_object["cid"] = self.increment_counter()
        self.ws.send(json.dumps(publish_object, sort_keys=True))
        self.acks[self.cnt] = [channel_object, ack]

    def get_subscribed_channels(self):
        return self.channels

    def subscribe_channels(self):
        for x in self.channels:
            self.sub(x)

    def ack(self, cid):
        ws = self.ws

        def message_ack(error, data):
            ackobject = json.loads('{}')
            ackobject["error"] = error
            ackobject["data"] = data
            ackobject["rid"] = cid
            ws.send(json.dumps(ackobject, sort_keys=True))

        return message_ack

    class BlankDict(dict):
        def __missing__(self, key):
            return ''

    def on_message(self, ws, message):
        if message == "":
            self.ws.send("")
            self.logger.debug("received ping, sending pong back")
        else:
            self.logger.debug(message)
            response_object = json.loads(message, object_hook=self.BlankDict)
            data_object = response_object["data"]
            rid = response_object["rid"]
            cid = response_object["cid"]
            event = response_object["event"]
            result = parser.parse(rid, event)
            if result == 1:
                self.subscribe_channels()
                if self.on_authentication is not None:
                    self.id = data_object["id"]
                    self.on_authentication(self, data_object["isAuthenticated"])
            elif result == 2:
                self.execute(data_object["channel"], data_object["data"])
                self.logger.debug("publish event received for channel :: " + data_object["channel"])
            elif result == 3:
                self.authToken = None
                self.logger.debug("remove token event received")
            elif result == 4:
                self.logger.debug("set token event received")
                if self.on_set_authentication is not None:
                    self.on_set_authentication(self, data_object["token"])
            elif result == 5:
                self.logger.debug("received data for event :: " + event)
                if self.haseventack(event):
                    self.executeack(event, data_object, self.ack(cid))
                else:
                    self.execute(event, data_object)
            else:
                if rid in self.acks:
                    tuple = self.acks[rid]
                    if tuple is not None:
                        self.logger.debug("Ack received for event :: " + tuple[0])
                        ack = tuple[1]
                        ack(tuple[0], response_object["error"], response_object["data"])
                    else:
                        self.logger.warning("Ack function not found for rid :: " + rid)

    def on_error(self, ws, error):
        if self.on_connect_error is not None:
            self.on_connect_error(self, error)
            # self.reconnect()

    def on_close(self, ws):
        if self.on_disconnected is not None:
            self.on_disconnected(self)
        if self.enable_reconnection:
            self.reconnect()

    def increment_counter(self):
        self.cnt += 1
        return self.cnt

    def reset_counter(self):
        self.cnt = 0

    def on_open(self, ws):
        self.reset_counter()

        handshake_object = json.loads('{}')
        handshake_object["event"] = "#handshake"
        auth_object = json.loads('{}')
        auth_object["authToken"] = self.authToken
        handshake_object["data"] = auth_object
        handshake_object["cid"] = self.increment_counter()
        self.ws.send(json.dumps(handshake_object, sort_keys=True))

        if self.on_connected is not None:
            self.on_connected(self)

    def set_auth_token(self, token):
        self.authToken = str(token)

    def get_auth_token(self):
        return self.authToken

    def __init__(self, url):
        self.logger = logging.getLogger(__name__)
        self.id = ""
        self.cnt = 0
        self.authToken = None
        self.url = url
        self.acks = {}
        self.channels = []
        self.enable_reconnection = False
        self.delay = 3
        self.ws = self.on_connected = self.on_disconnected = self.on_connect_error = self.on_set_authentication =\
            self.on_authentication = None
        emitter.Emitter.__init__(self)
        self._init_logger()

    def connect(self, sslopt=None, http_proxy_host=None, http_proxy_port=None):
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt=sslopt, http_proxy_host=http_proxy_host, http_proxy_port=http_proxy_port)

    def set_basic_listener(self, on_connected, on_disconnected, on_connect_error):
        self.on_connected = on_connected
        self.on_disconnected = on_disconnected
        self.on_connect_error = on_connect_error

    def reconnect(self):
        Timer(self.delay, self.connect).start()

    def set_delay(self, delay):
        self.delay = delay

    def set_reconnection(self, enable):
        self.enable_reconnection = enable

    def set_authentication_listener(self, on_set_authentication, on_authentication):
        self.on_set_authentication = on_set_authentication
        self.on_authentication = on_authentication

    def disconnect(self):
        self.enable_reconnection = False
        self.ws.close()
