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
    # socket.emit("chat", "Hello")
    socket.subscribeack('yell', suback)
    socket.publishack('yell', 'Hi dudies', puback)


def message(key, object):
    print "Got data " + object + " from key " + key


def messsageack(key, object, ackmessage):
    print "Got data " + object + " from key " + key
    ackmessage("this is error", "this is data")


def ack(key, error, object):
    print "Got ack data " + object + " and error " + error + " and key is " + key


def puback(channel, error, object):
    if error is '':
        print "Publish sent successfully to channel " + channel


def suback(channel, error, object):
    if error is '':
        print "Subscribed successfully to channel " + channel


if __name__ == "__main__":
    socket = Socketcluster.socket("ws://localhost:8000/socketcluster/")
    socket.setBasicListener(onconnect, ondisconnect, onConnectError)
    socket.setAuthenticationListener(onSetAuthentication, onAuthentication)
    socket.onack('ping', messsageack)
    socket.on('yell', message)
    socket.connect()
