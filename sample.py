import json
# x=json.dumps({"sac": "wefwef", "dydd": "fefewf", "qwdqwd": 0},sort_keys=True)
# print x

emitobject = json.loads('{"a":"hi"}')
print json.dumps(emitobject,sort_keys=True)