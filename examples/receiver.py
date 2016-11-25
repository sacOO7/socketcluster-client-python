from socketclusterclient import Socketcluster


def onconnect(socket):
    print "on connect got called"


def ondisconnect(socket):
    print "on disconnect got called"


def onConnectError(socket, error):
    print "On connect error got called"


def onSetAuthentication(socket, token):
    print "Token received " + token
    socket.setAuthtoken(token)


def onAuthentication(socket, isauthenticated):
    print "Authenticated is " + str(isauthenticated)

    # socket.emit("chat", "Hi")

    # Receiver code without ack
    socket.on("ping", message)

    # Receiver code with ack
    socket.onack("ping", messsageack)


def message(key, object):
    print "Got data " + object + " from key " + key


def messsageack(key, object, ackmessage):
    print "Got data " + object + " from key " + key
    ackmessage("this is error", "this is data")


if __name__ == "__main__":
    socket = Socketcluster.socket("ws://localhost:8000/socketcluster/")
    socket.setBasicListener(onconnect, ondisconnect, onConnectError)
    socket.setAuthenticationListener(onSetAuthentication, onAuthentication)
    socket.connect()
