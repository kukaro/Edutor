import json
import urllib


def byteArrayToStr(arr):
    tmp = str('')
    for i in range(len(arr)):
        tmp = tmp + chr(arr[i])
    return tmp


def addDialog(dialog, name, email, time, callState):
    data = {'email': email, 'name': name, 'message': dialog, 'time': time, 'callState': callState}
    jsonData = bytes(json.dumps(data).encode())
    print('Add Dialog Result : ')
    print(jsonData)
    req = urllib.request.Request("http://localhost:5001/dialog", data=jsonData)
    req.get_method = lambda: 'post'
    jsonResult = urllib.request.urlopen(req).read()
    result = json.loads(jsonResult.decode())
    print('Add Dialog Result : ')
    print(result)
    if result['success'] == 'ok':
        return True
    else:
        return False
