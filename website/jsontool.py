#-*- coding:utf-8 -*-


def encode_login(data):
    para = ("id", "password")
    for item in para:
        if not data.has_key(item):
            return ""
    command = "login {id} {password}\n".format(**data)

    return command

def decode_login(data):
    if data == "1\n":
        return {"success" : True}
    else:
        return {"success" : False}

def encode_register(data):
    para = ("name", "password", "email", "phone")
    for item in para:
        if not data.has_key(item):
            return ""
    command = "register {name} {password} {email} {phone}\n".format(**data)
    return command

def decode_register(data):
    result = {}
    if (data == "0\n"):
        result["success"] = False
    else:
        result["success"] = True
        result["id"] = data[:-1]
    return result

def encode_query_profile(data):
    para = ("id",)
    for item in para:
        if not data.has_key(item):
            return ""
    command = "query_profile {id}\n".format(**data)
    return command

def decode_query_profile(data):
    result={}
    if data == "0\n":
        result["success"] = False
    else:
        result["success"] = True
        info = data[:-1].split(' ')
        result["name"]  = info[0]
        result["email"] = info[1]
        result["phone"] = info[2]
    return result

def encode_modify_profile(data):
    para = ("id", "name", "password", "email", "phone")
    for item in para:
        if not data.has_key(item):
            return ""
    command = "modify_profile {id} {name} {password} {email} {phone}\n".format(**data)
    return command

def decode_modify_profile(data):
    result={}
    if data == "0\n":
        result["success"] = False
    else:
        result["success"] = True
    return result

def encode_modify_privilege(data):
    para = ("id1", "id2", "privilege")
    for item in para:
        if not data.has_key(item):
            return ""
    command = "modify_privilege {id1} {id2} {privilege}\n".format(**data)
    return command

def decode_modify_privilege(data):
    result={}
    if data == "0\n":
        result["success"] = False
    else:
        result["success"] = True
    return result

def encode_sale_train(data):
    para = ("id",)
    for item in para:
        if not data.has_key(item):
            return ""
    command = "modify_privilege {id}\n".format(**data)
    return command

def decode_sale_train(data):
    result={}
    if data == "0\n":
        result["success"] = False
    else:
        result["success"] = True
    return result

def encode_add_train(data):
    para = ("train_id", "name", "catalog", "stationnum", "pricenum",
        "ticket", "station")
    for item in para:
        if not data.has_key(item):
            return ""
    command = "add_train {train_id} {name} {catalog} {stationnum} {pricenum}".format(**data)
    for pricename in data["ticket"]:
        command += " "+pricename
    command += "\n"
    station_para = ("name","timearriv","timestart","timestopover","ticket")
    for station in data["station"]:
        for item in station_para:
            if not station.has_key(item):
                return ""
        command += "{name} {timearriv} {timestart} {timestopover}".format(**station)
        for price in station["ticket"]:
            command += " ￥" + str(price)
        command += "\n"
    return command

def decode_add_train(data):
    result={}
    if data == "1\n":
        result["success"] = True
    else:
        result["success"] = False
    return result

def encode_query_ticket(data):
    para = ("loc1", "loc2", "date", "catalog")
    for item in para:
        if not data.has_key(item):
            return ""
    #print "haha"
    return "query_ticket {loc1} {loc2} {date} {catalog}\n".format(**data)    

def decode_query_ticket(data):
    result = {}
    if data == "-1\n":
        result["success"] = False
    else:
        result["success"] = True
        trainlist = data.split("\n")
        result["num"] = int(trainlist[0])
        result["ticket"] = []
        keywd = ("train_id", "locfrom", "datefrom", "timefrom", "locto",
            "dateto", "timeto")
        for item in trainlist[1:]:
            info = item.split(" ")
            if (len(info) < len(keywd)):
                continue
            info_dict = {}
            for i in range(len(keywd)):
                info_dict[keywd[i]] = info[i]
            info_dict["ticket"] = {}
            info.remove("")
            #print info,len(info)
            for i in range(len(keywd), len(info), 3):
                #print i
                info_dict["ticket"][info[i]] = {"num": int(info[i+1]), "price":float(info[i+2])}
            result["ticket"].append(info_dict)
    return result

def encode_query_train(data):
    para = ("train_id",)
    for item in para:
        if not data.has_key(item):
            return ""
    return "query_train {train_id}\n".format(**data)    

def decode_query_train(data):
    #print data
    #print "haha"
    result = {}
    if data == "-1\n" or data == "": 
        result["success"] = False
    else:
        result["success"] = True
        trainlist = data.split("\n")
        keywd = ("train_id", "name", "catalog", "stationnum", "pricenum",)
        station_keywd = ("name", "timearriv", "timestart", "timestopover")
        first_line = trainlist[0].split(" ")
        for i in range(len(keywd)):
            result[keywd[i]] = first_line[i]
        result["stationnum"] = int(result["stationnum"])
        result["pricenum"] = int(result["pricenum"])
        result["ticket"] = []
        for i in first_line[len(keywd):]:
            result["ticket"].append(i)
        result["station"] = []
        for item in trainlist[1:]:
            info = item.split(" ")
            if (len(info) < len(station_keywd)):
                continue
            info_dict = {}
            for i in range(len(station_keywd)):
                info_dict[station_keywd[i]] = info[i]
            info_dict["ticket"] = []
            for i in range(len(station_keywd), len(info)):
                if (info[i]):
                    print info[i][1:]
                    info_dict["ticket"].append(float(info[i][1:]))
            result["station"].append(info_dict)
    return result