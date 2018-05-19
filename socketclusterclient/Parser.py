# ISAUTHENTICATED,1
# PUBLISH,2
# REMOVETOKEN,3
# SETTOKEN,4
# EVENT,5
# ACKRECEIVE,6


def parse(dataobject, rid, cid, event):
    if event is not '':
        if event == "#publish":
            return 2
        elif event == "#removeAuthToken":
            return 3
        elif event == "#setAuthToken":
            return 4
        else:
            return 5
    elif rid == 1:
        return 1
    else:
        return 6
