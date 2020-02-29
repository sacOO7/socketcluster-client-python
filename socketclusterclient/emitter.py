class Emitter(object):
    def on(self, key, function):
        self.map[key] = function

    def on_channel(self, key, function):
        self.map[key] = function

    def on_ack(self, key, function):
        self.map_ack[key] = function

    def execute(self, key, object):

        if key in self.map:
            function = self.map[key]
            if function is not None:
                function(key, object)

    def has_event_ack(self, key):
        return key in self.map_ack

    def execute_ack(self, key, object, ack):
        if key in self.map_ack:
            function = self.map_ack[key]
            if function is not None:
                function(key, object, ack)

    def __init__(self):
        self.map = {}
        self.map_ack = {}

