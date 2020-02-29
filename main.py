from socketclusterclient import socketcluster
import logging

mylogger = logging.getLogger(__name__)
mylogger.setLevel(logging.DEBUG)


def on_connect(socket):
    mylogger.debug("on connect got called")


def on_disconnect(socket):
    logging.info("on disconnect got called")


def on_connect_error(socket, error):
    logging.info("On connect error got called")


def on_set_authentication(socket, token):
    logging.info("Token received " + token)
    socket.set_auth_token(token)


def on_authentication(socket, isauthenticated):
    logging.info("Authenticated is " + str(isauthenticated))
    # socket.emit("chat", "Hello")
    socket.subscribe_ack('yell', sub_ack)
    socket.publish_ack('yell', 'Hi dudies', pub_ack)


def msg(key, object):
    logging.info("Got data " + object + " from key " + key)


def msg_ack(key, object, ackmessage):
    logging.info("Got data " + object + " from key " + key)
    ackmessage("this is error", "this is data")


def ack(key, error, object):
    logging.info("Got ack data " + object + " and error " + error + " and key is " + key)


def pub_ack(channel, error, object):
    if error is '':
        logging.info("Publish sent successfully to channel " + channel)


def sub_ack(channel, error, object):
    if error is '':
        logging.info("Subscribed successfully to channel " + channel)


if __name__ == "__main__":
    socket = socketcluster.Socket("ws://localhost:8000/socketcluster/")
    socket.set_basic_listener(on_connect, on_disconnect, on_connect_error)
    socket.set_authentication_listener(on_set_authentication, on_authentication)
    socket.on_ack('ping', msg_ack)
    socket.enable_logger(True)
    # socket.on('yell', msg)
    # socket.set_reconnection(True)
    socket.connect()
    # socket.connect(sslopt={"cert_reqs": ssl.CERT_NONE})
