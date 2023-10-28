import copy

def mergeContext(previous: dict, current: dict):
    print(previous, current)
    curr_keys = current.keys()
    prev_keys = previous.keys()
    res = copy.deepcopy(current)
    for key in curr_keys:
        if key == "title" or key == "director":
            continue
        if type(res[key]) == str:
            print(key)
            tmp=[]
            tmp.append(res[key])
            res[key] = tmp
        if key in prev_keys:
            if type(previous[key]) == str:
                res[key].append(previous[key])
            else:
                res[key].extend(previous[key])
            # res[key].extend(previous[key])
            # print(key, type(res[key]), res[key])
            res[key]=list(set(res[key]))
    
    for key in previous.keys():
        if key not in curr_keys:
            res.setdefault(key, previous[key])

    
    return res

def textToDict(parsed_text): 
    parsed_fields = parsed_text.lower().split("\n")
    req = dict()
    for item in parsed_fields:
        tmp = item.split(":")
        val = tmp[1].strip().split(", ")
        if len(val) == 1:
            if val[0] != "unknown":
                req.setdefault(tmp[0].strip(), val[0])
            continue

        req.setdefault(tmp[0].strip(), val)
    
    return req
