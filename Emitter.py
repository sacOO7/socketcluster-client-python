class emitter(object):
    def on(self, key, function):
        self.map[key] = function

    def execute(self, key,object):
        function = self.map[key]
        if function is not None:
            function(object)

    def __init__(self):
        self.map = {}
        print "super init got called"
