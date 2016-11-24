# ISAUTHENTICATED,1
# PUBLISH,2
# REMOVETOKEN,3
# SETTOKEN,4
# EVENT,5
# ACKRECEIVE,6
import json


def parse(dataobject, rid, cid, event):
    if event is not '':
        if event == "#publish":
            # print "publish got called"
            return 2
        elif event == "#removeAuthToken":
            # print "remove auth got called"
            return 3
        elif event == "#setAuthToken":
            # print "set authtoken called"
            return 4
        else:
            # print "event got called with cid"+cid
            return 5
    elif rid == 1:
        # print "is authenticated got called"
        return 1
    else:
        # print "got ack"
        return 6
