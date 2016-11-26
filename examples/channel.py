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


    socket.subscribeack('yell', suback)

    socket.publishack('yell', 'Hi dudies', puback)

    socket.onchannel('yell', channelmessage)

    socket.unsubscribeack('yell', unsuback)


def suback(channel, error, object):
    if error is '':
        print "Subscribed successfully to channel " + channel


def puback(channel, error, object):
    if error is '':
        print "Publish sent successfully to channel " + channel


def channelmessage(key, object):
    print "Got data " + object + " from key " + key


def unsuback(channel, error, object):
    if error is '':
        print "Unsubscribed to channel " + channel


if __name__ == "__main__":
    socket = Socketcluster.socket("ws://localhost:8000/socketcluster/")
    socket.setBasicListener(onconnect, ondisconnect, onConnectError)
    socket.setAuthenticationListener(onSetAuthentication, onAuthentication)
    socket.connect()

