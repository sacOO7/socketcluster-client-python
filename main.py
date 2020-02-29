from socketclusterclient import Socketcluster
import logging

mylogger = logging.getLogger(__name__)
mylogger.setLevel(logging.DEBUG)

def onconnect(socket):
    mylogger.debug("on connect got called")


def ondisconnect(socket):
    logging.info("on disconnect got called")


def onConnectError(socket, error):
    logging.info("On connect error got called")


def onSetAuthentication(socket, token):
    logging.info("Token received " + token)
    socket.setAuthtoken(token)


def onAuthentication(socket, isauthenticated):
    logging.info("Authenticated is " + str(isauthenticated))
    # socket.emit("chat", "Hello")
    socket.subscribeack('yell', suback)
    socket.publishack('yell', 'Hi dudies', puback)


def message(key, object):
    logging.info("Got data " + object + " from key " + key)


def messsageack(key, object, ackmessage):
    logging.info("Got data " + object + " from key " + key)
    ackmessage("this is error", "this is data")


def ack(key, error, object):
    logging.info("Got ack data " + object + " and error " + error + " and key is " + key)


def puback(channel, error, object):
    if error is '':
        logging.info("Publish sent successfully to channel " + channel)


def suback(channel, error, object):
    if error is '':
        logging.info("Subscribed successfully to channel " + channel)


if __name__ == "__main__":
    socket = Socketcluster.socket("ws://localhost:8000/socketcluster/")
    socket.setBasicListener(onconnect, ondisconnect, onConnectError)
    socket.setAuthenticationListener(onSetAuthentication, onAuthentication)
    socket.onack('ping', messsageack)
    socket.enablelogger(True)
    # socket.on('yell', message)
    # socket.setreconnection(True)
    socket.connect()
    # socket.connect(sslopt={"cert_reqs": ssl.CERT_NONE})
