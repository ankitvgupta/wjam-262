import io
import binascii
import struct

class WireProtocolStub:
    def __init__(self):
        pass

    #TODO add version to everything?
    # Takes in a string representation of http binary field
    def decode(self, path, b):
        b = b.data
        
        type = struct.unpack("<B", b[0])[0]

        ret_obj = {}

        def get_user_pwd(b, ret_obj):
            usernamelen = struct.unpack("<i", b[1:5])[0]
            username = b[5:(5 + usernamelen)]
            passwordlen = struct.unpack("<i", b[5 + usernamelen : 5 + usernamelen + 4])[0]
            password = b[5 + usernamelen + 4 : 5 + usernamelen + 4 + passwordlen]
            start = 5 + usernamelen + 4 + passwordlen
            ret_obj["username"] = username
            ret_obj["password"] = password
            return username, password, start

        if type == 0:
            # register
            user, pwd, st = get_user_pwd(b, ret_obj)
            ret_obj["task"] = "CreateUser"
            return ret_obj

        elif type == 1:
            # list accounts
            user, pwd, st = get_user_pwd(b)
            matchstringlen = struct.unpack("<i", b[1 + start:5 + start])[0]
            matchstring = b[5 + start:5 + matchstringlen + start]
            ret_obj["task"] = "ListAccounts"
            return ret_obj

        elif type == 2:
            # create group
            user, pwd, st = get_user_pwd(b)
            num_users = struct.unpack("<i", b[st: st + 4])
            groupnamelen = struct.unpack("<i", b[st + 4: st + 8])
            groupname = b[st + 8:st + 8 + groupnamelen]
            ret_obj["groupname"] = groupname
            init = st + 4 + 4 + groupnamelen
            for i in range(num_users):
                tmpuserlen = struct.unpack("<i", b[init:init+4])
                tmpusern = b[init+4:init+4+tmpuserlen]
                init += 4 + tmpuserlen
                if i == 0:
                    ret_obj["groupuseres"] = [tmpusern]
                else:
                    ret_obj["groupusers"].append(tmpusern)
            ret_obj["task"] = "CreateGroup"
            return ret_obj

        elif type == 3:
            # list groups
            user, pwd, st = get_user_pwd(b)
            # that's all the info we need
            ret_obj["task"] = "GetGroups"
            return ret_obj

        elif type == 4:
            # send_message
            user, pwd, st = get_user_pwd(b)   
            usr_or_group = struct.unpack("<i", b[st : st + 4])
            namelen = struct.unpack("<i", b[st+4:st+8])
            name = b[st+8:st+ 8 + namelen]
            msglen = struct.unpack("<i", b[st+ 8 + namelen:st+ 12 + namelen])[0]
            msg = b[st+ 12 + namelen:st+ 12 + namelen + msglen]
            ret_obj["message"] = msg
            ret_obj["targetgroup"] = name
            ret_obj["task"] = "SendMessage"
            return ret_obj

        elif type == 5:
            #get messages
            user, pwd, st = get_user_pwd(b)
            # that's all we need
            ret_obj["task"] = "GetMessages"
            return ret_obj

        elif type == 6:
            # delete account
            user, pwd, st = get_user_pwd(b)
            # that's all we need
            ret_obj["task"] = "DeleteAccount"
            return ret_obj

        else:
            ret_obj["task"] = "INVALID"
            return ret_obj

    def encode(self, response):
        s = response["success"]
        resp = response["response"]
        # 0 if success, 1 if failure
        i = 0 if s else 1
        resplen = len(resp)
        output = ""
        output += struct.pack("<i", s)
        output += struct.pack("<i", resplen)
        output += resp
        return output


# Run on the output of check.c
# def test():
#     f = open("output")
#     s = f.read()
#     bytestream_to_request(s)
