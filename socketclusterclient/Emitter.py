class emitter(object):
    def on(self, key, function):
        self.map[key] = function

    def onchannel(self, key, function):
        self.map[key] = function

    def onack(self, key, function):
        self.mapack[key] = function

    def execute(self, key, object):

        if self.map.has_key(key):
            function = self.map[key]
            if function is not None:
                function(key, object)

    def haseventack(self, key):
        # print "return value is "+self.mapack[key]
        return self.mapack.has_key(key)
        # return False

    def executeack(self, key, object, ack):
        if self.mapack.has_key(key):
            function = self.mapack[key]
            if function is not None:
                function(key, object,ack)

    def __init__(self):
        self.map = {}
        self.mapack = {}

        print "super init got called"
