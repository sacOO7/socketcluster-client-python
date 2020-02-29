from socketclusterclient import socketcluster


def on_connect(_socket):
    print "on connect got called"


def on_disconnect(_socket):
    print "on disconnect got called"


def on_connect_error(_socket, error):
    print "On connect error got called"


def on_set_authentication(socket, token):
    print "Token received " + token
    socket.set_auth_token(token)


def on_authentication(socket, is_authenticated):
    print "Authenticated is " + str(is_authenticated)

    # socket.emit("chat", "Hi")

    # Receiver code without ack
    socket.on("ping", message)

    # Receiver code with ack
    socket.on_ack("ping", messsage_ack)


def message(key, object):
    print "Got data " + object + " from key " + key


def messsage_ack(key, object, ackmessage):
    print "Got data " + object + " from key " + key
    ackmessage("this is error", "this is data")


if __name__ == "__main__":
    socket = socketcluster.Socket("ws://localhost:8000/socketcluster/")
    socket.set_basic_listener(on_connect, on_disconnect, on_connect_error)
    socket.set_authentication_listener(on_set_authentication, on_authentication)
    socket.connect()
