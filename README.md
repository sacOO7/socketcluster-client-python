# socketcluster-client-python
Refer examples for more details :
    
Overview
--------
This client provides following functionality

- Easy to setup and use
- Can be used for extensive unit-testing of all server side functions
- Support for emitting and listening to remote events
- Automatic reconnection
- Pub/sub
- Authentication (JWT)
- Support for python2.x.x / python3.x.x

To install use
```python
    sudo pip install socketclusterclient
```

Description
-----------
Create instance of `Socket` class by passing url of socketcluster-server end-point 

```python
    //Create a socket instance
    socket = Socketcluster.socket("ws://localhost:8000/socketcluster/") 
    
```
**Important Note** : Default url to socketcluster end-point is always *ws://somedomainname.com/socketcluster/*.

#### Registering basic listeners
 
Different functions are given as an argument to register listeners

```python
        from socketclusterclient import socketcluster
        import logging
        
        logging.basicConfig(format='%(levelname)s:%(msg)s', level=logging.DEBUG)
        
        
        def on_connect(socket):
            logging.info("on connect got called")
        
        
        def on_disconnect(socket):
            logging.info("on disconnect got called")
        
        
        def on_connect_error(socket, error):
            logging.info("On connect error got called")
        
        
        def on_set_authentication(socket, token):
            logging.info("Token received " + token)
            socket.set_auth_token(token)
        
        
        def on_authentication(socket, isauthenticated):
            logging.info("Authenticated is " + str(isauthenticated))
            
            
        if __name__ == "__main__":
            socket = socketcluster.socket("ws://localhost:8000/socketcluster/")
            socket.set_basic_listener(on_connect, on_disconnect, on_connect_error)
            socket.set_authentication_listener(on_set_authentication, on_authentication)
            socket.connect()
```

#### Connecting to server

- For connecting to server:

```python
    //This will send websocket handshake request to socketcluster-server
    socket.connect();
```


- By default reconnection to server is disabled (since latest release) , to enable it and configure delay for connection

```python
    //This will set automatic-reconnection to server with delay of 2 seconds and repeating it for infinitely
   socket.set_delay(2)
   socket.set_reconnection(True)
   socket.connect();
```

- By default logging of messages in disabled (since latest release), to enable it

```python
   socket.enable_logger(True)
```

Emitting and listening to events
--------------------------------
#### Event emitter

- eventname is name of event and msg can be String, boolean, int or JSON-object

```python

    socket.emit(eventname,msg);
        
    # socket.emit("chat", "Hi")
```

- To send event with acknowledgement

```python

    socket.emit_ack("chat", "Hi", ack)  
        
    def ack(eventname, error, object):
        print "Got ack data " + object + " and error " + error + " and eventname is " + eventname
```

#### Event Listener

- For listening to events :

The object received can be String, Boolean, Long or JSONObject.

```python
     # Receiver code without sending acknowledgement back
     socket.on("ping", msg)
     
     def msg(eventname, object):
         print "Got data " + object + " from eventname " + eventname
```

- To send acknowledgement back to server

```python
    # Receiver code with ack
    socket.on_ack("ping", msg_ack)
    
    def msg_ack(eventname, object, ackmessage):
        print "Got data " + object + " from eventname " + eventname
        ackmessage("this is error", "this is data")
        
```

Implementing Pub-Sub via channels
---------------------------------

#### Creating channel

- For creating and subscribing to channels:

```python
    
    # without acknowledgement
    socket.subscribe('yell')
    
    #with acknowledgement
    socket.subscribe_ack('yell', sub_ack)
    
    def sub_ack(channel, error, object):
        if error is '':
            print "Subscribed successfully to channel " + channel
```

- For getting list of created channels :
 
```python
        channels = socket.getsubscribedchannels()

``` 





#### Publishing event on channel

- For publishing event :

```python

       # without acknowledgement
       socket.publish('yell', 'Hi dudies')
       
       #with acknowledgement
       socket.publish_ack('yell', 'Hi dudies', pub_ack)
       
       def pub_ack(channel, error, object):
           if error is '':
               print "Publish sent successfully to channel " + channel
``` 
 
#### Listening to channel

- For listening to channel event :

```python
        
        socket.on_channel('yell', channel_message)
    
        def channel_message(key, object):
            print "Got data " + object + " from key " + key
    
``` 
     
#### Un-subscribing to channel

```python
         # without acknowledgement
         socket.unsubscribe('yell')
         
         # with acknowledgement
         socket.unsubscribe_ack('yell', unsub_ack) 
         
         def unsub_ack(channel, error, object):
              if error is '':
                   print "Unsubscribed to channel " + channel 
```
      
#### Disable SSL Certificate Verification

```python
        socket = Socketcluster.socket("wss://localhost:8000/socketcluster/")
        socket.connect(sslopt={"cert_reqs": ssl.CERT_NONE})
```

#### HTTP proxy

Support websocket access via http proxy. The proxy server must allow "CONNECT" method to websocket port. Default squid setting is "ALLOWED TO CONNECT ONLY HTTPS PORT".

```python
        socket = Socketcluster.socket("wss://localhost:8000/socketcluster/")
        socket.connect(http_proxy_host="proxy_host_name", http_proxy_port=3128)
```

- To have custom settings over internal logger, you can get logger instance and apply necessary settings over it.
```python
        sclogger = socket.get_logger()
```
Please follow logging tutorial over here : https://docs.python.org/3/howto/logging-cookbook.html