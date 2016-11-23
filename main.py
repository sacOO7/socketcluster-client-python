import Socketcluster


def onconnect(socket):
    print "on connect got called"


def ondisconnect(socket):
    print "on disconnect got called"


def onConnectError(socket, error):
    print "On connect error got called"


def onSetAuthentication(socket, token):
    print "Token received " + token
    # socket.setAuthtoken(token)


def onAuthentication(socket, isauthenticated):
    print "Authenticated is " + str(isauthenticated)
    socket.emit("chat", "Hello")


def message(object):
    print "Got data " + object


if __name__ == "__main__":
    socket = Socketcluster.socket("ws://localhost:8000/socketcluster/")
    socket.setBasicListener(onconnect, ondisconnect, onConnectError)
    socket.setAuthenticationListener(onSetAuthentication, onAuthentication)
    socket.on('ping',message)
    socket.connect()
