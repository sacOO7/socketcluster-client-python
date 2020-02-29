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
    socket.subscribe_ack('yell', sub_ack)
    socket.publish_ack('yell', 'Hi dudies', pub_ack)
    socket.on_channel('yell', channel_message)
    socket.unsubscribe_ack('yell', unsub_ack)


def sub_ack(channel, error, object):
    if error is '':
        print "Subscribed successfully to channel " + channel


def pub_ack(channel, error, object):
    if error is '':
        print "Publish sent successfully to channel " + channel


def channel_message(key, object):
    print "Got data " + object + " from key " + key


def unsub_ack(channel, error, object):
    if error is '':
        print "Unsubscribed to channel " + channel


if __name__ == "__main__":
    socket = socketcluster.Socket("ws://localhost:8000/socketcluster/")
    socket.set_basic_listener(on_connect, on_disconnect, on_connect_error)
    socket.set_authentication_listener(on_set_authentication, on_authentication)
    socket.connect()
