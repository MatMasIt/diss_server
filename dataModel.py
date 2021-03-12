import time
keysTypes = {
    "state": str,
    "details": str,
    "large_image": str,
    "small_image": str,
    "large_text": str,
    "small_text": str,
    "start": [float, int, None],
    "end": [float, int, None],
    "timeFlip": bool,
    "lastTimeUpdate": [float, int, bool]
}
default = {
    "default": {
        "state": "Idling",
        "details": "No workspace is enabled",
        "large_image": "laptop",
        "small_image": "waiting",
        "large_text": "Idling",
        "small_text": "Waiting",
        "start": time.time(),
        "end": None,
        "lastTimeUpdate": 0,
        "forgetTimeIfNoContact": 0,
        "issuerName": "base",
        "accessCode": "a",
        "publicRead": True,
        "descriptar": "default"
    }
}


def is_valid_current_data_format(dic):
    return True
    global keysTypes
    for key in keysTypes.keys():
        if not key in dic.keys():
            return False
        elif not isinstance(keysTypes[key], list):
            if not isinstance(dic[key], keysTypes[key]) or (dic[key]
                                                            == keysTypes[key]):
                return False
        else:
            flag = False
            for kType in keysTypes[key]:
                if isinstance(dic[key], kType) or (dic[key] == kType):
                    flag = True
                    break
            if not flag:
                return False
    return True
