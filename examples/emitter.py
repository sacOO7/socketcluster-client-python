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

    # Emitter code without ack
    socket.emit("chat", "Hi")

    # Emitter code with ack
    socket.emitack("chat", "Hi", ack)


def ack(key, error, object):
    print "Got ack data " + object + " and error " + error + " and key is " + key


if __name__ == "__main__":
    socket = Socketcluster.socket("ws://localhost:8000/socketcluster/")
    socket.setBasicListener(onconnect, ondisconnect, onConnectError)
    socket.setAuthenticationListener(onSetAuthentication, onAuthentication)
    socket.connect()
