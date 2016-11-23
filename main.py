import Socketcluster
import Emitter

if __name__ == "__main__":
    emitter = Emitter.emitter()
    print emitter
    socket = Socketcluster.socket("ws://localhost:8000/socketcluster/")
